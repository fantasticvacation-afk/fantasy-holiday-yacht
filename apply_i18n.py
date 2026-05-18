"""
apply_i18n.py
给指定 HTML 文件的所有文字元素自动加 data-i18n 属性
并生成带英文翻译的 i18n_dict 片段

策略：
  - 匹配常见标签：h1-h4, p, span, div, a, li, button 等
  - 跳过已有 data-i18n 的标签
  - 跳过 script/style/svg 内部
  - 为每段文字生成唯一 key
"""

import re, json, os, sys

def gen_key(prefix, counter):
    return f"{prefix}.{counter}"

def add_i18n_to_file(fpath, lang='zh'):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    base = os.path.splitext(os.path.basename(fpath))[0]
    translations = {}
    counter = [0]
    
    # 要处理的标签（有文字内容的）
    target_tags = r'h[1-6]|p|span|div|a|li|button|em|strong|small|label|option|td|th'
    
    def replacer(match):
        full_tag = match.group(0)
        tag = match.group(1)
        attrs = match.group(2) or ''
        inner = match.group(3)
        
        # 已有 data-i18n，跳过
        if 'data-i18n=' in attrs:
            return full_tag
        
        # 空内容或纯空白，跳过
        text = inner.strip()
        if not text or len(text) < 1:
            return full_tag
        
        # 跳过纯数字/符号
        if re.match(r'^[\d\s\.\-\+\(\)\/:]+$', text):
            return full_tag
        
        # 生成 key
        key = f"{base}.{counter[0]}"
        counter[0] += 1
        
        # 存入翻译词典
        translations[key] = {'zh': text, 'en': text}  # en 待翻译
        
        # 插入 data-i18n 属性（在 > 前）
        # 如果标签没有 > （已经是自闭合），跳过
        if '>' not in full_tag:
            return full_tag
        
        # 在标签的 > 前插入 data-i18n="key"
        # 处理形式：<tag attrs>inner</tag>
        new_attrs = attrs + f' data-i18n="{key}"'
        new_tag = f"<{tag}{new_attrs}>{inner}</{tag}>"
        return new_tag
    
    # 正则：匹配成对的标签
    pattern = re.compile(r'<(' + target_tags + r')([^>]*)>(.*?)</\1>', re.DOTALL)
    
    new_content = pattern.sub(replacer, content)
    
    # 写回文件
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return translations

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 apply_i18n.py index.html [page2.html ...]")
        sys.exit(1)
    
    all_trans = {}
    for fpath in sys.argv[1:]:
        print(f"处理: {fpath}")
        trans = add_i18n_to_file(fpath)
        all_trans.update(trans)
        print(f"  提取了 {len(trans)} 条")
    
    # 保存翻译模板
    out = 'i18n_new_entries.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(all_trans, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 翻译模板已保存到: {out}")
    print(f"  共 {len(all_trans)} 条，请人工翻译 en 字段")
