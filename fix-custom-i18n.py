#!/usr/bin/env python3
"""修复 custom.html 页面的 i18n 英文翻译 - 安全版本"""
import re

with open('i18n.js', 'r') as f:
    content = f.read()

# 需要修复的键: key -> (new_zh, new_en)
# 对于含HTML的值，JSON中需要转义双引号
fixes = {
    # 标题 (h3标签，包含span子元素) - HTML属性中的双引号需转义
    'custom.540': ('<span class=\\"dim-num\\">1</span> 外观定制', '<span class=\\"dim-num\\">1</span> Exterior Customization'),
    'custom.557': ('<span class=\\"dim-num\\">2</span> 内饰定制', '<span class=\\"dim-num\\">2</span> Interior Customization'),
    'custom.573': ('<span class=\\"dim-num\\">3</span> 功能定制', '<span class=\\"dim-num\\">3</span> Functional Customization'),
    'custom.589': ('<span class=\\"dim-num\\">4</span> 增值服务定制', '<span class=\\"dim-num\\">4</span> Value-Added Services'),
    # 外观定制标签
    'custom.545': ('船体线条优化', 'Hull line optimization'),
    'custom.546': ('专属配色方案', 'Exclusive color scheme'),
    'custom.547': ('品牌标识定制', 'Brand identity customization'),
    'custom.548': ('船名雕刻艺术', 'Ship name engraving art'),
    'custom.549': ('特殊涂装工艺', 'Special coating process'),
    'custom.550': ('LED动态灯效', 'LED dynamic lighting effects'),
    # 内饰定制标签
    'custom.562': ('东方美学/现代极简/复古奢华', 'Oriental aesthetics/modern minimalist/retro luxury'),
    'custom.563': ('健身房/影音室/SPA房', 'Gym/video room/SPA room'),
    'custom.564': ('家具软装全套定制', 'Full set of customized furniture and furnishings'),
    'custom.565': ('灯光氛围系统', 'Lighting atmosphere system'),
    'custom.566': ('艺术品陈设搭配', 'Art display matching'),
    # 功能定制标签
    'custom.578': ('航速与动力系统优化', 'Speed and power system optimization'),
    'custom.579': ('全屋智能中控系统', 'Whole house intelligent central control system'),
    'custom.580': ('卫星通信与联网', 'Satellite communication and networking'),
    'custom.581': ('海钓平台/潜水装备舱', 'Fishing platform/diving equipment cabin'),
    'custom.582': ('直升机起降平台', 'Helicopter landing platform'),
    # 增值服务标签
    'custom.594': ('专属管家全天候服务', 'Dedicated butler service around the clock'),
    'custom.595': ('米其林主厨定制菜单', 'Michelin chef customized menu'),
    'custom.596': ('私人航线规划设计', 'Private route planning and design'),
    'custom.597': ('全球港口VIP停靠', 'VIP docking at global ports'),
    'custom.598': ('会员制特权礼遇', 'Membership privileges'),
    # 空英文值 - 不含引号的文本
    'custom.960': ('\u300c探索全球，不负假期\u300d', 'Explore the Globe, Make Every Vacation Count'),
}

count = 0
for key, (new_zh, new_en) in fixes.items():
    old = f'"{key}": {{'
    idx = content.find(old)
    if idx < 0:
        print(f"NOT FOUND: {key}")
        continue
    
    start = idx
    brace_start = content.find('{', start)
    depth = 0
    end = brace_start
    for i in range(brace_start, len(content)):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    
    old_entry = content[start:end]
    new_entry = f'"{key}": {{ "zh": "{new_zh}", "en": "{new_en}" }}'
    content = content[:start] + new_entry + content[end:]
    count += 1
    print(f"OK: {key}")

print(f"\n共替换 {count} 个键")

with open('i18n.js', 'w') as f:
    f.write(content)

import subprocess
result = subprocess.run(['node', '--check', 'i18n.js'], capture_output=True, text=True)
if result.returncode == 0:
    print("✓ i18n.js 语法检查通过")
else:
    print(f"✗ 语法错误:\n{result.stderr[:500]}")
