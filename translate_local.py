#!/usr/bin/env python3
"""本地批量翻译 - 不依赖外部API"""
import json, re, subprocess

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

# 扩展翻译词典
DICT = {
    # 导航通用
    '首页': 'Home', '关于我们': 'About Us', '联系我们': 'Contact Us',
    '公司简介': 'Company Profile', '发展历程': 'History', '企业文化': 'Corporate Culture',
    '荣誉资质': 'Honors', '社会责任': 'Social Responsibility', '组织架构': 'Organization',
    '业务板块': 'Business', '新闻中心': 'News', '投资者关系': 'Investor Relations',
    '网站地图': 'Sitemap', '隐私政策': 'Privacy Policy', '使用条款': 'Terms',
    '版权所有': 'Copyright', '保留所有权利': 'All Rights Reserved',
    
    # 游艇相关
    '游艇': 'Yacht', '超级游艇': 'Superyacht', '豪华游艇': 'Luxury Yacht',
    '旗舰系列': 'Flagship Series', '远征系列': 'Expedition Series', '飞桥系列': 'Flybridge Series',
    '运动系列': 'Sport Series', '日间系列': 'Day Series', '君临系列': 'Monarch Series',
    '总长度': 'LOA', '型宽': 'Beam', '吃水': 'Draft', '排水量': 'Displacement',
    '最高航速': 'Max Speed', '巡航速度': 'Cruise Speed', '续航里程': 'Range',
    '客舱数量': 'Cabins', '最大载客': 'Max Guests', '船员人数': 'Crew',
    '建造年份': 'Year Built', '翻新年份': 'Refit Year', '船厂': 'Shipyard',
    '设计师': 'Designer', '发动机': 'Engine', '发电机': 'Generator',
    '燃油类型': 'Fuel Type', '柴油': 'Diesel', '混合动力': 'Hybrid', '纯电动': 'Electric',
    
    # 服务相关
    '全案定制': 'Full Customization', '租赁航线': 'Charter', '托管维保': 'Management',
    '案例展示': 'Cases', '全球合作': 'Partnership', '全系游艇': 'All Yachts',
    '了解更多': 'Learn More', '查看详情': 'View Details', '立即咨询': 'Inquire Now',
    '查看更多': 'View More', '了解详情': 'Learn More', '立即预约': 'Book Now',
    '预约体验': 'Book Experience', '咨询热线': 'Hotline', '尊享热线': 'VIP Hotline',
    '服务热线': 'Service Hotline',
    
    # 公司信息
    '公司地址': 'Address', '商务邮箱': 'Business Email', '办公时间': 'Office Hours',
    '电话': 'Tel', '邮箱': 'Email', '传真': 'Fax', '地址': 'Address', '邮编': 'Postal Code',
    
    # 新闻相关
    '公司动态': 'Company News', '行业资讯': 'Industry News', '媒体报道': 'Media Coverage',
    '公告通知': 'Announcements', '航海生活': 'Yachting Life',
    
    # 常用词
    '年': 'Year', '月': 'Month', '日': 'Day',
    '米': 'm', '节': 'kn', '海里': 'nm', '小时': 'h',
    '起': 'from', '周': 'week',
    '万元': 'Million CNY', '万欧元': 'Million EUR', '万美元': 'Million USD',
    '万元起': 'Million CNY from', '欧元': 'EUR', '美元': 'USD', '人民币': 'CNY',
    
    # 地理位置
    '地中海': 'Mediterranean', '加勒比海': 'Caribbean', '东南亚': 'Southeast Asia',
    '中东': 'Middle East', '北欧': 'Northern Europe', '亚洲': 'Asia', '欧洲': 'Europe',
    '香港': 'Hong Kong', '上海': 'Shanghai', '新加坡': 'Singapore', '迪拜': 'Dubai',
    '摩纳哥': 'Monaco', '迈阿密': 'Miami',
    
    # 状态词
    '新品': 'New', '热门': 'Popular', '推荐': 'Recommended', '全部': 'All',
    '筛选': 'Filter', '排序': 'Sort', '价格': 'Price', '尺寸': 'Size',
    '详情': 'Details', '概述': 'Overview', '规格': 'Specs', '配置': 'Config',
    '参数': 'Parameters', '性能': 'Performance', '内饰': 'Interior', '外观': 'Exterior',
    
    # 其他常见
    '奇幻假期': 'Fantastic Vacation', '加载中': 'Loading', '加载': 'Loading',
    '搜索': 'Search', '输入关键词': 'Enter keywords',
    '上一页': 'Previous', '下一页': 'Next',
    '分享': 'Share', '收藏': 'Favorite', '下载': 'Download',
    '打印': 'Print', '关闭': 'Close',
}

# 更多短语映射
PHRASES = {
    '为您推荐': 'Recommended for You',
    '相关推荐': 'Related',
    '查看全部': 'View All',
    '展开全部': 'Expand All',
    '收起': 'Collapse',
    '暂无数据': 'No Data',
    '暂无内容': 'No Content',
    '敬请期待': 'Coming Soon',
    '正在加载': 'Loading',
    '请稍候': 'Please Wait',
    '操作成功': 'Success',
    '操作失败': 'Failed',
    '确认': 'Confirm',
    '取消': 'Cancel',
    '保存': 'Save',
    '返回': 'Back',
    '继续': 'Continue',
    '开始': 'Start',
    '结束': 'End',
    '提交': 'Submit',
    '发送': 'Send',
    '接收': 'Receive',
    '在线咨询': 'Online Consultation',
    '发送消息': 'Send Message',
    '您的姓名': 'Your Name',
    '您的邮箱': 'Your Email',
    '您的电话': 'Your Phone',
    '您的留言': 'Your Message',
    '感兴趣的方向': 'Area of Interest',
    '产品与服务': 'Products & Services',
}

def smart_translate(text):
    """智能本地翻译"""
    if not text or not text.strip():
        return text
    
    # 无中文，保持原样
    if not any('\u4e00' <= c <= '\u9fff' for c in text):
        return text
    
    # 精确匹配
    if text in DICT:
        return DICT[text]
    if text in PHRASES:
        return PHRASES[text]
    
    # 部分匹配
    result = text
    for zh, en in {**DICT, **PHRASES}.items():
        if zh in result:
            result = result.replace(zh, en)
    
    if result != text:
        return result
    
    # 标点转换
    result = text
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
    
    # 如果还有中文，保持原样（后续可人工校对）
    return result

def main():
    print('\n=== 本地批量翻译 ===\n')
    
    # 加载进度
    try:
        with open(PROGRESS_PATH) as f:
            progress = json.load(f)
        print(f'已有翻译: {len(progress)} 条')
    except:
        progress = {}
    
    # 提取未翻译
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"'
    entries = re.findall(pattern, content)
    
    untranslated = []
    for key, zh, en in entries:
        if zh == en or not en.strip():
            if any('\u4e00' <= c <= '\u9fff' for c in zh):
                untranslated.append({'key': key, 'zh': zh})
    
    print(f'待翻译: {len(untranslated)} 条\n')
    
    # 批量翻译
    count = 0
    for entry in untranslated:
        key = entry['key']
        zh = entry['zh']
        
        if key in progress:
            continue
        
        en = smart_translate(zh)
        progress[key] = en
        count += 1
        
        if count <= 30:
            status = '✓' if en != zh else '○'
            print(f'{status} {zh[:35]} → {en[:35]}')
    
    print(f'\n本地翻译: {count} 条')
    
    # 保存进度
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    
    # 应用翻译
    print('\n应用翻译到 i18n.js...')
    
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
    
    # 验证语法
    r = subprocess.run(['node', '-c', I18N_PATH], capture_output=True, text=True)
    print(f'语法: {r.stdout.strip() or r.stderr.strip() or "OK"}')
    
    # 统计覆盖率
    with open(I18N_PATH) as f:
        content = f.read()
    
    en_values = re.findall(r'"en":\s*"([^"]*)"', content)
    total = len(en_values)
    translated = sum(1 for e in en_values if e.strip() and not any('\u4e00' <= c <= '\u9fff' for c in e))
    
    print(f'\n翻译覆盖率: {translated}/{total} ({translated/total*100:.1f}%)')
    remaining = total - translated
    print(f'剩余未翻译: {remaining} 条')
    
    return translated, total

if __name__ == '__main__':
    main()