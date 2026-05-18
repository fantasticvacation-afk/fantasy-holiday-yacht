/**
 * translate_remaining.js
 * 翻译 i18n.js 中剩余未翻译的条目（en === zh 的条目）
 * 使用 translate-google 库，带延迟以避免速率限制
 */

const fs = require('fs');
const { translate } = require('translate-google');

// 读取 i18n.js
const i18nPath = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js';
let content = fs.readFileSync(i18nPath, 'utf8');

// 提取所有条目
const entryRegex = /"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"\s*\}/g;

const entries = [];
let match;
while ((match = entryRegex.exec(content)) !== null) {
  const key = match[1];
  const zh = match[2];
  const en = match[3];
  entries.push({ key, zh, en, isUntranslated: zh === en });
}

console.log(`总条目数: ${entries.length}`);
const untranslated = entries.filter(e => e.isUntranslated);
console.log(`未翻译条目: ${untranslated.length}`);

// 优先翻译重要页面的条目
const priorityPrefixes = ['index.', 'about.', 'yachts.', 'contact.', 'news.'];
const priorityUntranslated = untranslated.filter(e => 
  priorityPrefixes.some(prefix => e.key.startsWith(prefix))
);
console.log(`优先翻译（重要页面）: ${priorityUntranslated.length} 条`);

// 翻译函数（带延迟）
async function translateEntries(entriesToTranslate) {
  const results = [];
  
  for (let i = 0; i < entriesToTranslate.length; i++) {
    const entry = entriesToTranslate[i];
    
    // 跳过空字符串
    if (!entry.zh || entry.zh.trim() === '') {
      results.push({ key: entry.key, zh: entry.zh, en: entry.zh });
      continue;
    }
    
    try {
      console.log(`[${i+1}/${entriesToTranslate.length}] 翻译: ${entry.zh.substring(0, 30)}...`);
      const res = await translate(entry.zh, { from: 'zh-CN', to: 'en' });
      results.push({ key: entry.key, zh: entry.zh, en: res.text });
      
      // 延迟 500ms 避免速率限制
      if (i < entriesToTranslate.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 500));
      }
    } catch (err) {
      console.error(`  翻译失败: ${entry.key} - ${err.message}`);
      results.push({ key: entry.key, zh: entry.zh, en: entry.zh }); // 失败时保留中文
    }
  }
  
  return results;
}

// 主函数
(async () => {
  console.log('\n开始翻译优先条目...');
  const translated = await translateEntries(priorityUntranslated);
  
  console.log('\n更新 i18n.js...');
  
  // 构建翻译字典
  const translatedDict = {};
  for (const t of translated) {
    translatedDict[t.key] = t.en;
  }
  
  // 替换 i18n.js 中的条目
  let newContent = content;
  for (const [key, en] of Object.entries(translatedDict)) {
    const zh = entries.find(e => e.key === key).zh;
    const oldEntry = `"${key}": { "zh": "${zh}", "en": "${zh}" }`;
    const newEntry = `"${key}": { "zh": "${zh}", "en": "${en}" }`;
    newContent = newContent.replace(oldEntry, newEntry);
  }
  
  // 保存
  fs.writeFileSync(i18nPath, newContent, 'utf8');
  
  console.log(`\n✓ 完成！翻译了 ${translated.length} 条`);
  console.log(`  保存至: ${i18nPath}`);
  
  // 验证语法
  try {
    require('child_process').execSync(`node -c "${i18nPath}"`, { stdio: 'inherit' });
    console.log('✓ 语法检查通过');
  } catch (e) {
    console.error('✗ 语法错误，请检查');
  }
})();
