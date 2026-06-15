#!/usr/bin/env python3
"""
扩写全部10篇新闻详情页内容 + 更新i18n.js + 同步语言版本
"""
import re, os, shutil, sys

BASE = '/Users/stone/.qclaw/workspace/fantasy-holiday-yacht'

# ==================== NEWS 001-002 (from JSON) ====================
import json
with open(os.path.join(BASE, 'news_expansion_content.json'), encoding='utf-8') as f:
    JSON_DATA = json.load(f)

# ==================== NEWS 003-010 (inline) ====================
# [All NEWS_CONTENT defined inline]

NEWS_CONTENT = {}

# Add 001-002 from JSON
for k in JSON_DATA:
    NEWS_CONTENT[k] = JSON_DATA[k]

# Add 003-010 inline
NEWS_CONTENT["003"] = {
    "zh": [
        "2026年4月28日，为期四天的第32届摩纳哥国际游艇展（Monaco International Yacht Show 2026）在赫库勒斯港圆满落幕。本届展会共吸引来自全球42个国家的628家参展商，展出超过120艘超级游艇，参观人数达38500人次。展会期间游艇订单总金额达47亿欧元，较上届增长23%，创历史新高。奇幻假期作为亚洲唯一受邀参展的游艇综合服务商，签下6艘超级游艇托管意向协议，总金额约2.8亿欧元，并荣获「最佳亚洲展商」大奖。",
        "摩纳哥国际游艇展创办于1991年，是全球规模最大、最具影响力的超级游艇专业展会。本届最大亮点是亚洲买家强势崛起，贡献了展会总成交额的41%，较五年前翻了两番多。奇幻假期首席商务官林浩然指出：「亚洲买家与传统欧洲买家在需求偏好上存在显著差异。欧洲客户更看重游艇的历史底蕴和工艺传承，而亚洲客户则对智能化配置、个性化定制和娱乐系统有更高要求。」",
        "新能源动力游艇成为展会最热话题。意大利阿兹姆SeaXplorer 72采用柴电混合动力，巡航半径达6500海里；荷兰Feadship的Project X是全球首艘固态电池全电动超级游艇；德国Lürssen展示了112米LNG动力巨型游艇。奇幻假期与多家厂商签订战略合作协议，将在两年内引进至少10艘新能源超级游艇。",
        "奇幻假期与意大利Ferretti集团签署的五年战略合作协议成为全场焦点。奇幻假期将成为Ferretti集团亚太区独家代理经销商，同时双方将共同投资3000万欧元成立合资公司，首款合作产品——45米「东西融合」系列豪华游艇预计2027年下水。Ferretti集团CEO阿尔贝托·加尔维斯表示：「奇幻假期拥有无与伦比的亚洲市场网络和客户资源，是我们拓展亚太市场的最佳战略伙伴。」",
        "在闭幕式上，奇幻假期被授予「最佳亚洲展商」称号。摩纳哥公国元首阿尔贝托二世亲王接见了奇幻假期代表团，并对公司「绿色海洋」计划表示赞赏。亲王殿下指出：「海洋是人类共同的财富，保护海洋环境是每一位航海者的责任。」",
        "展会期间，奇幻假期还发布了「环游世界66天」超级游艇之旅产品：从摩纳哥出发，穿越苏伊士运河，经印度洋到新加坡，再到香港、东京，最后横跨太平洋抵达洛杉矶，全程约22000海里。该航线将于2027年正式推出，每期限额12位宾客，已有7位客户完成预订。"
    ],
    "en": [
        "On April 28, 2026, the 32nd Monaco International Yacht Show concluded its four-day run at Port Hercule. The exhibition attracted 628 exhibitors from 42 countries, showcasing over 120 superyachts with a record 38,500 visitors. Cumulative yacht orders totalled 4.7 billion euros, a 23% increase, setting a new record. Fantastic Vacation, the only Asian comprehensive yacht service provider invited to exhibit, signed agreements for 6 superyacht management contracts worth approximately 280 million euros and won the 'Best Asian Exhibitor' award.",
        "The biggest highlight of this edition was the strong rise of Asian buyers, contributing 41% of total transaction value, more than quadrupling from five years ago. Fantastic Vacation CCO Lin Haoran noted: 'Asian buyers differ significantly from traditional European buyers in their preferences. European clients value heritage and craftsmanship more, while Asian clients have higher requirements for intelligent configurations, personalisation and entertainment systems.'",
        "New energy-powered yachts became the hottest topic. Italian Azimut's SeaXplorer 72 uses diesel-electric hybrid power with a 6,500-nautical-mile range; Dutch Feadship's Project X is the world's first solid-state battery fully electric superyacht; German Lürssen displayed a 112-metre LNG-powered mega yacht. Fantastic Vacation signed strategic agreements with several manufacturers to introduce at least 10 new energy superyachts within two years.",
        "The five-year strategic cooperation agreement between Fantastic Vacation and the Italian Ferretti Group was the centrepiece. Fantastic Vacation will become Ferretti Group's exclusive distributor in the Asia-Pacific region, while both parties will jointly invest 30 million euros in a joint venture. The first collaborative product — a 45-metre 'East Meets West' series luxury yacht — is expected to launch in 2027. Ferretti Group CEO Alberto Galvani stated: 'Fantastic Vacation has unparalleled Asian market networks and customer resources, making it our best strategic partner for Asia-Pacific expansion.'",
        "At the closing ceremony, Fantastic Vacation was awarded the 'Best Asian Exhibitor' title. Monaco's Grand Master Prince Albert II personally met with the Fantastic Vacation delegation and praised the company's 'Green Ocean' initiative, stating: 'The ocean is humanity's shared wealth, and protecting the marine environment is every seafarer's responsibility.'",
        "During the exhibition, Fantastic Vacation launched the '66-Day Around the World' superyacht journey: from Monaco, through the Suez Canal, across the Indian Ocean to Singapore, then Hong Kong and Tokyo, finally across the Pacific to Los Angeles — approximately 22,000 nautical miles. This route will officially launch in 2027, with 12 guests per departure, and 7 clients have already booked."
    ]
}

NEWS_CONTENT["004"] = {
    "zh": [
        "全球游艇行业协会（GLA）发布的《2026全球游艇市场报告》显示，2025年全球游艇市场规模达约284亿美元，较前一年增长11.3%，预计到2030年将突破420亿美元。新能源动力游艇订单量同比增长42%，首次占据新增订单总量的18%。亚洲市场以15.8%的年增长率成为全球增长最快区域，中国市场增速高达27%。",
        "报告由GLA联合麦肯锡、瑞银共同编撰，历时八个月，调研了全球89个国家和地区超过2000家游艇企业。报告指出，推动市场增长的核心动力已从「财富积累效应」转向「生活方式升级需求」。超过60%的受访高净值人士有意在五年内购买或租赁游艇，较三年前高出18个百分点。",
        "2025年亚洲游艇市场规模达约127亿美元，占全球份额的45%，较五年前增长近一倍。中国以约35%的亚洲市场份额位居第一，亚洲买家平均采购预算约1800万美元，较欧洲买家高出约15%。",
        "新能源游艇爆发式增长得益于三重因素：欧盟和IMO环保法规趋严；电池和电机技术快速进步；新能源汽车品牌培养了高净值人群对新能源产品的接受度。柴电混合动力是目前商业化程度最高的方案，荷兰Oceanco的55米混合动力游艇Artemis号碳排放降低38%，舱内噪音从72分贝降至52分贝。",
        "奇幻假期首席技术官赵明阳表示：「我们看好氢能游艇的未来，但短期内仍以混合动力为主流。公司计划2027年前将混合动力游艇在自有船队中占比提升至60%。」公司还启动了全面智能化升级，计划2027年推出自主研发的OceanX OS智能船队管理系统。",
        "报告预测全球游艇市场将呈现五大趋势：新能源化、智能化、共享化、体验化和绿色化。到2030年，新能源动力游艇在新增订单中的占比有望突破40%；智能驾驶辅助系统将成为30米以上游艇的标准配置。"
    ],
    "en": [
        "The Global Yachting Association (GLA) released the '2026 Global Yacht Market Report' showing the global yachting market reached approximately $28.4 billion in 2025, an 11.3% increase, expected to exceed $42 billion by 2030. New energy yacht orders grew 42% year-on-year, accounting for 18% of all new orders for the first time. The Asian market grew at 15.8% annually, becoming the world's fastest-growing region, with China at 27%.",
        "The report, compiled by GLA with McKinsey and UBS over eight months, surveyed over 2,000 yachting enterprises across 89 countries. It noted that the core growth driver has shifted from 'wealth accumulation' to 'lifestyle upgrade demand'. Over 60% of high-net-worth respondents expressed interest in purchasing or chartering a yacht within five years, 18 percentage points higher than three years ago.",
        "In 2025, the Asian yachting market reached approximately $12.7 billion, 45% of the global share, nearly doubling from five years ago. China ranks first with approximately 35% of the Asian market. Asian buyers' average purchase budget is approximately $18 million, about 15% higher than European buyers.",
        "The explosive growth of new energy yachts is driven by three factors: tightening EU and IMO environmental regulations; rapid advances in battery and motor technology; and new energy vehicle brands cultivating HNWIs' acceptance of new energy products. Diesel-electric hybrid is the most commercially mature solution; Dutch Oceanco's 55-metre hybrid yacht Artemis reduces carbon emissions by 38% and cabin noise from 72 to 52 decibels.",
        "Fantastic Vacation CTO Zhao Mingyang stated: 'We are optimistic about hydrogen-powered yachts' future, but hybrid power will remain the mainstream short-term solution. The company plans to increase hybrid yachts in its owned fleet to 60% before 2027.' The company has also launched a comprehensive intelligentisation upgrade, planning to release its OceanX OS intelligent fleet management system in 2027.",
        "The report predicts five major trends: new energy transition, intelligentisation, sharing economy, experiential focus and green development. By 2030, new energy yachts are expected to exceed 40% of new orders; intelligent driving assistance systems will become standard on yachts over 30 metres."
    ]
}

NEWS_CONTENT["005"] = {
    "zh": [
        "2026年4月15日，奇幻假期与意大利Ferretti集团在米兰总部举行战略合作签约仪式。奇幻假期将成为Ferretti集团旗下全部七个品牌在亚太区的独家代理经销商，同时双方将共同投资3000万欧元成立合资公司。这是Ferretti集团160年历史上首次与亚洲企业达成如此深度的战略合作。",
        "Ferretti集团年营收超过10亿欧元，2025年亚洲市场贡献了集团全球营收的22%。奇幻假期拥有亚洲最大的游艇买家数据库，涵盖15个国家和地区的超过5000位活跃高净值客户，这正是Ferretti选择奇幻假期的关键原因。",
        "合资公司将在深圳设立亚洲研发中心，首期开发两款定制产品：45米「东西合璧」系列豪华游艇（融合意大利经典工艺与中国传统文化元素），预计2027年下水；65米「亚洲雄心」系列超级游艇（配备智能化中医养生舱和粤菜专业厨房），预计2028年交付。",
        "协议还包含船员培训与认证合作。Ferretti集团授权奇幻假期船员培训学院使用其全球认证体系，并派遣意大利资深船长和工程师定期来华授课。首期联合培训班计划2026年第三季度开课，预计培养30名国际认证高级船员。",
        "瑞银游艇行业分析师弗朗索瓦·杜邦表示：「奇幻假期与Ferretti的联姻是双赢选择，有望催生年营收超过5亿美元的亚太游艇服务巨头。」消息公布后，Ferretti集团股价单日上涨8.3%，创近三年最大单日涨幅。"
    ],
    "en": [
        "On April 15, 2026, Fantastic Vacation and the Italian Ferretti Group held a strategic cooperation signing ceremony at Ferretti's Milan headquarters. Fantastic Vacation will become the exclusive distributor for all seven Ferretti Group brands in the Asia-Pacific region, while both parties will jointly invest 30 million euros to establish a joint venture. This is the first time in Ferretti Group's 160-year history that it has entered such deep strategic cooperation with an Asian enterprise.",
        "Ferretti Group generates annual revenue exceeding 1 billion euros, with the Asian market contributing 22% of global revenue in 2025. Fantastic Vacation possesses Asia's largest yacht buyer database, covering over 5,000 active high-net-worth clients across 15 countries and regions — the key reason Ferretti chose Fantastic Vacation.",
        "The joint venture will establish an Asia R&D Centre in Shenzhen, initially developing two customised products: a 45-metre 'East Meets West' series luxury yacht blending Italian classic craftsmanship with Chinese cultural elements, expected to launch in 2027; and a 65-metre 'Asian Ambition' series superyacht with an intelligent TCM wellness cabin and Cantonese kitchen, expected for delivery in 2028.",
        "The agreement also includes crew training and certification cooperation. Ferretti Group authorises Fantastic Vacation's Crew Training Academy to use its global certification system and will send Italian senior captains and engineers to China for regular teaching. The first joint training class is planned for Q3 2026, expecting to train 30 internationally certified senior crew members.",
        "UBS yachting industry analyst Francois Dupont stated: 'The marriage of Fantastic Vacation and Ferretti is a win-win choice, expected to give birth to an Asia-Pacific yachting service giant with annual revenue exceeding $500 million.' Following the announcement, Ferretti Group's stock rose 8.3% in a single day, its largest single-day increase in nearly three years."
    ]
}

NEWS_CONTENT["006"] = {
    "zh": [
        "游艇生日派对正在成为全球高净值人群最追捧的庆祝方式之一。不同于传统酒店宴会，游艇派对将庆典与旅行、美食、探索融为一体，创造独一无二的沉浸式体验。奇幻假期已为超过300位客户策划执行了各类海上庆典活动。",
        "选址规划是第一步。亚洲拥有得天独厚的游艇巡航资源：偏好热闹氛围可选泰国苏梅岛和印尼巴厘岛，拥有沙滩酒吧和海上浮台，适合双场景派对；追求宁静私密可选菲律宾巴拉望艾妮岛，以石灰岩峭壁和晶莹湖水闻名。",
        "场景布置决定派对氛围。奇幻假期建议：主色调选香槟金与象牙白营造高级感；甲板区适合悬挂花艺装置，室内适合桌面花艺和烛台组合；日落时分用暖色串灯和蜡烛，日落后切换彩色LED和激光灯效果。",
        "餐饮策划是核心环节。奇幻假期与全球超过80位米其林厨师合作，可安排随船主厨现场烹制各国美食。菜单建议：欢迎饮品配开胃小食、鱼子酱和牛塔塔松露鹅肝冻、主菜根据巡航海域选新鲜海钓鱼类龙虾或和牛、翻糖蛋糕配时令水果。",
        "娱乐安排要「动静结合」：静态活动包括海上SPA、美甲护理、摄影写真和品酒会；动态活动可安排浮潜、水上摩托、拖曳伞、皮划艇和海钓。派对高潮通常在日落时分——点燃海上烟花配合专业DJ音乐，将氛围推向顶点。",
        "安全预案不容忽视。奇幻假期标准配置包括：持国际救生证书的专业救生员、全套急救设备含AED、与海岸警卫队建立通讯联络、水上活动必须穿戴救生衣、派对区与游泳区设浮标隔离。所有宾客登船前须签署免责协议并接受安全简报。"
    ],
    "en": [
        "Yacht birthday parties are becoming one of the most sought-after celebration methods among global high-net-worth individuals. Different from traditional hotel banquets, yacht parties integrate celebrations with travel, cuisine and exploration. Fantastic Vacation has planned and executed various sea celebrations for over 300 clients.",
        "Location planning is the first step. Asia offers uniquely privileged yachting resources: for vibrant atmospheres, Koh Samui and Bali feature beach bars and sea platforms for dual-scene parties; for tranquility, El Nido in Palawan, Philippines, is famous for its limestone cliffs and crystal-clear waters.",
        "Scene decoration determines the atmosphere. Fantastic Vacation recommends: champagne gold and ivory white for premium feel; hanging floral installations for deck areas, table florals and candelabras for interiors; warm string lights and candles at sunset, switching to coloured LED strips and laser effects after dark.",
        "Catering planning is the core. Fantastic Vacation partners with over 80 Michelin chefs worldwide for onboard dining. Recommended menu: welcome drinks with appetisers, caviar and wagyu tartare with truffle foie gras, main course featuring fresh local catch or wagyu, fondant cake with seasonal fruits.",
        "Entertainment should combine 'dynamic and static': static activities include sea SPA, manicures, photography sessions and wine tasting; dynamic activities include snorkelling, jet skis, parasailing, kayaking and deep-sea fishing. The party climax is typically at sunset — fireworks accompanied by a professional DJ's music push the atmosphere to its peak.",
        "Safety planning is indispensable. Fantastic Vacation's standard configuration includes: professional lifeguards with international certification, full first aid equipment including AED, established coast guard communication links, mandatory life jackets for water activities, buoy barriers between party and swimming areas. All guests must sign waivers and receive safety briefings before boarding."
    ]
}

NEWS_CONTENT["007"] = {
    "zh": [
        "2026年3月28日，奇幻假期探险船队「极光号」和「冰魂号」顺利返航悉尼港，完成中国商业游艇服务业首次南极商业探险巡航。航行从阿根廷乌斯怀亚出发，穿越德雷克海峡，抵达南极半岛及南设得兰群岛，航程约5800海里。CEO陈永健表示：「这不仅是一次商业航行，更是人类探索精神的致敬。我们向世界证明，中国企业有能力到达地球上最遥远的地方。」",
        "筹备工作从一年前启动，组建了15人专业团队，含三位南极航行经验外籍探险队长、两位极地科学家和九位精选船员。「极光号」为38米极地改装双引擎探险游艇，配备加固船体和防冰雷达；「冰魂号」为专用极地探险艇，配伸缩螺旋桨和加厚保温舱壁。两船均配Inmarsat卫星通讯和铱星应急定位。",
        "穿越德雷克海峡是最具挑战的阶段。这片海域以恶劣天气著称，海浪常超10米。船队在3月窗口期出发，仍遭遇三天强风暴。探险队长、挪威极地航海专家埃里克·拉尔森凭借二十余次穿越经验，成功带领船队安全通过。",
        "驶入南极水域后，眼前的世界令人屏息：绵延冰川倾泻入海，巨大冰山呈现蓝白色调，成千上万企鹅列队行进，鲸鱼喷水柱此起彼伏。探险队在欺骗岛天然港湾抛锚——古老的火山口内部，风浪极小。队员们徒步登上火山口边缘，俯瞰海湾壮丽景色。",
        "环保是核心原则。奇幻假期严格执行《南极条约》环保议定书：所有废弃物带回船处理；登岸人员须清洁检查防外来物种入侵；与野生动物保持5米最小距离。探险期间队员们自发组织两次海滩清洁，清理约200公斤海洋塑料垃圾。",
        "奇幻假期已将南极航线纳入产品目录，每年3月定期发团，限额16位宾客，行程30天。2027年3月名额开售仅两小时即售罄，定价18.8万美元/人，充分证明市场热切需求。"
    ],
    "en": [
        "On March 28, 2026, Fantastic Vacation's expedition fleet 'Aurora' and 'Ice Spirit' returned to Sydney Harbour, completing China's first commercial Antarctic expedition cruise. The voyage departed from Ushuaia, Argentina, crossed the Drake Passage, reached the Antarctic Peninsula and South Shetland Islands, covering approximately 5,800 nautical miles. CEO Chen Yongjian stated: 'This is not merely a commercial voyage, but a tribute to the human spirit of exploration. We have proven that Chinese enterprises can reach the most remote places on Earth.'",
        "Preparations began a year in advance with a 15-person professional team, including three foreign expedition leaders with Antarctic experience, two polar scientists and nine screened crew. 'Aurora' is a 38-metre polar-modified twin-engine expedition yacht with reinforced hull and ice-penetrating radar; 'Ice Spirit' is a dedicated polar expedition vessel with retractable propellers and insulated bulkheads. Both carry Inmarsat satellite communications and Iridium emergency beacons.",
        "Crossing the Drake Passage was the most challenging phase. This body of water is notorious for severe weather, with waves frequently exceeding 10 metres. Despite departing during the March window, the fleet encountered a three-day severe storm. Expedition leader Erik Larsson, a Norwegian polar expert with over twenty Drake Passage crossings, guided the fleet through safely.",
        "Entering Antarctic waters, the world was breathtaking: glaciers cascading into the sea, massive icebergs in layered blue-white tones, thousands of penguins parading on shore, whale spouts rising in the distance. The team anchored at Deception Island's natural harbour — an ancient volcanic crater with calm conditions. Members hiked to the crater rim for panoramic views.",
        "Environmental protection was the core principle. Fantastic Vacation strictly observed the Antarctic Treaty Environmental Protocol: all waste returned to ship; landing personnel cleaned and inspected gear to prevent alien species; minimum 5-metre distance from wildlife. Team members organised two beach clean-ups, removing approximately 200 kg of marine plastic.",
        "Fantastic Vacation has added Antarctic routes to its product catalogue, departing every March with 16 guests maximum per 30-day trip. 2027 March spots sold out within two hours at $188,000 per person, demonstrating eager market demand."
    ]
}

NEWS_CONTENT["008"] = {
    "zh": [
        "新加坡以其独特地理优势、稳定政治环境和开放金融政策，迅速崛起为亚太地区最具吸引力的游艇中心。奇幻假期已在新加坡设立亚太区运营中心超过五年，深刻感受到这座城市国家在全球游艇产业格局中日益增长的影响力。",
        "新加坡游艇产业发展得益于多重优势：地理上扼守马六甲海峡，24小时内可达东南亚所有主要游艇目的地；气候上地处赤道无风带，全年水温26至30度，风浪小，适合全年巡航；政策上对游艇服务业开放友好，个人所得税最高税率仅22%，远低于周边国家。",
        "基础设施方面，圣淘沙One°15游艇会拥有超过200个泊位，可停靠100米超级游艇。滨海盛景城市游艇俱乐部以便利市区位置吸引中小型游艇主。大士超级码头配套项目中专门规划了游艇服务中心，预计2028年完工后将大幅提升接待能力。",
        "游艇经纪业务增长显著。辛普森游艇年均交易额超2亿美元，英国Burlington和意大利FSY也先后在新加坡设立亚太总部。奇幻假期观察到中国内地买家成交比例持续上升，已占其新加坡业务量40%以上。",
        "游艇保险和金融服务快速完善。苏黎世保险和安联均在新加坡设亚太游艇保险团队，提供全险、战争险和租船责任险。星展银行和华侨银行开发出游艇抵押贷款产品，贷款成数最高60%，期限最长15年。",
        "新加坡政府计划将游艇服务业打造为「五个转型产业」之一，目标2030年前游艇相关产业对GDP贡献提升至10亿新元。政府正研究设立游艇自由贸易区、推出专业人才签证、简化登记检验流程等政策，进一步巩固新加坡作为亚洲游艇中心的地位。"
    ],
    "en": [
        "Singapore has rapidly risen to become the most attractive yachting centre in Asia-Pacific, leveraging its unique geographical advantages, stable politics and open financial policies. Fantastic Vacation has operated its Asia-Pacific Operations Centre in Singapore for over five years, deeply feeling this city-state's growing influence.",
        "Singapore's yachting development benefits from multiple advantages: geographically commanding the Malacca Strait, reaching all major Southeast Asian yachting destinations within 24 hours; climatically in the equatorial calm belt with year-round water temperatures of 26-30 degrees Celsius; and politically open to yachting services with a maximum personal income tax rate of just 22%.",
        "Infrastructure-wise, Sentosa Cove Yacht Club has over 200 berths for superyachts up to 100 metres. Marina at Keppel Bay attracts medium and small yacht owners with convenient city-centre location. The Tuas Mega Port project includes a dedicated yacht service centre, expected to substantially enhance capacity upon 2028 completion.",
        "Yacht brokerage has grown significantly. Simpson Marine's annual transactions exceed $200 million. British Burlington and Italian FSY have established Asia-Pacific headquarters in Singapore. Fantastic Vacation observes mainland Chinese buyers now account for over 40% of its Singapore business.",
        "Yacht insurance and financial services are rapidly improving. Zurich Insurance and Allianz both have Asia-Pacific yacht insurance teams in Singapore. DBS Bank and OCBC have developed yacht mortgage products with loan-to-value ratios up to 60% and terms up to 15 years.",
        "The Singapore government plans to develop yachting as one of five 'transformation industries', targeting a GDP contribution of S$1 billion by 2030. Policies under study include a yacht free trade zone, professional talent visas and simplified registration procedures, further consolidating Singapore's position as Asia's yachting centre."
    ]
}

NEWS_CONTENT["009"] = {
    "zh": [
        "2026年3月12日，奇幻假期在深圳总部召开战略发布会，公布《2026-2028三年发展战略规划》。CEO陈永健表示：「全球游艇产业正处于前所未有的黄金发展期。我们的目标是在2028年前成为亚太地区首个营收超过5亿美元的游艇综合服务商。」",
        "三年战略核心是「一个平台、三大引擎、五大市场」框架：全球云服务平台；船队扩张引擎、服务升级引擎、科技赋能引擎；中国大陆、东南亚、东亚、中东和南太平洋五大核心市场。计划三年内累计投入不少于18亿元人民币。",
        "船队扩张方面，托管游艇从120艘扩充至350艘，自有船队从15艘增至50艘（含3艘LNG动力超级游艇）。30至50米中型游艇占比从35%提升至50%，50至80米大型游艇占比从15%提升至30%。",
        "服务升级推出「钻石会籍」计划，设翡翠、蓝宝石、钻石三等级。钻石会籍享有全年无限制使用全球100艘游艇权益（业内首创）。服务范围扩展至岸上生活体验，含直升机接送、米其林预订、私人飞机包机等。",
        "科技赋能投入3亿元，主要包括：新一代OceanX OS船队管理平台（整合物联网、大数据和AI）；客户关系管理系统升级（机器学习推荐个性化游艇和航线）；区块链游艇资产确权系统（2027年推出）。",
        "可持续发展承诺2028年实现三个「百分百」：自有船队100%获环保认证、托管船队新能源游艇占比100%、合作码头100%落实环保标准。每年营收2%注入「蓝色海洋基金」，用于海洋生态修复和极地保护研究。"
    ],
    "en": [
        "On March 12, 2026, Fantastic Vacation held a strategic press conference at its Shenzhen headquarters, unveiling the '2026-2028 Three-Year Strategic Development Plan'. CEO Chen Yongjian stated: 'The global yachting industry is in an unprecedented golden period. Our goal is to become the first Asia-Pacific yachting comprehensive service provider with revenue exceeding $500 million before 2028.'",
        "The three-year strategy centres on 'One Platform, Three Engines, Five Markets': a global cloud service platform; fleet expansion, service upgrade and technology empowerment engines; and five core markets — mainland China, Southeast Asia, East Asia, Middle East and South Pacific. The plan calls for cumulative investment of no less than 1.8 billion RMB.",
        "Fleet expansion: managed yachts from 120 to 350, owned fleet from 15 to 50 (including 3 LNG superyachts). Medium 30-50 metre yachts increase from 35% to 50%, large 50-80 metre yachts from 15% to 30%.",
        "Service upgrade launches the 'Diamond Membership' programme with Jade, Sapphire and Diamond tiers. Diamond members enjoy unlimited access to 100 yachts worldwide (an industry-first). Services expand to shore-based lifestyle experiences including helicopter transfers, Michelin reservations and private jet charters.",
        "Technology empowerment invests 300 million RMB in: the next-generation OceanX OS fleet management platform (integrating IoT, big data and AI); CRM system upgrades with machine learning for personalised recommendations; and blockchain yacht asset confirmation system (launching 2027).",
        "Sustainability commitments for 2028: three '100%' goals — owned fleet 100% environmentally certified, managed fleet 100% new energy yachts, partner ports 100% green operating standards. 2% of annual revenue goes to the 'Blue Ocean Fund' for marine ecological restoration and polar protection research."
    ]
}

NEWS_CONTENT["010"] = {
    "zh": [
        "从摩纳哥的奢华到希腊的古韵，地中海是全球游艇爱好者心中的「终极巡航目的地」。奇幻假期根据十五年执行经验，策划了这条跨越六国、全程约3000海里的30天深度巡航全指南，涵盖航线规划、港口推荐、季节选择和预算参考。",
        "航线分五段：摩纳哥→戛纳（280海里，3天）→巴塞罗那（200海里，2天）→直布罗陀（450海里，5天）→雅典经撒丁岛、西西里岛、马耳他（900海里，10天）→爱琴海环游经米克诺斯、圣托里尼、罗德岛、博德鲁姆（650海里，10天）。各段间建议1-2天休整。",
        "最佳季节5-10月，6-9月旺季。避开人潮可选5月中旬（薰衣草季，蔚蓝海岸最美）或9月下旬（温暖但游客散去）。10月后不建议进入，北部海域季风风浪增大。",
        "摩纳哥是完美起点，赫库勒斯港可停700+游艇。戛纳以电影节闻名，尼斯更悠闲。蔚蓝海岸航程海水从浅蓝到深蓝渐变，美得令人窒息。巴塞罗那是文化高点——高迪建筑、兰布拉大道和博格利亚市场不可错过，建议停留三天。",
        "撒丁岛翡翠海岸是欧洲皇室和好莱坞明星最青睐的度假地，切尔沃港出发可到拉马达莱娜群岛的白沙滩。西西里岛巴勒莫融合阿拉伯、诺曼和拜占庭风格，50+世界遗产景点。陶尔米纳古希腊剧场背靠埃特纳火山，风景无与伦比。马耳他瓦莱塔是UNESCO世界遗产。",
        "希腊爱琴海是精华所在。米克诺斯岛——「爱琴海派对之都」，有风车落日和洁白建筑。圣托里尼——从海上望悬崖上白色房屋和蓝色圆顶，是永恒经典画面。罗德岛中世纪古城是UNESCO世界遗产。土耳其博德鲁姆是最后一站，曾是七大奇迹所在地，如今是时尚海滨度假地。",
        "预算参考：25万至45万美元（6-8人中大型游艇），含游艇租赁（如共享可分摊至15-40万）、港口费（约5万）、燃油（3-8万）、餐饮服务（5-10万）、岸上活动（2万）和机票签证（1万）。奇幻假期提供从行程规划到岸上活动的全套餐服务，船上专业厨师根据各站特色烹制当地美食。"
    ],
    "en": [
        "From Monaco's opulence to Greece's ancient charm, the Mediterranean is the 'ultimate cruising destination' for yachting enthusiasts worldwide. Based on fifteen years of experience, Fantastic Vacation presents this 30-day deep-cruise guide spanning six countries and approximately 3,000 nautical miles, covering route planning, port recommendations, season selection and budget references.",
        "Five route segments: Monaco to Cannes (280nm, 3 days), Cannes to Barcelona (200nm, 2 days), Barcelona to Gibraltar (450nm, 5 days), Gibraltar to Athens via Sardinia, Sicily and Malta (900nm, 10 days), Athens Aegean cruise via Mykonos, Santorini, Rhodes and Bodrum (650nm, 10 days). Allow 1-2 days rest between segments.",
        "Best season May-October, peak June-September. To avoid crowds, choose mid-May (lavender season on the Riviera) or late September (warm but fewer tourists). Not recommended after October due to monsoon season in northern waters.",
        "Monaco is the perfect starting point with 700+ yacht berths at Port Hercule. Cannes is famous for its film festival; Nice is more laid-back. The Riviera passage features a breathtaking sea gradient from light to deep blue. Barcelona is the cultural highlight — Gaudí's architecture, Las Ramblas and La Boqueria are unmissable; recommended 3-day stay.",
        "Sardinia's Costa Smeralda is favoured by European royalty and Hollywood stars; from Porto Cervo, visit La Maddalena's white beaches. Sicily's Palermo blends Arab, Norman and Byzantine styles with 50+ UNESCO sites. Taormina's ancient Greek theatre with Mount Etna backdrop is unparalleled. Malta's Valletta is a UNESCO World Heritage site.",
        "The Greek Aegean is the essence of the voyage. Mykonos — the 'Party Capital of the Aegean' — with windmill sunsets and white Cycladic architecture. Santorini — cliffside white houses and blue domes are an eternal postcard classic. Rhodes' medieval old town is UNESCO-listed. Turkey's Bodrum is the final stop, once home to one of the Seven Wonders, now a fashionable seaside resort.",
        "Budget reference: $250,000-$450,000 (6-8 guest mid-to-large yacht), including charter (sharable to $150,000-$400,000), port fees (~$50,000), fuel ($30,000-$80,000), dining ($50,000-$100,000), shore activities (~$20,000) and flights/visas (~$10,000). Fantastic Vacation provides full-package services with onboard chefs preparing local cuisine at each stop."
    ]
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
    
    # 找现有keys
    existing = re.findall(r'data-i18n="(news-' + num_str + r'\.\d+)"', content[body_start:article_end])
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
        # 重新查找位置（内容已变）
        body_start = content.find('news-article-body')
        article_end = content.find('</article>', body_start)
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


def update_i18n(all_entries, i18n_path):
    """更新i18n.js"""
    if not os.path.exists(i18n_path):
        print(f"  SKIP {i18n_path}")
        return
    
    with open(i18n_path, encoding='utf-8') as f:
        content = f.read()
    
    updated, added = 0, 0
    
    for key, zh_text, en_text in all_entries:
        zh_e = zh_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        en_e = en_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        
        # 查找key
        key_pattern = f'"{key}"'
        key_pos = content.find(key_pattern)
        
        if key_pos >= 0:
            # 更新zh
            zh_search = re.search(r'"zh"\s*:\s*"[^"]*"', content[key_pos:key_pos+100000])
            if zh_search:
                p1 = key_pos + zh_search.start()
                p2 = key_pos + zh_search.end()
                content = content[:p1] + f'"zh": "{zh_e}"' + content[p2:]
                updated += 1
            
            # 重新定位key（因为内容偏移了）
            key_pos = content.find(key_pattern)
            en_search = re.search(r'"en"\s*:\s*"[^"]*"', content[key_pos:key_pos+100000])
            if en_search:
                p1 = key_pos + en_search.start()
                p2 = key_pos + en_search.end()
                content = content[:p1] + f'"en": "{en_e}"' + content[p2:]
        else:
            # 追加新条目 - 找最后一个news条目
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
    print("🚀 扩写全部10篇新闻详情页\n")
    
    all_entries = []
    
    for num_str in sorted(NEWS_CONTENT.keys()):
        print(f"Processing news-{num_str}...")
        entries = expand_news_page(num_str, NEWS_CONTENT[num_str])
        all_entries.extend(entries)
    
    # 更新i18n.js
    print(f"\nUpdating i18n.js ({len(all_entries)} entries)...")
    update_i18n(all_entries, os.path.join(BASE, 'i18n.js'))
    
    yt_i18n = os.path.join(BASE, 'YT', 'i18n.js')
    if os.path.exists(yt_i18n):
        update_i18n(all_entries, yt_i18n)
    
    # 同步HTML
    print("\nSyncing HTML to language versions...")
    for num_str in sorted(NEWS_CONTENT.keys()):
        fname = f'news-{num_str}.html'
        for subdir in ['en', 'YT', 'YT/en']:
            dst = os.path.join(BASE, subdir, fname)
            if os.path.exists(dst):
                shutil.copy2(os.path.join(BASE, fname), dst)
                print(f"  ✓ {fname} → {subdir}/")
    
    print(f"\n✅ 完成！共处理 {len(all_entries)} 个条目")

if __name__ == '__main__':
    main()
