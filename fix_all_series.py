#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix expedition, flybridge, sovereign - precise text replacement"""

import re

# ==========================================================
# 1. EXPEDITION 远征系列
# ==========================================================
print("="*60)
print("  远征系列")
print("="*60)

with open('yachts-expedition.html', 'r', encoding='utf-8') as f:
    h = f.read()

changes = 0

# 1a. Overview upgrade
old_ov = ('<p style="color:var(--text-muted);line-height:2;font-size:16px">'
           '远征系列专为热爱远洋探险和精神探索的船东设计。'
           '从50米远洋版到70米探险家，每一艘远征游艇均采用冰区加强船体、'
           '延长油箱系统和全天候稳定性设计，可在南极、北极、太平洋无人区等极端环境下安全航行，'
           '同时保持令人惊艳的奢华与舒适。我们的远征系列让您以全无妥协的方式探索世界上最神秘的海域。'
           '</p>')
new_ov = ('<p style="color:var(--text-muted);line-height:2;font-size:16px">'
           '远征系列专为热爱远洋探险和精神探索的船东设计。'
           '从50米远洋版到70米探险家，每一艘远征游艇均采用冰区加强船体、'
           '延长油箱系统和全天候稳定性设计，可在南极、北极、太平洋无人区等极端环境下安全航行，'
           '同时保持令人惊艳的奢华与舒适。远征系列适合追求极地航行、高纬度探险与长时间自持生活的船东。'
           '典型用途包括南极/北极科考巡航、跨洋长途 displacement 航行、无人海域的长时间自主生活。</p>'
           '<p style="color:var(--text-muted);line-height:2;font-size:15px;margin-top:12px">'
           '安全与冗余设计贯穿全系列——双机冗余动力系统、分舱水密设计、超大油水储备能力，'
           '以及可选配的冰区加强船体，让远航更安心。'
           '无论是科研组织、探险家，还是希望在海上长期旅居的家庭，远征系列都能提供从容的空间与可靠的保障。'
           '</p>')
if old_ov in h:
    h = h.replace(old_ov, new_ov)
    changes += 1
    print("  ✅ 1a. 概述升级")
else:
    print(f"  ❌ 1a. 概述未匹配 (len={len(old_ov)})")

# 1b. Specs upgrade 
old_spec = ('<p style="color:var(--text-muted);line-height:1.8;font-size:14px;margin-bottom:16px">'
            '50m - 70m (LOA) | 10.5m - 13.6m (Beam) | 1,200GT - 2,200GT | 12 - 18 Guests | 7,000 - 8,000nm</p>')
new_spec = ('<p style="color:var(--text-muted);line-height:1.8;font-size:14px;margin-bottom:8px">'
            '45m – 80m（全长 LOA） | 9.0m – 13.5m（船宽 B） | 4,000 – 8,000nm（经济续航） | 10 – 18 人（最大载客）</p>\n'
            '<p style="color:var(--text-dim);font-size:12px;line-height:1.6;margin-bottom:16px">'
            '可选配冰区加强船体（PC7/PC6）、额外油舱、直升机平台等远征专属配置，具体以设计方案为准。'
            '</p>')
if old_spec in h:
    h = h.replace(old_spec, new_spec)
    changes += 1
    print("  ✅ 1b. 技术参数升级为两层")
else:
    print("  ❌ 1b. 技术参数未匹配")

# 1c. Standardize existing model params
param_map = [
    ('远征70 探险家', '70m / 13.6m / 2,200GT / 18 Guests / 8,000nm',
     '长度：70m | 船宽：13.6m | 总吨：2,200 GT | 最大载客：18 人 | 续航里程：8,000nm'),
    ('远征60 极境版', '60m / 12.0m / 1,700GT / 14 Guests / 7,500nm',
     '长度：60m | 船宽：12.0m | 总吨：1,700 GT | 最大载客：14 人 | 续航里程：7,500nm'),
    ('远征50 远洋版', '50m / 10.5m / 1,200GT / 12 Guests / 7,000nm',
     '长度：50m | 船宽：10.5m | 总吨：1,200 GT | 最大载客：12 人 | 续航里程：7,000nm'),
]
for name, old_p, new_p in param_map:
    old_block = f'{name}</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">{old_p}</div>'
    new_block = f'{name}</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">{new_p}</div>'
    if old_block in h:
        h = h.replace(old_block, new_block)
        changes += 1
        print(f"  ✅ 1c. {name} 参数统一")
    else:
        print(f"  ⚠️  1c. {name} 参数行未匹配")

# 1d. Add 3 new models after 远征50
insert_after = ('远征50 远洋版</h3>\n'
                '      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">'
                '长度：50m | 船宽：10.5m | 总吨：1,200 GT | 最大载客：12 人 | 续航里程：7,000nm</div>\n'
                '      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">'
                '适合长途跨洋航行与极地探索，在续航、舒适与运营经济性之间取得良好平衡，是进入远征世界的理想起点'
                '</p>\n    </div>\n  </div>\n\n</div></div></section>')

new_models = (
    '适合长途跨洋航行与极地探索，在续航、舒适与运营经济性之间取得良好平衡，是进入远征世界的理想起点'
    '</p>\n    </div>\n  </div>\n'
    '  <!-- 远征80 破冰版 -->\n'
    '  <div class="reveal series-yacht-card" style="background:var(--card);border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap;margin-bottom:20px">\n'
    '    <div style="flex:0 0 300px;max-width:300px;min-height:200px;background:var(--dark2)">'
    '<img src="images/yttp/yacht-060.jpg" alt="远征80 破冰版" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block"/></div>\n'
    '    <div style="flex:1;min-width:300px;padding:24px">\n'
    '      <h3 style="font-family:Playfair Display,serif;font-size:22px;color:var(--gold);margin-bottom:8px">远征80 破冰版</h3>\n'
    '      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">'
    '长度：80m | 船宽：13.5m | 总吨：3,500 GT | 最大载客：20 人 | 续航里程：8,000nm</div>\n'
    '      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">'
    '远征系列旗舰，PC6冰区认证，配备双直升机平台与全船水密分舱，为极地科考与超长途环球航行而打造'
    '</p>\n    </div>\n  </div>\n'
    '  <!-- 远征65 科研版 -->\n'
    '  <div class="reveal series-yacht-card" style="background:var(--card);border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap;margin-bottom:20px">\n'
    '    <div style="flex:0 0 300px;max-width:300px;min-height:200px;background:var(--dark2)">'
    '<img src="images/yttp/yacht-070.jpg" alt="远征65 科研版" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block"/></div>\n'
    '    <div style="flex:1;min-width:300px;padding:24px">\n'
    '      <h3 style="font-family:Playfair Display,serif;font-size:22px;color:var(--gold);margin-bottom:8px">远征65 科研版</h3>\n'
    '      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">'
    '长度：65m | 船宽：12.5m | 总吨：2,600 GT | 最大载客：16 人 | 续航里程：7,500nm</div>\n'
    '      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">'
    '专为海洋科研与极地探索设计，预留ROV水下机器人甲板与移动实验室接口，兼顾长期自持生活需求'
    '</p>\n    </div>\n  </div>\n'
    '  <!-- 远征55 家庭版 -->\n'
    '  <div class="reveal series-yacht-card" style="background:var(--card);border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap;margin-bottom:20px">\n'
    '    <div style="flex:0 0 300px;max-width:300px;min-height:200px;background:var(--dark2)">'
    '<img src="images/yttp/yacht-080.jpg" alt="远征55 家庭版" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block"/></div>\n'
    '    <div style="flex:1;min-width:300px;padding:24px">\n'
    '      <h3 style="font-family:Playfair Display,serif;font-size:22px;color:var(--gold);margin-bottom:8px">远征55 家庭版</h3>\n'
    '      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">'
    '长度：55m | 船宽：11.0m | 总吨：1,600 GT | 最大载客：14 人 | 续航里程：7,000nm</div>\n'
    '      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">'
    '为跨洋家庭旅居而设计，宽敞的儿童活动区与海上教室布局，让持续数月以上的海上生活从容舒适'
    '</p>\n    </div>\n  </div>\n\n</div></div></section>'
)

if insert_after in h:
    h = h.replace(insert_after, new_models)
    changes += 1
    print("  ✅ 1d. 新增3艘远征型号（80/65/55）")
else:
    print("  ❌ 1d. 插入点未找到")

with open('yachts-expedition.html', 'w', encoding='utf-8') as f:
    f.write(h)
print(f"  修改项数: {changes}, 文件大小: {len(h)} bytes\n")


# ==========================================================
# 2. FLYBRIDGE 飞桥系列
# ==========================================================
print("="*60)
print("  飞桥系列")
print("="*60)

with open('yachts-flybridge.html', 'r', encoding='utf-8') as f:
    h = f.read()

changes = 0

# 2a. Overview upgrade
old_ov = ('<p style="color:var(--text-muted);line-height:2;font-size:16px">'
           '飞桥系列是奇幻假期最受欢迎的经典游艇形态，专为地中海式度假生活和家族海上聚会而设计。'
           '30米至45米的黄金尺寸段，在拥有充足社交空间的同时，保证了灵活的码头停靠能力和卓越的操控性。'
           '飞桥系列融合了意大利经典设计语言与现代智能科技，是追求优雅生活方式的完美之选。'
           '每艘飞桥游艇都配备了宽敞的飞桥娱乐区、齐全的厨房设施和专业的船员配置，让您的海上度假无需任何妥协。'
           '</p>')
new_ov = ('<p style="color:var(--text-muted);line-height:2;font-size:16px">'
           '飞桥系列是兼顾家族度假、日常出海与商务接待的综合型系列。'
           '飞桥甲板带来的开阔观景优势，让船上社交空间由内向外自然延伸——主甲板沙龙、飞桥露天用餐区、前甲板日光区三者联动，'
           '构成多层次的海上生活场景。无论是三代同船的家庭度假，还是海上商务接待，飞桥系列都能在舒适与实用性之间取得良好平衡。</p>'
           '<p style="color:var(--text-muted);line-height:2;font-size:15px;margin-top:12px">'
           '各型号在甲板层数（双层/三层飞桥）、厨房位置（上/下甲板）与船员舱配置上提供多种组合，'
           '可根据使用习惯灵活选择。'
           '</p>')
if old_ov in h:
    h = h.replace(old_ov, new_ov)
    changes += 1
    print("  ✅ 2a. 概述升级")
else:
    print(f"  ❌ 2a. 概述未匹配 (len={len(old_ov)})")

# 2b. Specs upgrade
old_spec = ('<p style="color:var(--text-muted);line-height:1.8;font-size:14px;margin-bottom:16px">'
            '30m - 45m (LOA) | 7.2m - 9.0m (Beam) | 380GT - 680GT | 8 - 12 Guests | 1,500 - 2,000nm</p>')
new_spec = ('<p style="color:var(--text-muted);line-height:1.8;font-size:14px;margin-bottom:8px">'
            '28m – 45m（全长 LOA） | 6.8m – 8.6m（船宽 B） | 24 – 32 kn（最高航速） | 8 – 14 人（最大载客）</p>\n'
            '<p style="color:var(--text-dim);font-size:12px;line-height:1.6;margin-bottom:16px">'
            '不同型号在甲板层数、飞桥布局、主沙龙落地窗配置上提供多种方案，具体以实际设计为准。'
            '</p>')
if old_spec in h:
    h = h.replace(old_spec, new_spec)
    changes += 1
    print("  ✅ 2b. 技术参数升级为两层")
else:
    print("  ❌ 2b. 技术参数未匹配")

# 2c. Standardize existing model params
param_map_fb = [
    ('飞桥45 尊享版', '45m / 9.0m / 680GT / 12 Guests / 2,000nm',
     '长度：45m | 船宽：9.0m | 总吨：680 GT | 最大载客：14 人 | 最高航速：28 kn | 续航里程：2,000nm'),
    ('飞桥38 经典版', '38m / 8.2m / 520GT / 10 Guests / 1,800nm',
     '长度：38m | 船宽：8.2m | 总吨：520 GT | 最大载客：12 人 | 最高航速：26 kn | 续航里程：1,800nm'),
    ('飞桥30 风尚版', '30m / 7.2m / 380GT / 8 Guests / 1,500nm',
     '长度：30m | 船宽：7.2m | 总吨：380 GT | 最大载客：10 人 | 最高航速：32 kn | 续航里程：1,500nm'),
]
for name, old_p, new_p in param_map_fb:
    old_block = f'{name}</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">{old_p}</div>'
    new_block = f'{name}</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">{new_p}</div>'
    if old_block in h:
        h = h.replace(old_block, new_block)
        changes += 1
        print(f"  ✅ 2c. {name} 参数统一")
    else:
        print(f"  ⚠️  2c. {name} 参数行未匹配")

# 2d. Add 3 new models after 飞桥30
insert_after_fb = ('飞桥30 风尚版</h3>\n'
                  '      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">'
                  '长度：30m | 船宽：7.2m | 总吨：380 GT | 最大载客：10 人 | 最高航速：32 kn | 续航里程：1,500nm</div>\n'
                  '      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">'
                  '飞桥入门首选，运动内饰+年轻设计语言，首次买家最优选择'
                  '</p>\n    </div>\n  </div>\n\n</div></div></section>')

new_models_fb = (
    '飞桥系列中最为灵动的中型款，三层飞桥布局搭配全落地窗主沙龙，适合家庭度假与朋友聚会，在尺寸与舒适度之间取得良好平衡'
    '</p>\n    </div>\n  </div>\n'
    '  <!-- 飞桥42 商务版 -->\n'
    '  <div class="reveal series-yacht-card" style="background:var(--card);border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap;margin-bottom:20px">\n'
    '    <div style="flex:0 0 300px;max-width:300px;min-height:200px;background:var(--dark2)">'
    '<img src="images/yttp/yacht-107.jpg" alt="飞桥42 商务版" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block"/></div>\n'
    '    <div style="flex:1;min-width:300px;padding:24px">\n'
    '      <h3 style="font-family:Playfair Display,serif;font-size:22px;color:var(--gold);margin-bottom:8px">飞桥42 商务版</h3>\n'
    '      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">'
    '长度：42m | 船宽：8.6m | 总吨：620 GT | 最大载客：14 人 | 最高航速：26 kn | 续航里程：1,900nm</div>\n'
    '      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">'
    '飞桥系列中适合商务接待的型号，宽敞飞桥甲板搭配可分隔多功能沙龙，兼顾海上商务会议与休闲娱乐双重需求'
    '</p>\n    </div>\n  </div>\n'
    '  <!-- 飞桥35 亲子版 -->\n'
    '  <div class="reveal series-yacht-card" style="background:var(--card);border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap;margin-bottom:20px">\n'
    '    <div style="flex:0 0 300px;max-width:300px;min-height:200px;background:var(--dark2)">'
    '<img src="images/yttp/yacht-115.jpg" alt="飞桥35 亲子版" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block"/></div>\n'
    '    <div style="flex:1;min-width:300px;padding:24px">\n'
    '      <h3 style="font-family:Playfair Display,serif;font-size:22px;color:var(--gold);margin-bottom:8px">飞桥35 亲子版</h3>\n'
    '      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">'
    '长度：35m | 船宽：7.8m | 总吨：450 GT | 最大载客：10 人 | 最高航速：28 kn | 续航里程：1,700nm</div>\n'
    '      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">'
    '专为家庭亲子设计，儿童活动区与主卧分离布局保障隐私与安全感，飞桥甲板是家庭聚餐与观星的理想空间'
    '</p>\n    </div>\n  </div>\n'
    '  <!-- 飞桥28 都市版 -->\n'
    '  <div class="reveal series-yacht-card" style="background:var(--card);border:1px solid var(--glass-border);border-radius:12px;overflow:hidden;display:flex;flex-wrap:wrap;margin-bottom:20px">\n'
    '    <div style="flex:0 0 300px;max-width:300px;min-height:200px;background:var(--dark2)">'
    '<img src="images/yttp/yacht-119.jpg" alt="飞桥28 都市版" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block"/></div>\n'
    '    <div style="flex:1;min-width:300px;padding:24px">\n'
    '      <h3 style="font-family:Playfair Display,serif;font-size:22px;color:var(--gold);margin-bottom:8px">飞桥28 都市版</h3>\n'
    '      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">'
    '长度：28m | 船宽：6.8m | 总吨：300 GT | 最大载客：8 人 | 最高航速：32 kn | 续航里程：1,500nm</div>\n'
    '      <p style="color:var(--text-muted);font-size:14px;line-height:1.7">'
    '飞桥系列中最为紧凑的型号，适合城市周边周末出海与短期亲友聚会，双层飞桥设计让小尺寸同样拥有丰富社交空间'
    '</p>\n    </div>\n  </div>\n\n</div></div></section>'
)

if insert_after_fb in h:
    h = h.replace(insert_after_fb, new_models_fb)
    changes += 1
    print("  ✅ 2d. 新增3艘飞桥型号（42/35/28）")
else:
    print("  ❌ 2d. 飞桥30插入点未找到")

with open('yachts-flybridge.html', 'w', encoding='utf-8') as f:
    f.write(h)
print(f"  修改项数: {changes}, 文件大小: {len(h)} bytes\n")


# ==========================================================
# 3. SOVEREIGN 君临系列
# ==========================================================
print("="*60)
print("  君临系列")
print("="*60)

with open('yachts-sovereign.html', 'r', encoding='utf-8') as f:
    h = f.read()

changes = 0

# 3a. Overview upgrade
old_ov = ('<p style="color:var(--text-muted);line-height:2;font-size:16px">'
           '君临系列代表着奇幻假期游艇工程的最高造诣，专为全球高端家族、皇室成员及超高净值人士打造。'
           '从78米的旗舰型到120米的传奇级，每一艘君临都是意大利设计与荷兰工程智慧的结晶。'
           '我们与全球高端船厂合作，将最前沿的船舶科技与非凡奢华融为一体，为船东提供无可比拟的海洋生活体验。'
           '</p>')
new_ov = ('<p style="color:var(--text-muted);line-height:2;font-size:16px">'
           '君临系列代表奇幻假期在游艇设计与建造领域的最高水准。'
           '每一艘君临系列游艇均为全定制项目，从线型设计、内装风格到系统配置，均由客户与我们的设计团队共同决定。'
           '君临系列适合追求环球远航、家族长期海上居住、以及高端商务接待的客户群体。'
           '宽体主甲板设计让舱内空间感大幅提升，而多项专属定制选项（如私人阳台、双主卧布局、海上spa区等）让每艘君临都与众不同。</p>'
           '<p style="color:var(--text-muted);line-height:2;font-size:15px;margin-top:12px">'
           '我们与欧洲高端船厂及国际知名设计师事务所有长期合作关系，'
           '在建造品质、交付周期与售后支持上均积累了丰富经验。'
           '</p>')
if old_ov in h:
    h = h.replace(old_ov, new_ov)
    changes += 1
    print("  ✅ 3a. 概述升级")
else:
    print(f"  ❌ 3a. 概述未匹配 (len={len(old_ov)})")

# 3b. Specs upgrade
old_spec = ('<p style="color:var(--text-muted);line-height:1.8;font-size:14px;margin-bottom:16px">'
            '78m - 120m (LOA) | 12.0m - 18.0m (Beam) | 2,000GT - 4,800GT | 16 - 36 Guests | 3,800 - 6,000nm</p>')
new_spec = ('<p style="color:var(--text-muted);line-height:1.8;font-size:14px;margin-bottom:8px">'
            '78m – 120m（全长 LOA） | 12.0m – 18.0m（船宽 B） | 2,000 – 4,800 GT（总吨） | 16 – 36 人（最大载客） | 3,800 – 6,000nm（续航里程）</p>\n'
            '<p style="color:var(--text-dim);font-size:12px;line-height:1.6;margin-bottom:16px">'
            '1 kn ≈ 1.852 km/h。所有尺寸与吨位数据均为参考值，以实际建造规格书为准。'
            '</p>')
if old_spec in h:
    h = h.replace(old_spec, new_spec)
    changes += 1
    print("  ✅ 3b. 技术参数升级 + 单位说明")
else:
    print("  ❌ 3b. 技术参数未匹配")

# 3c. Standardize all 6 model params
param_map_sv = [
    ('君临120 旗舰版', '120m / 18.0m / 4,800GT / 36 Guests / 6,000nm',
     '长度：120m | 船宽：18.0m | 总吨：4,800 GT | 最大载客：36 人 | 续航里程：6,000nm'),
    ('君临110 至尊版', '110m / 16.5m / 4,000GT / 30 Guests / 5,500nm',
     '长度：110m | 船宽：16.5m | 总吨：4,000 GT | 最大载客：30 人 | 续航里程：5,500nm'),
    ('君临100 典藏版', '100m / 15.0m / 3,200GT / 24 Guests / 5,000nm',
     '长度：100m | 船宽：15.0m | 总吨：3,200 GT | 最大载客：24 人 | 续航里程：5,000nm'),
    ('君临92 领航版', '92m / 14.0m / 2,800GT / 22 Guests / 4,800nm',
     '长度：92m | 船宽：14.0m | 总吨：2,800 GT | 最大载客：22 人 | 续航里程：4,800nm'),
    ('君临85 王者版', '85m / 13.5m / 2,400GT / 20 Guests / 4,500nm',
     '长度：85m | 船宽：13.5m | 总吨：2,400 GT | 最大载客：20 人 | 续航里程：4,500nm'),
    ('君临78 御风版', '78m / 12.0m / 2,000GT / 16 Guests / 3,800nm',
     '长度：78m | 船宽：12.0m | 总吨：2,000 GT | 最大载客：16 人 | 续航里程：3,800nm'),
]
for name, old_p, new_p in param_map_sv:
    old_block = f'{name}</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">{old_p}</div>'
    new_block = f'{name}</h3>\n      <div style="font-size:12px;color:var(--text-dim);letter-spacing:1px;margin-bottom:12px">{new_p}</div>'
    if old_block in h:
        h = h.replace(old_block, new_block)
        changes += 1
        print(f"  ✅ 3c. {name} 参数统一")
    else:
        print(f"  ⚠️  3c. {name} 参数行未匹配")

# 3d. Compliance check
banned = ['顶级', '唯一', '垄断', '保本', '保收益', '无风险', '颠覆', '重新定义', '绝对领先', '无人可及', 'IPO', '上市']
found = [b for b in banned if b in h]
if found:
    print(f"  ⚠️  3d. 合规问题: {found}")
else:
    print("  ✅ 3d. 合规检查通过（无禁用词）")

with open('yachts-sovereign.html', 'w', encoding='utf-8') as f:
    f.write(h)
print(f"  修改项数: {changes}, 文件大小: {len(h)} bytes")

print("\n" + "="*60)
print("  ALL DONE")
print("="*60)
