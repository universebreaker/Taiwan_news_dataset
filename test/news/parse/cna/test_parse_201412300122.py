import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.cna
import news.parse.db.schema


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='中央社')
    url = r'https://www.cna.com.tw/news/aipl/201412300122.aspx'
    response = news.crawlers.util.request_url.get(url=url)

    raw_news = news.crawlers.db.schema.RawNews(
        company_id=company_id,
        raw_xml=news.crawlers.util.normalize.compress_raw_xml(
            raw_xml=response.text,
        ),
        url_pattern=news.crawlers.util.normalize.compress_url(
            company_id=company_id,
            url=url,
        )
    )

    parsed_news = news.parse.cna.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            本地外交界消息指出,西班牙跨國電話公司西班牙電信(Telefónica)今年已斥資1億
            美元,在瓜地馬拉擴大3G行動電話的覆蓋率及發展本地的4G技術。
            '''
        ),
    )
    assert parsed_news.category == '產經'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1419868800
    assert parsed_news.reporter == '瓜地馬拉'
    assert parsed_news.title == '西企業斥資 發展瓜地馬拉4G'
    assert parsed_news.url_pattern == '201412300122'