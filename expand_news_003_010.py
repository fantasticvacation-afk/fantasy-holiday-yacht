#!/usr/bin/env python3
"""
扩写10篇新闻详情页内容 - 直接内联全部内容
"""
import re, os, shutil

BASE = '/Users/stone/.qclaw/workspace/fantasy-holiday-yacht'

# ==================== 全部内容 ====================

NEWS_CONTENT = {
    "003": {
        "zh": [
            "2026年4月28日，为期四天的第32届摩纳哥国际游艇展（Monaco International Yacht Show 2026）在赫库勒斯港圆满落幕。本届展会共吸引来自全球42个国家的628家参展商参展，展出超过120艘超级游艇和豪华帆船，参观人数达到创纪录的38500人次。展会期间累计完成的游艇订单总金额高达47亿欧元，较上届增长23%，创下历史新高。奇幻假期作为亚洲唯一受邀参展的游艇综合服务商，在展会上成功签下6艘超级游艇的托管意向协议，总金额约2.8亿欧元，并荣获「最佳亚洲展商」大奖。",
            "摩纳哥国际游艇展创办于1991年，是全球规模最大、最具影响力的超级游艇专业展会。本届展会的最大亮点是亚洲买家的强势崛起。数据显示，来自中国内地、香港、新加坡和阿联酋的买家贡献了展会总成交额的41%，较五年前翻了两番多。奇幻假期首席商务官林浩然指出：「亚洲买家与传统欧洲买家在需求偏好上存在显著差异。欧洲客户更看重游艇的历史底蕴和工艺传承，而亚洲客户则对智能化配置、个性化定制和娱乐系统有更高要求。」",
            "本届展会上，新能源动力游艇成为最热话题。意大利阿兹姆（Azimut）推出的SeaXplorer 72采用柴电混合动力，巡航半径达6500海里；荷兰Feadship发布的Project X是全球首艘采用固态电池技术的全电动超级游艇；德国Lürssen则展示了其正在建造的112米LNG动力巨型游艇。奇幻假期与其中多家厂商签订了战略合作协议，将在未来两年内引进至少10艘新能源动力超级游艇。",
            "奇幻假期在展会上与意大利Ferretti集团签署的五年战略合作协议成为全场焦点。根据协议，奇幻假期将成为Ferretti集团在亚太区的独家代理经销商，负责其在华所有品牌的市场推广、销售及售后服务。同时，双方将共同开发面向亚洲市场的定制化产品线，首款合作产品——一艘45米的「东西融合」系列豪华游艇预计将于2027年下水交付。Ferretti集团首席执行官阿尔贝托·加尔维斯表示：「奇幻假期拥有无与伦比的亚洲市场网络和客户资源，是我们拓展亚太市场的最佳战略伙伴。」",
            "在展会闭幕式颁奖典礼上，奇幻假期被授予「最佳亚洲展商」称号，以表彰其在促进亚欧游艇产业交流、推动行业标准制定和引领可持续发展方面的突出贡献。颁奖嘉宾、摩纳哥公国元首阿尔贝托二世亲王殿下亲切接见了奇幻假期代表团，并对公司「绿色海洋」计划表示赞赏。亲王殿下指出：「海洋是人类共同的财富，保护海洋环境是每一位航海者的责任。奇幻假期的实践为行业树立了良好典范。」",
            "展会期间，奇幻假期还组织了一场别开生面的「亚洲之夜」招待活动，邀请了200余位全球游艇行业领袖共同探讨合作机遇。招待会上，奇幻假期发布了专为亚洲高净值客户设计的「环游世界66天」超级游艇之旅产品：从摩纳哥出发，沿地中海一路向东，穿越苏伊士运河，经红海、印度洋，抵达新加坡，再北上香港、东京，最后横跨太平洋抵达洛杉矶，全程约22000海里。这条航线将于2027年正式推出，每期限额12位宾客，目前已有7位客户完成预订。"
        ],
        "en": [
            "On April 28, 2026, the 32nd Monaco International Yacht Show 2026 concluded its four-day run at Port Hercule. This year's exhibition attracted 628 exhibitors from 42 countries, showcasing over 120 superyachts and luxury sailing yachts, with a record 38,500 visitors. The event saw cumulative yacht orders totalling 4.7 billion euros, a 23% increase over the previous edition, setting a new historical record. Fantastic Vacation, as the only Asian comprehensive yacht service provider invited to exhibit, signed意向 agreements for 6 superyacht management contracts worth approximately 280 million euros and won the 'Best Asian Exhibitor' award.",
            "The Monaco International Yacht Show, founded in 1991, is the largest and most influential superyacht professional exhibition globally. The biggest highlight of this edition was the strong rise of Asian buyers. Data shows that buyers from mainland China, Hong Kong, Singapore and the UAE contributed 41% of the exhibition's total transaction value, more than quadrupling compared to five years ago. Fantastic Vacation's Chief Commercial Officer Lin Haoran pointed out: 'Asian buyers differ significantly from traditional European buyers in their preferences. European clients value a yacht's historical heritage and craftsmanship more, while Asian clients have higher requirements for intelligent configurations, personalised customisation and entertainment systems.'",
            "At this year's exhibition, new energy-powered yachts became the hottest topic. Italian shipbuilder Azimut's SeaXplorer 72 uses diesel-electric hybrid power with a cruise range of 6,500 nautical miles; Dutch Feadship's Project X is the world's first fully electric superyacht using solid-state battery technology; and German Lürssen displayed its 112-metre LNG-powered giant yacht under construction. Fantastic Vacation signed strategic cooperation agreements with several of these manufacturers to introduce at least 10 new energy-powered superyachts within the next two years.",
            "The five-year strategic cooperation agreement signed between Fantastic Vacation and the Italian Ferretti Group became the centrepiece of the exhibition. Under the agreement, Fantastic Vacation will become Ferretti Group's exclusive distributor in the Asia-Pacific region, responsible for marketing, sales and after-sales service for all its brands in China. Simultaneously, both parties will jointly develop customised product lines for the Asian market, with the first collaborative product — a 45-metre 'East Meets West' series luxury yacht — expected to be launched in 2027. Ferretti Group CEO Alberto Galvani stated: 'Fantastic Vacation has an unparalleled Asian market network and customer resources, making it the best strategic partner for us to expand into the Asia-Pacific market.'",
            "At the closing ceremony, Fantastic Vacation was awarded the 'Best Asian Exhibitor' title to recognise its outstanding contributions in promoting Asia-Europe yachting industry exchange, driving industry standard-setting and leading sustainable development. The Grand Master of Monaco, Prince Albert II, personally met with the Fantastic Vacation delegation and praised the company's 'Green Ocean' initiative. The Prince stated: 'The ocean is humanity's shared wealth, and protecting the marine environment is the responsibility of every seafarer. Fantastic Vacation's practices have set an excellent example for the industry.'",
            "During the exhibition, Fantastic Vacation also organised a distinctive 'Asian Night' reception, inviting over 200 global yachting industry leaders to explore cooperation opportunities. At the reception, Fantastic Vacation launched the '66-Day Around the World' superyacht journey product exclusively designed for Asian high-net-worth clients: departing from Monaco, sailing eastward along the Mediterranean, crossing the Suez Canal, through the Red Sea and Indian Ocean to Singapore, then north to Hong Kong and Tokyo, and finally across the Pacific to Los Angeles — approximately 22,000 nautical miles in total. This route will officially launch in 2027, with 12 guests per departure, and currently 7 clients have already completed bookings."
        ]
    },
    "004": {
        "zh": [
            "全球游艇行业协会（GLA）于2026年4月22日发布的《2026全球游艇市场报告》显示，2025年全球游艇市场规模达到约284亿美元，较前一年增长11.3%，预计到2030年将突破420亿美元大关。在各类细分市场中，新能源动力游艇的表现最为抢眼，全年订单量同比增长42%，首次占据新增游艇订单总量的18%。与此同时，亚洲市场以15.8%的年增长率成为全球增长最快的区域，其中中国市场的增速高达27%，令业界瞩目。",
            "报告由全球游艇行业协会联合麦肯锡咨询公司、瑞银财富管理部门共同编撰，历时八个月，对全球89个国家和地区的超过2000家游艇企业进行了调研。报告特别指出，推动全球游艇市场增长的核心动力已从「财富积累效应」转向「生活方式升级需求」。在全球高净值人群中，游艇正从「身份象征」向「生活必需品」转型。调研数据显示，超过60%的受访高净值人士表示「有意在未来五年内购买或租赁游艇」，这一比例较三年前的调查结果高出18个百分点。",
            "亚洲市场的崛起是本报告的另一大主题。2025年，亚洲游艇市场规模达到约127亿美元，占全球份额的45%，较五年前增长了近一倍。中国以约35%的亚洲市场份额位居第一，其次是新加坡（18%）、阿联酋（15%）、泰国（10%）和印度尼西亚（8%）。亚洲买家的平均游艇采购预算约为1800万美元，较欧洲买家高出约15%。",
            "新能源动力游艇的高速增长是本届报告最引人关注的数据。2025年，全球新能源动力游艇订单量达到约890艘，较2024年增长42%，订单总金额超过50亿美元。这一爆发式增长主要得益于三重因素的叠加：欧盟和IMO的环保法规趋严；电池和电机技术的快速进步；以特斯拉为代表的新能源汽车品牌成功培养了高净值人群对新能源产品的接受度。",
            "在新能源游艇技术路线上，柴电混合动力是目前商业化程度最高、接受度最广的方案。荷兰游艇制造商Oceanco的55米混合动力超级游艇Artemis号是目前全球最先进的混合动力游艇之一，采用ABB集团提供的Azipod吊舱式电动推进系统，碳排放较同级燃油游艇降低38%，同时将舱内噪音从传统的72分贝降至52分贝。奇幻假期首席技术官赵明阳表示：「我们看好氢能游艇的未来，但短期内仍将以混合动力为主流解决方案。公司计划在2027年前将混合动力游艇在自有船队中的占比提升至60%。」",
            "数字化和智能化是报告揭示的另一重要趋势。超过75%的新建游艇配备了智能家居级的中控系统，可通过手机APP或语音助手控制船上的照明、空调、窗帘、音响和安防系统。以色列游艇科技公司SeaTrac推出的AutoAnchor系统，可自动完成抛锚和起锚操作，大幅降低了游艇操作的复杂度。奇幻假期也已启动全面智能化升级，计划于2027年推出自主研发的OceanX OS智能船队管理系统。"
        ],
        "en": [
            "The Global Yachting Association (GLA) released the '2026 Global Yacht Market Report' on April 22, 2026, showing that the global yachting market reached approximately $28.4 billion in 2025, an 11.3% increase over the previous year, and is expected to exceed $42 billion by 2030. Among all market segments, new energy-powered yachts performed most impressively, with annual order volume growing 42% year-on-year and accounting for 18% of all new yacht orders for the first time. Meanwhile, the Asian market, growing at 15.8% annually, became the world's fastest-growing region, with China's market expanding at a striking 27%.",
            "The report, compiled by the GLA in conjunction with McKinsey & Company and UBS Wealth Management, took eight months and surveyed over 2,000 yachting enterprises across 89 countries and regions. The report particularly noted that the core driver of global yachting market growth has shifted from the 'wealth accumulation effect' to 'lifestyle upgrade demand'. Among global high-net-worth individuals, yachts are transitioning from 'status symbols' to 'life necessities'. Survey data shows that over 60% of high-net-worth respondents expressed 'interest in purchasing or chartering a yacht within the next five years', 18 percentage points higher than three years ago.",
            "The rise of the Asian market is another major theme of this report. In 2025, the Asian yachting market reached approximately $12.7 billion, accounting for 45% of the global share, nearly doubling compared to five years ago. China ranks first with approximately 35% of the Asian market, followed by Singapore (18%), UAE (15%), Thailand (10%) and Indonesia (8%). The average yacht purchase budget for Asian buyers is approximately $18 million, about 15% higher than European buyers.",
            "The explosive growth of new energy-powered yachts is the most attention-grabbing data in this report. In 2025, global new energy yacht orders reached approximately 890 units, a 42% increase over 2024, with total order value exceeding $5 billion. This explosive growth is mainly driven by three factors: tightening environmental regulations from the EU and IMO; rapid advances in battery and electric motor technology; and the success of new energy vehicle brands like Tesla in cultivating high-net-worth individuals' acceptance of new energy products.",
            "In terms of new energy yacht technology routes, diesel-electric hybrid is currently the most commercially mature and widely accepted solution. Dutch shipbuilder Oceanco's 55-metre hybrid superyacht Artemis is one of the world's most advanced hybrid yachts, using ABB Group's Azipod podded electric propulsion system, reducing carbon emissions by 38% compared to equivalent fuel-powered yachts while reducing cabin noise from the traditional 72 decibels to 52 decibels. Fantastic Vacation's Chief Technology Officer Zhao Mingyang stated: 'We are optimistic about the future of hydrogen-powered yachts, but in the short term, hybrid power will remain the mainstream solution. The company plans to increase the proportion of hybrid yachts in its owned fleet to 60% before 2027.'",
            "Digitalisation and intelligentisation is another important trend highlighted in the report. Over 75% of newly built yachts are equipped with smart home-level control systems, allowing control of lighting, air conditioning, curtains, audio and security systems via mobile apps or voice assistants. Israeli yachting technology company SeaTrac's AutoAnchor system can automatically complete anchoring and unanchoring operations, significantly reducing the complexity of yacht operation. Fantastic Vacation has also launched a comprehensive intelligentisation upgrade, planning to release its independently developed OceanX OS intelligent fleet management system in 2027."
        ]
    },
    "005": {
        "zh": [
            "2026年4月15日，奇幻假期实业有限公司与意大利Ferretti集团在米兰总部举行战略合作签约仪式。奇幻假期首席执行官陈永健与Ferretti集团首席执行官阿尔贝托·加尔维斯代表双方签署协议。根据协议，奇幻假期将成为Ferretti集团旗下全部七个品牌（包括Ferretti Yachts、Wally、Pershing、Itama、Riva、CRN和Custom Line）在亚太区的独家代理经销商，同时双方将共同投资3000万欧元成立合资公司，专注针对亚洲市场的新产品研发。这是Ferretti集团160年历史上首次与亚洲企业达成如此深度的战略合作，标志着亚欧游艇产业合作进入新纪元。",
            "Ferretti集团是全球历史最悠久、规模最大的豪华游艇制造商之一，旗下品牌矩阵覆盖从30英尺运动艇到100米以上巨型定制游艇的全价格区间。集团年营收超过10亿欧元，其中超过60%来自欧洲以外的市场。亚洲一直是Ferretti集团全球战略的重中之重，2025年亚洲市场贡献了集团全球营收的22%。Ferretti选择奇幻假期作为独家战略伙伴，正是看中了其独特的市场网络优势。",
            "根据协议，合资公司将在深圳设立亚洲研发中心，由奇幻假期提供市场洞察和客户需求数据，Ferretti提供造船工程技术和全球供应链支持。首期将开发两款专针对亚洲市场的定制产品：一款为45米的「东西合璧」系列豪华游艇，融合意大利经典工艺与中国传统文化元素，预计2027年下水；第二款为65米的「亚洲雄心」系列超级游艇，配备亚洲首个智能化中医养生舱和粤菜专业厨房，预计2028年交付。",
            "协议还包含船员培训与认证合作内容。Ferretti集团将授权奇幻假期船员培训学院使用其全球认证体系，并派遣意大利资深船长和工程师定期来华授课。这意味着奇幻假期的船员在完成培训后，不仅可获得意大利航海协会认证，还能得到Ferretti原厂的技术背书，大幅提升服务附加值和客户信任度。",
            "市场分析师对这一合作给予了高度评价。瑞银财富管理游艇行业分析师弗朗索瓦·杜邦表示：「奇幻假期与Ferretti的联姻是一个双赢的选择。Ferretti获得了进入亚洲主流市场的通行证，奇幻假期则获得了一个强大的产品背书和供应链支持。在亚洲游艇市场高速增长的背景下，这一合作有望催生出一个年营收超过5亿美元的亚太游艇服务巨头。」合作消息公布后，Ferretti集团在米兰证券交易所的股价单日上涨8.3%，创下近三年来的最大单日涨幅。"
        ],
        "en": [
            "On April 15, 2026, Fantastic Vacation Industrial Co., Ltd. and the Italian Ferretti Group held a strategic cooperation signing ceremony at Ferretti's Milan headquarters. Fantastic Vacation CEO Chen Yongjian and Ferretti Group CEO Alberto Galvani signed the agreement on behalf of their respective parties. Under the agreement, Fantastic Vacation will become the exclusive distributor in the Asia-Pacific region for all seven brands under the Ferretti Group — including Ferretti Yachts, Wally, Pershing, Itama, Riva, CRN and Custom Line — while both parties will jointly invest 30 million euros to establish a joint venture focused on new product development for the Asian market. This is the first time in Ferretti Group's 160-year history that it has entered such a deep strategic cooperation with an Asian enterprise, marking a new era in Asia-Europe yachting industry cooperation.",
            "The Ferretti Group is one of the world's oldest and largest luxury yacht manufacturers, with its brand portfolio covering the full price range from 30-foot sports boats to 100+ metre mega custom yachts. The Group generates annual revenue exceeding 1 billion euros, with over 60% coming from markets outside Europe. Asia has always been a priority in Ferretti Group's global strategy, with the Asian market contributing 22% of the Group's global revenue in 2025. Ferretti's choice of Fantastic Vacation as its exclusive strategic partner was precisely due to its unique market network advantages.",
            "According to the agreement, the joint venture will establish an Asia R&D Centre in Shenzhen, with Fantastic Vacation providing market insights and customer demand data, while Ferretti provides shipbuilding engineering technology and global supply chain support. The first phase will develop two products specifically for the Asian market: a 45-metre 'East Meets West' series luxury yacht blending Italian classic craftsmanship with traditional Chinese cultural elements, expected to be launched in 2027; and a 65-metre 'Asian Ambition' series superyacht equipped with Asia's first intelligent traditional Chinese medicine wellness cabin and authentic Cantonese kitchen, expected to be delivered in 2028.",
            "The agreement also includes crew training and certification cooperation. The Ferretti Group will authorise Fantastic Vacation's Crew Training Academy to use its global certification system and send Italian senior captains and engineers to China regularly for teaching. This means that after completing training, Fantastic Vacation's crew members can not only obtain certification from the Italian Nautical Association but also receive technical endorsement from Ferretti's factory, greatly enhancing service added value and customer trust.",
            "Market analysts gave high evaluations of this cooperation. UBS Wealth Management yachting industry analyst Francois Dupont stated: 'The marriage of Fantastic Vacation and Ferretti is a win-win choice. Ferretti gains access to the Asian mainstream market, while Fantastic Vacation gains powerful product endorsement and supply chain support. Against the backdrop of the high-speed growth of the Asian yachting market, this cooperation is expected to give birth to an Asia-Pacific yachting service giant with annual revenue exceeding $500 million.' Following the announcement, Ferretti Group's stock on the Milan Stock Exchange rose 8.3% in a single day, its largest single-day increase in nearly three years."
        ]
    },
    "006": {
        "zh": [
            "游艇生日派对正在成为全球高净值人群最追捧的庆祝方式之一。不同于传统的酒店宴会或私人会所，游艇派对将庆典与旅行、美食、探索融为一体，创造出独一无二的沉浸式体验。奇幻假期作为亚洲领先的游艇综合服务商，已为超过300位客户策划执行了各类海上庆典活动，积累了丰富的专业经验。",
            "第一步是选址规划。亚洲拥有得天独厚的游艇巡航资源，从泰国普吉岛的安达曼海到印尼龙目岛的科莫多国家公园，从菲律宾巴拉望的公主港到马尔代夫的环礁泻湖，每一处都有独特的自然风光和巡航体验。奇幻假期建议根据派对主题选择目的地：如果偏好热闹的派对氛围，泰国苏梅岛和印尼巴厘岛附近的水域拥有众多优质沙滩酒吧和海上浮台，适合举办融合沙滩与海上的双场景派对；如果追求宁静私密，菲律宾巴拉望的艾妮岛以其高耸的石灰岩峭壁和晶莹剔透的湖水闻名，适合营造探险感十足的小众派对。",
            "场景布置是决定派对氛围的关键。奇幻假期的专业活动策划团队建议从以下元素入手：首先是主色调选择，香槟金与象牙白的组合最易营造高级感；其次是花艺布置，甲板区域适合悬挂式花艺装置，室内区域则适合桌面花艺和烛台组合；第三是灯光设计，日落时分的甲板派对可使用暖色调串灯和蜡烛，日落后则切换为彩色LED灯带和激光灯效果。",
            "餐饮策划是派对体验的核心环节。奇幻假期与全球超过80位米其林厨师保持合作关系，可为客户安排随船主厨，在巡航途中现场烹制各国美食。建议的菜单结构包括：欢迎饮品（起泡酒或无酒精鸡尾酒配开胃小食）、正餐前小食（鱼子酱、和牛塔塔、松露鹅肝冻）、主菜（根据巡航海域可选当地新鲜海钓的鱼类、龙虾或澳洲和牛）、甜点（翻糖蛋糕配时令水果）。",
            "娱乐安排要根据宾客构成精心设计。奇幻假期建议采用「动静结合」的策划思路：静态活动包括海上SPA按摩、美甲护理、摄影写真和品酒会；动态活动则可根据海域条件安排浮潜、水上摩托、拖曳伞、皮划艇和海钓等项目。派对高潮通常安排在日落时分——此时可点燃海上烟花，配合专业DJ的音乐，将派对氛围推向顶点。",
            "安全预案是游艇派对策划中最不容忽视的环节。奇幻假期的标准配置包括：持有国际救生证书的专业救生员至少一名；全套急救设备包括AED（自动体外除颤器）和海上医疗急救包；与最近的海岸警卫队和直升机救援服务建立通讯联络；所有水上活动参与者必须穿戴救生衣；派对区域与游泳区域之间设置浮标隔离。所有宾客在登船前须签署免责协议并接受安全简报。"
        ],
        "en": [
            "Yacht birthday parties are becoming one of the most sought-after celebration methods among global high-net-worth individuals. Different from traditional hotel banquets or private clubs, yacht parties integrate celebrations with travel, cuisine and exploration, creating a unique immersive experience. Fantastic Vacation, as Asia's leading comprehensive yacht service provider, has planned and executed various sea celebration activities for over 300 clients, accumulating rich professional experience.",
            "The first step is location planning. Asia possesses uniquely privileged yachting resources, from the Andaman Sea around Phuket, Thailand, to the Komodo National Park in Lombok, Indonesia; from Puerto Princesa in Palawan, Philippines, to the atoll lagoons of the Maldives — each destination offers unique natural scenery and cruising experiences. Fantastic Vacation recommends selecting destinations based on party themes: for vibrant party atmospheres, waters around Koh Samui, Thailand, and Bali, Indonesia, with numerous quality beach bars and sea floating platforms, are ideal for dual-scene parties combining beach and sea; for those seeking tranquility and privacy, El Nido in Palawan, Philippines, famous for its towering limestone cliffs and crystal-clear turquoise waters, is perfect for creating an adventurous and exclusive party atmosphere.",
            "Scene decoration is key to determining the party atmosphere. Fantastic Vacation's professional event planning team recommends starting with the following elements: first, primary colour scheme — champagne gold and ivory white combinations most easily create a premium feel; second, floral arrangements — the deck area suits hanging floral installations while the interior is suited for table florals and candelabra combinations; third, lighting design — deck parties during sunset can use warm-toned string lights and candles, switching to coloured LED strips and laser effects after sunset.",
            "Catering planning is the core of the party experience. Fantastic Vacation maintains cooperative relationships with over 80 Michelin chefs globally, arranging onboard executive chefs to cook various international cuisines live during the cruise. Recommended menu structure includes: welcome drinks (sparkling wine or non-alcoholic cocktails with appetisers), pre-main bites (caviar, wagyu tartare, truffle foie gras terrine), main course (fresh local caught fish, lobster or Australian wagyu depending on cruise waters) and desserts (fondant cake with seasonal fruits).",
            "Entertainment arrangements should be carefully designed based on guest composition. Fantastic Vacation recommends a 'dynamic and static combination' approach: static activities include sea SPA massage, manicure services, photography sessions and wine tasting; dynamic activities can arrange snorkelling, jet skis, parasailing, kayaking and deep-sea fishing depending on sea conditions. The party climax is typically arranged at sunset — when sea fireworks can be ignited accompanied by a professional DJ's music, pushing the party atmosphere to its peak.",
            "Safety planning is the most indispensable element in yacht party planning. Fantastic Vacation's standard configuration includes: at least one professional lifeguard with international lifesaving certification; full first aid equipment including AED (Automated External Defibrillator) and maritime medical emergency kit; established communication links with the nearest coast guard and helicopter rescue services; all water activity participants must wear life jackets; a buoy barrier between party and swimming areas. All guests must sign liability waivers and receive safety briefings before boarding."
        ]
    },
    "007": {
        "zh": [
            "2026年3月28日，历经28天的艰苦航行，奇幻假期探险船队「极光号」和「冰魂号」顺利返航抵达澳大利亚悉尼港，完成了中国商业游艇服务业历史上首次南极大陆商业探险巡航。此次航行从阿根廷乌斯怀亚出发，穿越德雷克海峡，抵达南极半岛及南设得兰群岛海域，航程约5800海里。奇幻假期首席执行官陈永健亲自担任此次探险的荣誉领队，他在悉尼港的欢迎仪式上表示：「这不仅仅是一次商业航行，更是人类探索精神的一次致敬。我们向世界证明，中国企业有能力、有勇气到达地球上最遥远的地方。」",
            "南极探险的筹备工作从一年前就已启动。奇幻假期组建了一支由15人组成的专业筹备团队，其中包括三位具有南极航行经验的外籍探险队长、两位极地科学家、一位野生动物保护专家和九位经过严格筛选的船员。船只方面，「极光号」是一艘经过极地改装的双引擎探险游艇，总长38米，配备加固船体、零级隔热系统和防冰雷达；「冰魂号」是一艘专门为极地巡航设计的极地探险艇，配备伸缩式螺旋桨和加厚保温舱壁。两艘船均配备了Inmarsat卫星通讯系统、铱星应急定位信标和独立的淡水制取装置。",
            "航程中最具挑战性的阶段是穿越德雷克海峡。这片位于南美洲最南端与南极半岛之间的海域以恶劣天气著称，海浪经常超过10米。探险船队选择了每年3月窗口期出发，虽然风浪相对较小，但穿越期间仍然遭遇了持续三天的强风暴。探险队长、来自挪威的极地航海专家埃里克·拉尔森凭借二十余次德雷克海峡穿越经验，成功带领船队安全通过。",
            "当船队终于驶入南极水域，眼前的世界让所有人屏息：绵延数公里的冰川从岸边倾泻入海，巨大的冰山在阳光下呈现出层次分明的蓝白色调，成千上万的企鹅在岸边列队行进，鲸鱼的喷水柱在远处此起彼伏。探险队选择在欺骗岛（Deception Island）的天然港湾抛锚，这里是一个古老的火山口内部，风浪极小，是南极最受欢迎的停泊点之一。队员们在这里开展了首次登陆，徒步登上了火山口的边缘观景点，俯瞰整个海湾的壮丽景色。",
            "环保是此次南极探险的核心原则。奇幻假期严格执行《南极条约》环境保护议定书的所有规定：所有废弃物均带回船上进行处理，不在南极土地上留下一片纸屑；所有登岸人员必须彻底清洁和检查衣物及装备，防止外来物种入侵；与野生动物保持至少5米的最小安全距离，不主动靠近或干扰企鹅、海豹和海鸟的活动。探险期间，队员们还自发组织了两次海滩清洁行动，清理了约200公斤的海洋塑料垃圾。",
            "展望未来，奇幻假期已将南极航线正式纳入产品目录，每年3月定期发团，每次限额16位宾客，行程为期30天。首批2027年3月的南极探险名额已在返航当天开放预订，定价为每人18.8万美元，开售仅两小时即告售罄。这充分证明了市场对这一产品的热切需求，也标志着中国高净值人群的探险精神和消费能力已迈入新的阶段。"
        ],
        "en": [
            "On March 28, 2026, after a gruelling 28-day voyage, Fantastic Vacation's expedition fleet 'Aurora' and 'Ice Spirit' successfully returned to Sydney Harbour, Australia, completing the first commercial expedition cruise to Antarctica in the history of China's commercial yachting industry. The voyage departed from Ushuaia, Argentina, crossed the Drake Passage, reached the Antarctic Peninsula and South Shetland Islands waters, covering approximately 5,800 nautical miles. Fantastic Vacation CEO Chen Yongjian personally served as honorary leader of this expedition. At the welcome ceremony at Sydney Harbour, he stated: 'This is not merely a commercial voyage, but a tribute to the human spirit of exploration. We have proven to the world that Chinese enterprises have the capability and courage to reach the most remote places on Earth.'",
            "Preparations for the Antarctic expedition began a year in advance. Fantastic Vacation assembled a 15-person professional preparation team, including three foreign expedition leaders with Antarctic voyage experience, two polar scientists, one wildlife conservation expert and nine carefully screened crew members. Regarding vessels, 'Aurora' is a polar-modified twin-engine expedition yacht, 38 metres in length, equipped with reinforced hulls, zero-grade insulation systems and ice-penetrating radar; 'Ice Spirit' is a polar expedition vessel specifically designed for polar cruising, equipped with retractable propellers and thick insulated bulkheads. Both vessels are equipped with Inmarsat satellite communication systems, Iridium emergency position-indicating radio beacons and independent freshwater production devices.",
            "The most challenging phase of the voyage was crossing the Drake Passage. This body of water between the southern tip of South America and the Antarctic Peninsula is notorious for severe weather, with waves frequently exceeding 10 metres. The expedition fleet chose to depart during the March window each year. Although the winds and waves were relatively smaller, the fleet still encountered a three-day-long severe storm during the crossing. Expedition leader Erik Larsson, a Norwegian polar navigation expert with over twenty Drake Passage crossings, successfully guided the fleet through safely.",
            "When the fleet finally entered Antarctic waters, the world before everyone's eyes took their breath away: glaciers extending several kilometres cascaded from shore into the sea, enormous icebergs displayed distinct blue-white tones under the sunlight, thousands of penguins paraded along the shores in formation, and whale spouts rose and fell in the distance. The expedition team chose to anchor at Deception Island's natural harbour — an ancient volcanic crater interior with extremely calm winds and waters, one of the most popular anchoring points in Antarctica. The team conducted their first landing here, hiking to the edge viewpoint of the crater to overlook the magnificent scenery of the entire bay.",
            "Environmental protection was the core principle of this Antarctic expedition. Fantastic Vacation strictly observed all provisions of the Antarctic Treaty Environmental Protocol: all waste was brought back to the ship for processing, leaving not a scrap of paper on Antarctic soil; all landing personnel thoroughly cleaned and inspected clothing and equipment to prevent the introduction of alien species; a minimum safety distance of 5 metres from wildlife was maintained at all times, without actively approaching or disturbing penguins, seals or seabirds. During the expedition, team members also spontaneously organised two beach clean-up actions, removing approximately 200 kilograms of marine plastic waste.",
            "Looking ahead, Fantastic Vacation has officially included Antarctic routes in its product catalogue, departing every March with 16 guests maximum per trip, for a 30-day itinerary. The first batch of Antarctic expedition spots for March 2027 opened for booking on the return day, priced at $188,000 per person, and sold out within just two hours of opening. This fully demonstrates the market's eager demand for this product and marks a new stage in the exploratory spirit and spending capability of China's high-net-worth individuals."
        ]
    },
    "008": {
        "zh": [
            "在过去五年里，新加坡以其独特的地理优势、稳定的政治环境和开放的金融政策，迅速崛起为亚太地区最具吸引力的游艇中心。来自全球各地的游艇服务商、经纪公司、造船商和超级游艇买家纷纷将目光投向这颗「东南亚明珠」，使新加坡在全球游艇产业版图中的地位日益重要。奇幻假期作为深耕亚洲市场十五年的行业领军者，已在新加坡设立亚太区运营中心超过五年，深刻感受到了这座城市国家在全球游艇产业格局中日益增长的影响力。",
            "新加坡的游艇产业发展得益于多重有利因素的叠加。首先是地理优势——新加坡扼守马六甲海峡这一全球最重要的海上通道之一，从新加坡出发，可在24小时内抵达东南亚所有主要游艇目的地。其次是气候优势——新加坡地处赤道无风带，全年水温在26至30摄氏度之间，风浪较小，非常适合全年巡航。第三是政策优势——新加坡政府对游艇服务业采取开放和友好的态度，外国游艇可在简化手续下进入新加坡水域并获得临时登记；个人所得税最高税率仅为22%，远低于周边国家和地区。",
            "基础设施方面，新加坡近年来大幅增加了对游艇码头的投入。已有的圣淘沙One°15游艇会是东南亚最顶级的私人游艇会之一，拥有超过200个泊位，可停靠长达100米的超级游艇。2019年启用的滨海盛景城市游艇俱乐部则以其便利的市区位置和亲民的价格吸引了大批中小型游艇主。此外，新加坡政府正在推进的大士超级码头配套项目中，专门规划了游艇服务中心区域，预计2028年完工后将大幅提升新加坡接待超级游艇的能力。",
            "游艇经纪和销售业务在新加坡的增长尤为显著。以辛普森游艇（Simpson Marine）为代表的本地经纪公司，年均完成的游艇交易额超过2亿美元。英国伯尔尼特（Burlington）游艇经纪和意大利FSY游艇也先后在新加坡设立亚太总部，使新加坡成为亚洲高端游艇经纪的中心市场。奇幻假期观察到，近年来来自中国内地买家的成交比例持续上升，已占其新加坡业务量的40%以上。",
            "新加坡游艇保险和金融服务也在快速完善。苏黎世保险和安联全球游艇保险均在新加坡设有专属的亚太游艇保险团队，可为超级游艇提供定制化的全险、战争险和租船责任险服务。在融资方面，星展银行和华侨银行已开发出专门针对游艇资产的抵押贷款产品，贷款成数最高可达评估价值的60%，贷款期限最长15年，大大降低了游艇购买的门槛。",
            "展望未来，新加坡政府计划将游艇服务业打造成为「五个转型产业」之一，目标是在2030年前将游艇相关产业对GDP的贡献提升至10亿新元。政府正在研究设立游艇自由贸易区、推出游艇产业专业人才签证、以及简化游艇登记和检验流程等支持政策。这些政策的落地将进一步巩固新加坡作为亚洲游艇中心的地位。"
        ],
        "en": [
            "Over the past five years, Singapore has rapidly risen to become the most attractive yachting centre in the Asia-Pacific region, leveraging its unique geographical advantages, stable political environment and open financial policies. Yachting service providers, brokerage companies, shipbuilders and superyacht buyers from around the world have increasingly focused their attention on this 'Southeast Asian Pearl', elevating Singapore's position in the global yachting industry map. Fantastic Vacation, as an industry leader deeply rooted in the Asian market for fifteen years, has had its Asia-Pacific Operations Centre in Singapore for over five years, deeply feeling this city-state's growing influence in the global yachting industry landscape.",
            "Singapore's yachting industry development benefits from a combination of multiple favourable factors. First is geographical advantage — Singapore commands the Malacca Strait, one of the world's most important sea lanes, enabling departure from Singapore to reach all major Southeast Asian yachting destinations within 24 hours. Second is climatic advantage — Singapore lies in the equatorial calm belt, with year-round water temperatures between 26 and 30 degrees Celsius and gentle winds and waves, making it ideal for year-round cruising. Third is policy advantage — the Singapore government adopts an open and friendly attitude toward yachting services; foreign yachts can enter Singapore waters and obtain temporary registration with simplified procedures; the maximum personal income tax rate is only 22%, far lower than neighbouring countries and regions.",
            "In terms of infrastructure, Singapore has significantly increased investment in yachting marinas in recent years. The existing Sentosa Cove Yacht Club is one of the top private yacht clubs in Southeast Asia, with over 200 berths that can accommodate superyachts up to 100 metres in length. The Marina at Keppel Bay, opened in 2019, attracts many medium and small yacht owners with its convenient city-centre location and affordable prices. Additionally, the Singapore government's Tuas Mega Port project currently under construction specifically includes a yacht service centre area, expected to substantially enhance Singapore's capacity to receive superyachts upon completion in 2028.",
            "Yacht brokerage and sales business has grown particularly significantly in Singapore. Local broker Simpson Marine, as the representative, completes annual yacht transactions exceeding $200 million. British yacht broker Burlington and Italian FSY Yacht have also successively established Asia-Pacific headquarters in Singapore, making Singapore the centre market for Asian high-end yacht brokerage. Fantastic Vacation has observed that the proportion of buyers from mainland China has continued to rise in recent years, now accounting for over 40% of its Singapore business.",
            "Singapore's yacht insurance and financial services are also rapidly improving. Zurich Insurance and Allianz Global Marine Insurance both have dedicated Asia-Pacific yacht insurance teams in Singapore, providing customisable comprehensive insurance, war risk insurance and charter liability insurance for superyachts. In financing, DBS Bank and OCBC have developed mortgage products specifically for yacht assets, with loan-to-value ratios up to 60% of assessed value and loan terms up to 15 years, greatly lowering the threshold for yacht purchases.",
            "Looking ahead, the Singapore government plans to develop the yachting service industry as one of the 'five transformation industries', aiming to increase the yacht-related industry's contribution to GDP to S$1 billion by 2030. The government is studying supportive policies such as establishing a yacht free trade zone, introducing professional yacht industry talent visas, and simplifying yacht registration and inspection procedures. The implementation of these policies will further consolidate Singapore's position as the Asian yachting centre."
        ]
    },
    "009": {
        "zh": [
            "2026年3月12日，奇幻假期实业有限公司在深圳总部召开了战略发布会，正式公布《奇幻假期2026-2028三年发展战略规划》。公司董事会全体成员、管理层代表、主要合作伙伴及媒体记者共150余人出席发布会。奇幻假期首席执行官陈永健在发布会上系统阐述了公司在未来三年的战略愿景、业务布局和核心举措。他表示：「全球游艇产业正处于前所未有的黄金发展期，奇幻假期必须以更宏大的视野、更坚定的投入和更创新的思维，牢牢把握这一历史机遇。我们的目标是在2028年前成为亚太地区首个营收超过5亿美元的游艇综合服务商。」",
            "三年战略规划的核心是「一个平台、三大引擎、五大市场」的的整体框架。一个平台即「奇幻假期全球云服务平台」，三大引擎分别是船队扩张引擎、服务升级引擎和科技赋能引擎，五大市场则指中国大陆、东南亚、东亚、中东和南太平洋五大核心市场。公司计划在三年内累计投入不少于18亿元人民币，用于实现这一战略蓝图。",
            "在船队扩张方面，奇幻假期计划到2028年底将托管游艇数量从目前的120艘扩充至350艘，增幅近两倍。其中自有船队将从15艘增至50艘（含3艘液化天然气动力超级游艇），联合所有权和托管船队从105艘增至300艘。船队结构也将优化——30至50米的中型游艇占比从35%提升至50%，50至80米的大型游艇占比从15%提升至30%。",
            "服务升级是三年战略的重中之重。奇幻假期将推出全新升级的「钻石会籍」计划，设置入门级翡翠、商务级蓝宝石和旗舰级钻石三个等级，不同等级对应不同的服务内容和专属权益。钻石会籍客户将享有全年无限制使用全球超过100艘游艇的权益，这在业内属于首创。服务范围也将从传统的水上活动扩展至岸上生活体验，包括直升机接送、米其林餐厅预订、私人飞机包机和奢华酒店集团专属礼遇等。",
            "科技赋能是奇幻假期构建竞争优势的关键战略。公司将在未来三年投入3亿元用于智能化系统建设，主要包括：新一代船队管理平台OceanX OS的开发，该系统将整合物联网、大数据和人工智能技术，实现对全球船队的实时监控、智能调度和预测性维护；客户关系管理系统的升级，引入机器学习算法为客户推荐个性化的游艇和航线；以及区块链技术的应用，计划于2027年推出基于区块链的游艇资产确权系统。",
            "可持续发展是三年战略的重要组成部分。奇幻假期承诺到2028年实现三个「百分百」目标：自有船队100%获得环保认证、托管船队中新能源动力游艇占比达到100%、全球所有合作码头100%落实环保运营标准。公司还将把每年营业收入的2%注入「蓝色海洋基金」，用于海洋生态修复、海洋塑料清理和极地保护研究。奇幻假期因此成为亚洲首家提出如此全面环保承诺的游艇服务商。"
        ],
        "en": [
            "On March 12, 2026, Fantastic Vacation Industrial Co., Ltd. held a strategic press conference at its Shenzhen headquarters, officially unveiling the 'Fantastic Vacation 2026-2028 Three-Year Strategic Development Plan'. All board members, management representatives, major partners and media journalists totalling over 150 people attended the press conference. Fantastic Vacation CEO Chen Yongjian systematically elaborated on the company's strategic vision, business layout and core initiatives for the next three years. He stated: 'The global yachting industry is in an unprecedented golden period of development. Fantastic Vacation must firmly seize this historical opportunity with a grander vision, more determined investment and more innovative thinking. Our goal is to become the first Asia-Pacific yachting comprehensive service provider with revenue exceeding $500 million before 2028.'",
            "The core of the three-year strategic plan is the overall framework of 'One Platform, Three Engines, Five Markets'. The one platform is the 'Fantastic Vacation Global Cloud Service Platform'; the three engines are the Fleet Expansion Engine, Service Upgrade Engine and Technology Empowerment Engine; and the five markets refer to mainland China, Southeast Asia, East Asia, the Middle East and the South Pacific as the five core markets. The company plans to cumulatively invest no less than 1.8 billion RMB within three years to realise this strategic blueprint.",
            "In terms of fleet expansion, Fantastic Vacation plans to increase managed yachts from the current 120 to 350 by the end of 2028, a nearly threefold increase. Owned vessels will grow from 15 to 50 (including 3 LNG-powered superyachts), while joint ownership and managed fleets will increase from 105 to 300. Fleet structure will also be optimised — medium-sized yachts of 30 to 50 metres will increase from 35% to 50%, and large-sized yachts of 50 to 80 metres will increase from 15% to 30%.",
            "Service upgrade is a priority of the three-year strategy. Fantastic Vacation will launch the newly upgraded 'Diamond Membership' programme with three tiers — entry-level Jade, business-level Sapphire and flagship Diamond — with different tiers corresponding to different service contents and exclusive benefits. Diamond membership clients will enjoy unlimited access to over 100 yachts worldwide throughout the year, which is an industry-first. Service scope will also expand from traditional water activities to shore-based lifestyle experiences, including helicopter transfers, Michelin restaurant reservations, private jet charters and luxury hotel group exclusive privileges.",
            "Technology empowerment is a key strategic pillar for Fantastic Vacation to build competitive advantages. The company will invest 300 million RMB in intelligent system construction over the next three years, primarily including: the development of a new-generation fleet management platform OceanX OS, which will integrate IoT, big data and AI technologies to achieve real-time monitoring, intelligent scheduling and predictive maintenance of the global fleet; the upgrade of the customer relationship management system, introducing machine learning algorithms to recommend personalised yachts and routes for clients; and the application of blockchain technology, planning to launch a blockchain-based yacht asset confirmation system in 2027.",
            "Sustainable development is an important component of the three-year strategy. Fantastic Vacation commits to achieving three '100%' goals by 2028: 100% of owned vessels obtaining environmental certification, 100% of new energy-powered yachts in the managed fleet, and 100% of all global partner ports implementing environmental operating standards. The company will also inject 2% of annual operating revenue into the 'Blue Ocean Fund' for marine ecological restoration, ocean plastic cleanup and polar protection research. Fantastic Vacation thus becomes Asia's first yachting service provider to put forward such a comprehensive environmental commitment."
        ]
    },
    "010": {
        "zh": [
            "从摩纳哥的奢华到希腊的古韵，从克罗地亚的海湾到土耳其的阳光，地中海是全球游艇爱好者心中的「终极巡航目的地」。这条跨越六国、全程约3000海里的30天深度巡航航线，将带您从西向东穿越地中海最美的海域，每一站都是世界级的风景与文化盛宴。奇幻假期根据过去十五年的执行经验，为您精心策划了这份全程指南，涵盖航线规划、港口推荐、季节选择和预算参考。",
            "航线规划是整次巡航的基础。这条30天航线分为五个航段：第一段从摩纳哥到戛纳，途经尼斯和昂蒂布，约280海里，需3天；第二段从戛纳到巴塞罗那，穿越蔚蓝海岸，约200海里，需2天；第三段从巴塞罗那沿西班牙东海岸南行至直布罗陀，约450海里，需5天；第四段从直布罗陀穿越地中海西部抵达希腊雅典，途经撒丁岛、西西里岛和马耳他，约900海里，需10天；第五段从雅典出发环游爱琴海，途经米克诺斯、圣托里尼、罗德岛和土耳其博德鲁姆，约650海里，需10天。每个航段之间建议留出1至2天的港口休整时间。",
            "最佳航行季节是五月至十月，其中六月至九月是旺季，地中海阳光充沛、风平浪静。如果想避开人潮并享受较为宁静的巡航体验，建议选择五月中旬（薰衣草季节，蔚蓝海岸最美的时刻）或九月下旬（气温仍然温暖，但夏季游客已开始散去）。奇幻假期不建议在十月以后进入地中海巡航，因为北部海域已开始进入季风季节，风浪显著增大。",
            "摩纳哥是这条航线的完美起点。这座面积仅两平方公里的袖珍公国汇聚了全球最顶级的游艇服务。赫库勒斯港的超级游艇泊位可停靠超过700艘游艇，其中最长的泊位超过110米。戛纳和尼斯是蔚蓝海岸的两颗明珠。戛纳以其电影节闻名于世，尼斯则更为悠闲，适合在老城区的露天咖啡馆度过一个慵懒的下午。整段航程约60海里，海水呈现出从浅蓝到深蓝的渐变，美得令人窒息。",
            "巴塞罗那是这趟巡航的文化高点。高迪的圣家堂、古埃尔公园和米拉之家是不可错过的建筑奇观；兰布拉大道和博格利亚市场的美食让人流连忘返。巴塞罗那港提供超过1500个泊位，设施齐全。奇幻假期建议在巴塞罗那停留三天，充分感受这座城市的艺术与活力，同时对游艇进行中期保养检修。撒丁岛的斯梅拉尔达翡翠海岸（Costa Smeralda）是欧洲皇室和好莱坞明星最青睐的度假胜地，从切尔沃港出发，还可前往附近的拉马达莱娜群岛，那里有令人窒息的白沙滩和湛蓝海水。",
            "西西里岛是地中海最大的岛屿，也是这次巡航的文化重镇。首府巴勒莫融合了阿拉伯、诺曼和拜占庭建筑风格，世界遗产名录上的景点超过50处。陶尔米纳的古希腊剧场是西西里岛的标志，剧场背靠埃特纳火山，面临爱奥尼亚海，风景无与伦比。马耳他是地中海中部一颗被严重低估的宝石，首都瓦莱塔被UNESCO列为世界遗产。",
            "希腊爱琴海是这次30天航程的精华所在。从雅典比雷埃夫斯港出发，首先抵达米克诺斯岛——这座被誉为「爱琴海派对之都」的小岛，拥有惊艳的风车落日、洁白的基克拉迪建筑和热闹的沙滩派对文化。圣托里尼则完全是另一种气质——乘坐游艇从海上望去，那悬崖上层层叠叠的白色房屋和蓝色圆顶教堂，是明信片上永恒的经典画面。罗德岛是十字军骑士团的驻地，岛上的中世纪古城被UNESCO列为世界遗产。土耳其博德鲁姆是这次巡航的最后一站，曾是古代世界七大奇迹之一摩索拉斯王陵的所在地，如今则是土耳其最时尚的海滨度假胜地。",
            "巡航地中海30天，总预算参考约为25万至45万美元（按一艘6至8名客人的中大型游艇计算）。主要花费包括：游艇租赁（按天计，约2万至5万美元/天，30天合计60万至150万美元，如选择共享则可分摊至15万至40万美元）、港口费用（约5万美元）、燃油费（约3万至8万美元）、餐饮和服务费（约5万至10万美元）、岸上活动和景点门票（约2万美元）及往返机票和签证费（约1万美元）。奇幻假期为这条航线提供从行程规划、船舶租赁、船员配备、港口预订到岸上活动的全套餐服务。"
        ],
        "en": [
            "From Monaco's opulence to Greece's ancient charm, from Croatia's tranquil bays to Turkey's sunny shores, the Mediterranean is the 'ultimate cruising destination' in the hearts of yachting enthusiasts worldwide. This 30-day deep-cruise route spanning six countries and approximately 3,000 nautical miles will take you from west to east through the most beautiful sea areas of the Mediterranean, with every stop offering world-class scenery and cultural feasts. Drawing on fifteen years of operational experience, Fantastic Vacation has carefully planned this comprehensive guide for you, covering route planning, port recommendations, season selection and budget reference.",
            "Route planning is the foundation of the entire cruise. This 30-day route is divided into five segments: first, Monaco to Cannes via Nice and Antibes, approximately 280 nautical miles, requiring 3 days; second, Cannes to Barcelona across the French Riviera, approximately 200 nautical miles, requiring 2 days; third, Barcelona south along Spain's east coast to Gibraltar, approximately 450 nautical miles, requiring 5 days; fourth, crossing the western Mediterranean from Gibraltar to Athens, Greece, via Sardinia, Sicily and Malta, approximately 900 nautical miles, requiring 10 days; fifth, departing Athens to cruise the Aegean Sea via Mykonos, Santorini, Rhodes and Bodrum, Turkey, approximately 650 nautical miles, requiring 10 days. It is recommended to留出1至2天的港口休整时间 between each segment.",
            "The best cruising season is May to October, with June to September being peak season when the Mediterranean is sunny and calm. To avoid crowds and enjoy a more tranquil cruising experience, it is recommended to choose mid-May (lavender season, the most beautiful time on the French Riviera) or late September (temperatures still warm, but summer tourists have begun to disperse). Fantastic Vacation does not recommend cruising in the Mediterranean after October, as the northern seas begin entering monsoon season with significantly increased winds and waves.",
            "Monaco is the perfect starting point for this route. This miniature principality of just two square kilometres gathers the world's top yachting services. The superyacht berths at Port Hercule can accommodate over 700 yachts, with the longest berths exceeding 110 metres. Cannes and Nice are the two gems of the French Riviera. Cannes is world-famous for its film festival, while Nice is more laid-back, perfect for spending a lazy afternoon at outdoor cafés in the old town. The entire passage is approximately 60 nautical miles, with the sea displaying a breathtaking gradient from light blue to deep blue.",
            "Barcelona is the cultural highlight of this cruise. Gaudí's Sagrada Familia, Park Güell and Casa Milà are unmissable architectural wonders; Las Ramblas and La Boqueria Market offer unforgettable culinary experiences. Barcelona Port provides over 1,500 berths with comprehensive facilities. Fantastic Vacation recommends staying in Barcelona for three days to fully experience the city's art and vitality while conducting mid-cruise maintenance on the yacht. The Costa Smeralda of Sardinia is the most favoured resort destination for European royalty and Hollywood celebrities. From Porto Cervo, you can also visit the nearby La Maddalena Archipelago, with its breathtaking white sandy beaches and azure waters.",
            "Sicily is the largest island in the Mediterranean and the cultural highlight of this cruise. The capital Palermo blends Arab, Norman and Byzantine architectural styles, with over 50 UNESCO World Heritage-listed sites. Taormina's ancient Greek theatre is Sicily's landmark, with Mount Etna as its backdrop and the Ionian Sea before it — an unparalleled landscape. Malta is a severely underestimated gem in the central Mediterranean, with its capital Valletta listed as a UNESCO World Heritage site.",
            "The Greek Aegean Sea is the essence of this 30-day voyage. Departing from Athens' Piraeus Port, the first stop is Mykonos — this island dubbed the 'Party Capital of the Aegean' boasts stunning windmill sunsets, pure white Cycladic architecture and lively beach party culture. Santorini offers an entirely different atmosphere — viewed from the sea, the layered white houses on cliffs and blue-domed churches are an eternal classic on postcards. Rhodes was the seat of the Knights of the Crusader Order, with its medieval old town listed as a UNESCO World Heritage site. Turkey's Bodrum is the final stop on this cruise, once the site of one of the Seven Wonders of the Ancient World — the Mausoleum at Halicarnassus — and now Turkey's most fashionable seaside resort destination.",
            "The total budget for a 30-day Mediterranean cruise is approximately $250,000 to $450,000 USD (calculated for a mid-to-large yacht accommodating 6-8 guests). Major expenses include: yacht charter (priced per day, approximately $20,000 to $50,000 per day, totalling $600,000 to $1.5 million for 30 days, or $150,000 to $400,000 if sharing), port fees (approximately $50,000), fuel costs (approximately $30,000 to $80,000), dining and service expenses (approximately $50,000 to $100,000), shore activities and attraction tickets (approximately $20,000), and round-trip airfare and visa fees (approximately $10,000). Fantastic Vacation provides full-package services for this route, from itinerary planning and vessel charter to crew provisioning, port bookings and shore-based activities."
        ]
    }
}


def expand_news_page(num_str, data):
    """扩写单个新闻页面"""
    fname = os.path.join(BASE, f'news-{num_str}.html')
    if not os.path.exists(fname):
        print(f"  SKIP news-{num_str}: file not found")
        return []
    
    with open(fname, encoding='utf-8') as f:
        content = f.read()
    
    zh = data['zh']
    en = data['en']
    
    body_start = content.find('news-article-body')
    if body_start < 0:
        print(f"  SKIP news-{num_str}: no news-article-body")
        return []
    
    article_end = content.find('</article>', body_start)
    body_region = content[body_start:article_end]
    
    # 找现有keys
    existing = re.findall(r'data-i18n="(news-' + num_str + r'\.\d+)"', body_region)
    if not existing:
        print(f"  SKIP news-{num_str}: no existing i18n keys")
        return []
    
    last_key_num = int(existing[-1].split('.')[1])
    entries = []
    
    # 替换现有段落
    for i, key in enumerate(existing):
        if i < len(zh):
            pattern = f'({re.escape(key)}">)([^<]+)(</p>)'
            m = re.search(pattern, content)
            if m:
                content = content[:m.start(2)] + zh[i] + content[m.end(2):]
                entries.append((key, zh[i], en[i] if i < len(en) else zh[i]))
    
    # 追加新段落
    if len(zh) > len(existing):
        div_close = content.rfind('</div>', body_start, article_end)
        extra = ""
        for i in range(len(existing), len(zh)):
            k = f"news-{num_str}.{last_key_num + (i - len(existing)) + 1}"
            extra += f'\n<p style="color:var(--text-muted);line-height:2;font-size:15px;margin-bottom:20px" data-i18n="{k}">{zh[i]}</p>'
            entries.append((k, zh[i], en[i] if i < len(en) else zh[i]))
        content = content[:div_close] + extra + '\n' + content[div_close:]
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ news-{num_str}.html: {len(entries)} entries")
    return entries


def update_i18n(entries, i18n_path):
    if not os.path.exists(i18n_path):
        print(f"  SKIP {i18n_path}: not found")
        return
    
    with open(i18n_path, encoding='utf-8') as f:
        content = f.read()
    
    updated, added = 0, 0
    for key, zh_text, en_text in entries:
        zh_e = zh_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        en_e = en_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        
        # 尝试更新已有key
        key_pos = content.find(f'"{key}"')
        if key_pos >= 0:
            # 找这个key对应的zh值区域
            search = content[key_pos:key_pos+2000]
            zh_m = re.search(r'"zh"\s*:\s*"[^"]*"', search)
            en_m = re.search(r'"en"\s*:\s*"[^"]*"', search)
            if zh_m:
                p1 = key_pos + zh_m.start()
                p2 = key_pos + zh_m.end()
                content = content[:p1] + f'"zh": "{zh_e}"' + content[p2:]
            if en_m:
                en_pos = content.find(f'"en"', key_pos)
                en_m2 = re.search(r'"en"\s*:\s*"[^"]*"', content[en_pos:en_pos+500])
                if en_m2:
                    p1 = en_pos + en_m2.start()
                    p2 = en_pos + en_m2.end()
                    content = content[:p1] + f'"en": "{en_e}"' + content[p2:]
            updated += 1
        else:
            # 追加新条目
            last = None
            for m in re.finditer(r'"news-\d+\.\d+"\s*:\s*\{[^}]*\}', content):
                last = m
            if last:
                entry_str = f',\n  "{key}": {{"zh": "{zh_e}", "en": "{en_e}"}}'
                content = content[:last.end()] + entry_str + content[last.end():]
                added += 1
    
    with open(i18n_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ {os.path.basename(i18n_path)}: {updated} updated, {added} added")


def main():
    print("🚀 扩写新闻详情页 003-010\n")
    all_entries = []
    
    for num_str in sorted(NEWS_CONTENT.keys()):
        print(f"Processing news-{num_str}...")
        entries = expand_news_page(num_str, NEWS_CONTENT[num_str])
        all_entries.extend(entries)
    
    # 更新i18n.js
    print(f"\nUpdating i18n.js with {len(all_entries)} entries...")
    update_i18n(all_entries, os.path.join(BASE, 'i18n.js'))
    
    yt_i18n = os.path.join(BASE, 'YT', 'i18n.js')
    if os.path.exists(yt_i18n):
        update_i18n(all_entries, yt_i18n)
    
    # 同步HTML
    print("\nSyncing HTML...")
    for num_str in sorted(NEWS_CONTENT.keys()):
        fname = f'news-{num_str}.html'
        for subdir in ['en', 'YT', 'YT/en']:
            dst = os.path.join(BASE, subdir, fname)
            if os.path.exists(dst):
                shutil.copy2(os.path.join(BASE, fname), dst)
    
    print(f"\n✅ 完成！共处理 {len(all_entries)} 个条目")

if __name__ == '__main__':
    main()
