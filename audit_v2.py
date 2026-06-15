#!/usr/bin/env python3
"""
全站质量检测引擎 v2 - Fantasy Holiday Yacht
扫描854个HTML文件，输出JSON Lines格式的问题台账
改进：使用更可靠的HTML解析方式，减少误报
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
    href = href.split('#')[0].split('?')[0]
    if not href:
        return None
    src_dir = os.path.dirname(src_file)
    resolved = os.path.normpath(os.path.join(src_dir, href))
    return resolved

def file_exists(rel_path):
    norm = os.path.normpath(rel_path)
    return norm in all_files

# ─── HTML Parser - simplified, focused on real issues ───
class AuditHTMLParser(HTMLParser):
    VOID_ELEMENTS = frozenset([
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'
    ])
    
    # Invalid nesting patterns that browsers reject
    INVALID_NESTING = {
        'p': frozenset(['div', 'ul', 'ol', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                        'hr', 'pre', 'blockquote', 'form', 'fieldset', 'section', 'article',
                        'aside', 'nav', 'header', 'footer', 'main', 'figure', 'dl']),
        'a': frozenset(['a']),
        'button': frozenset(['button']),
        'label': frozenset(['label']),
    }
    
    def __init__(self, filepath, rel_path):
        super().__init__(convert_charrefs=False)
        self.filepath = filepath
        self.rel_path = rel_path
        self.ids_seen = {}
        self.issues = []
        self.resources = []     # (href/src, line, tag, attr)
        self.images = []        # (src, line, has_alt)
        self.css_refs = []      # (href, line)
        self.js_refs = []       # (src, line)
        self.text_chunks = []   # (text, line)
        self.tag_stack = []     # (tag, line) - for invalid nesting detection only
        self._in_script = False
        
    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        attrs_dict = dict(attrs)
        
        if tag == 'script':
            self._in_script = True
        if tag == 'style':
            return  # skip style content
        
        # Track resources
        href_val = attrs_dict.get('href', '')
        src_val = attrs_dict.get('src', '')
        if href_val:
            self.resources.append((href_val, line, tag, 'href'))
        if src_val:
            self.resources.append((src_val, line, tag, 'src'))
        
        # Track images
        if tag == 'img':
            has_alt = 'alt' in attrs_dict
            self.images.append((src_val, line, has_alt))
        
        # Track CSS/JS refs
        if tag == 'link' and attrs_dict.get('rel', '') == 'stylesheet':
            if href_val:
                self.css_refs.append((href_val, line))
        if tag == 'script' and src_val:
            self.js_refs.append((src_val, line))
        
        # Check duplicate IDs
        elem_id = attrs_dict.get('id', '')
        if elem_id:
            if elem_id in self.ids_seen:
                self.issues.append(('html_error', 'major', line,
                    f'重复id="{elem_id}"，首次出现在第{self.ids_seen[elem_id]}行',
                    f'修改第{line}行的id为唯一值'))
            else:
                self.ids_seen[elem_id] = line
        
        # Void elements don't need closing
        if tag.lower() in self.VOID_ELEMENTS:
            return
        
        # Check invalid nesting (only for specific dangerous combos)
        if self.tag_stack and tag in self.INVALID_NESTING:
            # Walk up the stack to find if we're inside a forbidden parent
            for pt, pl in reversed(self.tag_stack):
                if pt in self.INVALID_NESTING.get(tag, set()):
                    self.issues.append(('html_error', 'major', line,
                        f'<{tag}>嵌套在<{pt}>内（第{pl}行），这是无效的HTML嵌套',
                        f'将<{tag}>移到<{pt}>外面或重构DOM结构'))
                    break
        
        self.tag_stack.append((tag, line))
    
    def handle_endtag(self, tag):
        if tag == 'script':
            self._in_script = False
        
        if tag.lower() in self.VOID_ELEMENTS:
            return
        
        # Pop from stack - find matching tag
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


# ─── Unclosed tag detection via balanced tag counting ───
def check_unclosed_tags(content, rel_path):
    """Check for truly unclosed tags by counting open vs close for non-void elements."""
    issues = []
    VOID = frozenset([
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr'
    ])
    
    # Track per-tag open/close counts and positions
    tag_opens = defaultdict(list)  # tag -> list of line numbers
    tag_closes = defaultdict(int)  # tag -> count of closes
    
    for i, line in enumerate(content.split('\n'), 1):
        # Find opening tags (not self-closing, not void)
        for m in re.finditer(r'<([a-zA-Z][a-zA-Z0-9]*)((?:\s+[^>]*)?)(/?)>', line):
            tag = m.group(1).lower()
            is_self_close = m.group(3) == '/'
            if tag in VOID or is_self_close:
                continue
            # Skip script/style content tags
            if tag in ('script', 'style'):
                tag_opens[tag].append(i)
                continue
            tag_opens[tag].append(i)
        
        # Find closing tags
        for m in re.finditer(r'</([a-zA-Z][a-zA-Z0-9]*)\s*>', line):
            tag = m.group(1).lower()
            tag_closes[tag] += 1
    
    # Compare
    for tag in tag_opens:
        if tag in ('script', 'style'):
            continue  # These are special
        open_count = len(tag_opens[tag])
        close_count = tag_closes.get(tag, 0)
        if open_count > close_count:
            diff = open_count - close_count
            # Only flag if meaningful
            if diff >= 1:
                # Find last unclosed position
                last_line = tag_opens[tag][-1]
                issues.append(('html_error', 'major', last_line,
                    f'<{tag}>有{diff}个未闭合标签（开{open_count}个/闭{close_count}个）',
                    f'检查文件中<{tag}>的闭合情况，补充{diff}个</{tag}>'))
    
    return issues


# ─── Content quality checker ───
def check_content_quality(text, line, rel_path):
    issues = []
    
    # ── 的/地/得 混用 ──
    de_patterns = [
        # 的+verb patterns (should be 地)
        (r'(?:认真|仔细|努力|快速|安静|热情|专业|用心|精心|真诚|亲密|舒适|愉快|完美|深入|持续|不断|积极|主动|热情|安静|缓慢|迅速|悄悄|默默)(?:的)(?:说|看|做|发|走|跑|写|学|工作|服务|打造|设计|邀请|接待|享受|旅行|呈现|了解|创新|追求|推动|探索|发展|前进)', '地', '副词修饰动词应用"地"而非"的"'),
        # 得+adj complement  
        (r'走(?:的)很快', '得', '动词+补语应用"得"而非"的"'),
        (r'做(?:的)很好', '得', '动词+补语应用"得"而非"的"'),
        (r'说(?:的)很对', '得', '动词+补语应用"得"而非"的"'),
        (r'发展(?:的)很快', '得', '动词+补语应用"得"而非"的"'),
    ]
    for pattern, fix_char, desc in de_patterns:
        if re.search(pattern, text):
            issues.append(('content', 'minor', f'{desc}（文本: ...{text[:30]}...）', f'将"的"修改为"{fix_char}"'))
            break  # One issue per chunk is enough
    
    # ── 同义反复 ──
    tautology_patterns = [
        (r'免费赠送', '"免费"与"赠送"同义反复'),
        (r'携手合作', '"携手"与"合作"近义反复'),
        (r'共同一起', '"共同"与"一起"同义反复'),
        (r'大约左右', '"大约"与"左右"同义反复'),
        (r'大约差不多', '"大约"与"差不多"同义反复'),
        (r'奢华的豪华', '"奢华"与"豪华"同义反复'),
        (r'顶级的顶尖', '"顶级"与"顶尖"同义反复'),
        (r'优秀的卓越', '"优秀"与"卓越"近义反复'),
    ]
    for pattern, desc in tautology_patterns:
        if re.search(pattern, text):
            issues.append(('content', 'minor', desc, '删除冗余词语'))
    
    # ── 常见错别字 ──
    typo_patterns = [
        (r'渡假', '"渡假"应为"度假"', '度假'),
        (r'按耐', '"按耐"应为"按捺"', '按捺'),
        (r'帐蓬', '"帐蓬"应为"帐篷"', '帐篷'),
        (r'座落', '"座落"应为"坐落"', '坐落'),
        (r'渡过.{0,4}(?:假期|时光|岁月)', '"渡过"表示时间应用"度过"', '度过'),
        (r'倾力打造.*倾力打造', '重复表述'),
    ]
    for pattern, desc, *fix in typo_patterns:
        if re.search(pattern, text):
            fix_text = f'修改为"{fix[0]}"' if fix else '修正错别字'
            issues.append(('content', 'major', desc, fix_text))
    
    # ── English grammar issues ──
    en_grammar = [
        (r'\bWelcome to visit us\b', '中式英语"Welcome to visit us"', '"Please visit us"或"We welcome your visit"'),
        (r'\bthe most unique\b', '"unique"已是最高级，不加"most"', '"unique"或"absolutely unique"'),
        (r'\bmore better\b', '双重比较级错误', '"better"或"much better"'),
        (r'\bmore superior\b', '"superior"已含比较义', '"superior to"'),
        (r'\bvery unique\b', '"unique"无需程度副词修饰', '"unique"'),
        (r'\bprovides.*with.*experience\b', '检查是否为冗余表达', '精简表达'),
    ]
    for pattern, desc, fix in en_grammar:
        if re.search(pattern, text):
            issues.append(('content', 'minor', desc, fix))
    
    return issues


# ─── Main scanning loop ───
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
    
    # ─── Quick regex-based pre-checks for missing quotes ───
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'(?:href|src)\s*=\s*([^"\'\s>][^\s>]*)', line):
            val = m.group(1)
            if val in ('true', 'false', 'null'):
                continue
            add_issue(html_rel, i, 'html_error', 'major',
                f'属性值缺少引号: {m.group(0)[:80]}',
                f'为属性值添加引号')
    
    # ─── Parse with custom HTML parser ───
    parser = AuditHTMLParser(html_path, html_rel)
    try:
        parser.feed(content)
    except Exception as e:
        add_issue(html_rel, 0, 'html_error', 'critical', f'HTML解析失败: {e}', '')
    
    # Collect parser-found issues (IDs, nesting)
    for itype, severity, line, detail, fix in parser.issues:
        add_issue(html_rel, line, itype, severity, detail, fix)
    
    # ─── Unclosed tags check ───
    unclosed_issues = check_unclosed_tags(content, html_rel)
    for itype, severity, line, detail, fix in unclosed_issues:
        add_issue(html_rel, line, itype, severity, detail, fix)
    
    # ─── 1. Dead link detection ───
    for href, line, tag, attr in parser.resources:
        if not href:
            if attr == 'href':
                add_issue(html_rel, line, 'dead_link', 'major',
                    f'<{tag}> href为空字符串',
                    '设置有效的链接地址或使用button替代')
            continue
        
        # Empty link
        if href == '' and attr == 'href':
            add_issue(html_rel, line, 'dead_link', 'major',
                f'<{tag}> href为空字符串',
                '设置有效的链接地址或使用button替代')
            continue
        
        # Anchor-only links (informational)
        if href == '#':
            add_issue(html_rel, line, 'dead_link', 'minor',
                f'<{tag}> href="#" 锚点链接',
                '如非必要，替换为有意义的锚点或使用button')
            continue
        
        # JavaScript void links
        if href.startswith('javascript:'):
            if 'void(0)' in href or 'void 0' in href or href == 'javascript:;':
                add_issue(html_rel, line, 'dead_link', 'minor',
                    f'<{tag}> javascript空链接',
                    '使用button替代a标签，或添加实际功能')
            continue
        
        # Skip external URLs, mailto, tel, data URIs
        if href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:')):
            continue
        
        # Resolve local path
        resolved = resolve_path(html_rel, href)
        if resolved and not file_exists(resolved):
            add_issue(html_rel, line, 'dead_link', 'critical',
                f'<{tag} {attr}="{href}"> 指向不存在的文件 (解析路径: {resolved})',
                f'创建缺失文件 {resolved} 或修正链接地址')
    
    # ─── 4. Image issues ───
    for src, line, has_alt in parser.images:
        if src and not src.startswith(('http://', 'https://', 'data:')):
            resolved = resolve_path(html_rel, src)
            if resolved and not file_exists(resolved):
                add_issue(html_rel, line, 'image', 'critical',
                    f'图片文件不存在: src="{src}" (解析路径: {resolved})',
                    f'上传图片 {resolved} 或修正路径')
        
        if not has_alt:
            add_issue(html_rel, line, 'image', 'minor',
                f'<img> 缺少alt属性 (src="{src[:50]}")',
                '添加描述性alt属性以提升可访问性')
    
    # ─── 5. CSS/JS resource checks ───
    css_seen = {}
    for href, line in parser.css_refs:
        if href.startswith(('http://', 'https://', 'data:')):
            # Still check for duplicate external refs
            if href in css_seen:
                add_issue(html_rel, line, 'resource', 'minor',
                    f'重复引用外部CSS: href="{href[:60]}"（首次在第{css_seen[href]}行）',
                    f'删除第{line}行的重复引用')
            else:
                css_seen[href] = line
            continue
        resolved = resolve_path(html_rel, href)
        if resolved and not file_exists(resolved):
            add_issue(html_rel, line, 'resource', 'critical',
                f'引用不存在的CSS文件: href="{href}" (解析路径: {resolved})',
                f'创建 {resolved} 或修正引用路径')
        if href in css_seen:
            add_issue(html_rel, line, 'resource', 'minor',
                f'重复引用CSS: href="{href}"（首次在第{css_seen[href]}行）',
                f'删除第{line}行的重复引用')
        else:
            css_seen[href] = line
    
    js_seen = {}
    for src, line in parser.js_refs:
        if src.startswith(('http://', 'https://', 'data:')):
            if src in js_seen:
                add_issue(html_rel, line, 'resource', 'minor',
                    f'重复引用外部JS: src="{src[:60]}"（首次在第{js_seen[src]}行）',
                    f'删除第{line}行的重复引用')
            else:
                js_seen[src] = line
            continue
        resolved = resolve_path(html_rel, src)
        if resolved and not file_exists(resolved):
            add_issue(html_rel, line, 'resource', 'critical',
                f'引用不存在的JS文件: src="{src}" (解析路径: {resolved})',
                f'创建 {resolved} 或修正引用路径')
        if src in js_seen:
            add_issue(html_rel, line, 'resource', 'minor',
                f'重复引用JS: src="{src}"（首次在第{js_seen[src]}行）',
                f'删除第{line}行的重复引用')
        else:
            js_seen[src] = line
    
    # ─── 3. Content quality checks ───
    for text, line in parser.text_chunks:
        content_issues = check_content_quality(text, line, html_rel)
        for itype, severity, detail, fix in content_issues:
            add_issue(html_rel, line, itype, severity, detail, fix)

# ─── Bilingual consistency check ───
print("Checking bilingual consistency...", file=sys.stderr)
en_htmls = [f for f in html_files if '/en/' in f]
for en_rel in en_htmls:
    # Map en/about.html -> about.html, en/investment/x.html -> investment/x.html
    parts = en_rel.split('/en/')
    if len(parts) == 2:
        cn_rel = parts[1] if parts[0] == '' else parts[0] + parts[1]
    else:
        continue
    
    if cn_rel in html_files:
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
            
            # Compare email addresses
            en_emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', en_content))
            cn_emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', cn_content))
            if en_emails != cn_emails and en_emails and cn_emails:
                add_issue(en_rel, 0, 'content', 'major',
                    f'双语页面邮箱不一致: EN={en_emails}, CN={cn_emails}',
                    '统一中英文页面的联系邮箱')
            
            # Compare prices
            en_prices = set(re.findall(r'[¥$€£]\s*[\d,]+(?:\.\d+)?(?:\s*[万亿])?', en_content))
            cn_prices = set(re.findall(r'[¥$€£]\s*[\d,]+(?:\.\d+)?(?:\s*[万亿])?', cn_content))
            if en_prices != cn_prices and en_prices and cn_prices:
                add_issue(en_rel, 0, 'content', 'major',
                    f'双语页面价格信息不一致: EN={en_prices}, CN={cn_prices}',
                    '核实并统一中英文页面的价格信息')
        except Exception:
            pass
    else:
        add_issue(en_rel, 0, 'content', 'major',
            f'英文页面缺少对应的中文版本: {cn_rel}',
            f'创建 {cn_rel} 或确认该页面仅需英文版本')

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
