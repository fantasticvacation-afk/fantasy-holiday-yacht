#!/usr/bin/env python3
"""完善翻译 - 处理剩余6599条"""
import json, re, subprocess, time, urllib.request, urllib.parse

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

# 更完整的翻译词典
FULL_DICT = {
    # 品牌与公司名
    '奇幻假期': 'Fantastic Vacation', 'FANTASTIC VACATION': 'FANTASTIC VACATION',
    '奇幻假期实业有限公司': 'Fantastic Vacation Industrial Co., Ltd.',
    'FANTASTIC VACATION INDUSTRIAL CO., LTD.': 'FANTASTIC VACATION INDUSTRIAL CO., LTD.',
    
    # 导航与页面元素
    '首页': 'Home', '关于我们': 'About Us', '联系我们': 'Contact Us',
    '公司简介': 'Company Profile', '发展历程': 'History', '企业文化': 'Corporate Culture',
    '荣誉资质': 'Honors & Qualifications', '社会责任': 'Social Responsibility', '组织架构': 'Organization',
    '业务板块': 'Business', '新闻中心': 'News', '投资者关系': 'Investor Relations',
    '网站地图': 'Sitemap', '隐私政策': 'Privacy Policy', '使用条款': 'Terms of Use',
    '版权所有': 'Copyright', '保留所有权利': 'All Rights Reserved',
    
    # 游艇类型
    '游艇': 'Yacht', '超级游艇': 'Superyacht', '豪华游艇': 'Luxury Yacht',
    '旗舰系列': 'Flagship Series', '远征系列': 'Expedition Series', '飞桥系列': 'Flybridge Series',
    '运动系列': 'Sport Series', '君临系列': 'Monarch Series', '日间系列': 'Day Cruiser Series',
    '极光号': 'Aurora', '星辰号': 'Stellar', '天际号': 'Horizon',
    
    # 服务类型
    '全案定制': 'Full Customization', '租赁航线': 'Charter Routes', '托管维保': 'Management & Maintenance',
    '案例展示': 'Case Studies', '全球合作': 'Global Partnership', '全系游艇': 'All Yachts',
    '客户案例': 'Client Cases', '极地航线': 'Polar Routes', '环保科技': 'Eco Technology',
    
    # 规格参数
    '总长度': 'LOA', '型宽': 'Beam', '吃水': 'Draft', '排水量': 'Displacement',
    '最高航速': 'Max Speed', '巡航速度': 'Cruise Speed', '续航里程': 'Range',
    '客舱数量': 'Cabins', '最大载客': 'Max Guests', '船员人数': 'Crew',
    '建造年份': 'Year Built', '翻新年份': 'Refit Year', '船厂': 'Shipyard',
    '设计师': 'Designer', '发动机': 'Engine', '发电机': 'Generator',
    '燃油类型': 'Fuel Type', '柴油': 'Diesel', '混合动力': 'Hybrid', '纯电动': 'Electric',
    '冰级认证': 'Ice Class', '冰级钢制船体': 'Ice-class Steel Hull',
    '客舱套房': 'Guest Suites', '极地': 'Polar',
    
    # 地理位置
    '地中海': 'Mediterranean', '加勒比海': 'Caribbean', '东南亚': 'Southeast Asia',
    '中东': 'Middle East', '北欧': 'Northern Europe', '亚洲': 'Asia', '欧洲': 'Europe',
    '南极': 'Antarctic', '阿拉斯加': 'Alaska', '香港': 'Hong Kong', '上海': 'Shanghai',
    '新加坡': 'Singapore', '迪拜': 'Dubai', '摩纳哥': 'Monaco', '迈阿密': 'Miami',
    
    # 常见动词
    '查看': 'View', '了解': 'Learn', '咨询': 'Inquire', '预约': 'Book',
    '探索': 'Explore', '发现': 'Discover', '体验': 'Experience', '享受': 'Enjoy',
    '提供': 'Provide', '打造': 'Create', '实现': 'Achieve', '获得': 'Gain',
    
    # 常见形容词
    '专业': 'Professional', '专属': 'Exclusive', '定制': 'Custom', '豪华': 'Luxury',
    '顶级': 'Top-tier', '全球': 'Global', '高端': 'High-end', '优质': 'Premium',
    
    # 数量单位
    '年': 'Year', '月': 'Month', '日': 'Day', '周': 'Week',
    '米': 'm', '节': 'kn', '海里': 'nm', '小时': 'Hour',
    '万元': 'Million CNY', '万欧元': 'Million EUR', '万美元': 'Million USD',
    
    # 常见短语
    '了解更多': 'Learn More', '查看详情': 'View Details', '立即咨询': 'Inquire Now',
    '查看更多': 'View More', '了解详情': 'Learn More', '立即预约': 'Book Now',
    '在线咨询': 'Online Consultation', '发送消息': 'Send Message',
    '咨询热线': 'Consultation Hotline', '尊享热线': 'VIP Hotline', '服务热线': 'Service Hotline',
    '公司地址': 'Company Address', '商务邮箱': 'Business Email', '办公时间': 'Office Hours',
    '电话': 'Tel', '邮箱': 'Email', '传真': 'Fax', '地址': 'Address', '邮编': 'Postal Code',
    
    # 公司动态相关
    '公司动态': 'Company News', '行业资讯': 'Industry News', '媒体报道': 'Media Coverage',
    '公告通知': 'Announcements', '航海生活': 'Yachting Life',
    '产品与服务': 'Products & Services',
    
    # 案例相关
    '案例概览': 'Case Overview', '服务类型': 'Service Type', '服务海域': 'Service Area',
    '设计→建造→交付': 'Design → Build → Deliver', '项目背景': 'Project Background',
    '核心诉求': 'Core Requirements', '项目难点': 'Project Challenges',
    '核心亮点': 'Key Highlights', '客户背景': 'Client Background',
    '环保企业家': 'Eco Entrepreneur', '极地探险': 'Polar Expedition',
    '科研支持': 'Research Support', '卫星通讯': 'Satellite Communication',
    '直升机停机坪': 'Helipad', '数据采集': 'Data Collection',
    
    # 行业荣誉
    '行业荣誉': 'Industry Honors', '年度提名': 'Annual Nomination',
    '最佳游艇服务商': 'Best Yacht Service Provider',
    
    # 其他
    '为您推荐': 'Recommended for You', '相关推荐': 'Related',
    '查看全部': 'View All', '展开全部': 'Expand All', '收起': 'Collapse',
    '暂无数据': 'No Data', '暂无内容': 'No Content', '敬请期待': 'Coming Soon',
    '正在加载': 'Loading', '请稍候': 'Please Wait',
    '加载中': 'Loading', '搜索': 'Search', '输入关键词': 'Enter Keywords',
}

# emoji映射（移除emoji或替换）
EMOJI_MAP = {
    '📋': '', '🎯': '', '⚠️': '', '💡': '', '🌟': '', '⭐': '',
    '📞': '', '📧': '', '💬': '', '🔍': '', '📱': '', '🌐': '',
    '🚀': '', '⚓': '', '🎨': '', '🌍': '', '🛡️': '', '☀️': '',
    '❄️': '', '🌊': '', '🔥': '', '✨': '', '💎': '',
}

def translate_local(text):
    """本地智能翻译"""
    if not text or not text.strip():
        return text
    
    # 无中文
    if not any('\u4e00' <= c <= '\u9fff' for c in text):
        return text
    
    # 精确匹配
    if text in FULL_DICT:
        return FULL_DICT[text]
    
    # 移除emoji
    result = text
    for emoji, replacement in EMOJI_MAP.items():
        result = result.replace(emoji, replacement)
    result = result.strip()
    
    # 短语替换
    for zh, en in sorted(FULL_DICT.items(), key=lambda x: -len(x[0])):
        if zh in result:
            result = result.replace(zh, en)
    
    # 标点转换
    result = result.replace('，', ', ')
    result = result.replace('。', '. ')
    result = result.replace('：', ': ')
    result = result.replace('；', '; ')
    result = result.replace('！', '!')
    result = result.replace('？', '?')
    result = result.replace('、', ', ')
    result = result.replace('（', ' (')
    result = result.replace('）', ')')
    result = result.replace('【', '[')
    result = result.replace('】', ']')
    result = result.replace('→', ' → ')
    
    # 清理多余空格
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

def translate_api(text):
    """API翻译作为后备"""
    if not text:
        return text
    
    try:
        encoded = urllib.parse.quote(text[:500])
        url = f'https://api.mymemory.translated.net/get?q={encoded}&langpair=zh-CN|en'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            return data['responseData']['translatedText']
    except:
        return None

def main():
    print('\n=== 完善翻译 - 剩余6599条 ===\n')
    
    # 加载进度
    try:
        with open(PROGRESS_PATH) as f:
            progress = json.load(f)
    except:
        progress = {}
    
    # 提取未翻译
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"'
    entries = re.findall(pattern, content)
    
    untranslated = []
    for key, zh, en in entries:
        if any('\u4e00' <= c <= '\u9fff' for c in en):
            untranslated.append({'key': key, 'zh': zh, 'en': en})
    
    print(f'待处理: {len(untranslated)} 条\n')
    
    # 第一遍：本地翻译
    print('=== 本地翻译 ===')
    local_count = 0
    for entry in untranslated:
        key = entry['key']
        zh = entry['zh']
        
        if key in progress:
            continue
        
        en = translate_local(zh)
        if en and not any('\u4e00' <= c <= '\u9fff' for c in en):
            progress[key] = en
            local_count += 1
            if local_count <= 20:
                print(f'✓ {zh[:40]} → {en[:40]}')
    
    print(f'\n本地翻译: {local_count} 条')
    
    # 保存进度
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    
    # 应用翻译
    print('\n应用翻译...')
    
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    applied = 0
    for key, en in progress.items():
        if not en:
            continue
        escaped_key = key.replace('\\', '\\\\').replace('"', '\\"')
        escaped_en = en.replace('\\', '\\\\').replace('"', '\\"')
        pattern = rf'("{escaped_key}":\s*\{{\s*"zh":\s*"[^"]*",\s*"en":\s*")[^"]*(")'
        replacement = rf'\g<1>{escaped_en}\g<2>'
        new_content, n = re.subn(pattern, replacement, content)
        if n > 0:
            content = new_content
            applied += 1
    
    with open(I18N_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'应用: {applied} 条')
    
    # 验证
    r = subprocess.run(['node', '-c', I18N_PATH], capture_output=True, text=True)
    print(f'语法: {r.stdout.strip() or r.stderr.strip() or "OK"}')
    
    # 统计
    with open(I18N_PATH) as f:
        content = f.read()
    
    en_values = re.findall(r'"en":\s*"([^"]*)"', content)
    total = len(en_values)
    translated = sum(1 for e in en_values if e.strip() and not any('\u4e00' <= c <= '\u9fff' for c in e))
    
    print(f'\n翻译覆盖率: {translated}/{total} ({translated/total*100:.1f}%)')
    remaining = total - translated
    print(f'剩余未翻译: {remaining} 条')
    
    # 如果还有剩余，尝试API翻译一部分
    if remaining > 0:
        print(f'\n=== API翻译（限制100条）===')
        
        # 重新提取未翻译
        api_count = 0
        for entry in untranslated:
            if api_count >= 100:
                break
            
            key = entry['key']
            zh = entry['zh']
            
            if key in progress:
                continue
            
            en = translate_api(zh)
            if en:
                progress[key] = en
                api_count += 1
                print(f'[{api_count}] ✓ {zh[:30]} → {en[:30]}')
                time.sleep(0.5)
        
        if api_count > 0:
            # 保存并应用
            with open(PROGRESS_PATH, 'w') as f:
                json.dump(progress, f, ensure_ascii=False, indent=2)
            
            # 应用
            with open(I18N_PATH, 'r') as f:
                content = f.read()
            
            for key, en in list(progress.items())[-api_count:]:
                if not en:
                    continue
                escaped_key = key.replace('\\', '\\\\').replace('"', '\\"')
                escaped_en = en.replace('\\', '\\\\').replace('"', '\\"')
                pattern = rf'("{escaped_key}":\s*\{{\s*"zh":\s*"[^"]*",\s*"en":\s*")[^"]*(")'
                replacement = rf'\g<1>{escaped_en}\g<2>'
                content = re.sub(pattern, replacement, content)
            
            with open(I18N_PATH, 'w') as f:
                f.write(content)
            
            print(f'API翻译应用: {api_count} 条')
    
    # 最终统计
    with open(I18N_PATH) as f:
        content = f.read()
    
    en_values = re.findall(r'"en":\s*"([^"]*)"', content)
    total = len(en_values)
    translated = sum(1 for e in en_values if e.strip() and not any('\u4e00' <= c <= '\u9fff' for c in e))
    
    print(f'\n=== 最终结果 ===')
    print(f'翻译覆盖率: {translated}/{total} ({translated/total*100:.1f}%)')
    print(f'总处理: {len(progress)} 条')

if __name__ == '__main__':
    main()