#!/usr/bin/env python3
"""完成 100% 翻译 - 批量处理剩余 5945 条"""
import json
import re
import time
import subprocess
import urllib.request
import urllib.parse

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

# 扩展本地词典
LOCAL_DICT = {
    # 导航
    '首页': 'Home', '关于我们': 'About Us', '联系我们': 'Contact Us',
    '公司简介': 'Company Profile', '发展历程': 'History', '企业文化': 'Corporate Culture',
    '荣誉资质': 'Honors', '社会责任': 'Social Responsibility',
    '业务板块': 'Business', '新闻中心': 'News', '投资者关系': 'Investor Relations',
    '网站地图': 'Sitemap', '隐私政策': 'Privacy Policy', '使用条款': 'Terms of Use',
    
    # 服务
    '全案定制': 'Full Customization', '租赁航线': 'Charter Routes', '托管维保': 'Management',
    '案例展示': 'Case Studies', '全球合作': 'Global Partnership', '全系游艇': 'All Yachts',
    '了解更多': 'Learn More', '查看详情': 'View Details', '立即咨询': 'Inquire Now',
    '查看更多': 'View More', '了解详情': 'Learn More', '立即预约': 'Book Now',
    '在线咨询': 'Online Consultation', '咨询热线': 'Hotline', '服务热线': 'Service Hotline',
    
    # 公司信息
    '公司地址': 'Address', '商务邮箱': 'Business Email', '办公时间': 'Office Hours',
    '电话': 'Tel', '邮箱': 'Email', '传真': 'Fax', '地址': 'Address',
    
    # 常用词
    '年': 'Year', '月': 'Month', '日': 'Day', '周': 'Week',
    '米': 'm', '节': 'kn', '海里': 'nm', '小时': 'h',
    '万元': 'Million CNY', '万欧元': 'Million EUR', '万美元': 'Million USD',
    
    # 游艇
    '游艇': 'Yacht', '超级游艇': 'Superyacht', '豪华游艇': 'Luxury Yacht',
    '旗舰系列': 'Flagship Series', '远征系列': 'Expedition Series',
    '总长度': 'LOA', '型宽': 'Beam', '吃水': 'Draft',
    '最高航速': 'Max Speed', '巡航速度': 'Cruise Speed',
    
    # 地理
    '地中海': 'Mediterranean', '加勒比海': 'Caribbean', '东南亚': 'Southeast Asia',
    '中东': 'Middle East', '北欧': 'Northern Europe',
    
    # 其他
    '奇幻假期': 'Fantastic Vacation',
    '版权所有': 'Copyright', '保留所有权利': 'All Rights Reserved',
    '加载中': 'Loading', '搜索': 'Search',
}

def remove_emoji(text):
    """移除 emoji"""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text).strip()

def translate_with_api(text):
    """使用 MyMemory API 翻译"""
    if not text or not text.strip():
        return text
    
    try:
        encoded = urllib.parse.quote(text[:500])
        url = f'https://api.mymemory.translated.net/get?q={encoded}&langpair=zh-CN|en'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            result = data['responseData']['translatedText']
            
            # 检查是否翻译成功（返回的不是原文）
            if result and result != text:
                return result
    except Exception as e:
        pass
    
    return None

def smart_translate(text):
    """智能翻译：本地词典 + 规则"""
    if not text or not text.strip():
        return text
    
    # 无中文，保持原样
    if not any('\u4e00' <= c <= '\u9fff' for c in text):
        return text
    
    # 精确匹配
    if text in LOCAL_DICT:
        return LOCAL_DICT[text]
    
    # 移除 emoji
    text_no_emoji = remove_emoji(text)
    if text_no_emoji in LOCAL_DICT:
        return LOCAL_DICT[text_no_emoji]
    
    # 部分匹配替换
    result = text
    for zh, en in sorted(LOCAL_DICT.items(), key=lambda x: -len(x[0])):
        if zh in result:
            result = result.replace(zh, en)
    
    # 如果替换后没有中文了，返回结果
    if not any('\u4e00' <= c <= '\u9fff' for c in result):
        return result
    
    # 标点转换
    result = result.replace('，', ', ').replace('。', '. ').replace('：', ': ')
    result = result.replace('；', '; ').replace('！', '!').replace('？', '?')
    result = result.replace('、', ', ').replace('（', ' (').replace('）', ')')
    
    return result

def apply_to_i18n(progress):
    """应用翻译到 i18n.js"""
    print('\n应用翻译到 i18n.js...')
    
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    applied = 0
    new_lines = []
    
    for line in lines:
        match = re.match(r'^(\s*)"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"\s*\},?.*$', line)
        
        if match:
            indent = match.group(1)
            key = match.group(2)
            zh_val = match.group(3)
            
            if key in progress and progress[key]:
                en_new = progress[key].replace('\\', '\\\\').replace('"', '\\"')
                new_line = f'{indent}"{key}": {{ "zh": "{zh_val}", "en": "{en_new}" }},\n'
                new_lines.append(new_line)
                applied += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    with open(I18N_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f'✓ 应用 {applied} 条')
    
    # 验证语法
    result = subprocess.run(['node', '-c', I18N_PATH], capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print('✅ 语法正确')
        return True
    else:
        print(f'❌ 语法错误:\n{result.stderr}')
        return False

def main():
    print('\n=== 完成 100% 翻译 ===\n')
    
    # 加载进度
    try:
        with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
            progress = json.load(f)
        print(f'✓ 加载进度: {len(progress)} 条')
    except:
        progress = {}
        print('✓ 新建进度文件')
    
    # 读取 i18n.js，找出未翻译条目
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"'
    entries = re.findall(pattern, content)
    
    untranslated = []
    for key, zh, en in entries:
        # 判断是否需要翻译
        has_chinese_en = any('\u4e00' <= c <= '\u9fff' for c in en)
        is_empty = not en.strip()
        
        if has_chinese_en or is_empty:
            if key not in progress or not progress[key]:
                untranslated.append({'key': key, 'zh': zh})
    
    print(f'待翻译: {len(untranslated)} 条\n')
    
    if not untranslated:
        print('✅ 全部翻译完成!')
        return True
    
    # 第一阶段：本地词典翻译
    print('=== 第一阶段：本地词典 ===')
    local_count = 0
    for entry in untranslated:
        key = entry['key']
        zh = entry['zh']
        
        if key in progress and progress[key]:
            continue
        
        en = smart_translate(zh)
        
        # 检查是否成功翻译（没有中文了）
        if en and not any('\u4e00' <= c <= '\u9fff' for c in en):
            progress[key] = en
            local_count += 1
            
            if local_count <= 20:
                print(f'  ✓ {zh[:35]} → {en[:35]}')
    
    print(f'\n✓ 本地翻译: {local_count} 条')
    
    # 保存进度
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    
    # 应用已翻译的
    apply_to_i18n(progress)
    
    # 第二阶段：API 翻译（分批处理）
    remaining = [e for e in untranslated if e['key'] not in progress or not progress[e['key']]]
    
    if remaining:
        print(f'\n=== 第二阶段：API 翻译 ({len(remaining)} 条) ===')
        print('使用 MyMemory API（免费，限制宽松）\n')
        
        api_count = 0
        for i, entry in enumerate(remaining):
            key = entry['key']
            zh = entry['zh']
            
            # 清理文本
            zh_clean = remove_emoji(zh)
            
            en = translate_with_api(zh_clean)
            
            if en:
                progress[key] = en
                api_count += 1
                print(f'[{i+1}/{len(remaining)}] ✓ {zh[:30]} → {en[:30]}')
            else:
                # API 失败，保留原文
                progress[key] = zh_clean
                print(f'[{i+1}/{len(remaining)}] ○ 保留原文')
            
            # 每 50 条保存一次
            if (i + 1) % 50 == 0:
                with open(PROGRESS_PATH, 'w') as f:
                    json.dump(progress, f, ensure_ascii=False, indent=2)
                print(f'  保存进度: {i+1}/{len(remaining)}\n')
            
            # 延迟避免速率限制
            time.sleep(1)
        
        print(f'\n✓ API 翻译: {api_count} 条')
        
        # 最终保存和应用
        with open(PROGRESS_PATH, 'w') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
        
        apply_to_i18n(progress)
    
    # 最终统计
    print('\n=== 最终统计 ===')
    with open(I18N_PATH, 'r') as f:
        content = f.read()
    
    entries = re.findall(r'"en":\s*"([^"]*)"', content)
    total = len(entries)
    translated = sum(1 for e in entries if e.strip() and not any('\u4e00' <= c <= '\u9fff' for c in e))
    
    print(f'总条目: {total}')
    print(f'已翻译: {translated} ({translated/total*100:.1f}%)')
    print(f'未翻译: {total - translated}')
    
    if translated == total:
        print('\n🎉 100% 翻译完成!')
        return True
    else:
        print(f'\n⚠️ 还有 {total - translated} 条未翻译')
        return False

if __name__ == '__main__':
    success = main()
    if success:
        print('\n✅ 可以提交代码了!')
    else:
        print('\n⚠️ 需要继续翻译')