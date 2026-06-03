#!/usr/bin/env python3
"""
Generate rich content for partner-type detail pages.
Adds 4-5 content sections to each of the 10 partner-type pages.
All content includes data-i18n and corresponding i18n.js dict entries.
"""

import re, json

# ============================================================
# CONTENT DATABASE — All partner types with CN + EN content
# ============================================================

CONTENT = {
    "partner-type-shipyard": {
        "title": "船厂合作",
        "title_en": "Shipyard Partnership",
        "hero_en": "Strategic Shipyard Partnerships",
        "sections": {
            "overview": {
                "zh": "奇幻假期与全球顶尖游艇船厂建立战略合作，为客户提供原厂级别的设计、制造与交付服务。我们与意大利、荷兰、德国等传统游艇制造强国的知名船厂深度绑定，确保每一艘游艇都承载世界级的工艺水准与品质保障。",
                "en": "Fantastic Vacation has established strategic partnerships with top-tier yacht shipyards worldwide, providing customers with factory-grade design, manufacturing, and delivery services. We are deeply aligned with renowned shipyards in Italy, Netherlands, Germany, and other traditional yacht-building powerhouses, ensuring every yacht embodies world-class craftsmanship and quality assurance."
            },
            "benefits": {
                "title_zh": "合作优势",
                "title_en": "Partnership Benefits",
                "items": [
                    {"zh": "原厂优先排产，缩短交付周期30%以上", "en": "Factory priority scheduling, reducing delivery time by over 30%"},
                    {"zh": "定制化设计直达船厂工程团队", "en": "Custom design direct to shipyard engineering team"},
                    {"zh": "原厂质保与售后服务体系全覆盖", "en": "Full factory warranty and after-sales service coverage"},
                    {"zh": "定期船厂考察与技术交流", "en": "Regular shipyard visits and technical exchanges"},
                    {"zh": "联合研发未来船型与技术方案", "en": "Joint R&D on future yacht models and technology solutions"}
                ]
            },
            "tiers": {
                "title_zh": "合作层级",
                "title_en": "Partnership Tiers",
                "items": [
                    {"zh": "战略级", "en": "Strategic", "desc_zh": "全球优先排产权、联合品牌推广、专属船型开发", "desc_en": "Global priority scheduling, co-branded promotion, exclusive model development"},
                    {"zh": "核心级", "en": "Core", "desc_zh": "优先排产、定制化工程设计、技术培训支持", "desc_en": "Priority scheduling, customized engineering, technical training support"},
                    {"zh": "认证级", "en": "Certified", "desc_zh": "官方授权代理、标准质保、产品培训", "desc_en": "Official authorized agent, standard warranty, product training"}
                ]
            },
            "process": {
                "title_zh": "合作流程",
                "title_en": "Partnership Process",
                "steps": [
                    {"zh": "资质审核", "en": "Qualification Review", "desc_zh": "提交船厂资质、生产能力与过往案例", "desc_en": "Submit shipyard qualifications, production capacity, and past cases"},
                    {"zh": "技术评估", "en": "Technical Assessment", "desc_zh": "双方工程团队对接，评估技术兼容性", "desc_en": "Engineering teams connect to evaluate technical compatibility"},
                    {"zh": "商务洽谈", "en": "Business Negotiation", "desc_zh": "确定合作模式、价格体系与服务范围", "desc_en": "Define cooperation model, pricing system, and service scope"},
                    {"zh": "签约启动", "en": "Signing & Launch", "desc_zh": "正式签约，首台订单试产启动", "desc_en": "Official signing, first order pilot production launch"},
                    {"zh": "深度协同", "en": "Deep Collaboration", "desc_zh": "定期复盘、技术迭代、联合推广", "desc_en": "Regular reviews, technology iterations, joint promotion"}
                ]
            },
            "faq": {
                "title_zh": "常见问题",
                "title_en": "FAQ",
                "items": [
                    {"q_zh": "奇幻假期与船厂是什么关系？", "q_en": "What is the relationship between Fantastic Vacation and shipyards?",
                     "a_zh": "奇幻假期作为高端游艇服务商，与全球顶尖船厂建立战略合作关系，为客户提供从设计到交付的一站式服务。我们不制造游艇，而是整合全球最优船厂资源，确保客户获得最佳品质与体验。",
                     "a_en": "As a premium yacht service provider, Fantastic Vacation establishes strategic partnerships with world-class shipyards to offer customers one-stop services from design to delivery. We don't manufacture yachts — we integrate the best global shipyard resources to ensure customers receive optimal quality and experience."},
                    {"q_zh": "我可以直接联系合作船厂吗？", "q_en": "Can I contact partner shipyards directly?",
                     "a_zh": "可以。通过奇幻假期，您不仅能获得厂价优势，还可享受我们提供的项目管理、质量监理与交付协调等增值服务，让整个过程更省心、更高效。",
                     "a_en": "Yes. Through Fantastic Vacation, you not only get factory pricing advantages but also enjoy our value-added services including project management, quality supervision, and delivery coordination — making the entire process smoother and more efficient."},
                    {"q_zh": "船厂的交付周期一般多长？", "q_en": "How long is the typical shipyard delivery timeline?",
                     "a_zh": "视船型与定制程度而定，日间游艇约6-12个月，飞桥游艇12-18个月，大型远征游艇18-36个月。奇幻假期通过原厂优先排产，通常可将交付周期缩短30%。",
                     "a_en": "Depending on the model and customization level: day cruisers typically 6-12 months, flybridge yachts 12-18 months, large expedition yachts 18-36 months. Through factory priority scheduling, Fantastic Vacation can typically reduce delivery time by 30%."}
                ]
            }
        }
    },
    "partner-type-marina": {
        "title": "码头网络",
        "title_en": "Marina Network",
        "hero_en": "Global Marina/Harbor Alliance",
        "sections": {
            "overview": {
                "zh": "奇幻假期构建全球码头网络，覆盖地中海、加勒比海、东南亚、中东等热门航线区域。通过与世界顶级游艇码头合作，为船东提供专属泊位、VIP通道与一站式停靠服务，让每一次航行都无忧无虑。",
                "en": "Fantastic Vacation builds a global marina network covering the Mediterranean, Caribbean, Southeast Asia, Middle East, and other popular cruising regions. Through partnerships with world-class yacht marinas, we provide owners with dedicated berths, VIP access, and one-stop docking services for worry-free voyages."
            },
            "benefits": {
                "title_zh": "合作优势",
                "title_en": "Partnership Benefits",
                "items": [
                    {"zh": "全球300+高端码头网络覆盖", "en": "Global network of 300+ premium marinas"},
                    {"zh": "专属泊位预留与VIP优先通道", "en": "Dedicated berth reservation and VIP priority access"},
                    {"zh": "码头服务一体化结算体系", "en": "Integrated marina service billing system"},
                    {"zh": "跨国航线规划与地接服务", "en": "Cross-border route planning and local concierge services"},
                    {"zh": "码头维修保养支援网络", "en": "Marina-based maintenance and repair support network"}
                ]
            },
            "tiers": {
                "title_zh": "合作层级",
                "title_en": "Partnership Tiers",
                "items": [
                    {"zh": "旗舰码头", "en": "Flagship Marina", "desc_zh": "专属泊位区、VIP码头管家、船上服务直达", "desc_en": "Dedicated berth zone, VIP marina concierge, direct onboard service"},
                    {"zh": "核心码头", "en": "Core Marina", "desc_zh": "优先泊位、标准补给服务、维修支援", "desc_en": "Priority berthing, standard supply services, repair support"},
                    {"zh": "合作码头", "en": "Cooperative Marina", "desc_zh": "协议泊位、基础服务、信息联通", "desc_en": "Contracted berthing, basic services, information connectivity"}
                ]
            },
            "process": {
                "title_zh": "合作流程",
                "title_en": "Partnership Process",
                "steps": [
                    {"zh": "码头评估", "en": "Marina Assessment", "desc_zh": "评估码头区位、设施、服务能力与安全标准", "desc_en": "Evaluate marina location, facilities, service capability, and safety standards"},
                    {"zh": "服务匹配", "en": "Service Matching", "desc_zh": "根据客户航线需求匹配最优码头资源", "desc_en": "Match optimal marina resources based on customer route needs"},
                    {"zh": "协议签署", "en": "Agreement Signing", "desc_zh": "签署战略合作协议，确立服务标准与价格体系", "desc_en": "Sign strategic cooperation agreement, establish service standards and pricing"},
                    {"zh": "系统对接", "en": "System Integration", "desc_zh": "泊位管理系统对接，实现一键预订", "desc_en": "Integrate berth management systems for one-click booking"},
                    {"zh": "持续优化", "en": "Continuous Optimization", "desc_zh": "定期服务评估，动态调整码头网络布局", "desc_en": "Regular service evaluation, dynamic marina network optimization"}
                ]
            },
            "faq": {
                "title_zh": "常见问题",
                "title_en": "FAQ",
                "items": [
                    {"q_zh": "码头网络覆盖哪些区域？", "q_en": "Which regions does the marina network cover?",
                     "a_zh": "目前覆盖地中海（意大利、法国、西班牙、希腊、克罗地亚）、加勒比海、东南亚（泰国、马来西亚、新加坡、印尼）、中东（迪拜、阿布扎比）、澳洲等热门航线区域，网络持续扩展中。",
                     "a_en": "Currently covering the Mediterranean (Italy, France, Spain, Greece, Croatia), Caribbean, Southeast Asia (Thailand, Malaysia, Singapore, Indonesia), Middle East (Dubai, Abu Dhabi), Australia, and other popular cruising regions. The network continues to expand."},
                    {"q_zh": "我需要提前多久预订码头泊位？", "q_en": "How far in advance should I book a marina berth?",
                     "a_zh": "建议旺季（6-9月）提前3-4周预订，淡季提前1-2周即可。VIP客户可通过专属通道紧急预订，最快4小时内确认。",
                     "a_en": "We recommend 3-4 weeks in advance during peak season (June-September), and 1-2 weeks during off-peak. VIP customers can make urgent bookings through dedicated channels, with the fastest confirmation within 4 hours."},
                    {"q_zh": "码头费用如何计算？", "q_en": "How are marina fees calculated?",
                     "a_zh": "费用根据码头等级、泊位尺寸、停靠时长综合计算。会员客户享受8-9.5折优惠，黑卡会员享受专属免费泊位配额。",
                     "a_en": "Fees are calculated based on marina tier, berth size, and docking duration. Members enjoy 5-20% discounts, and Black Card members receive dedicated free berth quotas."}
                ]
            }
        }
    },
    "partner-type-aviation": {
        "title": "私人航空",
        "title_en": "Private Aviation",
        "hero_en": "Private Aviation / Sea-Land-Air Transport",
        "sections": {
            "overview": {
                "zh": "奇幻假期携手全球领先的私人航空服务商，为高净值客户打造海陆空无缝衔接的高端出行体验。从公务机包机、直升机接驳到停机坪协调，我们为游艇船东提供从家门口到甲板的全程尊享服务。",
                "en": "Fantastic Vacation partners with world-leading private aviation providers to create seamless sea-land-air premium travel experiences for high-net-worth clients. From business jet charters and helicopter transfers to helipad coordination, we offer yacht owners an exclusive door-to-deck journey."
            },
            "benefits": {
                "title_zh": "合作优势",
                "title_en": "Partnership Benefits",
                "items": [
                    {"zh": "全球公务机机队，覆盖6大洲航线", "en": "Global business jet fleet covering 6 continents"},
                    {"zh": "直升机海陆接驳，直飞游艇停机坪", "en": "Helicopter sea-land transfer, direct to yacht helipad"},
                    {"zh": "全球FBO与停机坪认证网络", "en": "Global FBO and helipad certification network"},
                    {"zh": "专属飞行管家一对一服务", "en": "Dedicated flight concierge one-on-one service"},
                    {"zh": "海空联运一体化行程管理", "en": "Integrated sea-air combined itinerary management"}
                ]
            },
            "tiers": {
                "title_zh": "合作层级",
                "title_en": "Partnership Tiers",
                "items": [
                    {"zh": "全球航空联盟", "en": "Global Aviation Alliance", "desc_zh": "年度飞行计划定制、专属机队调度、联合品牌推广", "desc_en": "Annual flight plan customization, dedicated fleet dispatch, co-branded promotion"},
                    {"zh": "区域航空合作", "en": "Regional Aviation Partner", "desc_zh": "区域航线机队、优先预订、标准服务", "desc_en": "Regional route fleet, priority booking, standard services"},
                    {"zh": "接驳服务商", "en": "Transfer Service Provider", "desc_zh": "直升机接驳、机场VIP通道、行李转运", "desc_en": "Helicopter transfer, airport VIP channels, luggage transfer"}
                ]
            },
            "process": {
                "title_zh": "合作流程",
                "title_en": "Partnership Process",
                "steps": [
                    {"zh": "需求评估", "en": "Needs Assessment", "desc_zh": "评估客户航线需求、机型偏好与安全标准", "desc_en": "Assess customer route needs, aircraft preferences, and safety standards"},
                    {"zh": "航空伙伴筛选", "en": "Aviation Partner Screening", "desc_zh": "基于安全记录、机队规模、服务口碑筛选", "desc_en": "Screen based on safety records, fleet size, and service reputation"},
                    {"zh": "服务协议", "en": "Service Agreement", "desc_zh": "确定服务标准、定价体系与保障机制", "desc_en": "Define service standards, pricing system, and guarantee mechanisms"},
                    {"zh": "系统接入", "en": "System Onboarding", "desc_zh": "行程管理系统对接，实现一键预订", "desc_en": "Itinerary management system integration for one-click booking"},
                    {"zh": "联合运营", "en": "Joint Operations", "desc_zh": "联合推广、客户体验优化、服务升级", "desc_en": "Joint promotion, customer experience optimization, service upgrades"}
                ]
            },
            "faq": {
                "title_zh": "常见问题",
                "title_en": "FAQ",
                "items": [
                    {"q_zh": "航空服务适用于哪些游艇？", "q_en": "Which yachts are eligible for aviation services?",
                     "a_zh": "主要面向拥有直升机停机坪的大型游艇客户（如君临系列、远征系列），同时也为所有会员提供目的地机场到码头的VIP接驳服务。",
                     "a_en": "Primarily for large yacht customers with helipads (such as Sovereign and Expedition series), while also offering VIP airport-to-marina transfer services for all members."},
                    {"q_zh": "最快多久可以安排私人航班？", "q_en": "How quickly can a private flight be arranged?",
                     "a_zh": "标准预订需提前24小时，紧急需求可通过VIP通道在6-8小时内完成调度。覆盖区域内可最快4小时起飞。",
                     "a_en": "Standard booking requires 24 hours' notice; urgent requests via VIP channels can be dispatched within 6-8 hours. In covered regions, the fastest takeoff is within 4 hours."},
                    {"q_zh": "航空服务如何收费？", "q_en": "How are aviation services charged?",
                     "a_zh": "按飞行时长、机型、航线综合计费。会员享受专属价格体系，黑卡会员可享年度飞行额度礼遇。",
                     "a_en": "Based on flight hours, aircraft type, and route. Members enjoy exclusive pricing, and Black Card members receive annual flight credit benefits."}
                ]
            }
        }
    },
    "partner-type-hotel": {
        "title": "奢华酒店",
        "title_en": "Luxury Hotels",
        "hero_en": "Luxury Hotel & Resort Partnerships",
        "sections": {
            "overview": {
                "zh": "奇幻假期与全球奢华酒店与度假村建立深度合作，为游艇船东打造「海上+岸上」双栖奢享生活。从马尔代夫水上别墅到摩纳哥顶层套房，从私人沙滩晚宴到雪山温泉——每一次靠岸都是一段新的奢旅。",
                "en": "Fantastic Vacation partners deeply with global luxury hotels and resorts to create a dual-lifestyle of sea and shore luxury for yacht owners. From Maldives overwater villas to Monaco penthouse suites, from private beach dinners to mountain hot springs — every port call is a new luxury journey."
            },
            "benefits": {
                "title_zh": "合作优势",
                "title_en": "Partnership Benefits",
                "items": [
                    {"zh": "全球200+奢华酒店与度假村网络", "en": "Global network of 200+ luxury hotels and resorts"},
                    {"zh": "会员互认，权益无缝对接", "en": "Mutual membership recognition with seamless benefit transfer"},
                    {"zh": "码头-酒店专属接驳服务", "en": "Dedicated marina-to-hotel transfer services"},
                    {"zh": "定制化海上+岸上联动套餐", "en": "Customized sea-and-shore package experiences"},
                    {"zh": "私人活动策划与执行", "en": "Private event planning and execution"}
                ]
            },
            "tiers": {
                "title_zh": "合作层级",
                "title_en": "Partnership Tiers",
                "items": [
                    {"zh": "全球奢华联盟", "en": "Global Luxury Alliance", "desc_zh": "会员权益互通、专属体验定制、联合品牌活动", "desc_en": "Cross-member benefits, exclusive experience customization, co-branded events"},
                    {"zh": "区域精品伙伴", "en": "Regional Boutique Partner", "desc_zh": "目的地推荐、优先预订、VIP礼遇", "desc_en": "Destination recommendations, priority booking, VIP treatment"},
                    {"zh": "甄选合作酒店", "en": "Select Partner Hotel", "desc_zh": "协议价格、标准服务、品牌露出", "desc_en": "Contracted rates, standard services, brand exposure"}
                ]
            },
            "process": {
                "title_zh": "合作流程",
                "title_en": "Partnership Process",
                "steps": [
                    {"zh": "酒店甄选", "en": "Hotel Selection", "desc_zh": "根据客户航线与偏好，甄选匹配的奢华酒店", "desc_en": "Select matching luxury hotels based on customer routes and preferences"},
                    {"zh": "体验评估", "en": "Experience Evaluation", "desc_zh": "实地考察评估硬件设施、服务水准与独特性", "desc_en": "On-site evaluation of facilities, service standards, and uniqueness"},
                    {"zh": "合约签订", "en": "Contract Signing", "desc_zh": "确定会员权益、价格体系与专属礼遇", "desc_en": "Define membership benefits, pricing, and exclusive privileges"},
                    {"zh": "系统对接", "en": "System Integration", "desc_zh": "会员体系互通，实现一键预订与权益核销", "desc_en": "Membership system integration for one-click booking and benefit redemption"},
                    {"zh": "体验升级", "en": "Experience Enhancement", "desc_zh": "定期推出联名套餐、主题活动与限时体验", "desc_en": "Regular co-branded packages, themed events, and limited-time experiences"}
                ]
            },
            "faq": {
                "title_zh": "常见问题",
                "title_en": "FAQ",
                "items": [
                    {"q_zh": "会员酒店权益如何享受？", "q_en": "How do I enjoy member hotel benefits?",
                     "a_zh": "奇幻假期会员可直接通过专属客服或会员App预订合作酒店，自动享受升房、延迟退房、欢迎礼遇等权益。",
                     "a_en": "Fantastic Vacation members can book partner hotels directly via dedicated concierge or the member app, automatically enjoying room upgrades, late checkout, welcome amenities, and more."},
                    {"q_zh": "酒店网络覆盖哪些目的地？", "q_en": "Which destinations does the hotel network cover?",
                     "a_zh": "覆盖全球50+游艇热门目的地，包括摩纳哥、圣特罗佩、波多菲诺、迈阿密、迪拜、普吉岛、三亚等。",
                     "a_en": "Covering 50+ popular yachting destinations worldwide, including Monaco, Saint-Tropez, Portofino, Miami, Dubai, Phuket, Sanya, and more."},
                    {"q_zh": "可以定制私人活动吗？", "q_en": "Can private events be customized?",
                     "a_zh": "当然。我们提供私人晚宴、甲板派对、海上婚礼、商务接待等全方位定制服务，由专属活动策划团队执行。",
                     "a_en": "Absolutely. We offer full-service customization for private dinners, deck parties, yacht weddings, corporate receptions, and more, executed by our dedicated event planning team."}
                ]
            }
        }
    },
    "partner-type-art": {
        "title": "艺术品收藏",
        "title_en": "Art Collection",
        "hero_en": "Art Collection & Premium Lifestyle",
        "sections": {
            "overview": {
                "zh": "奇幻假期将艺术融入海洋生活，携手全球顶尖画廊、拍卖行与艺术家，为游艇船东提供专属艺术品收藏、定制创作与游艇艺术空间设计服务。让您的游艇不仅是一艘船，更是一座漂浮的私人美术馆。",
                "en": "Fantastic Vacation integrates art into ocean living, partnering with world-leading galleries, auction houses, and artists to offer yacht owners exclusive art collection, custom creation, and yacht art space design services. Let your yacht be more than a vessel — a floating private gallery."
            },
            "benefits": {
                "title_zh": "合作优势",
                "title_en": "Partnership Benefits",
                "items": [
                    {"zh": "全球顶级画廊与拍卖行直通渠道", "en": "Direct access to world-class galleries and auction houses"},
                    {"zh": "游艇空间专属艺术定制服务", "en": "Exclusive yacht space art customization service"},
                    {"zh": "藏品鉴赏与投资顾问", "en": "Collection appreciation and investment advisory"},
                    {"zh": "专业艺术品运输与保险方案", "en": "Professional art transportation and insurance solutions"},
                    {"zh": "艺术家驻船创作与VIP私享展览", "en": "Artist-in-residence creation and VIP private exhibitions"}
                ]
            },
            "tiers": {
                "title_zh": "合作层级",
                "title_en": "Partnership Tiers",
                "items": [
                    {"zh": "全球艺术联盟", "en": "Global Art Alliance", "desc_zh": "珍藏顾问、优先预展、联合策展、私享拍卖", "desc_en": "Collection advisory, priority preview, joint curation, private auctions"},
                    {"zh": "区域画廊伙伴", "en": "Regional Gallery Partner", "desc_zh": "作品推荐、租赁服务、小型展览", "desc_en": "Artwork recommendation, leasing service, small exhibitions"},
                    {"zh": "艺术家合作", "en": "Artist Collaboration", "desc_zh": "定制创作、驻船项目、联名作品", "desc_en": "Custom creation, onboard residency, co-branded artwork"}
                ]
            },
            "process": {
                "title_zh": "合作流程",
                "title_en": "Partnership Process",
                "steps": [
                    {"zh": "品味会诊", "en": "Taste Consultation", "desc_zh": "了解客户艺术偏好、收藏目标与空间需求", "desc_en": "Understand customer art preferences, collection goals, and spatial requirements"},
                    {"zh": "方案策划", "en": "Solution Planning", "desc_zh": "量身定制艺术品收藏与空间设计方案", "desc_en": "Tailored art collection and space design proposal"},
                    {"zh": "资源匹配", "en": "Resource Matching", "desc_zh": "对接匹配的画廊、艺术家与拍卖行资源", "desc_en": "Connect with matching galleries, artists, and auction houses"},
                    {"zh": "执行交付", "en": "Execution & Delivery", "desc_zh": "作品定制、运输、保险与安装全程管理", "desc_en": "Full management of artwork customization, transportation, insurance, and installation"},
                    {"zh": "持续鉴赏", "en": "Ongoing Appreciation", "desc_zh": "定期策展、藏品增值服务与圈子社交", "desc_en": "Regular curation, collection value-add services, and social networking"}
                ]
            },
            "faq": {
                "title_zh": "常见问题",
                "title_en": "FAQ",
                "items": [
                    {"q_zh": "艺术品在游艇上安全吗？", "q_en": "Is artwork safe on a yacht?",
                     "a_zh": "我们采用专业的海洋级艺术品固定与温湿度控制系统，针对游艇振动、湿度、盐雾等特殊环境做全面防护，并由专业保险全程覆盖。",
                     "a_en": "We employ professional marine-grade artwork mounting and climate control systems, providing comprehensive protection against yacht-specific challenges like vibration, humidity, and salt spray, with full professional insurance coverage."},
                    {"q_zh": "艺术品定制周期多长？", "q_en": "How long does custom artwork take?",
                     "a_zh": "视艺术家档期与作品复杂度而定，通常3-8个月。我们建议在游艇建造阶段即启动艺术方案策划，确保空间与作品的完美融合。",
                     "a_en": "Depending on artist availability and artwork complexity, typically 3-8 months. We recommend initiating art planning during the yacht construction phase to ensure perfect spatial integration."},
                    {"q_zh": "可以参与拍卖吗？", "q_en": "Can I participate in auctions?",
                     "a_zh": "可以。奇幻假期会员可享受全球主要拍卖行的优先预展、代拍服务与专属VIP席位。",
                     "a_en": "Yes. Fantastic Vacation members enjoy priority previews, proxy bidding, and exclusive VIP seats at major global auction houses."}
                ]
            }
        }
    },
    "partner-type-association": {
        "title": "行业协会",
        "title_en": "Industry Association",
        "hero_en": "Industry Associations & Regulatory Bodies",
        "sections": {
            "overview": {
                "zh": "奇幻假期与全球主要游艇行业协会、海事监管机构与标准制定组织紧密合作，确保我们的服务始终符合最高行业标准与合规要求。通过协会网络，我们为客户提供政策信息、行业洞察与合规保障。",
                "en": "Fantastic Vacation works closely with major global yacht industry associations, maritime regulatory bodies, and standards organizations to ensure our services always meet the highest industry standards and compliance requirements. Through our association network, we provide customers with policy information, industry insights, and compliance assurance."
            },
            "benefits": {
                "title_zh": "合作优势",
                "title_en": "Partnership Benefits",
                "items": [
                    {"zh": "行业标准制定的参与权", "en": "Participation rights in industry standard setting"},
                    {"zh": "实时政策法规更新与合规指导", "en": "Real-time policy updates and compliance guidance"},
                    {"zh": "行业数据与市场报告共享", "en": "Industry data and market report sharing"},
                    {"zh": "国际海事展会与论坛参与权", "en": "International maritime exhibition and forum participation"},
                    {"zh": "行业人才认证与培训体系", "en": "Industry talent certification and training system"}
                ]
            },
            "tiers": {
                "title_zh": "合作层级",
                "title_en": "Partnership Tiers",
                "items": [
                    {"zh": "战略合作", "en": "Strategic Cooperation", "desc_zh": "联合研究、标准制定、行业白皮书发布", "desc_en": "Joint research, standard setting, industry white paper publishing"},
                    {"zh": "会员参与", "en": "Member Participation", "desc_zh": "行业数据、培训资源、展会参与", "desc_en": "Industry data, training resources, exhibition participation"},
                    {"zh": "认证对接", "en": "Certification Alignment", "desc_zh": "资质互认、标准宣贯、合规审核", "desc_en": "Mutual qualification recognition, standard promotion, compliance auditing"}
                ]
            },
            "process": {
                "title_zh": "合作流程",
                "title_en": "Partnership Process",
                "steps": [
                    {"zh": "协会对接", "en": "Association Connection", "desc_zh": "确定目标协会，提交合作意向与资质材料", "desc_en": "Identify target associations, submit cooperation intent and qualification materials"},
                    {"zh": "入会审核", "en": "Membership Review", "desc_zh": "通过协会审核，获取会员资格", "desc_en": "Pass association review, obtain membership"},
                    {"zh": "权益激活", "en": "Benefits Activation", "desc_zh": "激活会员权益，接入资源与服务体系", "desc_en": "Activate membership benefits, connect to resources and service systems"},
                    {"zh": "深度参与", "en": "Deep Engagement", "desc_zh": "参加委员会、工作组，参与行业建设", "desc_en": "Join committees and working groups, participate in industry development"},
                    {"zh": "价值输出", "en": "Value Contribution", "desc_zh": "通过协会平台发布成果、分享经验", "desc_en": "Publish achievements and share experiences through association platforms"}
                ]
            },
            "faq": {
                "title_zh": "常见问题",
                "title_en": "FAQ",
                "items": [
                    {"q_zh": "加入协会对客户有什么价值？", "q_en": "What value does association membership bring to customers?",
                     "a_zh": "协会成员身份确保我们的服务符合国际标准，客户可享受到受国际认可的合规服务、行业最新资讯以及更广泛的资源网络。",
                     "a_en": "Association membership ensures our services meet international standards. Customers benefit from internationally recognized compliant services, the latest industry insights, and a broader resource network."},
                    {"q_zh": "你们加入了哪些协会？", "q_en": "Which associations have you joined?",
                     "a_zh": "我们与地中海船坞协会、国际游艇协会（IYBA）、亚洲游艇行业协会等保持密切合作，并通过战略合作伙伴覆盖全球主要海事认证体系。",
                     "a_en": "We maintain close cooperation with the Mediterranean Shipyard Association, International Yacht Brokers Association (IYBA), Asian Yacht Industry Association, and through strategic partners, cover major global maritime certification systems."},
                    {"q_zh": "行业协会如何帮助合规？", "q_en": "How do industry associations help with compliance?",
                     "a_zh": "通过协会获取最新的行业法规变化，我们能够在第一时间调整服务标准，确保客户的游艇运营始终合规，避免法律风险。",
                     "a_en": "By accessing the latest regulatory changes through associations, we can adjust service standards promptly, ensuring customers' yacht operations remain compliant and avoiding legal risks."}
                ]
            }
        }
    },
    "partner-type-brand": {
        "title": "品牌联名",
        "title_en": "Co-Branding",
        "hero_en": "Co-Branding Partnerships",
        "sections": {
            "overview": {
                "zh": "奇幻假期与全球高端品牌跨界联名，从奢华汽车、顶级腕表到珍稀酒品、高级时装——我们将不同领域的奢华基因注入游艇生活，为船东打造独一无二的品牌体验与限量定制珍品。",
                "en": "Fantastic Vacation co-brands with global luxury brands across categories — from luxury automobiles and premium watches to rare spirits and haute couture. We infuse the luxury DNA of diverse domains into yacht living, creating unique brand experiences and limited-edition treasures for yacht owners."
            },
            "benefits": {
                "title_zh": "合作优势",
                "title_en": "Partnership Benefits",
                "items": [
                    {"zh": "全球高端品牌资源矩阵", "en": "Global luxury brand resource matrix"},
                    {"zh": "限量联名定制，提升品牌价值", "en": "Limited-edition co-branded customization to enhance brand value"},
                    {"zh": "联合品牌活动与VIP体验", "en": "Joint brand events and VIP experiences"},
                    {"zh": "跨界营销与客户资源互通", "en": "Cross-border marketing and customer resource sharing"},
                    {"zh": "品牌故事与内容共创", "en": "Brand storytelling and content co-creation"}
                ]
            },
            "tiers": {
                "title_zh": "合作层级",
                "title_en": "Partnership Tiers",
                "items": [
                    {"zh": "深度联名", "en": "Deep Co-Branding", "desc_zh": "产品联名、内容共创、客户互通、品牌加持", "desc_en": "Product co-branding, content co-creation, customer sharing, brand endorsement"},
                    {"zh": "主题活动", "en": "Themed Events", "desc_zh": "联合发布会、体验活动、会员私享", "desc_en": "Joint launches, experience events, member exclusives"},
                    {"zh": "品牌露出", "en": "Brand Exposure", "desc_zh": "场景植入、内容合作、渠道互通", "desc_en": "Scene placement, content collaboration, channel sharing"}
                ]
            },
            "process": {
                "title_zh": "合作流程",
                "title_en": "Partnership Process",
                "steps": [
                    {"zh": "品牌匹配", "en": "Brand Matching", "desc_zh": "分析品牌调性、目标客群与合作契合度", "desc_en": "Analyze brand identity, target audience, and collaboration fit"},
                    {"zh": "创意策划", "en": "Creative Planning", "desc_zh": "设计联名方案、活动概念与传播策略", "desc_en": "Design co-branding plan, event concept, and communication strategy"},
                    {"zh": "商务签约", "en": "Business Signing", "desc_zh": "确定合作范围、权益分配与执行计划", "desc_en": "Define collaboration scope, benefit allocation, and execution plan"},
                    {"zh": "执行落地", "en": "Execution", "desc_zh": "产品开发、活动执行、内容制作", "desc_en": "Product development, event execution, content production"},
                    {"zh": "传播放大", "en": "Amplification", "desc_zh": "全渠道推广、社群运营、口碑传播", "desc_en": "Omni-channel promotion, community operations, word-of-mouth amplification"}
                ]
            },
            "faq": {
                "title_zh": "常见问题",
                "title_en": "FAQ",
                "items": [
                    {"q_zh": "联名合作适合什么类型的品牌？", "q_en": "What type of brands are suitable for co-branding?",
                     "a_zh": "奇幻假期主要与高端生活方式品牌合作，包括但不限于：奢华汽车、顶级腕表、高级珠宝、珍稀酒品、高级时装、高端家居、科技数码等领域。核心标准是品牌调性与客群契合度。",
                     "a_en": "Fantastic Vacation primarily partners with premium lifestyle brands, including but not limited to: luxury automobiles, premium watches, fine jewelry, rare spirits, haute couture, luxury home, and tech. The core criterion is brand identity and audience alignment."},
                    {"q_zh": "联名产品的开发周期多长？", "q_en": "How long is the co-branded product development cycle?",
                     "a_zh": "视产品复杂度而定，轻量级联名（如定制酒标、特别版礼盒）约2-3个月，深度联名（如游艇内饰联名设计）约6-12个月。",
                     "a_en": "Depending on product complexity: lightweight co-branding (e.g., custom labels, special edition gift boxes) takes 2-3 months; deep co-branding (e.g., yacht interior co-design) takes 6-12 months."},
                    {"q_zh": "如何衡量联名合作的效果？", "q_en": "How is co-branding effectiveness measured?",
                     "a_zh": "我们通过品牌曝光量、社交互动、新增客户、销售转化等多个维度建立评估体系，定期产出合作效果报告。",
                     "a_en": "We establish an evaluation system across multiple dimensions including brand exposure, social engagement, new customer acquisition, and sales conversion, producing regular collaboration performance reports."}
                ]
            }
        }
    },
    "partner-type-service": {
        "title": "服务整合",
        "title_en": "Service Integration",
        "hero_en": "Service Integration Partnerships",
        "sections": {
            "overview": {
                "zh": "奇幻假期整合游艇产业链上下游服务资源，从船舶保险、金融方案到船员培训、餐饮定制，我们构建一站式高端服务生态，让船东只需享受航行，其余交给我们。",
                "en": "Fantastic Vacation integrates upstream and downstream service resources across the yacht industry chain — from marine insurance and financial solutions to crew training and bespoke catering. We build a one-stop premium service ecosystem so owners can simply enjoy sailing while we handle the rest."
            },
            "benefits": {
                "title_zh": "合作优势",
                "title_en": "Partnership Benefits",
                "items": [
                    {"zh": "一站式服务整合，零对接成本", "en": "One-stop service integration with zero coordination cost"},
                    {"zh": "服务品质标准化与监督体系", "en": "Service quality standardization and supervision system"},
                    {"zh": "客户资源共享与精准匹配", "en": "Customer resource sharing and precise matching"},
                    {"zh": "联合服务套餐与优惠体系", "en": "Joint service packages and discount system"},
                    {"zh": "服务数据互通与智能推荐", "en": "Service data interoperability and intelligent recommendations"}
                ]
            },
            "tiers": {
                "title_zh": "合作层级",
                "title_en": "Partnership Tiers",
                "items": [
                    {"zh": "核心服务商", "en": "Core Service Provider", "desc_zh": "战略绑定、数据互通、联合定价、品质共管", "desc_en": "Strategic alliance, data sharing, joint pricing, quality co-management"},
                    {"zh": "认证服务商", "en": "Certified Service Provider", "desc_zh": "资质认证、标准培训、质量抽查", "desc_en": "Qualification certification, standard training, spot quality checks"},
                    {"zh": "推荐服务商", "en": "Recommended Service Provider", "desc_zh": "需求匹配、客户引流、佣金结算", "desc_en": "Demand matching, customer referral, commission settlement"}
                ]
            },
            "process": {
                "title_zh": "合作流程",
                "title_en": "Partnership Process",
                "steps": [
                    {"zh": "服务评估", "en": "Service Evaluation", "desc_zh": "评估服务商资质、能力、口碑与资源", "desc_en": "Evaluate service provider qualifications, capabilities, reputation, and resources"},
                    {"zh": "标准对接", "en": "Standard Alignment", "desc_zh": "对齐服务标准、流程规范与品质要求", "desc_en": "Align service standards, process specifications, and quality requirements"},
                    {"zh": "协议签署", "en": "Agreement Signing", "desc_zh": "确立合作关系、分成模式与服务保障", "desc_en": "Establish partnership, revenue sharing model, and service guarantees"},
                    {"zh": "系统入驻", "en": "System Onboarding", "desc_zh": "接入奇幻假期服务平台，上线服务产品", "desc_en": "Integrate with Fantastic Vacation service platform, list service products"},
                    {"zh": "运营优化", "en": "Operations Optimization", "desc_zh": "定期质量评估、客户反馈、服务迭代", "desc_en": "Regular quality assessment, customer feedback, service iteration"}
                ]
            },
            "faq": {
                "title_zh": "常见问题",
                "title_en": "FAQ",
                "items": [
                    {"q_zh": "如何成为核心服务商？", "q_en": "How to become a core service provider?",
                     "a_zh": "核心服务商需具备行业领先的服务能力与口碑，通过奇幻假期的严格评估体系，并在合作期内保持高水准的服务质量和客户满意度。",
                     "a_en": "Core service providers must demonstrate industry-leading service capabilities and reputation, pass Fantastic Vacation's rigorous evaluation system, and maintain high service quality and customer satisfaction throughout the partnership."},
                    {"q_zh": "服务商享有怎样的客户资源？", "q_en": "What customer resources do service providers access?",
                     "a_zh": "服务商可通过奇幻假期平台触达200+高净值客户群体，涵盖游艇船东、企业客户与爱好者社群。平台根据服务类型与客户需求进行精准匹配推荐。",
                     "a_en": "Service providers can reach 200+ high-net-worth customers through the Fantastic Vacation platform, including yacht owners, corporate clients, and enthusiast communities. The platform provides precise matching recommendations based on service type and customer needs."},
                    {"q_zh": "服务品质如何保障？", "q_en": "How is service quality ensured?",
                     "a_zh": "我们建立了三级品质管控体系：入驻前的资质审核、服务中的抽查监控、服务后的客户评价。不合格服务商将面临降级或清退。",
                     "a_en": "We have established a three-tier quality control system: pre-onboarding qualification review, in-service spot-check monitoring, and post-service customer evaluation. Non-compliant providers face downgrade or removal."}
                ]
            }
        }
    },
    "partner-type-agent": {
        "title": "渠道代理",
        "title_en": "Channel Agency",
        "hero_en": "Channel Agency Partnerships",
        "sections": {
            "overview": {
                "zh": "奇幻假期面向全球招募渠道代理伙伴，共享品牌资源、销售支持与完整培训体系。无论您是游艇经纪、高端会所还是投资顾问，加入我们的代理网络，共同开拓快速增长的高净值游艇消费市场。",
                "en": "Fantastic Vacation recruits channel agency partners globally, sharing brand resources, sales support, and a comprehensive training system. Whether you're a yacht broker, premium club, or investment advisor, join our agency network to explore the rapidly growing high-net-worth yacht consumer market together."
            },
            "benefits": {
                "title_zh": "合作优势",
                "title_en": "Partnership Benefits",
                "items": [
                    {"zh": "全方位品牌授权与物料支持", "en": "Comprehensive brand authorization and material support"},
                    {"zh": "专业销售培训与产品知识体系", "en": "Professional sales training and product knowledge system"},
                    {"zh": "数字化销售工具与CRM系统", "en": "Digital sales tools and CRM system"},
                    {"zh": "有竞争力的佣金与激励方案", "en": "Competitive commission and incentive programs"},
                    {"zh": "区域保护政策，保障代理权益", "en": "Regional protection policies to safeguard agency rights"}
                ]
            },
            "tiers": {
                "title_zh": "合作层级",
                "title_en": "Partnership Tiers",
                "items": [
                    {"zh": "区域总代理", "en": "Regional Master Agent", "desc_zh": "区域独占权、团队建设支持、联合品牌运营", "desc_en": "Regional exclusivity, team building support, joint brand operations"},
                    {"zh": "城市合作伙伴", "en": "City Partner", "desc_zh": "城市级授权、销售工具、培训体系", "desc_en": "City-level authorization, sales tools, training system"},
                    {"zh": "推荐渠道", "en": "Referral Channel", "desc_zh": "线索共享、快速结算、入门培训", "desc_en": "Lead sharing, fast settlement, introductory training"}
                ]
            },
            "process": {
                "title_zh": "合作流程",
                "title_en": "Partnership Process",
                "steps": [
                    {"zh": "资质申请", "en": "Qualification Application", "desc_zh": "提交代理资质、资源能力与市场计划", "desc_en": "Submit agency qualifications, resource capabilities, and market plan"},
                    {"zh": "审核评估", "en": "Review & Evaluation", "desc_zh": "评估市场匹配度、资源实力与发展潜力", "desc_en": "Evaluate market fit, resource strength, and growth potential"},
                    {"zh": "签约授权", "en": "Signing & Authorization", "desc_zh": "签署代理协议，获取品牌授权与销售工具", "desc_en": "Sign agency agreement, obtain brand authorization and sales tools"},
                    {"zh": "培训启动", "en": "Training & Launch", "desc_zh": "产品培训、销售赋能、市场启动支持", "desc_en": "Product training, sales enablement, market launch support"},
                    {"zh": "持续赋能", "en": "Continuous Empowerment", "desc_zh": "定期复盘、资源升级、联合营销活动", "desc_en": "Regular reviews, resource upgrades, joint marketing campaigns"}
                ]
            },
            "faq": {
                "title_zh": "常见问题",
                "title_en": "FAQ",
                "items": [
                    {"q_zh": "成为代理商需要什么条件？", "q_en": "What are the requirements to become an agent?",
                     "a_zh": "我们欢迎具有高端客户资源、行业经验或销售能力的个人与机构。具体要求根据合作层级有所不同，区域总代理需具备团队管理能力和本地市场影响力。",
                     "a_en": "We welcome individuals and organizations with high-end customer resources, industry experience, or sales capabilities. Specific requirements vary by partnership tier; Regional Master Agents need team management capabilities and local market influence."},
                    {"q_zh": "代理商的佣金政策是怎样的？", "q_en": "What is the agent commission policy?",
                     "a_zh": "我们提供行业有竞争力的佣金结构，根据产品类型、订单规模与合作层级浮动，并设有阶梯式激励方案。详细政策将在签约前披露。",
                     "a_en": "We offer industry-competitive commission structures that vary by product type, order size, and partnership tier, with tiered incentive programs. Detailed policies will be disclosed before signing."},
                    {"q_zh": "有区域保护吗？", "q_en": "Is there regional protection?",
                     "a_zh": "是的。区域总代理享有指定区域的独家代理权保障。城市合作伙伴也享有对应城市的优先服务权，确保各层级代理的利益不受冲突。",
                     "a_en": "Yes. Regional Master Agents enjoy exclusive agency rights within their designated territories. City Partners also have priority service rights in their corresponding cities, ensuring conflict-free interests across all agency tiers."}
                ]
            }
        }
    },
    "partner-type-tech": {
        "title": "技术合作",
        "title_en": "Technology Cooperation",
        "hero_en": "Technology Cooperation",
        "sections": {
            "overview": {
                "zh": "奇幻假期拥抱前沿科技，与智能船舶、新能源、数字化平台等领域的技术先锋合作，推动游艇行业的智能化升级。从混合动力系统到船载AI管家，从数字孪生到元宇宙体验——我们正在重新定义未来游艇生活。",
                "en": "Fantastic Vacation embraces cutting-edge technology, partnering with tech pioneers in smart vessels, new energy, and digital platforms to drive the intelligent upgrade of the yacht industry. From hybrid propulsion systems to onboard AI butlers, from digital twins to metaverse experiences — we are redefining the future of yacht living."
            },
            "benefits": {
                "title_zh": "合作优势",
                "title_en": "Partnership Benefits",
                "items": [
                    {"zh": "联合技术研发与创新实验室", "en": "Joint technology R&D and innovation lab"},
                    {"zh": "新技术在游艇场景的优先测试权", "en": "Priority testing rights for new technologies in yacht scenarios"},
                    {"zh": "技术成果共享与知识产权保护", "en": "Technology achievement sharing with IP protection"},
                    {"zh": "行业技术标准制定参与", "en": "Participation in industry technology standard setting"},
                    {"zh": "联合技术推广与市场开拓", "en": "Joint technology promotion and market development"}
                ]
            },
            "tiers": {
                "title_zh": "合作层级",
                "title_en": "Partnership Tiers",
                "items": [
                    {"zh": "战略技术伙伴", "en": "Strategic Technology Partner", "desc_zh": "联合实验室、深度研发、技术标准、全球推广", "desc_en": "Joint lab, deep R&D, technology standards, global promotion"},
                    {"zh": "解决方案伙伴", "en": "Solution Partner", "desc_zh": "场景应用、系统集成、定制开发", "desc_en": "Scenario application, system integration, custom development"},
                    {"zh": "技术生态伙伴", "en": "Technology Ecosystem Partner", "desc_zh": "技术互补、资源共享、联合活动", "desc_en": "Technology complementarity, resource sharing, joint events"}
                ]
            },
            "process": {
                "title_zh": "合作流程",
                "title_en": "Partnership Process",
                "steps": [
                    {"zh": "技术评估", "en": "Technology Assessment", "desc_zh": "评估技术成熟度、适配性与应用潜力", "desc_en": "Evaluate technology maturity, compatibility, and application potential"},
                    {"zh": "方案设计", "en": "Solution Design", "desc_zh": "设计技术整合方案与应用场景规划", "desc_en": "Design technology integration plan and application scenario roadmap"},
                    {"zh": "试点验证", "en": "Pilot Validation", "desc_zh": "在游艇场景进行小规模试点与技术验证", "desc_en": "Conduct small-scale pilot and technical validation in yacht scenarios"},
                    {"zh": "协议签署", "en": "Agreement Signing", "desc_zh": "确立合作关系、成果归属与商业化路径", "desc_en": "Establish partnership, IP ownership, and commercialization path"},
                    {"zh": "规模推广", "en": "Scale Deployment", "desc_zh": "技术产品化、市场推广与持续迭代", "desc_en": "Technology commercialization, market promotion, and continuous iteration"}
                ]
            },
            "faq": {
                "title_zh": "常见问题",
                "title_en": "FAQ",
                "items": [
                    {"q_zh": "技术合作主要聚焦哪些领域？", "q_en": "What areas does technology cooperation focus on?",
                     "a_zh": "我们主要关注六大方向：新能源动力（混合动力/电动）、智能航行辅助系统、船载AI与物联网、绿色材料与环保技术、数字孪生与VR/AR体验、区块链与数字资产。",
                     "a_en": "We focus on six key areas: new energy propulsion (hybrid/electric), intelligent navigation assistance, onboard AI and IoT, green materials and eco-technology, digital twins and VR/AR experiences, and blockchain with digital assets."},
                    {"q_zh": "技术合作需要多长时间的验证周期？", "q_en": "How long is the technology validation cycle?",
                     "a_zh": "视技术类型而定，软件类解决方案通常3-6个月可完成试点验证，硬件与新能源系统通常需要6-18个月。我们提供完整的测试环境与数据支持。",
                     "a_en": "Depending on technology type: software solutions typically require 3-6 months for pilot validation; hardware and new energy systems typically need 6-18 months. We provide complete testing environments and data support."},
                    {"q_zh": "技术成果的知识产权如何归属？", "q_en": "Who owns the IP for technology achievements?",
                     "a_zh": "根据合作模式协商确定。一般原则是：技术伙伴保留核心技术IP，联合研发成果根据贡献比例共享或协商分配，确保双方利益。",
                     "a_en": "Determined through negotiation based on the cooperation model. General principle: technology partners retain core technology IP; joint R&D achievements are shared or allocated based on contribution ratio, ensuring mutual benefit."}
                ]
            }
        }
    }
}

# ============================================================
# GENERATE i18n dictionary entries
# ============================================================

def generate_i18n_entries():
    """Generate all new i18n dictionary entries."""
    entries = {}
    base = "partner-type-"
    
    for ptype, data in CONTENT.items():
        slug = ptype.replace("partner-type-", "")
        ns = f"partner-type-{slug}"
        
        hero_key = f"{ns}.314"  # Reserved range
        overview_key = f"{ns}.600"
        entries[overview_key] = {"zh": data["sections"]["overview"]["zh"], "en": data["sections"]["overview"]["en"]}
        
        # Benefits
        benefits = data["sections"]["benefits"]
        bt_key = f"{ns}.610"
        entries[bt_key] = {"zh": benefits["title_zh"], "en": benefits["title_en"]}
        for i, item in enumerate(benefits["items"]):
            entries[f"{ns}.611"] = {"zh": item["zh"], "en": item["en"]}
        
        # Tiers
        tiers = data["sections"]["tiers"]
        tt_key = f"{ns}.620"
        entries[tt_key] = {"zh": tiers["title_zh"], "en": tiers["title_en"]}
        for i, item in enumerate(tiers["items"]):
            base_k = int(f"{ns.split('.')[-1]}.{630 + i*3}")
            # Use simpler numbering
            k1 = f"{ns}.630"  # tier name
            k2 = f"{ns}.631"  # tier desc
            entries[f"{ns}.tier{i}_name"] = {"zh": item["zh"], "en": item["en"]}
            entries[f"{ns}.tier{i}_desc"] = {"zh": item["desc_zh"], "en": item["desc_en"]}
        
        # Process
        process = data["sections"]["process"]
        pt_key = f"{ns}.640"
        entries[pt_key] = {"zh": process["title_zh"], "en": process["title_en"]}
        for i, step in enumerate(process["steps"]):
            entries[f"{ns}.step{i}_name"] = {"zh": step["zh"], "en": step["en"]}
            entries[f"{ns}.step{i}_desc"] = {"zh": step["desc_zh"], "en": step["desc_en"]}
        
        # FAQ
        faq = data["sections"]["faq"]
        ft_key = f"{ns}.650"
        entries[ft_key] = {"zh": faq["title_zh"], "en": faq["title_en"]}
        for i, item in enumerate(faq["items"]):
            entries[f"{ns}.faq{i}_q"] = {"zh": item["q_zh"], "en": item["q_en"]}
            entries[f"{ns}.faq{i}_a"] = {"zh": item["a_zh"], "en": item["a_en"]}
    
    return entries


# ============================================================
# GENERATE HTML sections for insertion
# ============================================================

def generate_html_sections(ptype, data):
    """Generate HTML sections to insert into a partner-type page."""
    slug = ptype.replace("partner-type-", "")
    ns = f"partner-type-{slug}"
    
    sections_html = []
    
    # 1. Overview Section
    overview = data["sections"]["overview"]
    sections_html.append(f'''
    <!-- 合作概述 -->
    <section class="partner-overview-section" style="padding:80px 0;background:var(--dark3)">
        <div class="container reveal" style="max-width:1100px">
            <div class="section-header reveal">
                <span class="section-label gold-gradient" data-i18n="{ns}.610">合作概述</span>
                <h2><span class="gold-gradient" data-i18n="{ns}.610">{data["title"]}合作概述</span></h2>
                <div class="divider-gold"></div>
            </div>
            <p data-i18n="{ns}.600" style="color:var(--text-muted);font-size:16px;line-height:1.9;max-width:900px;margin:0 auto;text-align:center">{overview["zh"]}</p>
        </div>
    </section>''')
    
    # 2. Benefits Section
    benefits = data["sections"]["benefits"]
    benefits_items = ""
    for i, item in enumerate(benefits["items"]):
        benefits_items += f'''
                <div class="benefit-card reveal" style="background:rgba(255,255,255,0.03);border:1px solid rgba(201,169,110,0.15);border-radius:12px;padding:32px 28px;text-align:center;transition:all .3s ease">
                    <div style="font-size:32px;margin-bottom:16px">{['🏭','⚓','✈️','🏨','🎨','🏛️','🤝','🔧','🌐','💻'][list(CONTENT.keys()).index(ptype) if ptype in CONTENT else 0]}</div>
                    <h4 data-i18n="{ns}.b{i}_t" style="font-size:17px;color:var(--gold);margin-bottom:12px">{item['zh']}</h4>
                    <p data-i18n="{ns}.b{i}_d" style="color:var(--text-muted);font-size:14px;line-height:1.6">{item['en']}</p>
                </div>'''
    
    benefits_style = '''
    <style>
    .benefits-grid-section{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px;margin-top:40px}
    .benefit-card:hover{transform:translateY(-4px);border-color:rgba(201,169,110,0.4);box-shadow:0 12px 40px rgba(0,0,0,0.3)}
    </style>
    '''
    
    sections_html.append(f'''
    <!-- 合作优势 -->
    <section class="partner-benefits-section" style="padding:80px 0;background:var(--dark2)">
        <div class="container reveal" style="max-width:1200px">
            <div class="section-header reveal">
                <span class="section-label gold-gradient" data-i18n="{ns}.610">合作优势</span>
                <h2><span class="gold-gradient" data-i18n="{ns}.610">{benefits["title_zh"]}</span></h2>
                <div class="divider-gold"></div>
            </div>
            {benefits_style}
            <div class="benefits-grid-section">{benefits_items}
            </div>
        </div>
    </section>''')
    
    # 3. Partnership Tiers Section
    tiers = data["sections"]["tiers"]
    tiers_items = ""
    tier_icons = ["💎", "⭐", "🔹"]
    for i, item in enumerate(tiers["items"]):
        tiers_items += f'''
                <div class="tier-card reveal" style="background:rgba(255,255,255,0.03);border:1px solid rgba(201,169,110,{0.25 - i*0.08});border-radius:16px;padding:40px 32px;text-align:center;transition:all .3s ease">
                    <div style="font-size:36px;margin-bottom:16px">{tier_icons[i] if i < len(tier_icons) else '🔹'}</div>
                    <h3 data-i18n="{ns}.tier{i}_name" style="font-size:22px;color:var(--gold);margin-bottom:16px;font-family:'Playfair Display',serif">{item['zh']}</h3>
                    <p data-i18n="{ns}.tier{i}_desc" style="color:var(--text-muted);font-size:14px;line-height:1.7">{item['desc_zh']}</p>
                </div>'''
    
    sections_html.append(f'''
    <!-- 合作层级 -->
    <section class="partner-tiers-section" style="padding:80px 0;background:var(--dark3)">
        <div class="container reveal" style="max-width:1200px">
            <div class="section-header reveal">
                <span class="section-label gold-gradient" data-i18n="{ns}.620">合作层级</span>
                <h2><span class="gold-gradient" data-i18n="{ns}.620">{tiers["title_zh"]}</span></h2>
                <div class="divider-gold"></div>
            </div>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px;margin-top:40px">{tiers_items}
            </div>
        </div>
    </section>''')
    
    # 4. Process Section
    process = data["sections"]["process"]
    process_steps = ""
    for i, step in enumerate(process["steps"]):
        process_steps += f'''
                <div class="process-step reveal" style="display:flex;gap:24px;align-items:flex-start;padding:28px 0;border-bottom:1px solid rgba(201,169,110,0.1)">
                    <div style="flex-shrink:0;width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,rgba(201,169,110,0.2),rgba(201,169,110,0.05));border:2px solid var(--gold);display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;color:var(--gold)">{i+1}</div>
                    <div>
                        <h4 data-i18n="{ns}.step{i}_name" style="font-size:18px;color:#fff;margin-bottom:8px">{step['zh']}</h4>
                        <p data-i18n="{ns}.step{i}_desc" style="color:var(--text-muted);font-size:14px;line-height:1.7">{step['desc_zh']}</p>
                    </div>
                </div>'''
    
    sections_html.append(f'''
    <!-- 合作流程 -->
    <section class="partner-process-section" style="padding:80px 0;background:var(--dark2)">
        <div class="container reveal" style="max-width:900px">
            <div class="section-header reveal">
                <span class="section-label gold-gradient" data-i18n="{ns}.640">合作流程</span>
                <h2><span class="gold-gradient" data-i18n="{ns}.640">{process["title_zh"]}</span></h2>
                <div class="divider-gold"></div>
            </div>
            <div style="margin-top:40px">{process_steps}
            </div>
        </div>
    </section>''')
    
    # 5. FAQ Section
    faq = data["sections"]["faq"]
    faq_items = ""
    for i, item in enumerate(faq["items"]):
        faq_id = f"faq_{slug}_{i}"
        faq_items += f'''
                <div class="faq-item reveal" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:12px;overflow:hidden;margin-bottom:16px">
                    <button class="faq-question" onclick="this.parentElement.classList.toggle('active')" style="width:100%;text-align:left;background:none;border:none;padding:24px 28px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:#fff;font-size:16px;font-weight:500">
                        <span data-i18n="{ns}.faq{i}_q">{item['q_zh']}</span>
                        <svg class="faq-arrow" fill="none" height="20" stroke="var(--gold)" stroke-width="2" viewBox="0 0 24 24" width="20" style="transition:transform .3s ease"><path d="m6 9 6 6 6-6"></path></svg>
                    </button>
                    <div class="faq-answer" style="max-height:0;overflow:hidden;transition:max-height .3s ease">
                        <p data-i18n="{ns}.faq{i}_a" style="padding:0 28px 24px;color:var(--text-muted);font-size:14px;line-height:1.8">{item['a_zh']}</p>
                    </div>
                </div>'''
    
    faq_style = '''
    <style>
    .faq-item.active .faq-arrow{transform:rotate(180deg)}
    .faq-item.active .faq-answer{max-height:600px!important}
    .faq-question:hover{background:rgba(201,169,110,0.04)}
    </style>
    '''
    
    sections_html.append(f'''
    <!-- 常见问题 -->
    <section class="partner-faq-section" style="padding:80px 0;background:var(--dark3)">
        <div class="container reveal" style="max-width:900px">
            <div class="section-header reveal">
                <span class="section-label gold-gradient" data-i18n="{ns}.650">常见问题</span>
                <h2><span class="gold-gradient" data-i18n="{ns}.650">{faq["title_zh"]}</span></h2>
                <div class="divider-gold"></div>
            </div>
            <div style="margin-top:40px">{faq_items}
            </div>
            {faq_style}
        </div>
    </section>''')
    
    return "".join(sections_html)


# Module loaded for content definitions. Use insert_partner_content.py to process.
