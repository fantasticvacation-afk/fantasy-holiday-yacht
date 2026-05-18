// extract_untranslated.js
// 提取 i18n.js 中未翻译的条目（zh === en）

const fs = require('fs');
const i18nPath = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js';
const outputPath = '/Users/hs/.qclaw/workspace/fh-yacht-site/untranslated.json';

const content = fs.readFileSync(i18nPath, 'utf8');

// 简单解析：逐行匹配
const untranslated = [];
const lines = content.split('\n');

for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trim();
  
  // 匹配模式: "key": { "zh": "text", "en": "text" }
  const match = line.match(/^"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"\s*\}/);
  
  if (match) {
    const key = match[1];
    const zh = match[2];
    const en = match[3];
    
    // 未翻译：zh === en 且 zh 不为空
    if (zh === en && zh !== '') {
      untranslated.push({ key, zh });
    }
  }
}

console.log(`未翻译条目: ${untranslated.length}`);
console.log('保存到:', outputPath);

fs.writeFileSync(outputPath, JSON.stringify(untranslated, null, 2), 'utf8');
console.log('✓ 完成');
