#!/usr/bin/env python3
"""应用翻译进度到 i18n.js - 正确版本"""
import json
import re
import subprocess

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

def escape_js(s):
    """转义 JavaScript 字符串"""
    if not s or not isinstance(s, str):
        return ''
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    s = s.replace('\t', '\\t')
    return s

def main():
    print('\n=== 应用翻译 v3 ===\n')
    
    # 加载翻译进度
    try:
        with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
            progress = json.load(f)
        print(f'✓ 加载 {len(progress)} 条翻译')
    except Exception as e:
        print(f'✗ 失败: {e}')
        return False
    
    # 读取 i18n.js
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'✓ 读取 i18n.js ({len(content)} 字符)\n')
    
    # 逐条替换
    applied = 0
    for key, en in progress.items():
        if not en or not isinstance(en, str):
            continue
        
        en_escaped = escape_js(en)
        
        # 构建查找和替换模式
        # 查找: "key": { "zh": "...", "en": "..." }
        key_escaped = re.escape(key)
        pattern = r'("' + key_escaped + r'"\s*:\s*\{\s*"zh"\s*:\s*"[^"]*",\s*"en"\s*:\s*")([^"]*?)("\s*\})'
        
        replacement = r'\1' + en_escaped + r'\3'
        
        new_content, n = re.subn(pattern, replacement, content)
        if n > 0:
            content = new_content
            applied += 1
        
        if (applied) % 500 == 0:
            print(f'  处理: {applied}/{len(progress)}')
    
    print(f'\n✓ 应用: {applied} 条\n')
    
    # 写回
    with open(I18N_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
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
        for line in result.stderr.split('\n'):
            if 'i18n.js:' in line:
                match = re.search(r'i18n\.js:(\d+)', line)
                if match:
                    error_line = int(match.group(1))
                    lines = content.split('\n')
                    if 0 < error_line <= len(lines):
                        print(f'\n错误在第 {error_line} 行:')
                        start = max(0, error_line - 3)
                        end = min(len(lines), error_line + 2)
                        for j in range(start, end):
                            marker = '>>>' if j == error_line - 1 else '   '
                            print(f'{marker} {j+1}: {lines[j][:100]}')
                break
        
        return False

if __name__ == '__main__':
    success = main()
    if success:
        print('\n🎉 完成!')
    else:
        print('\n❌ 失败')