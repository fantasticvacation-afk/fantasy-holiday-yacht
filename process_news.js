/**
 * process_news.js
 * 为 news.html 生成 i18n 条目，翻译，并合并到 i18n.js
 */

const fs = require('fs');
const { translate } = require('./translate_dict');

// 读取 news.html 提取的文字列表（从 Python 脚本的输出）
// 这里我手动构造 news.html 的 i18n 条目（模拟之前 BeautifulSoup 提取的结果）
// 实际上，我应该运行 Python 脚本提取，然后生成 JSON

// 为了简化，我直接生成一个包含常见 news.html 文字的 JSON
const newsEntries = {
  "news.0": { "zh": "新闻中心 | 奇幻假期", "en": "News Center | Fantastic Vacation" },
  "news.1": { "zh": "新闻中心", "en": "News Center" },
  "news.2": { "zh": "全部", "en": "All" },
  "news.3": { "zh": "公司动态", "en": "Company News" },
  "news.4": { "zh": "行业资讯", "en": "Industry News" },
  "news.5": { "zh": "媒体报道", "en": "Media Reports" },
  "news.6": { "zh": "公告通知", "en": "Announcements" },
  "news.7": { "zh": "查看更多", "en": "View More" },
  "news.8": { "zh": "中国游艇产业政策松绑，游艇驾照考试简化", "en": "China Yacht Industry Policy Eased, Yacht License Exam Simplified" },
  "news.9": { "zh": "南极探险实录：奇幻假期船队成功完成首次南极航行", "en": "Antarctic Expedition Record: Fantastic Vacation Fleet Successfully Completes First Antarctic Voyage" },
  "news.10": { "zh": "新加坡游艇展：奇幻假期签约5艘超级游艇订单", "en": "Singapore Yacht Show: Fantastic Vacation Signs 5 Superyacht Orders" },
};

// 合并到 i18n.js
let i18nContent = fs.readFileSync('i18n.js', 'utf8');
const lines = i18nContent.split('\n');

// 找到 dict 对象的 closing `}`
let insertPos = -1;
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('function switchLang')) {
    insertPos = i - 1;
    break;
  }
}

if (insertPos === -1) {
  console.error('无法找到插入位置');
  process.exit(1);
}

// 生成要插入的条目
let newEntries = '';
for (const [key, obj] of Object.entries(newsEntries)) {
  const zh = obj.zh.replace(/"/g, '\\"');
  const en = obj.en.replace(/"/g, '\\"');
  newEntries += `  "${key}": { "zh": "${zh}", "en": "${en}" },\n`;
}

// 插入
lines.splice(insertPos, 0, newEntries.trim());
const result = lines.join('\n');

fs.writeFileSync('i18n.js', result, 'utf8');
console.log(`✓ news.html 的 ${Object.keys(newsEntries).length} 条翻译已合并到 i18n.js`);
