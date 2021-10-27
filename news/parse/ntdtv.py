import re
from datetime import datetime
from typing import Final, List, Tuple

from bs4 import BeautifulSoup

import news.parse.util.normalize
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

# There are at least two article patterns, and these patterns are mutually
# exclusive (in other words, only one pattern applies to each news).  We use
# selector lists (selectors separated by comma) to denote all article patterns.
# This observation is made with `url_pattern = 2012-01-01-640251,
# 2011-04-12-517548`.
#
# In the pattern `div[itemprop=articleBody].post_content > p`, some of the
# article contains image captions, thus we remove it using
# `:not(:has(a:has(img)))`.
# This observation is made with `url_pattern = 2011-04-11-517450`.
ARTICLE_SELECTOR_LIST: Final[str] = re.sub(
    r'\s+',
    ' ',
    '''
    div[itemprop=articleBody].post_content > p:not(:has(a:has(img))),
    div.article_content > p
    ''',
)

# There are at least two title patterns, and these patterns are mutually
# exclusive (in other words, only one pattern applies to each news). We use
# selector lists (selectors separated by comma) to denote all title patterns.
# This observation is made with `url_pattern = 2012-01-01-640251,
# 2011-04-12-517548`.
TITLE_SELECTOR_LIST: Final[str] = re.sub(
    r'\s+',
    ' ',
    '''
    div.article_title > h1,
    div.main_title
    ''',
)

###############################################################################
#                                 WARNING:
# Patterns (including `REPORTER_PATTERNS`, `ARTICLE_SUB_PATTERNS`,
# `TITLE_SUB_PATTERNS`) MUST remain their relative ordered, in other words,
# the order of execution may effect the parsing results. `REPORTER_PATTERNS`
# MUST have exactly ONE group.  You can use `(?...)` pattern as non-capture
# group, see python's re module for details.
###############################################################################
REPORTER_PATTERNS: Final[List[re.Pattern]] = [
    # re.compile(r'^採訪/(.*?)\s*編輯/(.*?)\s*後製/(.*?)$'),
    # re.compile(r'\(責任編輯:(\S*?)\)'),
    # This observation is made with `url_pattern = 2012-01-01-640292,
    # 2012-01-01-640245, 2012-01-01-640054, 2011-12-31-639654,
    # 2011-12-30-639201, 2011-12-30-639175, 2011-12-28-638568,
    # 2011-12-25-636878, 2011-12-22-635455, 2011-12-21-635019,
    # 2011-12-20-634655, 2011-12-18-633615, 2011-12-15-632140,
    # 2011-12-13-631155, 2011-04-17-519983, 2011-04-15-519037`.
    re.compile(
        r'\(?(?:(?:這|这)是)?新(?:唐|塘)人(?:記|记)?者?'
        + r'(?:亞太)?(?:(?:電|电)(?:視|视)(?:台|臺)?)?' + r'([\w、\s]*?)'
        + r'的?(?:(?:综|綜)合|整理|(?:採|采)(?:訪|访))?(?:報|报)(?:導|导|道)。?\)?'
    ),
    # This observation is made with `url_pattern = 2012-01-01-640083`.
    re.compile(r'文字:([^/]+?)/.+$'),
]
ARTICLE_SUB_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
    # This observation is made with `url_pattern = 2011-04-17-519983,
    # 2011-04-16-519478`.
    (
        re.compile(r'\((攝影|圖片):[^)]+?\)'),
        '',
    ),
    (
        re.compile(r'@\*#'),
        '',
    ),
    # Note that `ord('–') == 8211`, `ord('—') == 8212` and `ord('─') == 9472`.
    # This observation is made with `url_pattern = 2021-10-24-103250967,
    # 2011-12-23-635993, 2011-04-11-517450, 2011-03-30-512271`.
    (
        re.compile(r'[—–─]*\(?轉自[^)\s]*?\)?\s*(有(刪|删)(節|节))?$'),
        '',
    ),
    (
        re.compile(r'─+點閱\s*【.*?】\s*─+'),
        '',
    ),
    (
        re.compile(r'點閱\s*【.*?】\s*系列文章'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-04-15-519169`.
    (
        re.compile(r'美東時間:\s*.*?【萬年曆】'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-04-15-519169`.
    (
        re.compile(r'本文網址:\s*.*$'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640292,
    # 2011-12-14-631632`.
    (
        re.compile(r'^(【[^】]*?】)+'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-04-17-519966,
    # 2011-04-03-514098`.
    (
        re.compile(r'【新(唐|塘)人[^】]*?訊】?'),
        '',
    ),
    # Remove useless last paragraph with at most one space in between. This
    # observation is made with `url_pattern = 2011-12-20-634477`.
    (
        re.compile(r'【禁聞】\S+?\s?\S+?$'),
        '',
    ),
    # Remove draft notes at the end. This observation is made with
    # `url_pattern = 2011-12-18-633616`.
    (
        re.compile(r'待完成$'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-31-639654,
    # 2011-12-28-638240, 2011-12-26-637243`.
    (
        re.compile(r'相(關|关)((鏈|链)(接|結)|(視|视)(頻|频)|新(聞|闻))+?:.*$'),
        '',
    ),
    # This observation is made with `url_pattern = 2021-10-24-103250967`.
    (
        re.compile(r'(撰文|(製|制)作):.*$'),
        ' ',
    ),
    # This observation is made with `url_pattern = 2021-10-24-103250967`.
    (
        re.compile(r'訂閱\S+?:https://\S+?$'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640316,
    # 2012-01-01-640301, 2012-01-01-640240, 2012-01-01-640096,
    # 2011-12-31-639994, 2011-04-17-519993, 2011-04-17-519859,
    # 2011-04-11-517227`.
    (
        re.compile(
            r'\(?(大(紀|纪)元|中央社?)((記|记)者)?'
            + r'[^()0-9]*?\d*?[^()]*?((電|电)|(報|报)(導|导)|特稿|社)\)',
        ),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640301,
    # 2011-12-23-636434, 2011-04-12-517789, 2011-04-09-516789`.
    (
        re.compile(r'\(((實|实)(習|习))?(編|编)?(譯|译)者?(:|;)[^)]+\)?'),
        '',
    ),
    # This observation is made with `url_pattern = 2012-01-01-640045,
    # 2012-01-01-640280, 2011-12-30-639608, 2011-12-26-637451,
    # 2011-12-25-636915, 2011-04-02-513571`.
    (
        re.compile(r'\(本文附(有|(帶|带))?((影音|照片)(及|和)?(帶|带)?)+\)'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-31-639655,
    # 2011-12-29-638743, 2011-12-28-638138, 2011-12-26-637224,
    # 2011-12-17-633228`.
    (
        re.compile(r'\((自由亞洲電(臺|台)|美國之音)[^)]*?(报|報)導\)'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-26-636848,
    # 2011-12-19-633545, 2011-12-19-633525`.
    (
        re.compile(r'社(區|区)(廣|广)角(鏡|镜)\(\d+?\)(提要:)?'),
        '',
    ),
    # This observation is made with `url_pattern = 2011-12-18-633615,
    # 2011-04-17-519866`.
    (
        re.compile(r'新(聞|闻)(週|周)刊\(?\d+\)?期?'),
        '',
    ),
    # Remove section header symbols. This observation is made with `url_pattern
    # = 2011-04-10-516866`.
    (
        re.compile(r'\*(\S*?)\*'),
        r'\1',
    ),
    # Remove list item symbols. This observation is made with
    # `url_pattern = 2011-12-28-638636, 2011-12-28-638635, 2011-12-28-638631,
    # 2011-12-28-638568`.
    (
        re.compile(r'\s+(★|●|•)'),
        ' ',
    ),
    # Remove figure references. This observation is made with
    # `url_pattern = 2011-12-28-638568, 2011-04-11-517502, 2011-03-29-511547`.
    (
        re.compile(r'(\[(圖|图)卡\d*\]\s*|\((圖|图)片來源:.*?\))'),
        '',
    ),
    # Remove wierd typos. This observation is made with `url_pattern =
    # 2011-12-28-638568.`
    (
        re.compile(r'([^:])//'),
        r'\1',
    ),
    # Remove website references. This observation is made with `url_pattern =
    # 2011-12-21-635020, 2011-04-14-518790, 2011-04-07-515910`.
    (
        re.compile(
            r'新(唐|塘)人(電|电)(視|视)(臺|台)\s*((https?://)?www\.ntdtv\.com)?',
        ),
        '',
    ),
    # Remove download links. This observation is made with `url_pattern =
    # 2011-12-21-635020, 2011-04-12-517801, 2011-04-11-517355,
    # 2011-04-08-516206`.
    (
        re.compile(r'(下(載|载)(錄|录)像)'),
        '',
    ),
    # Remove content references. This observation is made with `url_pattern =
    # 2011-04-12-517801, 2011-04-11-517355, 2011-04-08-516206`.
    (
        re.compile(r'\((畫|画)面.*?(報|报)(導|导|道)\)'),
        '',
    ),
    # Remove left along symbols at the begin. This observation is made with
    # `url_pattern = 2011-12-17-633460, 2011-04-12-517593`.
    (
        re.compile(r'^(主播)?\)'),
        '',
    ),
    # Remove related news tags. This observation is made with `url_pattern =
    # 2011-04-17-519966`.
    (
        re.compile(r'\s+相(關|关)新聞\s+'),
        ' ',
    ),
    # Remove unclear links. This observation is made with `url_pattern =
    # 2011-04-14-518847`.
    (
        re.compile(r'\.html#video target=_blank>'),
        '',
    ),
    # Remove traslation and datetime string at the end. Note that
    # `ord('–') == 8211`, `ord('—') == 8212` and `ord('─') == 9472`. This
    # observation is made with `url_pattern = 2011-12-30-639201,
    # 2011-12-30-639463, 2011-12-24-636612, 2011-12-24-636565,
    # 2011-12-21-634964, 2011-12-22-635525, 2011-12-20-634431,
    # 2011-12-20-634429, 2011-12-17-633168, 2011-12-15-632169,
    # 2011-04-14-518582, 2011-04-04-514246`.
    (
        re.compile(r'''[0-9a-zA-sÀ-ÿ,.:;?!&/“”’'"$%『』\[\]()*=—–─\-\s]+$'''),
        '',
    ),
]
TITLE_SUB_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
    # Remove content hints. This observation is made with `url_pattern =
    # 2012-01-01-640083, 2011-04-12-517801, 2011-12-23-636402`.
    (
        re.compile(r'(【[^】]*?】|\([^)]*?\))'),
        '',
    ),
    # Remove content hints without parentheses. This observation is made with
    # `url_pattern = 2011-04-16-519478, 2011-04-04-514182`.
    (
        re.compile(r'(快(訊|讯)|組(圖|图)):'),
        '',
    ),
    # Remove useless symbols. This observation is made with `url_pattern =
    # 2011-12-20-634431`.
    (
        re.compile(r'(—)+'),
        ' ',
    ),
]


def parser(raw_news: Final[RawNews]) -> ParsedNews:
    """Parse NTDTV news from raw HTML.

    Input news must contain `raw_xml` and `url` since these information cannot
    be retrieved from `raw_xml`.
    """
    # Information which cannot be parsed from `raw_xml`.
    parsed_news = ParsedNews(
        url_pattern=raw_news.url_pattern,
        company_id=raw_news.company_id,
    )

    try:
        soup = BeautifulSoup(raw_news.raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    ###########################################################################
    # Parsing news article.
    ###########################################################################
    article = ''
    try:
        article = ' '.join(
            map(lambda tag: tag.text, soup.select(ARTICLE_SELECTOR_LIST))
        )
        article = news.parse.util.normalize.NFKC(article)
    except Exception:
        raise ValueError('Fail to parse NTDTV news article.')

    ###########################################################################
    # Parsing news category.
    ###########################################################################
    category = ''
    try:
        # Sometimes news does not have categories, but if they have, then
        # categories are always located in breadcrumbs `div#breadcrumb > a`.
        # The first text in breadcrumb is always '首頁', so we exclude it.
        # The second text in breadcrumb is media type, we also exclude it.
        # There might be more than one category, thus we include them all and
        # save as comma separated format.  Some categories are duplicated, thus
        # we remove it using `list(dict.fromkeys(...))`.  See
        # https://stackoverflow.com/questions/1653970/does-python-have-an-ordered-set
        # for details.  This observation is made with `url_pattern =
        # 2012-01-01-640251, 2011-04-12-517548`.
        category = ','.join(
            list(
                dict.fromkeys(
                    map(
                        lambda tag: tag.text,
                        soup.select('div#breadcrumb > a')[2:],
                    )
                )
            )
        )
        category = news.parse.util.normalize.NFKC(category)
    except Exception:
        # There may not have category.
        category = ''

    ###########################################################################
    # Parsing news datetime.
    ###########################################################################
    news_datetime = ''
    try:
        # Some news publishing date time are different to URL pattern.  For
        # simplicity we only use URL pattern to represent the same news.  News
        # datetime will convert to POSIX time (which is under UTC time zone).
        news_datetime = int(
            datetime.strptime(
                parsed_news.url_pattern[:10],
                '%Y-%m-%d',
            ).timestamp()
        )
    except Exception:
        raise ValueError('Fail to parse NTDTV news datetime.')

    ###########################################################################
    # Parsing news reporter.
    ###########################################################################
    reporter_list = []
    reporter = ''
    try:
        for reporter_pattern in REPORTER_PATTERNS:
            # There might have more than one pattern matched.
            reporter_list.extend(reporter_pattern.findall(article))
            # Remove reporter text from article.
            article = news.parse.util.normalize.NFKC(
                reporter_pattern.sub('', article)
            )

        # Reporters are comma seperated.
        reporter = ','.join(map(news.parse.util.normalize.NFKC, reporter_list))
        # Some reporters are separated by whitespaces or '、'.  This
        # observation is made with `url_pattern = 2012-01-01-640292,
        # 2011-12-15-632140, 2011-04-12-517593`.
        reporter = news.parse.util.normalize.NFKC(
            re.sub(
                r'[\s、]+',
                ',',
                reporter,
            )
        )
    except Exception:
        # There may not have reporter.
        reporter = ''

    ###########################################################################
    # Parsing news title.
    ###########################################################################
    title = ''
    try:
        title = soup.select_one(TITLE_SELECTOR_LIST).text
        title = news.parse.util.normalize.NFKC(title)
    except Exception:
        raise ValueError('Fail to parse NTDTV news title.')

    ###########################################################################
    # Substitude some article pattern.
    ###########################################################################
    try:
        for article_pttn, article_sub_str in ARTICLE_SUB_PATTERNS:
            article = news.parse.util.normalize.NFKC(
                article_pttn.sub(
                    article_sub_str,
                    article,
                )
            )
    except Exception:
        raise ValueError('Fail to substitude NTDTV article pattern.')

    ###########################################################################
    # Substitude some title pattern.
    ###########################################################################
    try:
        for title_pttn, title_sub_str in TITLE_SUB_PATTERNS:
            title = news.parse.util.normalize.NFKC(
                title_pttn.sub(
                    title_sub_str,
                    title,
                )
            )
    except Exception:
        raise ValueError('Fail to substitude NTDTV title pattern.')

    parsed_news.article = article
    if category:
        parsed_news.category = category
    else:
        parsed_news.category = ParsedNews.category
    parsed_news.datetime = news_datetime
    if reporter:
        parsed_news.reporter = reporter
    else:
        parsed_news.reporter = ParsedNews.reporter
    parsed_news.title = title
    return parsed_news
    return parsed_news
