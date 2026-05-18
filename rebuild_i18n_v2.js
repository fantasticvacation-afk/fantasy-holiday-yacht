/**
 * rebuild_i18n.js v2
 * 重新生成 i18n.js，确保所有 data-i18n key 都有对应的翻译条目
 * 使用正则表达式，不依赖外部库
 */

const fs = require('fs');
const path = require('path');
const { translate } = require('./translate_dict');

const HTML_DIR = __dirname;
const i18nPath = path.join(HTML_DIR, 'i18n.js');

// 1. 从现有 i18n.js 中读取已有翻译
let i18nContent = fs.readFileSync(i18nPath, 'utf8');

// 提取 dict 对象
const dictMatch = i18nContent.match(/var dict = (\{[\s\S]*?\}\n\});/);
if (!dictMatch) {
  console.error('无法解析 i18n.js');
  process.exit(1);
}

let dict;
eval('dict = ' + dictMatch[1]);

console.log(`现有翻译条目: ${Object.keys(dict).length}`);

// 2. 扫描所有 HTML 文件，收集 data-i18n key 和中文
const htmlFiles = fs.readdirSync(HTML_DIR).filter(f => f.endsWith('.html'));
let allKeys = new Set();
let keyToZh = {};

for (const file of htmlFiles) {
  const filePath = path.join(HTML_DIR, file);
  const content = fs.readFileSync(filePath, 'utf8');
  
  // 正则：匹配 data-i18n="key" ... >文字<  （简化版，可能不完美）
  const regex = /data-i18n="([^"]+)"[^>]*>([^<]+)</g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    const key = match[1];
    let text = match[2].trim();
    if (text && text.length > 0) {
      allKeys.add(key);
      if (!keyToZh[key] || keyToZh[key].length < text.length) {
        keyToZh[key] = text;
      }
    }
  }
}

console.log(`找到 ${allKeys.size} 个唯一的 data-i18n key`);

// 3. 为每个 key 添加翻译（如果不存在）
let added = 0;
for (const key of allKeys) {
  if (dict[key]) continue; // 已有翻译，跳过
  
  const zh = keyToZh[key] || key;
  let en = translate(zh);
  
  // 如果翻译失败，用中文
  if (en === zh) {
    en = zh;
  }
  
  dict[key] = { zh, en };
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
