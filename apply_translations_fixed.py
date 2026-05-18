#!/usr/bin/env python3
"""正确应用翻译到 i18n.js（修复引号转义问题）"""
import json, re, subprocess

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

def escape_js_string(s):
    """正确转义 JavaScript 字符串"""
    if not s:
        return ''
    # 转义反斜杠和引号
    s = s.replace('\\', '\\\\')  # 反斜杠
    s = s.replace('"', '\\"')    # 双引号
    s = s.replace('\n', '\\n')   # 换行
    s = s.replace('\r', '\\r')   # 回车
    s = s.replace('\t', '\\t')   # 制表符
    return s

def apply_translations():
    print('\n=== 正确应用翻译 ===\n')
    
    # 读取翻译进度
    try:
        with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
            progress = json.load(f)
        print(f'加载翻译进度: {len(progress)} 条')
    except Exception as e:
        print(f'读取进度文件失败: {e}')
        return False
    
    # 读取 i18n.js
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'i18n.js 大小: {len(content)} 字符\n')
    
    # 应用翻译
    applied = 0
    errors = []
    
    for i, (key, en) in enumerate(progress.items()):
        if not en or not isinstance(en, str):
            continue
        
        # 转义英文翻译
        en_escaped = escape_js_string(en)
        
        # 构建正则表达式（匹配 "key": { "zh": "...", "en": "..." }）
        # 使用非贪婪匹配
        key_escaped = re.escape(key)
        pattern = rf'("{key_escaped}"\s*:\s*\{{[^}}]*"en"\s*:\s*"[^"]*"[^}}]*\}})'
        
        # 替换为新的 en 值
        replacement = f'"{key}": {{ "zh": "{progress.get(key + "_zh", "")}", "en": "{en_escaped}" }}'
        
        # 尝试替换
        new_content = re.sub(pattern, replacement, content, count=1)
        
        if new_content != content:
            content = new_content
            applied += 1
        
        if (i + 1) % 500 == 0:
            print(f'  处理中: {i+1}/{len(progress)}')
    
    print(f'\n成功应用: {applied} 条\n')
    
    # 写回文件
    with open(I18N_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'已写入: {I18N_PATH}')
    
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
        
        # 尝试修复：找到错误行
        error_line = None
        for line in result.stderr.split('\n'):
            if '.js:' in line:
                match = re.search(r'\.js:(\d+)", line)
                if match:
                    error_line = int(match.group(1))
                    break
        
        if error_line:
            print(f'\n错误在第 {error_line} 行附近')
            lines = content.split('\n')
            if error_line <= len(lines):
                print(f'问题代码:\n{lines[error_line-2:error_line+2]}')
        
        return False

if __name__ == '__main__':
    success = apply_translations()
    if not success:
        print('\n❌ 应用翻译失败，请检查错误信息')
    else:
        print('\n✅ 翻译应用成功!')