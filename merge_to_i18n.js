/**
 * merge_to_i18n.js
 * 把 i18n_bs_entries.json (yachts.html) 合并到 i18n.js
 */

const fs = require('fs');

// 读取现有 i18n.js（它是一个 JS 文件，需要特殊处理）
let i18nContent = fs.readFileSync('i18n.js', 'utf8');

// 提取现有的翻译词典（const dict = {...}）
const dictMatch = i18nContent.match(/const dict = (\{[\s\S]*\});/);
if (!dictMatch) {
  console.error('无法解析 i18n.js 中的 dict 对象');
  process.exit(1);
}

let dict;
eval('dict = ' + dictMatch[1]); // 安全地解析 dict 对象

// 读取 yachts.html 的翻译
const yachtsEntries = JSON.parse(fs.readFileSync('i18n_bs_entries.json', 'utf8'));

// 合并（如果 key 已存在，跳过；否则添加）
let added = 0, skipped = 0;
for (const [key, obj] of Object.entries(yachtsEntries)) {
  if (dict[key]) {
    skipped++; // 已存在，跳过
  } else {
    dict[key] = { zh: obj.zh, en: obj.en };
    added++;
  }
}

// 重新生成 i18n.js 内容
const newDictStr = JSON.stringify(dict, null, 2)
  .replace(/"([^"]+)":/g, '$1:') // 去掉 key 的引号（JS 对象格式）
  .replace(/"/g, '\'') // 字符串用单引号（可选）
  ;

// 更安全的做法：直接生成 JS 对象字符串
let dictJS = 'const dict = {\n';
for (const [key, val] of Object.entries(dict)) {
  dictJS += `  "${key}": { zh: "${val.zh.replace(/"/g, '\\"')}", en: "${val.en.replace(/"/g, '\\"')}" },\n`;
}
dictJS += '};\n';

// 替换 i18n.js 中的 dict 部分
const newContent = i18nContent.replace(/const dict = \{[\s\S]*\};/, dictJS);

fs.writeFileSync('i18n.js', newContent, 'utf8');

console.log(`✓ 合并完成！`);
console.log(`  从 i18n_bs_entries.json 添加: ${added}`);
console.log(`  跳过(已存在): ${skipped}`);
console.log(`  i18n.js 总条目: ${Object.keys(dict).length}`);
