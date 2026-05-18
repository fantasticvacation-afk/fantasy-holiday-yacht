// translate_simple.js
// 简单直接的翻译脚本：逐条翻译，立即输出进度

const fs = require('fs');
const https = require('https');

const INPUT_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/untranslated.json';
const OUTPUT_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translations.json';
const PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json';

// 读取未翻译条目
const untranslated = JSON.parse(fs.readFileSync(INPUT_PATH, 'utf8'));
console.log(`\n=== 开始翻译 ===`);
console.log(`总数: ${untranslated.length}`);

// 读取进度
let translations = {};
if (fs.existsSync(PROGRESS_PATH)) {
  try {
    translations = JSON.parse(fs.readFileSync(PROGRESS_PATH, 'utf8'));
    console.log(`发现进度: ${Object.keys(translations).length} 条已翻译`);
  } catch (e) {
    console.log('进度文件损坏，从头开始');
  }
}

// 过滤已翻译
const remaining = untranslated.filter(e => !translations[e.key]);
console.log(`剩余: ${remaining.length} 条\n`);

if (remaining.length === 0) {
  console.log('✅ 所有条目已翻译！');
  process.exit(0);
}

// 使用 Google Translate 免费 API（无 key 版本）
function translateText(text) {
  return new Promise((resolve, reject) => {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q=${encodeURIComponent(text)}`;
    
    https.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          const translation = result[0][0][0];
          resolve(translation);
        } catch (e) {
          reject(new Error('解析失败'));
        }
      });
    }).on('error', (err) => {
      reject(err);
    });
  });
}

// 主函数
(async () => {
  const BATCH_SIZE = 10;
  const DELAY = 1000; // 1秒延迟
  
  for (let i = 0; i < remaining.length; i += BATCH_SIZE) {
    const batch = remaining.slice(i, i + BATCH_SIZE);
    console.log(`[${Math.floor(i/BATCH_SIZE) + 1}/${Math.ceil(remaining.length/BATCH_SIZE)}] 批次 ${i+1}-${i+batch.length}...`);
    
    for (const entry of batch) {
      try {
        process.stdout.write(`  ${entry.key}: `);
        const en = await translateText(entry.zh);
        translations[entry.key] = en;
        process.stdout.write(`✓ ${en.substring(0, 50)}\n`);
        
        // 每个条目后延迟
        await new Promise(resolve => setTimeout(resolve, DELAY));
      } catch (err) {
        process.stdout.write(`✗ 失败\n`);
        translations[entry.key] = entry.zh; // 失败时保留中文
      }
    }
    
    // 保存进度
    console.log(`  保存进度... (${Object.keys(translations).length}/${untranslated.length})`);
    fs.writeFileSync(PROGRESS_PATH, JSON.stringify(translations, null, 2), 'utf8');
    
    // 批次间延迟
    if (i + BATCH_SIZE < remaining.length) {
      console.log(`  等待 3 秒...\n`);
      await new Promise(resolve => setTimeout(resolve, 3000));
    }
  }
  
  // 保存最终结果
  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(translations, null, 2), 'utf8');
  console.log(`\n✅ 翻译完成！`);
  console.log(`  翻译了 ${Object.keys(translations).length} 条`);
  console.log(`  保存至: ${OUTPUT_PATH}`);
  
  // 删除进度文件
  if (fs.existsSync(PROGRESS_PATH)) {
    fs.unlinkSync(PROGRESS_PATH);
    console.log('✓ 进度文件已删除');
  }
})();
