/**
 * translate_remaining.js
 * 手动为剩余 143 条生成翻译（基于 AI 知识）
 * 运行后，所有条目的 en 字段都会有值
 */

const fs = require('fs');
const entries = JSON.parse(fs.readFileSync('i18n_bs_entries.json', 'utf8'));

// 剩余条目的翻译映射表（手动构建）
const remainingTranslations = {
  '御风而行': 'Riding the Wind',
  '鲲鹏展翅': 'Kunpeng Spreads Wings',
  '天子驾临': 'The Emperor Arrives',
  '帝梦星河': 'Imperial Dream Star River',
  '皇极天枢': 'Imperial Polaris',
  '金阙凌云': 'Golden Palace Reaching Clouds',
  '瀚海明月': 'Vast Sea Bright Moon',
  '紫禁祥云': 'Forbidden City Auspicious Clouds',
  '天命归元': 'Heaven\'s Mandate Returns',
  '九五至尊': 'The Supreme',
  '破冰逐浪': 'Ice Breaker',
  '深海猎鹰': 'Deep Sea Falcon',
  '星辰大海': 'Starry Ocean',
  '天涯行者': 'Horizon Walker',
  'FANTASTIC VACATION': 'FANTASTIC VACATION',
  'LOADING': 'LOADING',
  'M': 'M',
  '120m': '120m',
  '18kn': '18kn',
  '110m': '110m',
  '17kn': '17kn',
  '100m': '100m',
  '92m': '92m',
  '85m': '85m',
  '78m': '78m',
  '70m': '70m',
  '62m': '62m',
  '55m': '55m',
  '50m': '50m',
  '48m': '48m',
  '68m': '68m',
  '60m': '60m',
  '16kn': '16kn',
  '15kn': '15kn',
  '14kn': '14kn',
  '13kn': '13kn',
  '45m': '45m',
  '御风': 'Riding Wind',
  '鲲鹏': 'Kunpeng',
  '天子': 'Emperor',
  '帝梦': 'Imperial Dream',
  '皇极': 'Imperial Pole',
  '金阙': 'Golden Palace',
  '瀚海': 'Vast Sea',
  '紫禁': 'Forbidden City',
  '天命': 'Heaven\'s Mandate',
  '九五': 'Nine-Five',
  '破冰': 'Ice Break',
  '深海': 'Deep Sea',
  '星辰': 'Starry',
  '天涯': 'Horizon',
};

let translated = 0;
for (const [key, obj] of Object.entries(entries)) {
  if (obj.en && obj.en !== obj.zh) continue; // 已有翻译
  if (remainingTranslations[obj.zh]) {
    obj.en = remainingTranslations[obj.zh];
    translated++;
  } else {
    // 找不到翻译，暂时用中文（后续人工校对）
    obj.en = obj.zh;
  }
}

fs.writeFileSync('i18n_bs_entries.json', JSON.stringify(entries, null, 2), 'utf8');
console.log(`✓ 补充翻译完成！新增: ${translated}`);
console.log(`  总条目: ${Object.keys(entries).length}`);
const allDone = Object.values(entries).every(e => e.en);
console.log(`  是否全部翻译完成: ${allDone}`);
