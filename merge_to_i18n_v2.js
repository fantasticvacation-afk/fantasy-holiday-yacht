/**
 * merge_to_i18n_v2.js
 * 正确合并 i18n_bs_entries.json 到 i18n.js
 */

const fs = require('fs');

// 读取 i18n.js
let i18nContent = fs.readFileSync('i18n.js', 'utf8');

// 读取 yachts.html 的翻译
const yachtsEntries = JSON.parse(fs.readFileSync('i18n_bs_entries.json', 'utf8'));

// 生成要插入的条目字符串
let newEntries = '';
for (const [key, obj] of Object.entries(yachtsEntries)) {
  // 转义双引号
  const zh = obj.zh.replace(/"/g, '\\"');
  const en = (obj.en || obj.zh).replace(/"/g, '\\"');
  newEntries += `  "${key}": { "zh": "${zh}", "en": "${en}" },\n`;
}

// 找到 dict 对象的 closing `};` 位置
// 策略：找到第一个 `function switchLang` 或 `function updateI18n` 前面的 `};`
const lines = i18nContent.split('\n');
let insertPos = -1;
let braceCount = 0;
let inDict = false;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line.includes('var dict = {')) {
    inDict = true;
    braceCount = 1;
    continue;
  }
  if (inDict) {
    // 计算大括号
    for (const ch of line) {
      if (ch === '{') braceCount++;
      if (ch === '}') braceCount--;
    }
    if (braceCount === 0) {
      // 找到了 dict 的结束位置
      insertPos = i;
      break;
    }
  }
}

if (insertPos === -1) {
  console.error('无法找到 dict 对象的结束位置');
  process.exit(1);
}

// 在 dict 结束前插入新条目（替换最后一行的 `};`）
lines[insertPos] = lines[insertPos].replace('};', ',');
const result = lines.slice(0, insertPos + 1).join('\n') + '\n' + newEntries + '};\n' + lines.slice(insertPos + 1).join('\n');

fs.writeFileSync('i18n.js', result, 'utf8');

console.log(`✓ 合并完成！`);
console.log(`  插入了 ${Object.keys(yachtsEntries).length} 条翻译`);
console.log(`  i18n.js 已更新`);
