#!/usr/bin/env python3
"""安全应用翻译 - 解析并重建 i18n.js"""
import json
import re
import subprocess

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

def escape_js_string(s):
    """正确转义 JS 字符串"""
    if not s or not isinstance(s, str):
        return ''
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    s = s.replace('\t', '\\t')
    return s

def main():
    print('\n=== 安全应用翻译 ===\n')
    
    # 加载翻译
    try:
        with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
            progress = json.load(f)
        print(f'✓ 加载 {len(progress)} 条翻译')
    except Exception as e:
        print(f'✗ 失败: {e}')
        return False
    
    # 读取 i18n.js
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f'✓ 读取 {len(lines)} 行\n')
    
    # 处理每一行
    applied = 0
    new_lines = []
    
    for line in lines:
        # 匹配: "key": { "zh": "zh_val", "en": "en_val" },
        match = re.match(r'^(\s*)"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"\s*\},?\s*$', line)
        
        if match:
            indent = match.group(1)
            key = match.group(2)
            zh_val = match.group(3)
            
            # 如果有翻译，使用翻译后的 en 值
            if key in progress and progress[key]:
                en_new = escape_js_string(progress[key])
                new_line = f'{indent}"{key}": {{ "zh": "{zh_val}", "en": "{en_new}" }},\n'
                applied += 1
            else:
                # 保持原样
                new_line = line
        else:
            # 不是翻译行，保持原样
            new_line = line
        
        new_lines.append(new_line)
        
        if applied % 1000 == 0 and applied > 0:
            print(f'  处理: {applied} 条')
    
    print(f'\n✓ 应用: {applied} 条\n')
    
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
        return True
    else:
        print(f'❌ 语法错误:\n{result.stderr}')
        
        # 找到错误行
        for err_line in result.stderr.split('\n'):
            if 'i18n.js:' in err_line:
                match = re.search(r'i18n\.js:(\d+)', err_line)
                if match:
                    err_num = int(match.group(1))
                    print(f'\n错误在第 {err_num} 行:')
                    start = max(0, err_num - 3)
                    end = min(len(new_lines), err_num + 2)
                    for j in range(start, end):
                        marker = '>>>' if j == err_num - 1 else '   '
                        print(f'{marker} {j+1}: {new_lines[j].rstrip()[:120]}')
                break
        
        return False

if __name__ == '__main__':
    success = main()
    if success:
        print('\n🎉 完成!')
    else:
        print('\n❌ 需要修复')
        print('\n建议: 恢复备份后手动修复翻译脚本')