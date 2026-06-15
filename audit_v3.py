#!/usr/bin/env python3
"""
全站质量检测引擎 v3 - Fantasy Holiday Yacht
扫描854个HTML文件，输出JSON Lines格式的问题台账
v3: 修正嵌套检测逻辑，减少误报
"""

import os
import re
import json
import sys
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict

BASE_DIR = Path("/Users/stone/.qclaw/workspace/fantasy-holiday-yacht")
OUTPUT_FILE = Path("/Users/stone/.qclaw/workspace/audit-report.jsonl")

# ─── Build file existence sets ───
print("Building file existence sets...", file=sys.stderr)
all_files = set()
html_files = set()

for root, dirs, files in os.walk(BASE_DIR):
    if '.git' in root:
        continue
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, BASE_DIR)
        all_files.add(rel)
        if f.lower().endswith('.html'):
            html_files.add(rel)

print(f"  Total files: {len(all_files)}, HTML: {len(html_files)}", file=sys.stderr)

# ─── Results ───
results = []

def add_issue(file, line, itype, severity, detail, fix=""):
    results.append({
        "file": file,
        "line": line,
        "type": itype,
        "severity": severity,
        "detail": detail,
        "fix": fix
    })

def resolve_path(src_file, href):
    if not href or href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:', '#', 'javascript:')):
        return None
    href = href.split('#')[0].split('?')[0]
    if not href:
        return None
    src_dir = os.path.dirname(src_file)
    return os.path.normpath(os.path.join(src_dir, href))

def file_exists(rel_path):
    return os.path.normpath(rel_path) in all_files

# ─── HTML Parser ───
VOID_ELEMENTS = frozenset([
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr'
])

# INVALID: block element INSIDE phrasing/inline parent
# Key = parent tag, Value = set of child tags that are FORBIDDEN inside it
BLOCK_IN_INLINE = frozenset([
    'div', 'ul', 'ol', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'hr', 'pre', 'blockquote', 'form', 'fieldset', 'section', 'article',
    'aside', 'nav', 'header', 'footer', 'main', 'figure', 'dl', 'p'
])

FORBIDDEN_CHILDREN = {
    'p': frozenset(['div', 'ul', 'ol', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                    'hr', 'pre', 'blockquote', 'form', 'fieldset', 'section', 'article',
                    'aside', 'nav', 'header', 'footer', 'main', 'figure', 'dl', 'p']),
    'a': frozenset(['a']),
    'button': frozenset(['button']),
    'label': frozenset(['label']),
    'h1': frozenset(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']),
    'h2': frozenset(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']),
    'h3': frozenset(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']),
    'h4': frozenset(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']),
    'h5': frozenset(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']),
    'h6': frozenset(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']),
    'span': frozenset(['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'table']),
    'strong': frozenset(['div', 'p', 'ul', 'ol', 'table']),
    'em': frozenset(['div', 'p', 'ul', 'ol', 'table']),
    'time': frozenset(['div', 'p', 'ul', 'ol', 'table']),
}

class AuditHTMLParser(HTMLParser):
    def __init__(self, filepath, rel_path):
        super().__init__(convert_charrefs=False)
        self.rel_path = rel_path
        self.ids_seen = {}
        self.issues = []
        self.resources = []
        self.images = []
        self.css_refs = []
        self.js_refs = []
        self.text_chunks = []
        self.tag_stack = []  # (tag, line)
        self._in_script = False
        
    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        attrs_dict = dict(attrs)
        
        if tag == 'script':
            self._in_script = True
        if tag == 'style':
            self.tag_stack.append((tag, line))
            return
        
        href_val = attrs_dict.get('href', '')
        src_val = attrs_dict.get('src', '')
        if href_val:
            self.resources.append((href_val, line, tag, 'href'))
        if src_val:
            self.resources.append((src_val, line, tag, 'src'))
        
        if tag == 'img':
            has_alt = 'alt' in attrs_dict
            self.images.append((src_val, line, has_alt))
        
        if tag == 'link' and attrs_dict.get('rel', '') == 'stylesheet':
            if href_val:
                self.css_refs.append((href_val, line))
        if tag == 'script' and src_val:
            self.js_refs.append((src_val, line))
        
        elem_id = attrs_dict.get('id', '')
        if elem_id:
            if elem_id in self.ids_seen:
                self.issues.append(('html_error', 'major', line,
                    f'重复id="{elem_id}"，首次出现在第{self.ids_seen[elem_id]}行',
                    f'修改第{line}行的id为唯一值'))
            else:
                self.ids_seen[elem_id] = line
        
        if tag.lower() in VOID_ELEMENTS:
            return
        
        # Check invalid nesting: look up the stack for a forbidden parent
        if tag in BLOCK_IN_INLINE:
            for pt, pl in reversed(self.tag_stack):
                if pt in FORBIDDEN_CHILDREN and tag in FORBIDDEN_CHILDREN[pt]:
                    self.issues.append(('html_error', 'major', line,
                        f'<{tag}>嵌套在<{pt}>内（第{pl}行）是无效的HTML嵌套',
                        f'将<{tag}>移到<{pt}>外面，或将<{pt}>改为<div>'))
                    break
        
        self.tag_stack.append((tag, line))
    
    def handle_endtag(self, tag):
        if tag == 'script':
            self._in_script = False
        if tag.lower() in VOID_ELEMENTS:
            return
        for i in range(len(self.tag_stack) - 1, -1, -1):
            if self.tag_stack[i][0] == tag:
                self.tag_stack = self.tag_stack[:i]
                break
    
    def handle_data(self, data):
        if self._in_script:
            return
        line = self.getpos()[0]
        text = data.strip()
        if text and len(text) > 2:
            self.text_chunks.append((text, line))


# ─── Unclosed tag detection ───
def check_unclosed_tags(content, rel_path):
    issues = []
    tag_opens = defaultdict(list)
    tag_closes = defaultdict(int)
    
    for i, line in enumerate(content.split('\n'), 1):
        for m in re.finditer(r'<([a-zA-Z][a-zA-Z0-9]*)((?:\s+[^>]*)?)(/?)>', line):
            tag = m.group(1).lower()
            is_self_close = m.group(3) == '/'
            if tag in VOID_ELEMENTS or is_self_close:
                continue
            if tag not in ('script', 'style'):
                tag_opens[tag].append(i)
        
        for m in re.finditer(r'</([a-zA-Z][a-zA-Z0-9]*)\s*>', line):
            tag = m.group(1).lower()
            if tag not in ('script', 'style'):
                tag_closes[tag] += 1
    
    for tag in tag_opens:
        open_count = len(tag_opens[tag])
        close_count = tag_closes.get(tag, 0)
        if open_count > close_count:
            diff = open_count - close_count
            if diff >= 1:
                last_line = tag_opens[tag][-1]
                issues.append(('html_error', 'major', last_line,
                    f'<{tag}>有{diff}个未闭合标签（开{open_count}个/闭{close_count}个）',
                    f'检查<{tag}>的闭合情况，补充</{tag}>'))
    return issues


# ─── Content quality ───
def check_content_quality(text, line, rel_path):
    issues = []
    
    # 的/地/得 混用
    de_patterns = [
        (r'(?:认真|仔细|努力|快速|安静|热情|用心|精心|真诚|亲密|舒适|愉快|完美|深入|持续|不断|积极|主动|缓慢|迅速|悄悄|默默)(?:的)(?:说|看|做|发|走|跑|写|学|工作|服务|打造|设计|邀请|接待|享受|旅行|呈现|了解|创新|追求|推动|探索|发展|前进)', '地', '副词修饰动词应用"地"而非"的"'),
        (r'走(?:的)很快', '得', '动词+补语应用"得"而非"的"'),
        (r'做(?:的)很好', '得', '动词+补语应用"得"而非"的"'),
        (r'说(?:的)很对', '得', '动词+补语应用"得"而非"的"'),
        (r'发展(?:的)很快', '得', '动词+补语应用"得"而非"的"'),
    ]
    for pattern, fix_char, desc in de_patterns:
        if re.search(pattern, text):
            issues.append(('content', 'minor', f'{desc}', f'将"的"修改为"{fix_char}"'))
            break
    
    # 同义反复
    tautology_patterns = [
        (r'免费赠送', '"免费"与"赠送"同义反复'),
        (r'携手合作', '"携手"与"合作"近义反复'),
        (r'共同一起', '"共同"与"一起"同义反复'),
        (r'大约左右', '"大约"与"左右"同义反复'),
        (r'大约差不多', '"大约"与"差不多"同义反复'),
        (r'奢华的豪华', '"奢华"与"豪华"同义反复'),
        (r'顶级的顶尖', '"顶级"与"顶尖"同义反复'),
    ]
    for pattern, desc in tautology_patterns:
        if re.search(pattern, text):
            issues.append(('content', 'minor', desc, '删除冗余词语'))
    
    # 错别字
    typo_patterns = [
        (r'渡假', '"渡假"应为"度假"', '度假'),
        (r'按耐', '"按耐"应为"按捺"', '按捺'),
        (r'帐蓬', '"帐蓬"应为"帐篷"', '帐篷'),
        (r'座落', '"座落"应为"坐落"', '坐落'),
        (r'渡过.{0,4}(?:假期|时光|岁月)', '"渡过"表示时间应用"度过"', '度过'),
    ]
    for pattern, desc, *fix in typo_patterns:
        if re.search(pattern, text):
            fix_text = f'修改为"{fix[0]}"' if fix else '修正错别字'
            issues.append(('content', 'major', desc, fix_text))
    
    # English grammar
    en_grammar = [
        (r'\bWelcome to visit us\b', '中式英语"Welcome to visit us"', '"Please visit us"或"We welcome your visit"'),
        (r'\bthe most unique\b', '"unique"已是最高级，不加"most"', '"unique"'),
        (r'\bmore better\b', '双重比较级错误', '"better"'),
        (r'\bmore superior\b', '"superior"已含比较义', '"superior to"'),
        (r'\bvery unique\b', '"unique"无需程度副词修饰', '"unique"'),
    ]
    for pattern, desc, fix in en_grammar:
        if re.search(pattern, text):
            issues.append(('content', 'minor', desc, fix))
    
    return issues


# ─── Main loop ───
print("Scanning HTML files...", file=sys.stderr)
total = len(html_files)
processed = 0

for html_rel in sorted(html_files):
    processed += 1
    if processed % 100 == 0:
        print(f"  Progress: {processed}/{total}", file=sys.stderr)
    
    html_path = BASE_DIR / html_rel
    try:
        with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        add_issue(html_rel, 0, 'html_error', 'critical', f'文件读取失败: {e}', '')
        continue
    
    lines = content.split('\n')
    
    # Missing quotes check
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'(?:href|src)\s*=\s*([^"\'\s>][^\s>]*)', line):
            val = m.group(1)
            if val in ('true', 'false', 'null'):
                continue
            add_issue(html_rel, i, 'html_error', 'major',
                f'属性值缺少引号: {m.group(0)[:80]}',
                '为属性值添加引号')
    
    # Parse
    parser = AuditHTMLParser(html_path, html_rel)
    try:
        parser.feed(content)
    except Exception as e:
        add_issue(html_rel, 0, 'html_error', 'critical', f'HTML解析失败: {e}', '')
    
    for itype, severity, line, detail, fix in parser.issues:
        add_issue(html_rel, line, itype, severity, detail, fix)
    
    # Unclosed tags
    for itype, severity, line, detail, fix in check_unclosed_tags(content, html_rel):
        add_issue(html_rel, line, itype, severity, detail, fix)
    
    # Dead links
    for href, line, tag, attr in parser.resources:
        if not href:
            if attr == 'href':
                add_issue(html_rel, line, 'dead_link', 'major',
                    f'<{tag}> href为空字符串', '设置有效的链接地址或使用button')
            continue
        
        if href == '' and attr == 'href':
            add_issue(html_rel, line, 'dead_link', 'major',
                f'<{tag}> href为空字符串', '设置有效的链接地址')
            continue
        
        if href == '#':
            add_issue(html_rel, line, 'dead_link', 'minor',
                f'<{tag}> href="#" 锚点链接', '替换为有意义的锚点或使用button')
            continue
        
        if href.startswith('javascript:'):
            if 'void(0)' in href or 'void 0' in href or href == 'javascript:;':
                add_issue(html_rel, line, 'dead_link', 'minor',
                    f'<{tag}> javascript空链接', '使用button替代或添加实际功能')
            continue
        
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:')):
            continue
        
        resolved = resolve_path(html_rel, href)
        if resolved and not file_exists(resolved):
            add_issue(html_rel, line, 'dead_link', 'critical',
                f'<{tag} {attr}="{href}"> 指向不存在的文件 (解析: {resolved})',
                f'创建缺失文件 {resolved} 或修正链接')
    
    # Images
    for src, line, has_alt in parser.images:
        if src and not src.startswith(('http://', 'https://', 'data:')):
            resolved = resolve_path(html_rel, src)
            if resolved and not file_exists(resolved):
                add_issue(html_rel, line, 'image', 'critical',
                    f'图片文件不存在: src="{src}" (解析: {resolved})',
                    f'上传图片 {resolved} 或修正路径')
        if not has_alt:
            add_issue(html_rel, line, 'image', 'minor',
                f'<img> 缺少alt属性 (src="{src[:60]}")',
                '添加描述性alt属性')
    
    # CSS/JS
    css_seen = {}
    for href, line in parser.css_refs:
        if href in css_seen:
            add_issue(html_rel, line, 'resource', 'minor',
                f'重复引用CSS: href="{href[:60]}"（首次第{css_seen[href]}行）',
                f'删除第{line}行的重复引用')
        else:
            css_seen[href] = line
        if not href.startswith(('http://', 'https://', 'data:')):
            resolved = resolve_path(html_rel, href)
            if resolved and not file_exists(resolved):
                add_issue(html_rel, line, 'resource', 'critical',
                    f'引用不存在的CSS: href="{href}" (解析: {resolved})',
                    f'创建 {resolved} 或修正路径')
    
    js_seen = {}
    for src, line in parser.js_refs:
        if src in js_seen:
            add_issue(html_rel, line, 'resource', 'minor',
                f'重复引用JS: src="{src[:60]}"（首次第{js_seen[src]}行）',
                f'删除第{line}行的重复引用')
        else:
            js_seen[src] = line
        if not src.startswith(('http://', 'https://', 'data:')):
            resolved = resolve_path(html_rel, src)
            if resolved and not file_exists(resolved):
                add_issue(html_rel, line, 'resource', 'critical',
                    f'引用不存在的JS: src="{src}" (解析: {resolved})',
                    f'创建 {resolved} 或修正路径')
    
    # Content quality
    for text, line in parser.text_chunks:
        for itype, severity, detail, fix in check_content_quality(text, line, html_rel):
            add_issue(html_rel, line, itype, severity, detail, fix)

# Bilingual consistency
print("Checking bilingual consistency...", file=sys.stderr)
en_htmls = [f for f in html_files if '/en/' in f]
for en_rel in en_htmls:
    parts = en_rel.split('/en/')
    if len(parts) == 2:
        cn_rel = parts[1] if parts[0] == '' else (parts[0].rstrip('/') + '/' + parts[1]).lstrip('/')
    else:
        continue
    if cn_rel in html_files:
        try:
            with open(BASE_DIR / en_rel, 'r', encoding='utf-8', errors='replace') as f:
                en_content = f.read()
            with open(BASE_DIR / cn_rel, 'r', encoding='utf-8', errors='replace') as f:
                cn_content = f.read()
            
            en_phones = set(re.findall(r'\+?\d[\d\s\-()]{7,}', en_content))
            cn_phones = set(re.findall(r'\+?\d[\d\s\-()]{7,}', cn_content))
            if en_phones != cn_phones and en_phones and cn_phones:
                add_issue(en_rel, 0, 'content', 'major',
                    f'双语电话不一致: EN={en_phones}, CN={cn_phones}', '统一联系电话')
            
            en_emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', en_content))
            cn_emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', cn_content))
            if en_emails != cn_emails and en_emails and cn_emails:
                add_issue(en_rel, 0, 'content', 'major',
                    f'双语邮箱不一致: EN={en_emails}, CN={cn_emails}', '统一联系邮箱')
            
            en_prices = set(re.findall(r'[¥$€£]\s*[\d,]+(?:\.\d+)?(?:\s*[万亿])?', en_content))
            cn_prices = set(re.findall(r'[¥$€£]\s*[\d,]+(?:\.\d+)?(?:\s*[万亿])?', cn_content))
            if en_prices != cn_prices and en_prices and cn_prices:
                add_issue(en_rel, 0, 'content', 'major',
                    f'双语价格不一致: EN={en_prices}, CN={cn_prices}', '核实统一价格')
        except Exception:
            pass
    else:
        add_issue(en_rel, 0, 'content', 'major',
            f'英文页面缺少对应中文版: {cn_rel}', f'创建 {cn_rel} 或确认仅需英文版')

# Write
print(f"Writing {len(results)} issues to {OUTPUT_FILE}...", file=sys.stderr)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for issue in results:
        f.write(json.dumps(issue, ensure_ascii=False) + '\n')

severity_counts = defaultdict(int)
type_counts = defaultdict(int)
for issue in results:
    severity_counts[issue['severity']] += 1
    type_counts[issue['type']] += 1

print(f"\n{'='*60}", file=sys.stderr)
print(f"扫描完成！共扫描 {total} 个HTML文件", file=sys.stderr)
print(f"发现问题总数: {len(results)}", file=sys.stderr)
print(f"\n按严重度:", file=sys.stderr)
for sev in ['critical', 'major', 'minor']:
    print(f"  {sev}: {severity_counts[sev]}", file=sys.stderr)
print(f"\n按类型:", file=sys.stderr)
for t in ['dead_link', 'html_error', 'content', 'image', 'resource']:
    print(f"  {t}: {type_counts[t]}", file=sys.stderr)
print(f"\n结果已保存到: {OUTPUT_FILE}", file=sys.stderr)
