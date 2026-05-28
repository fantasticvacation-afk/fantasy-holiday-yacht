#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix yachts-daycruiser.html: overview, specs, 3 new models"""

with open('yachts-daycruiser.html', 'r', encoding='utf-8') as f:
    html = f.read()

changes = 0

# === 1. Add lifestyle paragraphs after overview ===
old1 = '旗舰系列相同的管家式售后服务和泊位保障。</p>\n<div class="series-gallery">'
new1 = '旗舰系列相同的管家式售后服务和泊位保障。</p>\n<div class="reveal" style="margin-top:24px">\n<p style="color:var(--text-muted);line-height:2;font-size:15px">日间系列特别适合沿海城市船东、首次购艇客户以及重视社交与城市周边航行体验的用户。无论是黄昏后的临海酒会、周末家庭出海野餐，还是城市湾区的一日短途旅行，每一艘日间系列游艇都在紧凑的尺度中，兼顾了甲板社交空间与基本的私密休憩区域。</p>\n<p style="color:var(--text-muted);line-height:2;font-size:15px;margin-top:12px">对于正在考虑从日间体验走向更大尺寸游艇的客户，日间系列也是理想的过渡选择，让您在可控预算内，提前熟悉航海生活的节奏与日常维护的要求。</p>\n</div>\n<div class="series-gallery">'
if old1 in html:
    html = html.replace(old1, new1)
    changes += 1
    print("✅ 1. 系列概述升级 - 新增生活方式段落")
else:
    print("❌ 1. 系列概述 - 未找到锚点")

# === 2. Upgrade tech specs ===
old2 = '<p style="color:var(--text-muted);line-height:1.8;font-size:14px;margin-bottom:16px">12m - 18m (LOA) | 3.8m - 5.2m (Beam) | 32 - 38 kn | 4 - 8 Guests | 300 - 500nm</p>'
new2 = '<p style="color:var(--text-muted);line-height:1.8;font-size:14px;margin-bottom:8px">12m – 18m（全长 LOA） | 3.8m – 5.2m（船宽 B） | 32 – 38 kn（最高航速） | 6 – 12人（最大载客） | 300 – 500nm（续航里程）</p>\n<p style="color:var(--text-dim);font-size:12px;line-height:1.6;margin-bottom:16px">不同型号在动力搭配、甲板布局与内部装饰上均可根据使用场景进行灵活定制，具体技术参数以实际设计方案与建造技术文件为准。</p>'
if old2 in html:
    html = html.replace(old2, new2)
    changes += 1
    print("✅ 2. 技术参数升级为两层格式")
else:
    print("❌ 2. 技术参数 - 未找到锚点")

# === 3. Standardize existing model param format ===
# 日间18: "18m / 5.2m / 38kn / 8 Guests / 500nm" -> new format
old_18 = '日间18 运动版</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">18m / 5.2m / 38kn / 8 Guests / 500nm</div>\n      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">日间旗舰，座舱影院+水上沙龙+全碳纤维甲板，海面终极体验</p>'
new_18 = '日间18 运动版</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">长度：18m | 船宽：5.2m | 总吨：约45 GT | 最大载客：10 人 | 最高航速：38 kn | 续航里程：500nm</div>\n      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">日间系列的销量主力，座舱影院+水上沙龙+轻量化甲板，兼顾运动性能与日间派对需求，适合城市精英的高频次出海社交</p>'
if old_18 in html:
    html = html.replace(old_18, new_18)
    changes += 1
    print("✅ 3a. 日间18 参数格式统一 + 卖点升级")

old_15 = '日间15 都市版</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">15m / 4.6m / 35kn / 6 Guests / 400nm</div>\n      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">最灵动，城市海滨日间巡游最佳搭档</p>'
new_15 = '日间15 都市版</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">长度：15m | 船宽：4.6m | 总吨：约35 GT | 最大载客：8 人 | 最高航速：35 kn | 续航里程：400nm</div>\n      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">日间系列中坚，灵动尺寸兼顾驾驶乐趣与舒适体验，城市海滨日间巡游的理想之选，尤其适合情侣度假与小型亲友聚会</p>'
if old_15 in html:
    html = html.replace(old_15, new_15)
    changes += 1
    print("✅ 3b. 日间15 参数格式统一 + 卖点升级")

old_12 = '日间12 自由版</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">12m / 3.8m / 32kn / 4 Guests / 300nm</div>\n      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">入门自由，告别沉重仪式，拥抱轻快航海</p>'
new_12 = '日间12 自由版</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">长度：12m | 船宽：3.8m | 总吨：约25 GT | 最大载客：6 人 | 最高航速：32 kn | 续航里程：300nm</div>\n      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">日间系列入门之选，紧凑轻便、操控友好，适合首次购艇客户与湾区短途出行，让航海生活从简单开始</p>'
if old_12 in html:
    html = html.replace(old_12, new_12)
    changes += 1
    print("✅ 3c. 日间12 参数格式统一 + 卖点升级")

# === 4. Add 3 new models after 日间12 (before the closing </div></div></section>) ===
old_close = '拥抱轻快航海</p>\n    </div>\n  </div>\n\n</div></div></section>'
new_close = '拥抱轻快航海</p>\n    </div>\n  </div>\n  <!-- 日间20 巅峰版 -->\n  <div class="reveal series-yacht-card" style="background:var(--card);border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap;margin-bottom:20px">\n    <div style="flex:0 0 300px;max-width:300px;min-height:200px;background:var(--dark2)"><img src="images/yttp/yacht-107.jpg" alt="日间20 巅峰版" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block"/></div>\n    <div style="flex:1;min-width:300px;padding:24px">\n      <h3 style="font-family:Playfair Display,serif;font-size:22px;color:var(--gold);margin-bottom:8px">日间20 巅峰版</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">长度：20m | 船宽：5.8m | 总吨：约55 GT | 最大载客：12 人 | 最高航速：38 kn | 续航里程：500nm</div>\n      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">日间系列旗舰，超大面积甲板搭配可扩展水上沙龙，适合海上派对与高端社交活动，让每一次出海都成为社交焦点</p>\n    </div>\n  </div>\n  <!-- 日间14 海岸版 -->\n  <div class="reveal series-yacht-card" style="background:var(--card);border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap;margin-bottom:20px">\n    <div style="flex:0 0 300px;max-width:300px;min-height:200px;background:var(--dark2)"><img src="images/yttp/yacht-115.jpg" alt="日间14 海岸版" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block"/></div>\n    <div style="flex:1;min-width:300px;padding:24px">\n      <h3 style="font-family:Playfair Display,serif;font-size:22px;color:var(--gold);margin-bottom:8px">日间14 海岸版</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">长度：14m | 船宽：4.2m | 总吨：约30 GT | 最大载客：8 人 | 最高航速：35 kn | 续航里程：350nm</div>\n      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">城市周边海岸巡航的理想搭档，兼顾甲板休闲与舒适过夜功能，适合小家庭周末出海与近岸海岛探索</p>\n    </div>\n  </div>\n  <!-- 日间10 微风版 -->\n  <div class="reveal series-yacht-card" style="background:var(--card);border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap;margin-bottom:20px">\n    <div style="flex:0 0 300px;max-width:300px;min-height:200px;background:var(--dark2)"><img src="images/yttp/yacht-119.jpg" alt="日间10 微风版" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block"/></div>\n    <div style="flex:1;min-width:300px;padding:24px">\n      <h3 style="font-family:Playfair Display,serif;font-size:22px;color:var(--gold);margin-bottom:8px">日间10 微风版</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">长度：10m | 船宽：3.4m | 总吨：约18 GT | 最大载客：6 人 | 最高航速：30 kn | 续航里程：250nm</div>\n      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">日间系列精巧入门款，可拖挂或停靠在小型码头，适合湾区短途与内湖休闲，是水上运动爱好者的灵活选择</p>\n    </div>\n  </div>\n\n</div></div></section>'
# Need to match the updated text
search_close = '让航海生活从简单开始</p>\n    </div>\n  </div>\n\n</div></div></section>'
if search_close in html:
    html = html.replace(search_close, new_close)
    changes += 1
    print("✅ 4. 新增3艘日间型号（20/14/10）")
else:
    print("❌ 4. 新增型号 - 未找到锚点")
    # Try backup search
    if '自由版</h3>' in html:
        import re
        # Find position of the closing section tag after the models
        idx = html.find('自由版</h3>')
        section_close = html.find('</div></div></section>', idx)
        context = html[section_close-50:section_close+50]
        print(f"   Context near close: ...{context}...")

# Write output
with open('yachts-daycruiser.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n{'='*50}")
print(f"Total changes: {changes}")
print(f"New file size: {len(html)} bytes")

# Verify model count
import re
model_count = len(re.findall(r'日间\d+', html))
print(f"日间 models found: {model_count}")