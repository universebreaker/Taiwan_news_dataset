import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/19/12/20/n11734006.htm'
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

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            今天是美東時間12月19號,星期四。 今天我們要聊的內容很多。最先要講到的是,最近大陸
            發生的兩件事,證明反送中這個香港式的抗爭風潮,已經悄然吹進大陸。一件發生在大學
            「復旦」,另一件,發生在廣東小鎮「播揚」,這兩個地方的名字就很有內涵。 但與此同時呢,
            香港資金援助抗爭者的「星火同盟」出事了,有4個相關的人被逮捕,「星火同盟」背後的
            支持者,大多是「和理非」抗爭人士,人們擔心,這些和理非的個人信息會被警方掌握。 復旦
            大學章程被改 學生杯葛聚集歌唱抗議 《願榮光歸香港》這首歌,今年9月開始,在香港抗爭
            市民中流行起來,大家聚集商場、廣場一期合唱,用歌聲表達訴求。 最近,大陸也出現了一個
            類似的場面。而且,還是在大學名校,就是上海「復旦大學」。 不少復旦大學學生,為了抗議
            大陸教育部批准了對復旦大學章程的修改,損害學術自由,自發要去學校運動場抗議,但是被
            校方阻止。結果他們在當地時間的12月18號下午,一起在學校食堂裡聚集,唱起了復旦大學的
            校歌。我們在視頻中看到,學生們站起來歌唱,旁邊保安無奈地阻止,並不成功。 復旦大學
            1925年創辦,目前在QS排名中位列世界第44,大陸高校排名第三。 學生們唱的復旦校歌,是
            1925年的老校歌,裡面有這麼一句話:復旦復旦旦復旦,巍巍學府文章煥,學術獨立思想自由,
            政羅教網無羈絆,無羈絆前程遠。 但是,新修改的學校章程,與校歌提出的精神,完全違背
            。 這起事件,我們從12月17號週二說起。這一天,大陸教育部網站發出一則通知,核准了復旦
            等三所大陸高等學府,對學校章程的修改。其中復旦的,受到的關注最多。 章程修改涉及
            幾十個地方。舉幾個例子。 章程中,「學校的辦學理念,是其校歌所傳頌的學術獨立和思想
            自由」,「思想自由」四個字被刪去。 「支持校長獨立負責地行使職權」中,「獨立」二字被
            刪去,變成了「依法」。 「按照黨委領導,校長負責,師生治學,民主管理的基本原則運行」,
            這句幾話,直接合併和簡略成一句話:「黨委領導下的校長負責制」。 並且,章程中還增加了
            「堅持用習近平新時代中國特色社會主義思想武裝師生員工頭腦」,這些話。 總之,修改的
            部分至少反映三點:堅持黨的全面領導、黨委是學校核心,以及突出了以習近平為主題的一些
            新內容。 校章被活生生改成了「黨章」,也有人嘲諷地說,新校章讓復旦變成「黨校」。這
            一次修改,除了涉及復旦,還有南京大學和陝西師範大學。改校章的事件,在中國的豆瓣、知乎
            等論壇,網友也發出一片罵聲。而復旦學生們在學校食堂合唱老校歌的抗議行為,也引起國際
            媒體關注。BBC引述網友留言,提到了「光復復旦 時代革命」的口號;《紐約時報》則分析
            指出,大陸當局在香港大學生的抗議中,似乎在加緊對高校學生意識形態「不留死角」地管控
            。 文樓「火葬場」未建先「火」!改址建設一樣引抗議 11月底,廣東茂名文樓鎮居民,為了
            阻止政府在當地修建火葬場,發起抗爭行動,很多人上街與警察對峙,場面像極了香港反送中:
            人們設置路障、朝警方扔磚頭、焚燒警方看守亭等等。當地人向《蘋果日報》說:就好像你們
            香港,遍地開花。也有《新唐人電視台》等海外中文媒體報導說:當地人喊出「光復茂名,時代
            革命」的口號。 讓外界意外的是,文樓的抗爭短短4天就結束了,而且跪低的是政府。當時,
            文樓鎮黨委書記李偉華提出了「五大回應」:1. 永不建火葬場;2. 調查鎮壓抗爭中的警察
            濫權;3. 釋放被捕人士,甚至對傷者提供醫療費補助;4. 有的設施被毀掉了、沒問題、政府
            出錢修;5. 施工地點立刻恢復綠化。 這麼振奮人心的五大回應,政府實際的執行情況咱們
            另說,但是單看字面,要是對香港五大訴求這麼痛快回應,事件也會早就平息,但為什麼區別
            對待呢!有的專家就分析,這是當局,怕香港的事擴散,所以想趕快平息。 人們以為事情就
            這樣結束了,結果不是。12月16號,在距離文樓僅僅27公里的茂名播揚鎮,又發生民眾的勇武
            抗爭事件,場面比文樓還激烈。 有當地人接受《蘋果日報》採訪時介紹說呢,事情起因是當地
            政府要建污水處理廠,但後來承認是要建火葬場。也有媒體報導說,這是文樓沒建成的火葬場,
            改到播揚來修建。不過後來當地政府又發聲明,說沒打算在當地建火葬場,類似說法是謠傳。
            政府說法反覆。但不管怎麼說,這場二次抗爭因為「火葬場」的問題爆發了。 最激烈的衝突
            在當地的12月16號晚爆發,上萬人走上街頭,兩百多公安武警到場鎮壓,使用了催淚彈、警棍、
            電槍等裝備,而抗議民眾,則用到了汽油彈、石頭、鞭炮,公安局被焚燒,並且堵路阻止警察行
            進。在受訪時,當地人說:哪裡有不公,哪裡就有反抗!但是當地人付出的代價不小。截至當晚
            9點,已經有四十多人受傷送院,有人傷勢嚴重,這個已得到醫院證實。網上還流傳說至少有
            一名青年被打死。 當地政府對播揚抗議的回應,則是有軟有硬,一方面,播揚鎮和其所在的
            化州市政府先後發聲明安撫,承諾不會在播揚建火葬場,另一方面,化州公安局又要求參與暴力
            示威的人「限期自首」,否則嚴懲。 播揚鎮的抗爭也引起了香港網友的議論,大家驚歎於抗爭
            場面與香港的相似,有人把這叫成了「火葬場革命」。 被指洗黑錢 香港「星火同盟」臉書
            發文澄清 那麼,說完大陸兩件跟香港反送中「撞臉」的抗議事件後,我們繼續關注香港。在
            6個多月的抗爭裡,香港的勇武派抗爭者受損失最大,很多人被捕。但現在香港有人擔心,當局
            為瓦解運動,或者在醞釀對「和理非」下手。 提起「星火同盟」,想人都知道。這是2016年
            香港「魚蛋革命」之後成立的非營利機構,他們通過眾籌捐款獲取資金,然後用這筆錢,協助
            被捕抗爭者保釋和法律諮詢服務,有時也會接濟經濟有困難的抗爭者。最近,他們還購買賀卡,
            呼籲市民寫聖誕賀卡,寄給獄中被囚的抗爭人士。「星火同盟」在抗爭者眼中,是慷慨解囊的
            義士,但是在反對者眼中,卻是接濟暴徒的黑手。 11月18號,香港《信報》報導,「星火同盟」
            因為銀行戶口跟當初報稱的開戶用途不符,被所在的「匯豐銀行」中止運作。同一天,「星火
            同盟」在臉書發貼文,說:由於各種因素,平台在匯豐銀行的帳戶11月21號之後暫停運作,但
            「星火同盟」會以其它方式接受捐款。 但到了12月19號,又出現另一事件。當天下午,香港
            警方開記者會,說破獲一宗「洗黑錢」案,指出案件與「星火同盟」有關,拘捕4人,並凍結了
            關聯「星火同盟」的空殼公司7000萬元資金。被捕的4個人,年齡在17歲到50歲之間,拘捕時
            警方還抄獲13萬現金,包括三千多張超市代金券,另外還有鐳射筆以及大量防護裝備。 警方
            說,星火在過去半年,籌得約8,000萬元,20%是現金,多數是香港當地的現金存款,而這些錢被
            轉入一家「空殼公司」,懷疑涉洗黑錢,其中一名被捕者是那間「空殼公司」的股東。 對此,
            「星火同盟」當天在臉書發文澄清,說「警方對星火同盟手足的拘捕行動,已進入法律程序」
            並且指出「警方企圖以失實陳述,將本平台之運作扭曲成洗黑錢等惡意用途,意圖抹黑星火及
            其它支援頻道,本平台譴責此等抹黑行為」。 在香港抗爭者聚集的連登討論區中,有很多貼文
            在聚焦此事,其中討論最多的問題之一就是,那些籌集去的幾千萬存款被凍結,如果香港有
            幾百萬人支持抗爭,那一個人捐幾十元很快還能湊起來。但是他們擔心,萬一警方通過這件
            案子,去查那些捐款背後的捐款人信息,就會很可怕。因為好多捐款的,是支持抗爭的和理非
            。 在當天下午的新聞會上,還有記者問到支援抗爭者是不是犯罪,警方給的回答是「複雜」,
            稱難以一概而論。 那「星火同盟」這件事情已經進入法律程序,更多細節和頭緒,我們接下去
            會繼續關注。 ~~~新拍探討~~~ 今天的「新拍探討」,我們簡單關件事。就是大陸又有一個
            公開的「五毛」,他自己遭遇了不公的待遇。這樣的例子之前也曝出好多了,比如染香啊、
            仇和啊,這都是大五毛。 最近這個呢,大家還記得,2014年10月,習近平在全國文藝座談會上,
            接待的人裡,有一個叫「花千芳」的網絡寫手吧。這是個東北撫順人,他稱自己是「自帶乾(干)
            糧的五毛」,簡稱「自乾五」。但是因為不會說話,曾說「中國引領信息時代的決心,已經是
            司馬昭之心」,「司馬昭之心」明顯是貶義詞,拍馬屁拍到了馬腿上,所以當局對這個人後來也
            是不冷不熱。 但是12月18號,花千芳突然在微博發了一篇文章抱怨,說自己母親「22年前的
            農村養老保險證書」上,原本說人到60歲後,每月會發200人民幣補貼,但最近政府說項目沒有
            了,就是說這一項「退休保障金」沒了。 花千芳在微博大倒苦水,但是沒多久,再顯五毛本色,
            他把自己的這則貼文隱藏了。然後又在微博發文,說目前還不清楚具體結算內容,以後每人也
            可能補幾十萬,又說今年比較亂,自己不添亂,最後勸其他網友「稍安勿躁」。 有網友評論說:
            東三省早就入不敷出了,哪裡還有錢給底層狗腿子呢。 這件事,我不發表議論,大家感興趣的,
            可以在今天節目下面留言探討,關下生活在大陸政權「食物鏈」最底層的這些人的命運。 ~~~
            新拍互動~~~ 現在我們進入「新拍互動」環節。 昨天的節目,我們主要談了川普的彈劾案
            。 先說一些對川普持正面觀點的觀眾。 觀眾gracewong說:過去三十年,西方不斷受文化
            馬克思主義所滲透,一埸西方的「文化大革命」正方興未艾,所以我2016年投票給 Trump,
            而2020年也會投給他。 觀眾TS說:川普總統的一些行事作風,例如把家族成員納入白宮幕僚,
            個人是無法接受的。但是,他在一些事情的敢作敢為,沒有一些政客的偽善和假道學,直接出面
            ,反而成為錢權當道下的「難能可貴」的真實。 觀眾yogi說:彈劾案恐是民主黨一方面,在
            保護拜登等更多被中共藍金黃的官員,假彈劾拉川普後腿以圖模糊焦點。 觀眾tintin說:
            彭斯真的不錯,但我選川普用商家的策略,以非常規對待中共有優勢。 還有一些觀眾,對川普
            的情感比較複雜啦。 觀眾ikimida說:身為女性真的好討厭川普,但我需要一個力量替我打
            包子,彭斯若可以繼續揍包子,我會很開心。但如果只有像川普說的he’s the chosen one,
            那我明年含淚投川普。 觀眾夢蝶說:我以前也可討厭川普了!我支持川普是因為川普反共
            ! 也有的觀眾,並不支持川普。 比如一位香港觀眾Heidy,用英文留言,我翻譯成中文,她
            這麼說:作為一名香港人,我很感謝你們最近有關香港的報導和陳述。我也完全支持川普跟中方
            的貿易戰,我也同意,川普說他是被選擇的那個人,去跟北京交手。因為,有時對待暴徒,就要
            用另一個暴徒。然而,我覺得你對川普彈劾案的報導很偏頗,因為你引用了太多川普寫給佩洛西
            的信,來描述這件案子,而川普的信裡有很多謊言和誤導。我想,任何公正的人,都會同意,川普
            應該被彈劾。 這位觀眾的觀點,確實代表了一批人的想法。美國社會對川普的彈劾案也是觀點
            分裂得很嚴重。今天我去查了一下民調,發現最新的民調,顯示美國民意又在發生著微妙的變化
            。 18號晚上,也就是眾議院投票正式彈劾川普的前後。CNN公布了一篇文章,標題是:《民主黨
            彈劾川普的同時 警燈也在閃爍》。文章引用一些最新的數據說:不斷增長的證據證明,對川普
            的彈劾正在使川普從政治上受益。 文章引用了12月17號早上的蓋洛普民調,顯示對川普工作
            的認可度,從10月份的39%,上漲到現在的45%,而不認可川普的比率,同期下降到51%。工作
            認可度能到45%,對一個美國總統來說,其實是個不壞的數字。 而支持彈劾的比率,從10月份
            的52%,下降到46%,同時不支持彈劾的比率,實現反超,從10月份的46%變成現在的51%。51%
            比46%,不支持彈劾的人現在更多。 CNN自己的民調也反映了這一點:本週早些時候的CNN民調
            顯示,支持彈劾川普的,從11月中旬的50%,掉到了現在的45%,不支持彈劾的比率,同期上升到
            46%。 現在是大選前夕,這些數字的變化,會引起川普對家的警覺,特別是那些中間派的獨立
            選民,會怎麼看待這些事情,需要特別的小心。 這兩天還有觀眾問翻牆用什麼軟件,有一位
            觀眾Aaron留言說:大陸想要VPN翻牆的,可以用自由門、無界,自從07年開始,我用了接近10
            年,直到出國。 Aaron建議不要用大陸產的瀏覽器,用海外的瀏覽器產品,複製粘帖動態ip,
            然後點擊下載自由門或無界就可以了。Aaron還說每天看大宇節目,謝謝您了! 至於什麼是
            「動態ip」,我查了一下大陸觀眾翻牆常看的「動態網」,網站最頂上有「用戶指南」的按鈕,
            我點進去看了一下,有一個辦法可以獲得能夠破網的「動態ip」,就是用海外信箱,比如gmail,
            寄一封信,標題不能空白,寄封信給freeget.ip@gmail.com,10分鐘內會得到回信,同時會
            得到幾個ip,這個郵件可能被當作垃圾郵件,所以收件箱裡沒有,可以去垃圾郵件裡找。 我
            看到,還有可以直接得到破網軟件下載鏈接的郵箱,方式同上,但是發郵件給
            freeget.one@gmail.com,也是10分鐘內就會有回信。 Aaron這個推薦的翻牆方式,我
            諮詢了比較可靠的人,與Aaron說的一樣。所以在這裡分享出來。大家還有什麼別的方法,歡迎
            繼續留言討論,但是翻牆「安全第一」,翻牆方式的選取,各位要謹慎。 昨天節目,我們還提到
            德國版香港人權法案的簽名請願,有觀眾留言說,簽名人數已經達標。在這裡也跟大家說一下
            。 再讀幾位澳門觀眾的留言。 澳門觀眾B說:很羨慕對岸的香港朋友能夠堅定自己的信念,
            對抗專制政權的惡行,身在澳門,知道別人是怎樣想我們的。最近覺得澳門已經成為一國一制
            了,心裡面很難受,百般滋味在心頭,雖然我們平時很少談政治,但是原來很多朋友和我一樣
            私底下也是一個黃絲,只是為了個人的安全不會說出來。 澳門觀眾T說:我是澳門人,我也是
            黃絲,心底裡討厭共產黨。 還一位澳門觀眾「白雲」說:我也有朋友是澳門人,也是黃絲,
            看到香港的情況只能氣憤。 最後讀一位觀眾Rosie的留言,她問:大宇,最後的 Frozen歌是
            剪壞了嗎? 還沒開始就結束了。 這裡要跟大家道歉,昨天結尾處,我們後期處理出了些問題,
            給大家感覺話沒說完。我們今天重新說一下,說清楚意思。就是有些觀眾留言,對於香港的
            情況,不相信,而且覺得我們有些報導,講的事情,比如可能的「被失蹤」、「被跳樓」啊,
            覺得不可思議。所以我引用了迪士尼新片《冰雪奇緣2》裡主題曲的一句歌詞:
            sing to those who’ll hear,唱給願意聽的人。這首主題曲叫《All Is Found》,
            我很喜歡,裡面還有別的歌詞,也很有意義,在這裡,我把按原文翻譯的中文歌詞貼出來幾句,
            跟大家分享: In her waters, deep and true 河水流動的
            深處 Lay the answers and a path for you 藏著答案指引你的
            路 Dive down deep into her sound 隨它的聲音探索 But not too far or you’
            ll be drowned 別走太遠怕被淹沒 Yes, she will sing to those who’
            ll hear 也許只有你能聽見 And in her song, all magic flows 它歌聲裡充滿
            神力 But can you brave what you most fear? 能否勇敢克服
            恐懼 Can you face what the river knows? 你能否面對這祕密
            '''
        ),
    )
    assert parsed_news.category == '新聞拍案驚奇'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1576771200
    assert parsed_news.reporter is None
    assert parsed_news.title == '抗爭風悄然北上 香港星火被盯上'
    assert parsed_news.url_pattern == '19-12-20-11734006'