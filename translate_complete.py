#!/usr/bin/env python3
"""使用本地词典+API完成剩余翻译"""
import json, time, re, subprocess

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
DICT_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translate_dict.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

# 加载翻译词典
def load_dict():
    """从translate_dict.js提取词典"""
    with open(DICT_PATH) as f:
        content = f.read()
    
    # 提取dict对象
    dict_obj = {}
    pattern = r"'([^']+)':\s*'([^']*)'"
    for match in re.finditer(pattern, content):
        zh, en = match.groups()
        if zh and en and zh != en:
            dict_obj[zh] = en
    return dict_obj

def smart_translate(text, local_dict):
    """智能翻译"""
    if not text or not text.strip():
        return text
    
    # 检查是否包含中文
    has_chinese = any('\u4e00' <= c <= '\u9fff' for c in text)
    if not has_chinese:
        return text  # 无中文，保持原样
    
    # 精确匹配词典
    if text in local_dict:
        return local_dict[text]
    
    # 部分匹配（替换词典中的短语）
    result = text
    for zh, en in sorted(local_dict.items(), key=lambda x: -len(x[0])):
        if zh in result:
            result = result.replace(zh, en)
    
    if result != text:
        return result
    
    # 纯数字/符号
    if not has_chinese:
        return text
    
    # 对于剩余中文，尝试提取并翻译关键词
    return None  # 需要API翻译

def translate_api(text):
    """API翻译（简化版）"""
    import urllib.request, urllib.parse
    
    # 常见短语映射（避免频繁调用API）
    common = {
        '首页': 'Home',
        '关于我们': 'About Us',
        '公司简介': 'Company Profile',
        '发展历程': 'History',
        '企业文化': 'Corporate Culture',
        '荣誉资质': 'Honors',
        '社会责任': 'Social Responsibility',
        '业务板块': 'Business',
        '新闻中心': 'News Center',
        '联系我们': 'Contact Us',
        '在线咨询': 'Online Consultation',
        '了解更多': 'Learn More',
        '查看详情': 'View Details',
        '立即咨询': 'Inquire Now',
        '查看更多': 'View More',
        '了解详情': 'Learn More',
        '立即预约': 'Book Now',
        '咨询热线': 'Hotline',
        '服务热线': 'Service Hotline',
        '尊享热线': 'VIP Hotline',
        '公司地址': 'Address',
        '商务邮箱': 'Business Email',
        '办公时间': 'Office Hours',
        '产品与服务': 'Products & Services',
        '投资者关系': 'Investor Relations',
        '公司动态': 'Company News',
        '行业资讯': 'Industry News',
        '媒体报道': 'Media Coverage',
        '公告通知': 'Announcements',
        '航海生活': 'Yachting Life',
        '全系游艇': 'All Yachts',
        '全案定制': 'Customization',
        '租赁航线': 'Charter Routes',
        '托管维保': 'Management',
        '案例展示': 'Cases',
        '全球合作': 'Partnership',
        '网站地图': 'Sitemap',
        '隐私政策': 'Privacy Policy',
        '使用条款': 'Terms of Use',
        '版权所有': 'Copyright',
        '保留所有权利': 'All Rights Reserved',
    }
    
    if text in common:
        return common[text]
    
    # 简单规则翻译
    # 移除/转换标点
    result = text
    result = result.replace('，', ', ')
    result = result.replace('。', '. ')
    result = result.replace('：', ': ')
    result = result.replace('；', '; ')
    result = result.replace('！', '!')
    result = result.replace('？', '?')
    
    # 尝试API
    try:
        encoded = urllib.parse.quote(text[:200])
        url = f'https://api.mymemory.translated.net/get?q={encoded}&langpair=zh-CN|en'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode('utf-8'))
            return data['responseData']['translatedText']
    except:
        pass
    
    return None

def extract_untranslated():
    """提取未翻译条目"""
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"'
    entries = re.findall(pattern, content)
    
    untranslated = []
    for key, zh, en in entries:
        if zh == en or not en.strip():
            if any('\u4e00' <= c <= '\u9fff' for c in zh):
                untranslated.append({'key': key, 'zh': zh})
    
    return untranslated

def apply_translations(translations):
    """应用翻译到i18n.js"""
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    count = 0
    for key, en in translations.items():
        if not en:
            continue
        escaped_key = key.replace('\\', '\\\\').replace('"', '\\"')
        escaped_en = en.replace('\\', '\\\\').replace('"', '\\"')
        pattern = rf'("{escaped_key}":\s*\{{\s*"zh":\s*"[^"]*",\s*"en":\s*")[^"]*(")'
        replacement = rf'\g<1>{escaped_en}\g<2>'
        new_content, n = re.subn(pattern, replacement, content)
        if n > 0:
            content = new_content
            count += 1
    
    with open(I18N_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return count

print('\n=== 本地词典 + API 翻译 ===\n')

# 加载词典
print('加载本地词典...')
local_dict = load_dict()
print(f'本地词典: {len(local_dict)} 条')

# 加载进度
try:
    with open(PROGRESS_PATH) as f:
        progress = json.load(f)
    print(f'已有翻译: {len(progress)} 条')
except:
    progress = {}

# 提取未翻译
untranslated = extract_untranslated()
print(f'待翻译: {len(untranslated)} 条\n')

# 第一遍：本地词典匹配
print('=== 第一遍：本地词典匹配 ===')
matched = 0
for entry in untranslated:
    key = entry['key']
    zh = entry['zh']
    
    if key in progress:
        continue
    
    en = smart_translate(zh, local_dict)
    if en:
        progress[key] = en
        matched += 1
        if matched <= 20:
            print(f'✓ {zh[:30]} → {en[:30]}')

print(f'\n本地词典匹配: {matched} 条')

# 保存进度
with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
    json.dump(progress, f, ensure_ascii=False, indent=2)

# 第二遍：API翻译剩余
remaining = [e for e in untranslated if e['key'] not in progress]
print(f'\n=== 第二遍：API翻译 {len(remaining)} 条 ===\n')

if remaining:
    for i, entry in enumerate(remaining):
        key = entry['key']
        zh = entry['zh']
        
        en = translate_api(zh)
        if en:
            progress[key] = en
            print(f'[{i+1}/{len(remaining)}] ✓ {zh[:30]} → {en[:30]}')
        else:
            progress[key] = zh  # 保留原文
            print(f'[{i+1}/{len(remaining)}] ○ 保留: {zh[:30]}')
        
        if (i+1) % 30 == 0:
            with open(PROGRESS_PATH, 'w') as f:
                json.dump(progress, f, ensure_ascii=False, indent=2)
            print(f'  保存进度: {i+1}/{len(remaining)}\n')
        
        time.sleep(0.5)

# 最终应用
print('\n=== 应用翻译到 i18n.js ===')
count = apply_translations(progress)
print(f'应用: {count} 条')

# 验证
r = subprocess.run(['node', '-c', I18N_PATH], capture_output=True, text=True)
print(f'语法: {r.stdout.strip() or r.stderr.strip() or "OK"}')

# 统计
with open(I18N_PATH) as f:
    content = f.read()
entries = re.findall(r'"en":\s*"([^"]*)"', content)
translated = sum(1 for e in entries if e.strip() and any('\u4e00' <= c <= '\u9fff' for c in e) == False)
total = len(entries)
print(f'\n翻译覆盖率: {translated}/{total} ({translated/total*100:.1f}%)')

print(f'\n✅ 完成! 共处理 {len(progress)} 条翻译')