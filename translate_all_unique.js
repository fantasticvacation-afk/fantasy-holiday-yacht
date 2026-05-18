/**
 * translate_all_unique.js
 * 翻译 all_unique_texts.json 中的 3727 条短语，生成 i18n 条目
 */

const fs = require('fs');
const { translate } = require('./translate_dict');

// 读取所有唯一短语
const uniqueTexts = JSON.parse(fs.readFileSync('all_unique_texts.json', 'utf8'));

console.log(`开始翻译 ${uniqueTexts.length} 条唯一短语...`);

const entries = {};
let translated = 0, untranslated = 0;

for (let i = 0; i < uniqueTexts.length; i++) {
  const zh = uniqueTexts[i];
  if (!zh || typeof zh !== 'string') continue;
  
  const en = translate(zh);
  
  // 生成 key（用前缀 + 索引）
  const key = `auto.${i}`;
  
  if (en !== zh) {
    entries[key] = { zh, en };
    translated++;
  } else {
    // 翻译失败，暂时用中文
    entries[key] = { zh, en: zh };
    untranslated++;
  }
}

// 保存翻译结果
fs.writeFileSync('all_unique_texts_translated.json', JSON.stringify(entries, null, 2), 'utf8');

console.log(`✓ 翻译完成！`);
console.log(`  成功翻译: ${translated}`);
console.log(`  未翻译(保留中文): ${untranslated}`);
console.log(`  结果已保存到 all_unique_texts_translated.json`);
