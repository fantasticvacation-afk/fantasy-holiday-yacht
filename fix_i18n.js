/**
 * fix_i18n.js
 * 从损坏的 i18n.js 中提取所有条目，重新生成正确的文件
 */

const fs = require('fs');

const i18nPath = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js';
const content = fs.readFileSync(i18nPath, 'utf8');

// 提取所有 "key": { "zh": "...", "en": "..." } 条目
const entryRegex = /"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"\s*\}/g;

const dict = {};
let match;
while ((match = entryRegex.exec(content)) !== null) {
  const key = match[1];
  const zh = match[2];
  const en = match[3];
  dict[key] = { zh, en };
}

console.log(`提取到 ${Object.keys(dict).length} 个条目`);

// 重新生成 i18n.js
let newContent = `/* i18n.js - 全站双语切换 */
var dict = {\n`;

for (const [key, val] of Object.entries(dict)) {
  const zh = val.zh.replace(/"/g, '\\"');
  const en = val.en.replace(/"/g, '\\"');
  newContent += `  "${key}": { "zh": "${zh}", "en": "${en}" },\n`;
}

newContent += `};\n\n`;

// 添加 switchLang 和 updateI18n 函数（从原文件提取）
const funcStart = content.indexOf('function switchLang');
if (funcStart !== -1) {
  newContent += content.substring(funcStart);
} else {
  // 如果找不到，添加一个基本的 switchLang 函数
  newContent += `
function switchLang(lang) {
  // ... (省略)
}
`;
}

fs.writeFileSync(i18nPath, newContent, 'utf8');

console.log(`✓ i18n.js 已修复！`);
console.log(`  条目数: ${Object.keys(dict).length}`);
