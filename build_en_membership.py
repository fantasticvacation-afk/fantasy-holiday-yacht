#!/usr/bin/env python3
"""Generate EN versions of membership/ sub-pages from CN sources."""
import re, os

SRC = 'membership'
DST = 'en/membership'

# Common nav/footer translations (ordered to avoid partial-match issues)
NAV_TRANSLATIONS = [
    # Nav logo
    ('<span class="nav-logo-text">奇幻假期 <em>FANTASTIC VACATION</em></span>',
     '<span class="nav-logo-text">Fantastic Vacation <em>FANTASTIC VACATION</em></span>'),
    # aria-labels
    ('aria-label="奇幻假期首页"', 'aria-label="Fantastic Vacation Home"'),
    ('aria-label="主导航"', 'aria-label="Main Navigation"'),
    ('aria-label="主导航菜单"', 'aria-label="Main Navigation"'),
    ('aria-label="全系游艇子菜单"', 'aria-label="Yacht Submenu"'),
    ('aria-label="定制服务子菜单"', 'aria-label="Services Submenu"'),
    ('aria-label="关于我们子菜单"', 'aria-label="About Submenu"'),
    ('aria-label="资讯与合作子菜单"', 'aria-label="News & IR Submenu"'),
    # Nav items
    ('>首页<', '>Home<'),
    ('>全系游艇<', '>Yachts<'),
    ('>君临系列<', '>Sovereign Series<'),
    ('>远征系列<', '>Expedition Series<'),
    ('>飞桥系列<', '>Flybridge Series<'),
    ('>日间系列<', '>Day Cruiser Series<'),
    ('>定制服务<', '>Services<'),
    ('>全案定制<', '>Custom Yachts<'),
    ('>租赁航线<', '>Charter Routes<'),
    ('>托管维保<', '>Management<'),
    ('>案例展示<', '>Cases<'),
    ('>关于我们<', '>About<'),
    ('>公司简介<', '>Company<'),
    ('>发展历程<', '>Milestones<'),
    ('>企业文化<', '>Culture<'),
    ('>组织架构<', '>Organization<'),
    ('>荣誉资质<', '>Honors<'),
    ('>社会责任<', '>ESG<'),
    ('>资讯与合作<', '>News & IR<'),
    ('>新闻资讯<', '>News<'),
    ('>投资者关系<', '>IR<'),
    ('>全球合作<', '>Partnerships<'),
    ('👑 尊享会员', '👑 Membership'),
    ('>联系我们<', '>Contact<'),
    # Search
    ('title="搜索"', 'title="Search"'),
    ('aria-label="搜索"', 'aria-label="Search"'),
    ('placeholder="搜索产品、新闻、案例..."', 'placeholder="Search yachts, news, cases..."'),
    # Search suggestions
    ('→ 探索全系游艇', '→ Explore Our Fleet'),
    ('→ 定制专属游艇', '→ Custom Your Own Yacht'),
    ('→ 浏览全球航线', '→ Browse Global Routes'),
    ('→ 联系专业顾问', '→ Contact Our Consultants'),
    # Dark mode
    ('title="深色模式"', 'title="Dark Mode"'),
    ('aria-label="切换深色模式"', 'aria-label="Toggle Dark Mode"'),
    ('aria-label="打开移动端菜单"', 'aria-label="Open Mobile Menu"'),
    # Mobile menu
    ('<span>奇幻假期</span>', '<span>FANTASTIC VACATION</span>'),
    ('<span>FANTASTIC VACATION</span>\n</div>\n<a class="mobile-nav-link" href="index.html">Home</a>', '<span>FANTASTIC VACATION</span>\n</div>\n<a class="mobile-nav-link" href="../index.html">Home</a>'),
    # Mobile nav groups (Yachts)
    ('<div class="mobile-nav-group-title">全系游艇</div>', '<div class="mobile-nav-group-title">Yachts</div>'),
    ('<div class="mobile-nav-group-title">关于我们</div>', '<div class="mobile-nav-group-title">About</div>'),
    ('<div class="mobile-nav-group-title">新闻资讯</div>', '<div class="mobile-nav-group-title">News &amp; IR</div>'),
    # Mobile nav links using href context (already translated via >...< pattern above)
    # Mobile menu footer
    ('🌐 English Version', '🌐 中文'),
    ('电话：', 'Tel: '),
    ('邮箱：', 'Email: '),
    # Footer social titles
    ('title="微信公众号"', 'title="WeChat"'),
    ('title="微博"', 'title="Weibo"'),
    ('title="抖音"', 'title="TikTok"'),
    # Footer column titles (both footer-template and index variants)
    ('快速导航', 'Quick Links'),
    ('联系我们', 'Contact Us'),
    ('资质与合作', 'Certifications & Partners'),
    ('公司地址', 'Address'),
    ('广东省深圳市宝安区<br/>松岗工业园1号', 'Bao\'an District<br/>No.1 Songgang Industrial Park'),
    ('咨询热线', 'Hotline'),
    ('商务邮箱', 'Business Email'),
    ('传真', 'Fax'),
    # Footer button
    ('在线咨询', 'Online Consultation'),
    # Footer slogan
    ('「探索全球，不负假期」<br/>全球一体化高端游艇定制与私人海享生活缔造者',
     '"Exploring the World, Fulfilling Every Journey"<br/>Global Luxury Yacht Customization & Private Maritime Lifestyle Creator'),
    # Footer desc
    ('奇幻假期实业有限公司深耕高端游艇行业15年，为200+全球高净值客户提供游艇定制、租赁、托管全产业链一站式服务。',
     'Fantastic Vacation Industrial Co. has served 200+ global HNW clients across the full yacht lifecycle — customization, charter & management — for 15 years.'),
    # Footer logo name
    ('>奇幻假期</div>', '>Fantastic Vacation</div>'),
    # Footer certs (use the ">...<" pattern for precision with data-i18n)
    ('>ISO 9001质量管理体系认证<', '>ISO 9001 Quality Management System<'),
    ('>意大利Ferretti集团授权经销商<', '>Authorized Ferretti Group Dealer<'),
    ('>荷兰Feadship技术合作伙伴<', '>Feadship Technical Partner<'),
    ('>地中海船坞协会认证会员<', '>Mediterranean Marina Association Member<'),
    ('>亚洲最佳游艇服务商三连冠<', '>Asia\'s Best Yacht Service Provider (3 Consecutive Years)<'),
    # Footer recruit
    ('加入我们 · 招聘职位', 'Join Us · Careers'),
    # Footer copyright
    ('© 2020-2026 奇幻假期实业有限公司 FANTASTIC VACATION INDUSTRIAL CO., LTD. 保留所有权利。',
     '© 2020-2026 Fantastic Vacation Industrial Co., Ltd. All rights reserved.'),
    # Footer legal links
    ('>隐私政策<', '>Privacy Policy<'),
    ('>使用条款<', '>Terms of Use<'),
    ('>网站地图<', '>Sitemap<'),
    # Nav Yachts
    ('>全系游艇<', '>Yachts<'),
    # Nav membership button
    ('👑 Membership<', '👑 Membership<'),
    ('尊享会员<', 'Membership<'),
    # Footer Quick Links section items
    ('>首页<', '>Home<'),
]

# Path fixes
PATH_FIXES = [
    # CSS
    ('href="../style.css"', 'href="../../style.css"'),
    # Favicon (both variants)
    ('href="favicon.svg"', 'href="../../favicon.svg"'),
    ('href="../favicon.svg"', 'href="../../favicon.svg"'),
    # JS
    ('src="../i18n.js"', 'src="../../i18n.js"'),
    ('src="../main.js"', 'src="../../main.js"'),
]

# Root-file link fixes: files in membership/ that use ../ to reach root →
# from en/membership/ need ../../ to reach root
ROOT_FILE_LINKS = [
    'yachts-sovereign.html',
    'yachts-expedition.html',
    'yachts-flybridge.html',
    'yachts-daycruiser.html',
    'about-history.html',
    'about-culture.html',
    'about-structure.html',
    'about-responsibility.html',
    'press.html',
]

def fix_root_links(content):
    """Change ../rootfile.html → ../../rootfile.html for root-only files."""
    # Also fix mobile menu links like href="yachts-sovereign.html" → href="../../yachts-sovereign.html"
    for fname in ROOT_FILE_LINKS:
        content = content.replace(f'href="../{fname}"', f'href="../../{fname}"')
        # Mobile menu: href="yachts-sovereign.html" → ../../ since en/membership/
        content = content.replace(f'href="{fname}"', f'href="../../{fname}"')
    return content

# Lang switch replacement
LANG_SWITCH_CN = '<a class="lang-switch-btn" href="../en/index.html" title="切换到英文版 (Switch to English)" aria-label="切换到英文版">EN</a>'
LANG_SWITCH_EN = '<a class="lang-switch-btn" href="../../index.html" title="Switch to Chinese" aria-label="Switch to Chinese">中文</a>'

# Mobile lang switch
MOBILE_LANG_CN = 'href="en/index.html"'
MOBILE_LANG_EN = 'href="../../index.html"'

PAGES = [
    'membership-apply.html',
    'membership-faq.html',
    'membership-process.html',
    'membership-compare.html',
    'membership-tiers.html',
    'membership-tier1.html',
    'membership-tier2.html',
    'membership-tier3.html',
    'membership-tier4.html',
    'membership-tier5.html',
]

for page in PAGES:
    src_path = os.path.join(SRC, page)
    dst_path = os.path.join(DST, page)

    if not os.path.exists(src_path):
        print(f'⚠️  Source not found: {src_path}, skipping')
        continue

    with open(src_path, 'r') as f:
        content = f.read()

    # 1. Change html lang
    content = content.replace('<html lang="zh-CN">', '<html lang="en">')

    # 2. Apply path fixes
    for old, new in PATH_FIXES:
        content = content.replace(old, new)

    # 3. Fix root-file links
    content = fix_root_links(content)

    # 4. Apply nav/footer translations
    for old, new in NAV_TRANSLATIONS:
        content = content.replace(old, new)

    # 5. Replace lang switches
    content = content.replace(LANG_SWITCH_CN, LANG_SWITCH_EN)
    content = content.replace(MOBILE_LANG_CN, MOBILE_LANG_EN)

    # 6. Fix mobile menu href="index.html" → href="../index.html"
    # (already done via NAV_TRANSLATIONS above for the Home link in mobile menu)

    # 7. Fix mobile nav links that go to en/ pages → need ../ prefix
    en_page_links = ['index.html', 'about.html', 'custom.html', 'charter.html',
                     'management.html', 'cases.html', 'honors.html', 'news.html',
                     'ir.html', 'partnership.html', 'contact.html', 'membership.html',
                     'privacy.html', 'terms.html', 'sitemap.html']
    for link in en_page_links:
        # Only in mobile menu context (href="pagename.html") → href="../pagename.html"
        # But NOT in already-fixed root links
        old_mobile = f'href="{link}"'
        new_mobile = f'href="../{link}"'
        # We need to be careful not to double-fix what's already done
        # Only fix if it's not already ../ or ../../
        content = re.sub(
            rf'(?<!\.\.\/)href="{re.escape(link)}"',
            f'href="../{link}"',
            content
        )

    # 8. Write output
    with open(dst_path, 'w') as f:
        f.write(content)
    print(f'✅ Created: {dst_path}')

print('\nDone! All membership sub-pages generated.')