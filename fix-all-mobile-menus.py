#!/usr/bin/env python3
"""
修复所有缺失移动端菜单和搜索功能的页面
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent

# 完整的移动端菜单和搜索框模板
mobile_menu_template = '''
<!-- Search Overlay -->
<div class="search-overlay" id="searchOverlay">
<div class="search-box">
<input autocomplete="off" class="search-input" id="searchInput" placeholder="搜索产品、新闻、案例..." data-i18n-attr="placeholder:_ph.index.0" type="text"/>
<button class="search-close" onclick="toggleSearch()">
<svg fill="none" height="20" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="20">
<line x1="18" x2="6" y1="6" y2="18"></line><line x1="6" x2="18" y1="6" y2="18"></line>
</svg>
</button>
</div>
<div class="search-suggestions">
<div class="search-suggestion-item" data-i18n="index.5">→ 探索全系游艇</div>
<div class="search-suggestion-item" data-i18n="index.6">→ 定制专属游艇</div>
<div class="search-suggestion-item" data-i18n="index.7">→ 浏览全球航线</div>
<div class="search-suggestion-item" data-i18n="index.8">→ 联系专业顾问</div>
</div>
</div>

<!-- Mobile Menu -->
<div class="mobile-menu" id="mobile-menu">
<button class="mobile-menu-close" onclick="toggleMobile()">
<svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewbox="0 0 24 24" width="24">
<line x1="18" x2="6" y1="6" y2="18"></line><line x1="6" x2="18" y1="6" y2="18"></line>
</svg>
</button>
<div class="mobile-menu-logo">
<svg fill="none" height="40" viewbox="0 0 32 32" width="40">
<path d="M4 24L16 4l12 20H4z" fill="none" stroke="#c9a96e" stroke-width="1.5"></path>
<path d="M8 20h16l-8-12-8 12z" fill="rgba(201,169,110,0.15)" stroke="#c9a96e" stroke-width="1"></path>
</svg>
<span data-i18n="index.9">奇幻假期</span>
</div>
<a class="mobile-nav-link" data-i18n="index.10" href="index.html">首页</a>
<div class="mobile-nav-group">
<div class="mobile-nav-group-title" data-i18n="index.11">关于我们</div>
<a class="mobile-nav-link sub" data-i18n="index.12" href="about.html">公司简介</a>
<a class="mobile-nav-link sub" data-i18n="index.13" href="about-history.html">发展历程</a>
<a class="mobile-nav-link sub" data-i18n="index.14" href="about-culture.html">企业文化</a>
<a class="mobile-nav-link sub" data-i18n="index.15" href="honors.html">荣誉资质</a>
</div>
<div class="mobile-nav-group">
<div class="mobile-nav-group-title" data-i18n="index.16">业务板块</div>
<a class="mobile-nav-link sub" data-i18n="index.17" href="custom.html">全案定制</a>
<a class="mobile-nav-link sub" data-i18n="index.18" href="charter.html">租赁航线</a>
<a class="mobile-nav-link sub" data-i18n="index.19" href="management.html">托管维保</a>
<a class="mobile-nav-link sub" data-i18n="index.20" href="partnership.html">全球合作</a>
</div>
<div class="mobile-nav-group">
<div class="mobile-nav-group-title" data-i18n="index.21">产品与服务</div>
<a class="mobile-nav-link sub" data-i18n="index.22" href="yachts.html">全系游艇</a>
<a class="mobile-nav-link sub" data-i18n="index.23" href="custom.html">定制解决方案</a>
<a class="mobile-nav-link sub" data-i18n="index.24" href="charter.html">租赁服务</a>
<a class="mobile-nav-link sub" data-i18n="index.25" href="management.html">托管服务</a>
<a class="mobile-nav-link sub" data-i18n="index.26" href="cases.html">客户案例</a>
</div>
<a class="mobile-nav-link" data-i18n="index.27" href="news.html">新闻中心</a>
<a class="mobile-nav-link" data-i18n="index.28" href="ir.html">投资者关系</a>
<a class="mobile-nav-link mobile-cta" data-i18n="index.29" href="contact.html">联系我们</a>
</div>
'''

print("🔧 扫描所有 HTML 文件...")

html_files = list(BASE_DIR.glob("*.html"))
print(f"找到 {len(html_files)} 个 HTML 文件")

fixed_count = 0
skipped_count = 0

for html_file in html_files:
    # 跳过模板文件
    if html_file.name in ['nav-template.html', 'footer-template.html']:
        skipped_count += 1
        continue

    try:
        content = html_file.read_text(encoding='utf-8')

        # 检查是否已有移动端菜单
        if 'id="mobile-menu"' in content:
            skipped_count += 1
            continue

        # 找到 </nav> 标签
        nav_close_match = re.search(r'</nav>\s*</nav>\s*</nav>\s*</nav>', content)
        if not nav_close_match:
            nav_close_match = re.search(r'</nav>', content)

        if nav_close_match:
            insert_pos = nav_close_match.end()
            new_content = content[:insert_pos] + '\n' + mobile_menu_template + '\n' + content[insert_pos:]
            html_file.write_text(new_content, encoding='utf-8')
            print(f"  ✅ 已修复: {html_file.name}")
            fixed_count += 1
        else:
            print(f"  ⚠️  {html_file.name}: 找不到 </nav> 标签")

    except Exception as e:
        print(f"  ❌ {html_file.name}: {e}")

print(f"\n✅ 修复完成！")
print(f"  已修复: {fixed_count} 个文件")
print(f"  已跳过: {skipped_count} 个文件")
