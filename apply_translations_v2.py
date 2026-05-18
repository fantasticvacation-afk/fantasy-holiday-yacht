#!/usr/bin/env python3
"""正确应用翻译到 i18n.js - 简化版"""
import json, re, subprocess

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

def escape_js_string(s):
    """正确转义 JavaScript 字符串中的特殊字符"""
    if not s or not isinstance(s, str):
        return ''
    # 顺序很重要：先转义反斜杠，再转义其他
    s = s.replace('\\', '\\\\')  # 反斜杠必须第一个处理
    s = s.replace('"', '\\"')    # 双引号
    s = s.replace('\n', '\\n')   # 换行符
    s = s.replace('\r', '\\r')   # 回车符
    s = s.replace('\t', '\\t')   # 制表符
    return s

def main():
    print('\n=== 应用翻译 v2 ===\n')
    
    # 读取翻译进度
    try:
        with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
            progress = json.load(f)
        print(f'✓ 加载翻译进度: {len(progress)} 条')
    except Exception as e:
        print(f'✗ 读取进度文件失败: {e}')
        return False
    
    # 读取 i18n.js
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f'✓ 读取 i18n.js: {len(lines)} 行\n')
    
    # 逐行处理
    applied = 0
    errors = []
    
    for i, line in enumerate(lines):
        # 匹配模式: "key": { "zh": "...", "en": "..." }
        match = re.match(r'\s*"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"\s*\},?', line)
        
        if match:
            key = match.group(1)
            
            # 如果这个 key 有翻译
            if key in progress:
                en_new = progress[key]
                
                # 转义英文翻译
                en_escaped = escape_js_string(en_new)
                
                # 重建这一行
                indent = line[:len(line) - len(line.lstrip())]
                new_line = f'{indent}"{key}": {{ "zh": "{match.group(2)}", "en": "{en_escaped}" }},\n'
                
                lines[i] = new_line
                applied += 1
        
        # 进度提示
        if (i + 1) % 5000 == 0:
            print(f'  处理: {i+1}/{len(lines)} 行')
    
    print(f'\n✓ 应用翻译: {applied} 条')
    
    # 写回文件
    with open(I18N_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f'✓ 写入文件: {I18N_PATH}')
    
    # 验证语法
    print('\n验证 JavaScript 语法...')
    result = subprocess.run(
        ['node', '-c', I18N_PATH],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print('✅ 语法检查通过!')
        return True
    else:
        print(f'❌ 语法错误:\n{result.stderr}')
        
        # 找到错误行
        error_line = None
        for line in result.stderr.split('\n'):
            if '.js:' in line:
                match = re.search(r'\.js:(\d+)', line)
                if match:
                    error_line = int(match.group(1))
                    break
        
        if error_line and error_line <= len(lines):
            print(f'\n错误在第 {error_line} 行:')
            start = max(0, error_line - 3)
            end = min(len(lines), error_line + 2)
            for j in range(start, end):
                marker = '>>>' if j == error_line - 1 else '   '
                print(f'{marker} {j+1}: {lines[j].rstrip()}')
        
        return False

if __name__ == '__main__':
    success = main()
    if not success:
        print('\n❌ 应用翻译失败')
    else:
        print('\n✅ 翻译应用成功!')