import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/2104606'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            進入秋季,氣候變得乾燥,身體也容易燥熱,由於代謝減緩,人也會感到疲倦,而良好的睡眠
            能夠幫助身體儲存更多能量,於是就成為秋天維持好精神的最佳解方。 現代人很容易有
            壓力大、情緒困擾等問題,累積之下也容易產生睡眠障礙,要如何克服,睡前的放鬆練習非常
            重要,而沐浴就是一種方式,推薦12款療癒系的沐浴品,可以有效幫助快速放鬆、改善心情,
            趕緊來看看! 1. Sukin乳霜沐浴乳|小黃瓜裡的檸檬香 這款無皂基沐浴露質地溫和不刺激,
            蘊含黃瓜、柑橘和乳木果油等美肌成分;賦予肌膚滋養保濕,可預防乾燥敏感,洗後絲毫不覺
            乾澀,特別推薦給缺水肌膚。天然檸檬和黃瓜的清新香氣,令人感受來自植萃的療癒力量,洗淨
            身體一整天的疲憊!500ml/NT$399 這個香氣一開始柑橘和橙花香味道會先浮現,沐浴的時候
            柑橘可以幫助釋放一天緊張的心情,橙花的輕盈讓身體與心情從放鬆變得愉快,最後木質香調
            的尾韻像地中海陽光般舒適。橙花的香氣留香度高,香味會環繞在身上與被窩間,早上起床也
            會先聞到淡淡的香氣! 除了沐浴油如果搭配同香味的身體磨砂膏與身體乳,肌膚會加倍感受
            到被滋潤,香氣延續時間也會更長一些。500ml/NT$1,280、300ml/NT$980 週年慶限定
            優惠:明星三部曲3件88折 清潔、磨砂、修護是SABON明星三部曲中的儀式三步驟,在沐浴過
            程中隨著水流,我們感受緩慢下來的時間,期待與自己的對話。 沐浴油500ml+身體磨砂膏6
            00g +身體乳液200ml(含絲綢身體乳、清爽保濕凝凍,不含身體保濕潤膚霜)、(香調任選,
            但以色列綠玫瑰、死海、限量新品除外) 是一款散發清涼豐郁香氛的舒活沐浴露,擦在身上
            時可感受肌膚沉醉在細膩綿密的泡沫之中,洗後通體舒暢,連手肘、膝蓋、腳跟等粗糙易生成
            角質的部分也變得細嫩光滑。若能配以天然素材的毛巾,從足尖開始按摩清洗,血行促進效果
            更佳。300ml/NT$1,000 主要保濕‧潤澤成分: 精油:葡萄柚精油/茶樹精油/乳香精油/澳
            洲尤加利精油 植物油:摩洛哥堅果油/茶籽油/荷荷巴油/琉璃苣油/柚子種籽油 植物純露:
            南高梅純露/碳酸溫泉水/月桃純露 週年慶推薦:居家生活防護組,購買精油香氛噴霧(正貨)
            +舒活沐浴露(正貨)+植萃防護乾洗手(正貨),贈送平衡護手霜15g+植萃防護乾洗手30ml+T
            HREE經典束口袋,價值NT$4,850、優惠價NT$3,900 4. Aromatherapy Associates
            晚間舒緩沐浴油 主成份為岩蘭草、洋甘菊、檀香,可說是失眠救星的晚間舒緩沐浴油,能夠
            幫助深度放鬆和舒眠,失眠、時差、睡眠品質不佳時非常適合使用,可讓心靈沉靜,提升睡眠
            品質,讓身心得到徹底的休息。55ml/NT$2,600 可搭配RELAX ROOM FRAGRANCER舒緩室
            內香薰(搭配水氧機或精油燈使用),成份為西印度月桂、天竺葵、沒藥,製造放鬆的環境,舒
            眠,鎮靜焦慮、緊張的心寧,達到徹底的放鬆。100ml/NT$1,300 蘊含薰衣草精華油,遇水
            之後會轉化成豐富綿密的柔滑泡沫,泡完澡後,肌膚會感受到非常地滑嫩細緻,散發舒心迷人
            的薰衣草淡雅香氣!500ml/NT$1,280 週年慶推薦:紓壓好眠推薦組,官網獨享-紓壓放鬆.
            助眠神器!至10/28(二)限定組合內容:紓壓枕巾香氛噴霧100ML+紓壓香氛皂200G+紓壓枕
            巾香氛噴霧15ML+普羅旺斯花植舒眠眼罩 *會員恕不再享折扣與積點、僅可累計第二階(含)
            以上滿額禮 、數量有限、售完為止。NT$1,380 以新鮮果香氣息幫助睡得更深更香甜!完美
            結合洋甘菊的蘋果蜜香、伊蘭伊蘭的恬雅花香,以及雪松柔和的木質氣息,以11種純淨精油共
            譜出自然清新的助眠香息。添加柔嫩肌膚的歐蜀葵和椰子油,以及舒緩身心的蘆薈葉和甜杏仁
            油。使用方式:將1瓶蓋靜心舒眠泡泡浴倒入流動的溫水中,入浴至少10-15分鐘。浴室充滿香
            氣時,以鼻子吸氣7秒,再慢慢從嘴裡吐氣11秒鐘,讓香氣達到最佳療癒效果。
            200ml/NT$1,200 添加法國普羅旺斯有機薰衣草精油,其舒緩功效及天然療癒安定氣息,
            透過浸泡時,身體便能快速達到放鬆舒緩的效果。有機芝麻油及有機葵花籽油,不僅有效
            滋潤肌膚,藉由浸泡過程,促進循環,使身體發熱,進而將體內老廢角質排出,讓身體更容易
            進入深層睡眠狀態,提升睡眠品質。140ml/NT$1,280 週年慶推薦:2021週慶香氛限定
            有機入門組年度鉅獻超值66折,主顧每年必預定、全台限量600組,搶先全亞洲首賣加味
            限量版「橙香摩洛哥堅果油」聯手小草作譜出活力柑橘協奏曲,推出全台僅有600組的限量
            週慶香氛限定有機入門組,一次擁有蜜葳特超經典油水三步驟,尤其內含全亞洲首賣新口味
            「橙香摩洛哥堅果油50ml」,及小草作獨家特調柑橘風味果乾水,整組充滿活力繽紛的
            柑橘氣息,雙限量只需不到3000元(週慶特價NT$2,980)就能一次擁有! 主要成分:黑胡椒、
            芫荽籽、廣藿香,氣味屬於溫暖的木質清香,可溫和徹底地清潔肌膚,含有優質的玫瑰花瓣油和
            其他軟化肌膚的植物萃取,是一款非常療癒的潔膚露
            。 100ml/NT$500、500ml補充裝/NT$1,350、500ml/NT$1,400 Bamford與芳療師
            共同為位於英國Cotswolds 科茲窩的 Bamford Haybarn SPA研發養心凝神的植萃
            保養療程,採用具活性成分的藥用植物與頂級天然有機成分,以甯靜金三角岩蘭草、洋甘菊
            、薰衣草 ,三款具安定、舒緩功效的精油為主軸,推出「B Silent 甯靜系列」
            。Bamford 相信植物的療癒力,為自己準備好進入更深沉、平穩的睡眠。 香氣怡人的
            甯靜浴油,含有最高濃度的有機精油,深層放鬆身體及心靈。以滋潤肌膚的杏桃核仁油為
            基底,調和具有助眠效果的有機羅馬洋甘菊、薰衣草、廣藿香及岩蘭草等精油。有機精油植萃
            成分高達16%,柔嫩滋養肌膚同時提供舒眠香氣。放鬆了雙腳也等於放鬆了身心
            。125ml/NT$3,900。 使用方式於澡盆中加入大約1瓶蓋的用量即可。可作為一周一次
            深層放鬆使用。 富含凝神舒緩的玫瑰花水、軟化肌膚的錦葵和高效保濕的椰子水,巧妙
            融合乳液軟化肌膚的特性與溫和潔膚功能,由乳液化成的泡沫蘊含庭園玫瑰系列
            標志性香氛,能夠柔軟肌膚散發迷人氣息,精神煥發一整天。250ml/NT$655 主要成份
            包括了: 玫瑰花水:保濕、舒緩、平衡肌膚,令肌膚充滿活力,散發清淡芳香。 椰子水
            :自然界的高效保濕成分,富含氨基酸和維生素。與人體PH值相近,對肌膚無負擔、高滲透
            補水。 蘆薈:舒緩肌膚,保濕補水,促進水分強力滲透肌膚,為為肌膚提供防護屏障
            。 維生素E :強大的抗氧化功效,保護、軟化並舒緩肌膚,使肌膚遠離乾燥
            、緊繃、敏感。 添加月桃精華,可幫助肌膚角質代謝,為乾燥疲憊的肌膚注入
            水潤感,洗後肌膚光滑柔嫩,細緻散發迷人的光澤!250ml/NT$780 週年慶推薦:
            阿原於全台店櫃以及官方商城購買,皂、臉、頭、身四大系列商品任選二件85折、
            三件8折的優惠,同時搭配五倍券優惠活動,即可享消費滿千送艾草皂。此外,阿原
            線上商城獨家加碼優惠,使用振興五倍券消費,即可享有買五送五優惠。無論紙本或是
            實體振興券都能讓消費者享受史上最划算的阿原週年慶優惠。 單筆滿額再送以下好禮
            ,四重好禮不累贈:『艾禮香氛鹽+舒方/悅方菁油棒』(價值NT$810)、『月桃皂120g+
            月桃50ml旅行組(洗澡水+洗頭水+潤髮乳)』 (價值NT$950)、『粉有愛臉部按摩組』
            (價值NT$2,590)、『金好梳+檸檬美髮素』(價值NT$2,060)。 面對濕度、溫度變化較大
            的秋天,可以避免使用較刺激的產品以減緩肌膚油脂和水分流失,而添加舒眠放鬆的精油,
            更能帶來良好的助眠效果。純真澄淨沐浴洗手露添加橙花複方精油,對神經擁有舒緩作用,
            有助於緩解壓力和焦慮,符合美國EWG健康友善認證與歐盟COSMOS有機認證標準,
            沒有過多成分造成肌膚負擔。250ml/NT$590
            '''
        ),
    )
    assert parsed_news.category == 'fashion'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1635074760
    assert parsed_news.reporter is None
    assert parsed_news.title == '睡前先做放鬆練習 秋季12款「療癒系沐浴」改善心情更好睡'
    assert parsed_news.url_pattern == '2104606'