#!/usr/bin/env python3
/**
 * translate_all_remaining.py
 * 翻译 i18n.js 中所有未翻译的条目（zh === en）
 * 使用 deep-translator (Google Translator)
 * 支持断点续传和批量翻译
 */

const fs = require('fs');
const { execSync } = require('child_process');

// 配置
const BATCH_SIZE = 100; // 每批翻译数量
const DELAY_BETWEEN_BATCHES = 3000; // 批次间延迟（ms，避免速率限制）

// 文件路径
const i18nPath = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js';
const progressPath = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n_progress.json';
const scriptPath = '/Users/hs/.qclaw/workspace/fh-yacht-site/translate_batch.py';

// 读取 i18n.js
let content = fs.readFileSync(i18nPath, 'utf8');

// 提取所有条目
const entryRegex = /"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"\s*\}/g;

const entries = [];
let match;
while ((match = entryRegex.exec(content)) !== null) {
  const key = match[1];
  const zh = match[2];
  const en = match[3];
  entries.append({ key, zh, en, is_untranslated: zh === en && zh !== '' });
}

console.log('\n=== i18n 翻译状态 ===');
console.log(`总条目数: ${entries.length}`);
const untranslated = entries.filter(e => e.is_untranslated);
console.log(`未翻译: ${untranslated.length}`);
console.log(`已翻译: ${entries.length - untranslated.length}`);

if (untranslated.length === 0) {
  console.log('\n✅ 所有条目已翻译！');
  process.exit(0);
}

// 读取进度
let translatedDict = {};
if (fs.existsSync(progressPath)) {
  try {
    translatedDict = JSON.parse(fs.readFileSync(progressPath, 'utf8'));
    console.log(`\n发现进度文件，已翻译: ${Object.keys(translatedDict).length} 条`);
  } catch (e) {
    console.log('\n进度文件损坏，从头开始');
  }
}

// 过滤掉已翻译的
const remaining = untranslated.filter(e => !translatedDict[e.key]);
console.log(`剩余待翻译: ${remaining.length} 条`);

if (remaining.length === 0) {
  console.log('\n✅ 所有条目已从进度文件恢复！');
  updateI18nFile(translatedDict);
  process.exit(0);
}

// 分批
const batches = [];
for (let i = 0; i < remaining.length; i += BATCH_SIZE) {
  batches.push(remaining.slice(i, i + BATCH_SIZE));
}

console.log(`\n=== 开始翻译 ===`);
console.log(`总批次数: ${batches.length}`);
console.log(`批次大小: ${BATCH_SIZE}`);
console.log(`预计时间: ~${Math.ceil(batches.length * DELAY_BETWEEN_BATCHES / 1000 / 60)} 分钟`);

// 生成 Python 脚本（用于批量翻译）
const pythonScript = `
import json
import sys
from deep_translator import GoogleTranslator

def translate_batch(texts):
    try:
        translator = GoogleTranslator(source='zh-CN', target='en')
        return translator.translate_batch(texts)
    except Exception as e:
        print(f"Batch translation failed: {e}", file=sys.stderr)
        return None

if __name__ == '__main__':
    data = json.loads(sys.stdin.read())
    texts = data['texts']
    keys = data['keys']
    
    results = translate_batch(texts)
    if results:
        output = {keys[i]: results[i] for i in range(len(keys))}
        print(json.dumps(output, ensure_ascii=False))
    else:
        sys.exit(1)
`;

fs.writeFileSync(scriptPath, pythonScript);

// 翻译批次
(async () => {
  let processedCount = Object.keys(translatedDict).length;
  
  for (let i = 0; i < batches.length; i++) {
    const batch = batches[i];
    console.log(`\n[批次 ${i + 1}/${batches.length}] 翻译 ${batch.length} 条...`);
    
    // 准备数据
    const texts = batch.map(e => e.zh);
    const keys = batch.map(e => e.key);
    const inputData = JSON.stringify({ texts, keys });
    
    try {
      // 调用 Python 脚本
      const stdout = execSync(`python3 "${scriptPath}"`, {
        input: inputData,
        encoding: 'utf8',
        timeout: 60000 // 60秒超时
      });
      
      const batchResults = JSON.parse(stdout);
      
      // 更新翻译字典
      for (const [key, en] of Object.entries(batchResults)) {
        translatedDict[key] = en;
      }
      
      processedCount += Object.keys(batchResults).length;
      console.log(`  ✓ 完成 ${Object.keys(batchResults).length} 条 (总计: ${processedCount})`);
      
      // 保存进度
      console.log('  保存进度...');
      fs.writeFileSync(progressPath, JSON.stringify(translatedDict, null, 2), 'utf8');
      
      // 批次间延迟
      if (i < batches.length - 1) {
        console.log(`  等待 ${DELAY_BETWEEN_BATCHES}ms...`);
        await new Promise(resolve => setTimeout(resolve, DELAY_BETWEEN_BATCHES));
      }
    } catch (err) {
      console.error(`  ✗ 批次 ${i + 1} 失败: ${err.message}`);
      console.log('  保存当前进度并继续...');
      fs.writeFileSync(progressPath, JSON.stringify(translatedDict, null, 2), 'utf8');
    }
  }
  
  // 最终保存
  console.log('\n=== 更新 i18n.js ===');
  updateI18nFile(translatedDict);
  
  console.log('\n✅ 翻译完成！');
  console.log(`  翻译了 ${Object.keys(translatedDict).length} 条`);
  console.log(`  保存至: ${i18nPath}`);
  
  // 验证语法
  try {
    execSync(`node -c "${i18nPath}"`, { stdio: 'inherit' });
    console.log('✓ 语法检查通过');
  } catch (e) {
    console.error('✗ 语法错误，请检查');
  }
  
  // 删除进度文件和临时脚本
  if (fs.existsSync(progressPath)) {
    fs.unlinkSync(progressPath);
    console.log('✓ 进度文件已删除');
  }
  if (fs.existsSync(scriptPath)) {
    fs.unlinkSync(scriptPath);
    console.log('✓ 临时脚本已删除');
  }
})();

// 更新 i18n.js 文件
function updateI18nFile(dict) {
  let newContent = fs.readFileSync(i18nPath, 'utf8');
  
  for (const [key, en] of Object.entries(dict)) {
    const entry = entries.find(e => e.key === key);
    if (!entry) continue;
    
    const oldEntry = `"${key}": { "zh": "${entry.zh}", "en": "${entry.zh}" }`;
    const newEntry = `"${key}": { "zh": "${entry.zh}", "en": "${en}" }`;
    newContent = newContent.replace(oldEntry, newEntry);
  }
  
  fs.writeFileSync(i18nPath, newContent, 'utf8');
}
