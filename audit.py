#!/usr/bin/env python3
"""
全站质量检测引擎 - Fantasy Holiday Yacht
扫描854个HTML文件，输出JSON Lines格式的问题台账
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

# ─── Build file existence sets for fast lookup ───
print("Building file existence sets...", file=sys.stderr)
all_files = set()
html_files = set()
css_files = set()
js_files = set()
img_files = set()

for root, dirs, files in os.walk(BASE_DIR):
    # Skip .git
    if '.git' in root:
        continue
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, BASE_DIR)
        all_files.add(rel)
        low = f.lower()
        if low.endswith('.html'):
            html_files.add(rel)
        elif low.endswith('.css'):
            css_files.add(rel)
        elif low.endswith('.js'):
            js_files.add(rel)
        elif low.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico', '.bmp')):
            img_files.add(rel)

print(f"  HTML: {len(html_files)}, CSS: {len(css_files)}, JS: {len(js_files)}, IMG: {len(img_files)}", file=sys.stderr)

# ─── Results collector ───
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

# ─── Helpers ───
def resolve_path(src_file, href):
    """Resolve a relative path from src_file's directory against BASE_DIR."""
    if not href or href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:', '#', 'javascript:')):
        return None
    # Remove fragment and query
    href = href.split('#')[0].split('?')[0]
    if not href:
        return None
    src_dir = os.path.dirname(src_file)
    resolved = os.path.normpath(os.path.join(src_dir, href))
    return resolved

def file_exists(rel_path):
    """Check if a relative path exists in our file sets."""
    # Normalize
    norm = os.path.normpath(rel_path)
    return norm in all_files

# ─── 1. Custom HTML Parser for syntax checking ───
class AuditHTMLParser(HTMLParser):
    """Custom parser to detect unclosed tags, duplicate IDs, nesting errors."""
    
    # Self-closing / void elements
    VOID_ELEMENTS = frozenset([
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'
    ])
    
    # Elements that auto-close certain parents
    AUTO_CLOSE_MAP = {
        'p': frozenset(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'table', 'blockquote', 'pre', 'hr', 'form', 'fieldset', 'address']),
        'li': frozenset(['li']),
        'dt': frozenset(['dt', 'dd']),
        'dd': frozenset(['dt', 'dd']),
        'tr': frozenset(['tr']),
        'td': frozenset(['td', 'th']),
        'th': frozenset(['td', 'th']),
        'thead': frozenset(['tbody', 'tfoot']),
        'tbody': frozenset(['tbody', 'tfoot']),
        'option': frozenset(['option']),
    }
    
    # Invalid nesting: block elements that cannot go inside inline/phrasing elements
    BLOCK_ELEMENTS = frozenset([
        'div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li',
        'table', 'tr', 'td', 'th', 'thead', 'tbody', 'tfoot', 'form', 'fieldset',
        'blockquote', 'pre', 'hr', 'section', 'article', 'aside', 'nav', 'header',
        'footer', 'main', 'figure', 'figcaption', 'details', 'summary', 'dl', 'dt', 'dd'
    ])
    
    INLINE_ELEMENTS = frozenset([
        'a', 'span', 'strong', 'em', 'b', 'i', 'u', 'small', 'sub', 'sup',
        'code', 'abbr', 'cite', 'q', 'time', 'var', 'mark', 'bdo', 'bdi',
        'data', 'wbr', 'br', 'img', 'input', 'label', 'select', 'textarea',
        'button', 'output'
    ])
    
    # Specifically: div inside p is invalid
    INVALID_NESTING = {
        'p': frozenset(['div', 'ul', 'ol', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'pre', 'blockquote', 'form', 'fieldset', 'section', 'article', 'aside', 'nav', 'header', 'footer', 'main', 'figure', 'dl']),
        'a': frozenset(['a']),
        'button': frozenset(['button']),
        'label': frozenset(['label']),
    }
    
    def __init__(self, filepath, rel_path, file_lines):
        super().__init__(convert_charrefs=False)
        self.filepath = filepath
        self.rel_path = rel_path
        self.file_lines = file_lines
        self.tag_stack = []  # (tag_name, line_number)
        self.ids_seen = {}   # id_value -> first_line
        self.issues = []
        self.resources = []  # (href/src value, line, tag, attr)
        self.images = []     # (src, line, has_alt)
        self.css_refs = []   # (href, line)
        self.js_refs = []    # (src, line)
        self.text_chunks = []  # (text, line) for content quality checks
        
    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        attrs_dict = dict(attrs)
        
        # Track resources
        if 'href' in attrs_dict:
            self.resources.append((attrs_dict['href'], line, tag, 'href'))
        if 'src' in attrs_dict:
            self.resources.append((attrs_dict['src'], line, tag, 'src'))
        
        # Track images
        if tag == 'img':
            has_alt = 'alt' in attrs_dict
            src = attrs_dict.get('src', '')
            self.images.append((src, line, has_alt))
            # Also add to resources for dead link check
            if src:
                self.resources.append((src, line, 'img', 'src'))
        
        # Track CSS/JS refs
        if tag == 'link' and attrs_dict.get('rel', '') == 'stylesheet':
            href = attrs_dict.get('href', '')
            if href:
                self.css_refs.append((href, line))
        if tag == 'script' and 'src' in attrs_dict:
            self.js_refs.append((attrs_dict['src'], line))
        
        # Check duplicate IDs
        elem_id = attrs_dict.get('id', '')
        if elem_id:
            if elem_id in self.ids_seen:
                self.issues.append(('html_error', 'major', line,
                    f'重复id="{elem_id}"，首次出现在第{self.ids_seen[elem_id]}行',
                    f'修改第{line}行的id为唯一值'))
            else:
                self.ids_seen[elem_id] = line
        
        # Handle void elements (no closing tag needed)
        if tag.lower() in self.VOID_ELEMENTS:
            return
        
        # Check auto-closing behavior
        if tag in self.AUTO_CLOSE_MAP:
            closes = self.AUTO_CLOSE_MAP[tag]
            while self.tag_stack and self.tag_stack[-1][0] in closes:
                self.tag_stack.pop()
        
        # Check invalid nesting
        if self.tag_stack:
            parent_tag = self.tag_stack[-1][0]
            if parent_tag in self.INVALID_NESTING:
                if tag in self.INVALID_NESTING[parent_tag]:
                    parent_line = self.tag_stack[-1][1]
                    self.issues.append(('html_error', 'major', line,
                        f'<{tag}>嵌套在<{parent_tag}>内（第{parent_line}行），这是无效嵌套',
                        f'将<{tag}>移到<{parent_tag}>外或替换<{parent_tag}>为<div>'))
        
        self.tag_stack.append((tag, line))
    
    def handle_endtag(self, tag):
        line = self.getpos()[0]
        if tag.lower() in self.VOID_ELEMENTS:
            return
        
        # Find matching open tag
        found = False
        for i in range(len(self.tag_stack) - 1, -1, -1):
            if self.tag_stack[i][0] == tag:
                found = True
                # Check for unclosed tags between
                if i < len(self.tag_stack) - 1:
                    unclosed = self.tag_stack[i+1:]
                    for ut, ul in unclosed:
                        # Skip auto-closing tags that browsers handle
                        if ut in ('p', 'li', 'td', 'th', 'tr', 'dt', 'dd', 'option', 'thead', 'tbody', 'tfoot'):
                            continue
                        self.issues.append(('html_error', 'major', ul,
                            f'<{ut}>标签未正确闭合（在<{tag}>闭合时发现）',
                            f'在第{ul}行之后添加</{ut}>闭合标签'))
                self.tag_stack = self.tag_stack[:i]
                break
        
        if not found:
            self.issues.append(('html_error', 'minor', line,
                f'</{tag}>没有匹配的开始标签',
                f'删除多余的</{tag}>或添加对应的开始标签'))
    
    def handle_data(self, data):
        line = self.getpos()[0]
        text = data.strip()
        if text and len(text) > 1:
            self.text_chunks.append((text, line))
    
    def handle_startendtag(self, tag, attrs):
        # Self-closing tags like <br/> - just treat as starttag for void elements
        self.handle_starttag(tag, attrs)


# ─── Content quality checker ───
def check_content_quality(text, line, rel_path):
    """Check Chinese/English content quality issues."""
    issues = []
    
    # 的/地/得 混用检测
    # Pattern: adjective + 的 + verb (should be 地)
    de_patterns = [
        (r'认真?(?:的|得)说', '认真地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'仔细?(?:的|得)看', '仔细地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'努力?(?:的|得)做', '努力地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'快速?(?:的|得)发', '快速地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'安静?(?:的|得)地', '安静地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'热情?(?:的|得)接待', '热情地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'专业?(?:的|得)服务', '专业地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'用心?(?:的|得)打造', '用心地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'精心?(?:的|得)设计', '精心地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'真诚?(?:的|得)邀请', '真诚地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'亲密?(?:的|得)接触', '亲密地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'舒适?(?:的|得)享受', '舒适地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'愉快?(?:的|得)旅行', '愉快地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'完美?(?:的|得)呈现', '完美地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'深入?(?:的|得)了解', '深入地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'持续?(?:的|得)创新', '持续地', '副词修饰动词应用"地"而非"的"或"得"'),
        (r'不断?(?:的|得)追求', '不断地', '副词修饰动词应用"地"而非"的"或"得"'),
    ]
    for pattern, fix_word, desc in de_patterns:
        if re.search(pattern, text):
            issues.append(('content', 'minor', desc, f'修改为"{fix_word}"'))
    
    # 同义反复检测
    tautology_patterns = [
        (r'免费赠送', '"免费"与"赠送"同义反复'),
        (r'携手合作', '"携手"与"合作"同义反复'),
        (r'共同一起', '"共同"与"一起"同义反复'),
        (r'唯一独一无二', '同义反复'),
        (r'大约左右', '"大约"与"左右"同义反复'),
        (r'大约差不多', '"大约"与"差不多"同义反复'),
        (r'先进的前沿', '"先进的"与"前沿"同义反复'),
        (r'奢华的豪华', '"奢华"与"豪华"同义反复'),
        (r'顶级的顶尖', '"顶级"与"顶尖"同义反复'),
    ]
    for pattern, desc in tautology_patterns:
        if re.search(pattern, text):
            issues.append(('content', 'minor', desc, '删除冗余词语'))
    
    # 常见错别字
    typo_patterns = [
        (r'渡假', '"渡假"应为"度假"'),
        (r'按耐', '"按耐"应为"按捺"'),
        (r'凑和', '"凑和"应为"凑合"'),
        (r'坐落', '常见错误，应为"坐落"（此条跳过，坐落本身正确）'),
        (r'蓝球', '"蓝球"应为"篮球"（如有）'),
        (r'帐蓬', '"帐蓬"应为"帐篷"'),
        (r'座落', '"座落"应为"坐落"'),
        (r'渡过.*假期', '"渡过假期"应为"度过假期"'),
        (r'渡过.*时光', '"渡过时光"应为"度过时光"'),
        (r'名牌.*座驾', '检查是否有误用'),
    ]
    for pattern, desc in typo_patterns:
        if '跳过' in desc:
            continue
        if re.search(pattern, text):
            issues.append(('content', 'major', desc, '修正错别字'))
    
    # English grammar - common Chinese-English issues
    en_grammar = [
        (r'\bWelcome to visit us\b', '中式英语"Welcome to visit us"，应为"Please visit us"或"We welcome your visit"'),
        (r'\bWe sincerely welcome\b', '中式英语，建议改为"We warmly welcome"'),
        (r'\byourself\b', '检查yourself是否应为yourselves（复数客户）'),
        (r'\bthe most unique\b', '"unique"本身已是最高级，不加"most"'),
        (r'\bmore better\b', '双重比较级错误，应为"better"或"much better"'),
        (r'\bmore superior\b', '"superior"已是比较级，应为"superior to"'),
        (r'\bvery unique\b', '"unique"无需程度副词修饰'),
        (r'\bcompletely free\b', '检查语境是否矛盾（奢侈品+免费）'),
        (r'\bThe ([A-Z][a-z]+ (?:Yacht|Vessel|Ship))s\b', '检查专有名词复数是否正确'),
        (r'\bprovides you with\s+\w+\s+\w+\s+experience\b', '检查是否为冗余表达'),
    ]
    for pattern, desc in en_grammar:
        if re.search(pattern, text):
            issues.append(('content', 'minor', desc, '修正英语表达'))
    
    return issues


# ─── Main scanning loop ───
print("Scanning HTML files...", file=sys.stderr)
total = len(html_files)
processed = 0

for html_rel in sorted(html_files):
    processed += 1
    if processed % 50 == 0:
        print(f"  Progress: {processed}/{total}", file=sys.stderr)
    
    html_path = BASE_DIR / html_rel
    try:
        with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        add_issue(html_rel, 0, 'html_error', 'critical', f'文件读取失败: {e}', '')
        continue
    
    lines = content.split('\n')
    
    # ─── Quick regex-based pre-checks for missing quotes ───
    # href=xxx or src=xxx without quotes (but not href="xxx")
    for i, line in enumerate(lines, 1):
        # Missing quotes: href=something (not href="..." or href='...')
        # Be careful: href="" is valid but empty
        for m in re.finditer(r'(?:href|src)\s*=\s*([^"\'\s>][^\s>]*)', line):
            val = m.group(1)
            # Skip valid unquoted values that are simple tokens
            if val in ('true', 'false', 'null'):
                continue
            add_issue(html_rel, i, 'html_error', 'major',
                f'属性值缺少引号: {m.group(0)[:60]}',
                f'为属性值添加引号: {m.group(0)[:30]}')
    
    # ─── Parse with custom HTML parser ───
    parser = AuditHTMLParser(html_path, html_rel, lines)
    try:
        parser.feed(content)
    except Exception as e:
        add_issue(html_rel, 0, 'html_error', 'critical', f'HTML解析失败: {e}', '')
    
    # Collect parser-found issues
    for itype, severity, line, detail, fix in parser.issues:
        add_issue(html_rel, line, itype, severity, detail, fix)
    
    # ─── 1. Dead link detection ───
    for href, line, tag, attr in parser.resources:
        if not href:
            continue
        
        # Empty link
        if href == '' and attr == 'href':
            add_issue(html_rel, line, 'dead_link', 'major',
                f'<{tag}> href为空字符串',
                '设置有效的链接地址或使用#占位')
            continue
        
        # Anchor-only links (not errors, just mark)
        if href == '#':
            add_issue(html_rel, line, 'dead_link', 'minor',
                f'<{tag}> href="#" 锚点链接',
                '如非必要，替换为有意义的锚点或按钮')
            continue
        
        # JavaScript void links
        if href.startswith('javascript:'):
            if 'void(0)' in href or 'void 0' in href or href == 'javascript:;':
                add_issue(html_rel, line, 'dead_link', 'minor',
                    f'<{tag}> javascript空链接: {href[:40]}',
                    '使用button替代a标签，或添加实际功能')
            continue
        
        # Skip external URLs, mailto, tel, data URIs
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:')):
            continue
        
        # Resolve local path
        resolved = resolve_path(html_rel, href)
        if resolved and not file_exists(resolved):
            add_issue(html_rel, line, 'dead_link', 'critical',
                f'<{tag} {attr}="{href}"> 指向不存在的文件 (解析为: {resolved})',
                f'创建缺失文件 {resolved} 或修正链接')
    
    # ─── 4. Image issues ───
    for src, line, has_alt in parser.images:
        if src and not src.startswith(('http://', 'https://', 'data:')):
            resolved = resolve_path(html_rel, src)
            if resolved and not file_exists(resolved):
                add_issue(html_rel, line, 'image', 'critical',
                    f'图片文件不存在: src="{src}" (解析为: {resolved})',
                    f'上传图片 {resolved} 或修正路径')
        
        if not has_alt:
            add_issue(html_rel, line, 'image', 'minor',
                f'<img> 缺少alt属性 (src="{src[:40]}")',
                '添加描述性alt属性以提升可访问性')
    
    # ─── 5. CSS/JS resource checks ───
    # CSS
    css_seen_in_file = {}
    for href, line in parser.css_refs:
        if href.startswith(('http://', 'https://', 'data:')):
            continue
        resolved = resolve_path(html_rel, href)
        if resolved and not file_exists(resolved):
            add_issue(html_rel, line, 'resource', 'critical',
                f'引用不存在的CSS文件: href="{href}" (解析为: {resolved})',
                f'创建 {resolved} 或修正引用路径')
        
        # Duplicate CSS reference
        if href in css_seen_in_file:
            add_issue(html_rel, line, 'resource', 'minor',
                f'重复引用CSS: href="{href}"（首次引用在第{css_seen_in_file[href]}行）',
                f'删除第{line}行的重复引用')
        else:
            css_seen_in_file[href] = line
    
    # JS
    js_seen_in_file = {}
    for src, line in parser.js_refs:
        if src.startswith(('http://', 'https://', 'data:')):
            continue
        resolved = resolve_path(html_rel, src)
        if resolved and not file_exists(resolved):
            add_issue(html_rel, line, 'resource', 'critical',
                f'引用不存在的JS文件: src="{src}" (解析为: {resolved})',
                f'创建 {resolved} 或修正引用路径')
        
        # Duplicate JS reference
        if src in js_seen_in_file:
            add_issue(html_rel, line, 'resource', 'minor',
                f'重复引用JS: src="{src}"（首次引用在第{js_seen_in_file[src]}行）',
                f'删除第{line}行的重复引用')
        else:
            js_seen_in_file[src] = line
    
    # ─── 3. Content quality checks ───
    for text, line in parser.text_chunks:
        content_issues = check_content_quality(text, line, html_rel)
        for itype, severity, detail, fix in content_issues:
            add_issue(html_rel, line, itype, severity, detail, fix)

# ─── Additional: Check for bilingual mismatch ───
# For files in /en/ directory, check if corresponding Chinese file exists and compare key data
print("Checking bilingual consistency...", file=sys.stderr)
en_htmls = [f for f in html_files if '/en/' in f]
for en_rel in en_htmls:
    # Find corresponding Chinese file
    # e.g., en/about.html -> about.html; en/yachts.html -> yachts.html
    cn_rel = en_rel.replace('/en/', '/')
    if cn_rel in html_files:
        # Extract numbers from both files and compare
        try:
            with open(BASE_DIR / en_rel, 'r', encoding='utf-8', errors='replace') as f:
                en_content = f.read()
            with open(BASE_DIR / cn_rel, 'r', encoding='utf-8', errors='replace') as f:
                cn_content = f.read()
            
            # Compare phone numbers
            en_phones = set(re.findall(r'\+?\d[\d\s\-()]{7,}', en_content))
            cn_phones = set(re.findall(r'\+?\d[\d\s\-()]{7,}', cn_content))
            if en_phones != cn_phones and en_phones and cn_phones:
                add_issue(en_rel, 0, 'content', 'major',
                    f'双语页面电话号码不一致: EN={en_phones}, CN={cn_phones}',
                    '统一中英文页面的联系电话')
                add_issue(cn_rel, 0, 'content', 'major',
                    f'双语页面电话号码不一致: EN={en_phones}, CN={cn_phones}',
                    '统一中英文页面的联系电话')
            
            # Compare email addresses
            en_emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', en_content))
            cn_emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', cn_content))
            if en_emails != cn_emails and en_emails and cn_emails:
                add_issue(en_rel, 0, 'content', 'major',
                    f'双语页面邮箱不一致: EN={en_emails}, CN={cn_emails}',
                    '统一中英文页面的联系邮箱')
                add_issue(cn_rel, 0, 'content', 'major',
                    f'双语页面邮箱不一致: EN={en_emails}, CN={cn_emails}',
                    '统一中英文页面的联系邮箱')
            
            # Compare prices/currency values
            en_prices = set(re.findall(r'[¥$€£]\s*[\d,]+(?:\.\d+)?(?:\s*[万万亿])?', en_content))
            cn_prices = set(re.findall(r'[¥$€£]\s*[\d,]+(?:\.\d+)?(?:\s*[万万亿])?', cn_content))
            if en_prices != cn_prices and en_prices and cn_prices:
                add_issue(en_rel, 0, 'content', 'major',
                    f'双语页面价格不一致: EN={en_prices}, CN={cn_prices}',
                    '核实并统一中英文页面的价格信息')
                add_issue(cn_rel, 0, 'content', 'major',
                    f'双语页面价格不一致: EN={en_prices}, CN={cn_prices}',
                    '核实并统一中英文页面的价格信息')
            
        except Exception:
            pass
    else:
        add_issue(en_rel, 0, 'dead_link', 'major',
            f'英文页面缺少对应的中文版本: {cn_rel}',
            f'创建 {cn_rel} 或确认该页面仅需英文版本')

# Also check if Chinese files are missing English versions
cn_only = [f for f in html_files if '/en/' not in f and '/YT/' not in f and not f.startswith('YT/')]
for cn_rel in cn_only:
    en_rel = cn_rel.replace('/', '/en/', 1) if '/' not in cn_rel else cn_rel.replace('/', '/en/', 1)
    # Simpler: just prepend en/
    parts = cn_rel.split('/')
    parts.insert(-1, 'en')
    en_candidate = '/'.join(parts)
    if en_candidate not in html_files:
        # Don't flag everything - only flag pages that have data-i18n (bilingual intent)
        pass  # Skip - too many false positives

# ─── Write results ───
print(f"Writing {len(results)} issues to {OUTPUT_FILE}...", file=sys.stderr)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for issue in results:
        f.write(json.dumps(issue, ensure_ascii=False) + '\n')

# ─── Summary ───
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
