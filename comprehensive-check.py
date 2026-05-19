#!/usr/bin/env python3
"""
fh-yacht-site 全站综合检查脚本
检查所有关键功能和样式
"""

import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent

print("=" * 80)
print("🔍 fh-yacht-site 全站综合检查")
print("=" * 80)

html_files = list(BASE_DIR.glob("*.html"))
# 过滤掉模板文件
html_files = [f for f in html_files if f.name not in ['nav-template.html', 'footer-template.html']]

print(f"\n📄 检查 {len(html_files)} 个 HTML 文件...")

# ============================================================
# 1. 检查 i18n 键的完整性
# ============================================================
print("\n" + "=" * 80)
print("📋 检查 1: i18n 键完整性")
print("=" * 80)

# 读取 i18n.js
i18n_file = BASE_DIR / "i18n.js"
i18n_content = i18n_file.read_text(encoding='utf-8')

# 提取所有定义的键
defined_keys = set(re.findall(r'"([^"]+)":\s*{', i18n_content))
print(f"i18n.js 中定义的键: {len(defined_keys)} 个")

# 检查所有 HTML 文件中使用的键
missing_keys = defaultdict(list)
total_used_keys = 0

for html_file in html_files:
    content = html_file.read_text(encoding='utf-8')

    # 提取所有 data-i18n 属性
    used_keys = re.findall(r'data-i18n="([^"]+)"', content)
    total_used_keys += len(used_keys)

    for key in used_keys:
        if key not in defined_keys:
            missing_keys[key].append(html_file.name)

print(f"HTML 文件中使用的键: {total_used_keys} 个")
print(f"缺失的键: {len(missing_keys)} 个")

if missing_keys:
    print("\n前 10 个缺失的键:")
    for i, (key, files) in enumerate(sorted(missing_keys.items())[:10]):
        print(f"  {i+1}. {key} (在 {files[0]} 等 {len(files)} 个文件中)")

# ============================================================
# 2. 检查链接有效性
# ============================================================
print("\n" + "=" * 80)
print("📋 检查 2: 链接有效性")
print("=" * 80)

broken_links = []
total_links = 0

for html_file in html_files:
    content = html_file.read_text(encoding='utf-8')

    # 提取所有内部链接
    links = re.findall(r'href="([^"#][^"]*\.html[^"]*)"', content)
    total_links += len(links)

    for link in links:
        # 跳过外部链接和锚点
        if link.startswith('http') or link.startswith('#'):
            continue

        # 提取文件名
        link_file = link.split('#')[0]
        target = BASE_DIR / link_file

        if not target.exists():
            broken_links.append({
                'file': html_file.name,
                'link': link
            })

print(f"总链接数: {total_links}")
print(f"失效链接: {len(broken_links)} 个")

if broken_links:
    print("\n前 10 个失效链接:")
    for i, item in enumerate(broken_links[:10]):
        print(f"  {i+1}. {item['file']} -> {item['link']}")

# ============================================================
# 3. 检查图片引用
# ============================================================
print("\n" + "=" * 80)
print("📋 检查 3: 图片引用")
print("=" * 80)

missing_images = []
total_images = 0

for html_file in html_files:
    content = html_file.read_text(encoding='utf-8')

    # 提取所有图片 src
    images = re.findall(r'<img[^>]+src="([^"]+)"', content)
    total_images += len(images)

    for img in images:
        if img.startswith('http') or img.startswith('data:'):
            continue

        img_path = BASE_DIR / img
        if not img_path.exists():
            missing_images.append({
                'file': html_file.name,
                'image': img
            })

print(f"总图片引用: {total_images}")
print(f"缺失图片: {len(missing_images)} 个")

if missing_images:
    print("\n前 10 个缺失图片:")
    for i, item in enumerate(missing_images[:10]):
        print(f"  {i+1}. {item['file']} -> {item['image']}")

# ============================================================
# 4. 检查响应式设计
# ============================================================
print("\n" + "=" * 80)
print("📋 检查 4: 响应式设计")
print("=" * 80)

# 检查 CSS 文件中的媒体查询
css_file = BASE_DIR / "style.css"
css_content = css_file.read_text(encoding='utf-8')

media_queries = re.findall(r'@media[^{]+\{', css_content)
print(f"CSS 中的媒体查询数量: {len(media_queries)}")

# 检查是否包含关键断点
breakpoints = {
    '768px': '平板端',
    '1024px': '小屏电脑',
    '480px': '大屏手机',
    '375px': 'iPhone',
}

print("\n关键断点检查:")
for bp, desc in breakpoints.items():
    if bp in css_content:
        print(f"  ✅ {bp} ({desc})")
    else:
        print(f"  ⚠️  {bp} ({desc}) - 未找到")

# ============================================================
# 5. 检查导航栏固定定位
# ============================================================
print("\n" + "=" * 80)
print("📋 检查 5: 导航栏固定定位")
print("=" * 80)

if 'position:fixed' in css_content and '#navbar' in css_content:
    print("  ✅ 导航栏使用固定定位")

    # 检查 z-index
    navbar_z = re.search(r'#navbar[^{]*{[^}]*z-index:\s*(\d+)', css_content)
    if navbar_z:
        print(f"  ✅ z-index: {navbar_z.group(1)}")
else:
    print("  ⚠️  导航栏未使用固定定位")

# ============================================================
# 6. 检查暗色模式
# ============================================================
print("\n" + "=" * 80)
print("📋 检查 6: 暗色模式")
print("=" * 80)

dark_mode_rules = re.findall(r'\.dark-mode[^{]*\{', css_content)
print(f"暗色模式规则: {len(dark_mode_rules)} 条")

if dark_mode_rules:
    print("  ✅ 暗色模式支持完整")
else:
    print("  ⚠️  缺少暗色模式样式")

# ============================================================
# 汇总结果
# ============================================================
print("\n" + "=" * 80)
print("📊 检查完成汇总")
print("=" * 80)

total_issues = len(missing_keys) + len(broken_links) + len(missing_images)

print(f"\n✅ 已检查项目:")
print(f"  - HTML 文件: {len(html_files)} 个")
print(f"  - i18n 键: {total_used_keys} 个使用，{len(missing_keys)} 个缺失")
print(f"  - 链接: {total_links} 个，{len(broken_links)} 个失效")
print(f"  - 图片: {total_images} 个引用，{len(missing_images)} 个缺失")
print(f"  - 响应式断点: {len(media_queries)} 个媒体查询")

print(f"\n📊 总问题数: {total_issues}")

if total_issues == 0:
    print("\n✅ 全站检查通过！网站状态良好！")
else:
    print(f"\n⚠️  发现 {total_issues} 个问题需要修复")
