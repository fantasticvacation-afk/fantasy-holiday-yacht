/**
 * translate_helper.js
 * 读取 i18n_bs_entries.json（中文已提取，en 为空）
 * 复用 i18n.js 中已有的翻译（避免重复）
 * 对剩余条目用词典做初步翻译
 * 输出到 i18n_bs_entries.json（en 字段已填）
 */

const fs = require('fs');
const path = require('path');

// 读取已有翻译词典
let existingDict = {};
try {
  const i18nContent = fs.readFileSync('i18n.js', 'utf8');
  const match = i18nContent.match(/^var dict = ([\s\S]*?);\n/m);
  if (match) existingDict = JSON.parse(match[1]);
} catch(e) { console.log('⚠ 无法读取已有词典'); }

console.log('已有翻译词条:', Object.keys(existingDict).length);

// 常用翻译词典（可不断扩充）
const wordDict = {
  '首页': 'Home', '关于我们': 'About Us', '联系我们': 'Contact Us',
  '全系游艇': 'All Yachts', '全案定制': 'Full Customization',
  '租赁航线': 'Charter Routes', '托管维保': 'Management & Maintenance',
  '产品与服务': 'Products & Services', '新闻中心': 'News Center',
  '公司动态': 'Company News', '行业资讯': 'Industry News',
  '媒体报道': 'Media Reports', '公告通知': 'Announcements',
  '投资者关系': 'Investor Relations', '案例展示': 'Case Showcase',
  '新闻资讯': 'News & Information', '全球合作': 'Global Partnership',
  '网站地图': 'Site Map', '隐私政策': 'Privacy Policy',
  '使用条款': 'Terms of Use', '公司简介': 'Company Profile',
  '发展历程': 'History', '企业文化': 'Corporate Culture',
  '荣誉资质': 'Honors & Certifications', '社会责任': 'Social Responsibility',
  '公司地址': 'Company Address', '咨询热线': 'Consultation Hotline',
  '传真': 'Fax', '商务邮箱': 'Business Email',
  'ISO 9001质量管理体系认证': 'ISO 9001 Quality Management System Certified',
  '意大利Ferretti集团授权经销商': 'Authorized Dealer of Ferretti Group, Italy',
  '荷兰Feadship技术合作伙伴': 'Technical Partner of Feadship, Netherlands',
  '地中海船坞协会认证会员': 'Certified Member of Mediterranean Shipyard Association',
  '亚洲最佳游艇服务商三连冠': 'Three-Time Winner: Asia\'s Best Yacht Service Provider',
  '保留所有权利': 'All Rights Reserved', '电话': 'Tel', '邮箱': 'Email',
  '邮编': 'Postal Code', '地址': 'Address',
  '服务范围': 'Service Scope', '办公时间': 'Office Hours',
  '在线咨询': 'Online Consultation', '发送消息': 'Send Message',
  '您的姓名': 'Your Name', '您的邮箱': 'Your Email',
  '感兴趣的方向': 'Area of Interest', '您的留言': 'Your Message', '提交': 'Submit',
  '查看更多': 'View More', '了解详情': 'Learn More', '立即咨询': 'Consult Now',
  '探索全系游艇': 'Explore All Yachts', '预约专属顾问': 'Book Exclusive Advisor',
  '浏览全部': 'Browse All', '查看全系': 'View Full Series',
  '旗舰系列': 'Flagship Series', '远征系列': 'Expedition Series',
  '飞桥系列': 'Flybridge Series', '日间系列': 'Day Cruiser Series',
  '超级游艇': 'Superyacht', '豪华游艇': 'Luxury Yacht',
  '总长度': 'Length Overall', '最大载客': 'Max Guests',
  '最高航速': 'Max Speed', '航行等级': 'Navigation Class',
  '无限航区': 'Unlimited Navigation', '极地/冰级': 'Polar/Ice Class',
  '特殊认证': 'Special Certification',
  '€': '€', '¥': '¥', '$': '$',
  '起/周': '/week from', '含船长船员': 'Incl. Captain & Crew',
  '含全套服务': 'Full Service Included',
  '地中海': 'Mediterranean', '加勒比海': 'Caribbean', '东南亚': 'Southeast Asia',
  '7-14天': '7-14 Days', '10-21天': '10-21 Days', '5-14天': '5-14 Days',
};

// 读取待翻译文件
const entries = JSON.parse(fs.readFileSync('i18n_bs_entries.json', 'utf8'));
let reused = 0, translated = 0, pending = 0;

for (const [key, obj] of Object.entries(entries)) {
  const zh = obj.zh.trim();
  if (!zh) continue;
  
  // 1. 复用已有翻译（通过中文原文匹配）
  let found = false;
  for (const [existingKey, existingObj] of Object.entries(existingDict)) {
    if (existingObj.zh === zh && existingObj.en) {
      obj.en = existingObj.en;
      reused++;
      found = true;
      break;
    }
  }
  if (found) continue;
  
  // 2. 词典翻译
  let en = zh;
  for (const [zhWord, enWord] of Object.entries(wordDict)) {
    en = en.replace(new RegExp(zhWord.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), enWord);
  }
  
  if (en !== zh) {
    obj.en = en;
    translated++;
  } else {
    // 暂未翻译，保留中文（后续人工审校）
    obj.en = zh;
    pending++;
  }
}

fs.writeFileSync('i18n_bs_entries.json', JSON.stringify(entries, null, 2), 'utf8');
console.log(`✓ 完成！复用已有: ${reused}，词典翻译: ${translated}，待人工审校: ${pending}`);
