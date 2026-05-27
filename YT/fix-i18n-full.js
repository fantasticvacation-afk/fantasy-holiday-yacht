const fs = require('fs');
const path = require('path');

// Step 1: Collect all Chinese alt and placeholder texts without i18n
const files = fs.readdirSync('.').filter(f => f.endsWith('.html'));
const altTranslations = {};
const phTranslations = {};
let globalIdx = 0;

function translateChinese(text) {
  // Translation map for common yacht/boat terms
  const map = {
    '驾驶舱': 'Cockpit', '内饰客厅': 'Interior Salon', '卧室套房': 'Master Suite',
    '甲板休闲区': 'Deck Lounge', '航行实拍': 'Sailing Photo', '落日余晖': 'Sunset Glow',
    '游艇系列': 'Yacht Series',
    '主厅内饰': 'Main Hall Interior', 'IMAX影院': 'IMAX Theater',
    '主人套房': 'Owner Suite', '潜艇车库': 'Submarine Garage', '医疗中心': 'Medical Center',
    '海上航行': 'Ocean Sailing',
    '意大利阿马尔菲': 'Amalfi, Italy', '法国蔚蓝海岸': 'Côte d\'Azur, France',
    '米其林定制晚宴': 'Michelin Custom Dinner', '私人潜水活动': 'Private Diving',
    '商务接待场景': 'Business Reception', '海上日落时光': 'Sunset at Sea',
    '商务艇': 'Business Yacht', '私人艇': 'Private Yacht',
    '保养现场': 'Maintenance', 'VIP服务': 'VIP Service',
    '船员培训': 'Crew Training', '海域航行': 'Ocean Voyage',
    '太阳能系统': 'Solar System', '科研平台': 'Research Platform',
    '直升机平台': 'Helipad', '科考活动': 'Research Activity',
    '阿拉斯加': 'Alaska', '动力系统': 'Power System',
    '中式婚礼': 'Chinese Wedding', '西式婚礼': 'Western Wedding',
    '婚宴定制': 'Custom Banquet', '水下派对': 'Underwater Party',
    '私人岛屿': 'Private Island', '纪录片拍摄': 'Documentary Filming',
    '旗舰版': 'Flagship', '尊享版': 'Premium', '传承版': 'Heritage',
    '典雅版': 'Elegant', '极地王': 'Polar King', '深海王': 'Deep Sea King',
    '航海家': 'Navigator', '探险家': 'Explorer', '自由号': 'Liberty',
    '航行者': 'Voyager', '挑战者': 'Challenger', '至尊版': 'Supreme',
    '先锋号': 'Pioneer', '远航版': 'Voyage', '开拓版': 'Pioneer',
    '探索版': 'Discovery', '发现号': 'Discovery', '派对王': 'Party King',
    '海风号': 'Sea Breeze', '逸享版': 'Leisure', '城市号': 'City',
    '极光号': 'Aurora', '典藏版': 'Collector', '优雅号': 'Elegant',
    '灵动号': 'Agile', '清风号': 'Breeze', '星辉版': 'Starlight',
    '碧海版': 'Azure', '悦航版': 'Joy Cruise', '翡翠号': 'Jade',
    '晨曦号': 'Dawn', '运动王': 'Sport King', '竞速号': 'Racer',
    '领航版': 'Pilot', '飞鱼号': 'Flying Fish', '闪电号': 'Lightning',
    '微风号': 'Gentle Breeze', '海豚号': 'Dolphin', '活力号': 'Vitality',
    '巡航版': 'Cruise', '破浪版': 'Wavebreaker', '乘风版': 'Windrider',
    '王者版': 'King', '翱翔版': 'Soaring', '御风版': 'Wind Master',
    '帝王版': 'Emperor', '精英版': 'Elite', '荣耀版': 'Glory',
    '君临': 'Sovereign', '远征': 'Expedition', '飞桥': 'Flybridge',
    '日间': 'Daytripper',
    '搜索产品、新闻、案例...': 'Search products, news, cases...',
    '联系电话': 'Contact Phone',
    '请描述您的定制需求或特殊要求（可选）...': 'Please describe your customization needs (optional)...',
    '搜索游艇、服务、案例...': 'Search yachts, services, cases...',
  };
  
  // Try direct match first
  if (map[text]) return map[text];
  
  // Try composite translation for yacht model names like "君临120 旗舰版 - 驾驶舱"
  const m = text.match(/^(.+?)\s*(\d+)\s+(.+?)\s*[-–—]\s*(.+)$/);
  if (m) {
    const brand = map[m[1]] || m[1];
    const size = m[2];
    const variant = map[m[3]] || m[3];
    const view = map[m[4]] || m[4];
    return `${brand} ${size} ${variant} - ${view}`;
  }
  
  // Try just brand + variant
  for (const [zh, en] of Object.entries(map)) {
    if (text.includes(zh) && zh.length > 1) {
      let result = text;
      // Sort by length descending to replace longer matches first
      const sorted = Object.entries(map).sort((a,b) => b[0].length - a[0].length);
      for (const [z, e] of sorted) {
        if (text.includes(z) && z.length > 1) {
          result = result.replace(z, e);
        }
      }
      if (result !== text) return result;
    }
  }
  
  return text; // fallback
}

// Step 2: Process each HTML file - add data-i18n-attr for alt and placeholder
let totalFixed = 0;
const newDictEntries = {};

files.forEach(file => {
  let html = fs.readFileSync(file, 'utf8');
  let modified = false;
  
  // Fix placeholder attributes with Chinese
  html = html.replace(/placeholder="([^"]*[\u4e00-\u9fff][^"]*)"/g, (match, text) => {
    // Check if already has data-i18n-attr nearby
    return match; // We'll handle this differently
  });
  
  // Fix alt attributes - add data-i18n-attr
  const prefix = file.replace('.html', '');
  
  // Process alt attributes with Chinese
  const altMatches = [...html.matchAll(/alt="([^"]*[\u4e00-\u9fff][^"]*)"/g)];
  altMatches.forEach((m, idx) => {
    const chineseText = m[1];
    const key = `_alt.${prefix}.${idx}`;
    const englishText = translateChinese(chineseText);
    newDictEntries[key] = { zh: chineseText, en: englishText };
  });
  
  // Process placeholder attributes with Chinese  
  const phMatches = [...html.matchAll(/placeholder="([^"]*[\u4e00-\u9fff][^"]*)"/g)];
  phMatches.forEach((m, idx) => {
    const chineseText = m[1];
    const key = `_ph.${prefix}.${idx}`;
    const englishText = translateChinese(chineseText);
    newDictEntries[key] = { zh: chineseText, en: englishText };
  });
  
  // Actually modify the HTML to add data-i18n-attr
  let altIdx = 0;
  html = html.replace(/alt="([^"]*[\u4e00-\u9fff][^"]*)"/g, (match, text) => {
    const key = `_alt.${prefix}.${altIdx}`;
    altIdx++;
    // Check if parent img already has data-i18n-attr
    return `alt="${text}" data-i18n-attr="alt:${key}"`;
  });
  
  let phIdx = 0;
  html = html.replace(/placeholder="([^"]*[\u4e00-\u9fff][^"]*)"/g, (match, text) => {
    const key = `_ph.${prefix}.${phIdx}`;
    phIdx++;
    return `placeholder="${text}" data-i18n-attr="placeholder:${key}"`;
  });
  
  if (altIdx > 0 || phIdx > 0) {
    fs.writeFileSync(file, html);
    totalFixed += altIdx + phIdx;
    console.log(`✓ ${file}: ${altIdx} alt + ${phIdx} placeholder`);
  }
});

console.log(`\nTotal attributes fixed: ${totalFixed}`);
console.log(`New dict entries: ${Object.keys(newDictEntries).length}`);

// Step 3: Add new entries to i18n.js
let i18n = fs.readFileSync('i18n.js', 'utf8');

// Find the closing of the dict object and insert before it
let insertStr = '';
for (const [key, val] of Object.entries(newDictEntries)) {
  const zh = val.zh.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
  const en = val.en.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
  insertStr += `"${key}":{"zh":"${zh}","en":"${en}"},`;
}

// Insert before the closing };
i18n = i18n.replace(/};\s*\n\s*function\s+applyI18n/, insertStr + '};\n\nfunction applyI18n');

fs.writeFileSync('i18n.js', i18n);
console.log('i18n.js updated');

// Verify syntax
try {
  require('child_process').execSync('node -c i18n.js', {stdio: 'pipe'});
  console.log('✓ i18n.js syntax OK');
} catch(e) {
  console.log('✗ i18n.js syntax error!');
}
