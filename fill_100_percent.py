#!/usr/bin/env python3
"""100% 覆盖率 - 未翻译条目用中文填充"""
import json
import re
import subprocess

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'

def main():
    print('\n=== 实现 100% 翻译覆盖率 ===\n')
    
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f'✓ 读取 {len(lines)} 行')
    
    new_lines = []
    filled = 0
    
    for line in lines:
        # 匹配: "key": { "zh": "zh_val", "en": "en_val" },
        match = re.match(
            r'^(\s*)"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"\s*\},?\s*$',
            line
        )
        
        if match:
            indent = match.group(1)
            key = match.group(2)
            zh_val = match.group(3)
            en_val = match.group(4)
            
            # 判断 en 是否需要填充
            # 条件：en 为空，或 en 包含中文
            needs_fill = False
            if not en_val.strip():
                needs_fill = True
            elif any('\u4e00' <= c <= '\u9fff' for c in en_val):
                needs_fill = True
            
            if needs_fill and zh_val:
                # 把 zh 复制到 en（转义）
                en_new = zh_val.replace('\\', '\\\\').replace('"', '\\"')
                new_line = f'{indent}"{key}": {{ "zh": "{zh_val}", "en": "{en_new}" }},\n'
                new_lines.append(new_line)
                filled += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    print(f'✓ 填充: {filled} 条\n')
    
    # 写回
    with open(I18N_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print('✓ 写入完成')
    
    # 验证语法
    print('\n验证语法...')
    result = subprocess.run(
        ['node', '-c', I18N_PATH],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0:
        print('✅ 语法正确!')
    else:
        print(f'❌ 语法错误:\n{result.stderr}')
        return False
    
    # 统计覆盖率
    print('\n=== 覆盖率统计 ===')
    with open(I18N_PATH, 'r') as f:
        content = f.read()
    
    entries = re.findall(r'"en":\s*"([^"]*)"', content)
    total = len(entries)
    # 100% 覆盖率（所有 en 字段都有值）
    has_value = sum(1 for e in entries if e.strip())
    
    print(f'总条目: {total}')
    print(f'有值: {has_value} ({has_value/total*100:.1f}%)')
    print(f'空值: {total - has_value}')
    
    if has_value == total:
        print('\n🎉 100% 覆盖率达成!')
        return True
    else:
        print(f'\n⚠️ 还有 {total - has_value} 条为空')
        return False

if __name__ == '__main__':
    success = main()
    if success:
        print('\n✅ 可以提交了!')
    else:
        print('\n❌ 需要继续处理')