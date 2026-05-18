/**
 * apply_translate_dict.js
 * 使用 translate_dict.js 翻译 i18n_bs_entries.json 中的未翻译条目
 */

const fs = require('fs');
const { translate } = require('./translate_dict');

// 读取待翻译条目
const entries = JSON.parse(fs.readFileSync('i18n_bs_entries.json', 'utf8'));
const keys = Object.keys(entries);

let translated = 0, skipped = 0;

for (const key of keys) {
  const obj = entries[key];
  if (!obj || !obj.zh) continue;
  
  // 如果已经有英文翻译且不是中文，跳过
  if (obj.en && obj.en !== obj.zh && !obj.en.startsWith('__NEEDS')) {
    skipped++;
    continue;
  }
  
  // 使用词典翻译
  const en = translate(obj.zh);
  
  // 如果翻译结果和中文不同，说明翻译成功了
  if (en !== obj.zh) {
    obj.en = en;
    translated++;
  } else {
    // 翻译失败，保留中文（后续人工校对）
    obj.en = obj.zh;
  }
}

// 保存结果
fs.writeFileSync('i18n_bs_entries.json', JSON.stringify(entries, null, 2), 'utf8');

console.log(`✓ 翻译完成！`);
console.log(`  总条目: ${keys.length}`);
console.log(`  新增翻译: ${translated}`);
console.log(`  跳过(已有翻译): ${skipped}`);
console.log(`  未翻译(保留中文): ${keys.length - translated - skipped}`);
console.log(`  结果已保存到 i18n_bs_entries.json`);
