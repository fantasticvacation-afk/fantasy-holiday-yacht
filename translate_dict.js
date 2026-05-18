/**
 * translate_dict.js - 中译英词典（可不断扩充）
 * 用法: node -e "const d=require('./translate_dict'); console.log(d.translate('首页'))"
 */

const dict = {
  // 导航与通用
  '首页': 'Home',
  '关于我们': 'About Us',
  '联系我们': 'Contact Us',
  '全系游艇': 'All Yachts',
  '全案定制': 'Full Customization',
  '租赁航线': 'Charter Routes',
  '托管维保': 'Management & Maintenance',
  '案例展示': 'Case Showcase',
  '新闻资讯': 'News & Information',
  '全球合作': 'Global Partnership',
  '网站地图': 'Site Map',
  '隐私政策': 'Privacy Policy',
  '使用条款': 'Terms of Use',
  
  // 游艇相关
  '游艇': 'Yacht',
  '超级游艇': 'Superyacht',
  '豪华游艇': 'Luxury Yacht',
  '旗舰系列': 'Flagship Series',
  '远征系列': 'Expedition Series',
  '飞桥系列': 'Flybridge Series',
  '日间系列': 'Day Cruiser Series',
  '总长度': 'Length Overall',
  '型宽': 'Beam',
  '吃水': 'Draft',
  '排水量': 'Displacement',
  '最高航速': 'Max Speed',
  '巡航速度': 'Cruise Speed',
  '续航里程': 'Range',
  '客舱数量': 'Cabins',
  '最大载客': 'Max Guests',
  '船员人数': 'Crew',
  '建造年份': 'Year Built',
  '翻新年份': 'Refit Year',
  '船厂': 'Shipyard',
  '设计师': 'Designer',
  '发动机': 'Engine',
  '发电机': 'Generator',
  '燃油类型': 'Fuel Type',
  '柴油': 'Diesel',
  '混合动力': 'Hybrid',
  '纯电动': 'Full Electric',
  '无限航区': 'Unlimited Navigation',
  '极地/冰级': 'Polar/Ice Class',
  '特殊认证': 'Special Certification',
  
  // 页面标题与按钮
  '了解更多': 'Learn More',
  '查看详情': 'View Details',
  '立即咨询': 'Inquire Now',
  '浏览全部': 'Browse All',
  '查看全系': 'View Full Series',
  '探索全系': 'Explore All Series',
  '预约专属顾问': 'Book Exclusive Advisor',
  '查看更多': 'View More',
  '了解详情': 'Learn More',
  '立即预约': 'Book Now',
  '咨询热线': 'Consultation Hotline',
  
  // 公司信息
  '公司简介': 'Company Profile',
  '发展历程': 'History',
  '企业文化': 'Corporate Culture',
  '荣誉资质': 'Honors & Certifications',
  '社会责任': 'Social Responsibility',
  '公司地址': 'Company Address',
  '传真': 'Fax',
  '商务邮箱': 'Business Email',
  '电话': 'Tel',
  '邮箱': 'Email',
  '地址': 'Address',
  '邮编': 'Postal Code',
  '服务范围': 'Service Scope',
  '办公时间': 'Office Hours',
  
  // 新闻中心
  '新闻中心': 'News Center',
  '公司动态': 'Company News',
  '行业资讯': 'Industry News',
  '媒体报道': 'Media Reports',
  '公告通知': 'Announcements',
  '投资者关系': 'Investor Relations',
  '产品与服务': 'Products & Services',
  
  // 联系方式
  '在线咨询': 'Online Consultation',
  '发送消息': 'Send Message',
  '您的姓名': 'Your Name',
  '您的邮箱': 'Your Email',
  '感兴趣的方向': 'Area of Interest',
  '您的留言': 'Your Message',
  '提交': 'Submit',
  
  // 单位与货币
  '米': 'm',
  '节': 'kn',
  '小时': 'h',
  '海里': 'nm',
  '起/周': '/week from',
  '万起': 'Million from',
  '万': 'Million',
  '€': '€',
  '¥': '¥',
  '$': '$',
  
  // 地理区域
  '地中海': 'Mediterranean',
  '加勒比海': 'Caribbean',
  '东南亚': 'Southeast Asia',
  '中东': 'Middle East',
  '北欧': 'Northern Europe',
  '7-14天': '7-14 Days',
  '10-21天': '10-21 Days',
  '5-14天': '5-14 Days',
  
  // 品牌与认证
  '奇幻假期': 'Fantastic Vacation',
  'FANTASTIC VACATION': 'FANTASTIC VACATION',
  'ISO 9001质量管理体系认证': 'ISO 9001 Quality Management System Certified',
  '意大利Ferretti集团授权经销商': 'Authorized Dealer of Ferretti Group, Italy',
  '荷兰Feadship技术合作伙伴': 'Technical Partner of Feadship, Netherlands',
  '地中海船坞协会认证会员': 'Certified Member of Mediterranean Shipyard Association',
  '亚洲最佳游艇服务商三连冠': 'Three-Time Winner: Asia\'s Best Yacht Service Provider',
  '保留所有权利': 'All Rights Reserved',
  '© 2020-2026': '© 2020-2026',
  
  // 社交媒体
  '微信公众号': 'WeChat Official Account',
  '微博': 'Weibo',
  '抖音': 'TikTok (Douyin)',
  'LinkedIn': 'LinkedIn',
  'YouTube': 'YouTube',
  
  // 服务描述
  '年行业深耕': 'Years of Industry Expertise',
  '全球高净值客户': 'Global High-Net-Worth Clients',
  '运营豪华游艇': 'Luxury Yachts Operated',
  '覆盖国际海域': 'Covering International Waters',
  '为何选择奇幻假期': 'Why Choose Fantastic Vacation',
  '我们不只是游艇服务商，更是您海洋生活方式的全方位策展人': 'We are not just a yacht service provider, but your all-around curator of marine lifestyle',
  '全产业链整合': 'Full Industry Chain Integration',
  '从游艇研发设计、船厂制造监造，到交付后的运营管理、维修保养、保险合规——我们提供游艇全生命周期的一站式解决方案。': 'From yacht R&D design, shipyard manufacturing supervision, to post-delivery operation management, maintenance, insurance & compliance — we provide one-stop solutions for the entire yacht lifecycle.',
  '顶级设计能力': 'Top-Tier Design Capability',
  '携手意大利、荷兰、德国等全球顶尖船舶设计事务所，将艺术美学与工程性能完美融合，每艘游艇都是独一无二的海上艺术品。': 'Partnered with world\'s top naval architecture firms in Italy, Netherlands, Germany, perfectly blending artistic aesthetics with engineering performance — each yacht is a unique seafaring artwork.',
  '全球网络覆盖': 'Global Network Coverage',
  '在地中海、加勒比海、东南亚、中东、北欧等全球30+热门海域设有服务基地，无论您的航程指向何方，我们都能即时响应。': 'Service bases in 30+ popular waters worldwide including Mediterranean, Caribbean, Southeast Asia, Middle East, Northern Europe — wherever your voyage leads, we respond instantly.',
  '管家式服务体系': 'Butler-Style Service System',
  '每位客户配备专属Yacht Manager，7×24小时响应需求，从航线规划到岸上行程，真正实现"拎包出海"的无忧体验。': 'Each client is assigned a dedicated Yacht Manager, 7×24h response, from route planning to onshore itineraries — truly realizing a worry-free "pack & sail" experience.',
  
  // yachts.html 补充词条
  '从入门到顶奢的全谱系覆盖': 'Full Spectrum Coverage from Entry-Level to Ultra-Luxury',
  '核心系列': 'Core Series',
  '船型款式': 'Model Types',
  '尺寸跨度': 'Size Range',
  '全部系列': 'All Series',
  '君临系列': 'Monarch Series',
  '龙腾四海': 'Dragon Soars Four Seas',
  '凤舞九天': 'Phoenix Dances Nine Heavens',
  '总长': 'Length',
  '载客': 'Guests',
  '航速': 'Speed',
  '详情 →': 'Details →',
  'M': 'M',
  '18kn': '18kn',
  '17kn': '17kn',
  '120m': '120m',
  '110m': '110m',
  '45-120M': '45-120M',
  '旗舰': 'Flagship',
  '超级': 'Super',
  '豪华': 'Luxury',
  '定制': 'Custom',
  '租赁': 'Charter',
  '新品': 'New',
  '热门': 'Popular',
  '推荐': 'Recommended',
  '全部': 'All',
  '筛选': 'Filter',
  '排序': 'Sort',
  '价格': 'Price',
  '尺寸': 'Size',
  '年份': 'Year',
  
  // yachts.html 游艇名称翻译（创意翻译）
  '御风而行': 'Riding the Wind',
  '鲲鹏展翅': 'Kunpeng Spreads Wings',
  '天子驾临': 'The Emperor Arrives',
  '帝梦星河': 'Imperial Dream Star River',
  '皇极天枢': 'Imperial Polaris',
  '金阙凌云': 'Golden Palace Reaching Clouds',
  '瀚海明月': 'Vast Sea Bright Moon',
  '紫禁祥云': 'Forbidden City Auspicious Clouds',
  '天命归元': 'Heaven\'s Mandate Returns',
  '九五至尊': 'The Supreme',
  '破冰逐浪': 'Ice Breaker',
  '深海猎鹰': 'Deep Sea Falcon',
  '星辰大海': 'Starry Ocean',
  '天涯行者': 'Horizon Walker',
  'FANTASTIC VACATION': 'FANTASTIC VACATION',
  'LOADING': 'LOADING',
  'M': 'M',
  'kn': 'kn',
};

/**
 * 翻译函数：优先查词典，查不到则返回原文（后续人工校对）
 */
function translate(text) {
  if (!text || typeof text !== 'string') return text;
  // 精确匹配
  if (dict[text]) return dict[text];
  // 部分匹配（替换词典中的短语）
  let result = text;
  for (const [zh, en] of Object.entries(dict)) {
    if (zh.length > 1 && result.includes(zh)) {
      result = result.split(zh).join(en);
    }
  }
  return result === text ? text : result;
}

module.exports = { dict, translate };
