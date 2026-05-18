/**
 * rebuild_i18n.js
 * 重新生成 i18n.js，确保所有 data-i18n key 都有对应的翻译条目
 */

const fs = require('fs');
const { translate } = require('./translate_dict');
const path = require('path');

const HTML_DIR = __dirname;
const i18nPath = path.join(HTML_DIR, 'i18n.js');

// 1. 从现有 i18n.js 中读取已有翻译
let i18nContent = fs.readFileSync(i18nPath, 'utf8');
const dictMatch = i18nContent.match(/var dict = (\{[\s\S]*\});/);
if (!dictMatch) {
  console.error('无法解析 i18n.js');
  process.exit(1);
}

let dict;
eval('dict = ' + dictMatch[1]);

// 2. 扫描所有 HTML 文件，收集 data-i18n key 和中文
const fsExtra = require('fs'); // 重新声明
const { JSDOM } = require('jsdom'); // 如果没有，用正则提取

const htmlFiles = fs.readdirSync(HTML_DIR).filter(f => f.endsWith('.html'));
let allKeys = new Set();
let keyToZh = {};

for (const file of htmlFiles) {
  const filePath = path.join(HTML_DIR, file);
  const content = fs.readFileSync(filePath, 'utf8');
  
  // 用正则提取 data-i18n="key" 和对应的文字
  const regex = /data-i18n="([^"]+)"[\s\S]*?>(.*?)</g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    const key = match[1];
    let text = match[2].replace(/<[^>]+>/g, '').trim(); // 去掉 HTML 标签
    if (text && text.length > 1) {
      allKeys.add(key);
      if (!keyToZh[key]) keyToZh[key] = text;
    }
  }
}

console.log(`找到 ${allKeys.size} 个唯一的 data-i18n key`);

// 3. 为每个 key 添加翻译（如果不存在）
let added = 0;
for (const key of allKeys) {
  if (dict[key]) continue; // 已有翻译，跳过
  
  const zh = keyToZh[key] || key;
  const en = translate(zh);
  dict[key] = { zh, en: en !== zh ? en : zh }; // 翻译失败则用中文
  added++;
}

console.log(`新增 ${added} 个翻译条目`);

// 4. 重新生成 i18n.js
let newDictStr = 'var dict = {\n';
for (const [key, val] of Object.entries(dict)) {
  const zh = val.zh.replace(/"/g, '\\"');
  const en = val.en.replace(/"/g, '\\"');
  newDictStr += `  "${key}": { "zh": "${zh}", "en": "${en}" },\n`;
}
newDictStr = newDictStr.replace(/,\n$/, '\n};\n'); // 去掉最后一个逗号

// 替换 i18n.js 中的 dict 部分
const newContent = i18nContent.replace(/var dict = \{[\s\S]*\};/, newDictStr);
fs.writeFileSync(i18nPath, newContent, 'utf8');

console.log(`✓ i18n.js 已更新，共 ${Object.keys(dict).length} 个条目`);
