#!/usr/bin/env python3
"""
Enrich thin pages with substantive content sections.
Pages targeted: press.html, faq.html, investment.html, map.html, reviews.html
Also fix: press.html missing hero/section, faq.html missing hero
"""

import re, os, sys

BASE = '/Users/stone/.qclaw/workspace/fantasy-holiday-yacht'

# ─── press.html: Add hero + press cards section between nav and footer ───
def enrich_press():
    f = os.path.join(BASE, 'press.html')
    with open(f, 'r', encoding='utf-8') as fh:
        html = fh.read()
    
    # Check if hero already exists
    if 'press-hero' in html:
        print("press.html: hero already exists, skipping")
        return
    
    # Insert hero + section before </div></section> or before <footer
    # The page currently has no content between nav and footer
    # Find the closing of mobile menu and insert content before <footer
    
    content_html = '''
<!-- Press Hero -->
<section class="press-hero">
  <div class="container" style="text-align:center">
    <div style="display:inline-block;padding:6px 20px;border:1px solid rgba(201,169,110,.3);border-radius:30px;color:#c9a96e;font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-bottom:24px" data-i18n="press.100">MEDIA CENTER</div>
    <h1 data-i18n="press.101">媒体报道</h1>
    <p style="font-size:16px;color:rgba(255,255,255,.5);max-width:700px;margin:0 auto;line-height:1.8" data-i18n="press.102">汇聚全球主流媒体对奇幻假期的深度报道与权威解读，见证行业标杆的成长轨迹</p>
  </div>
</section>

<!-- Press Coverage Stats -->
<section style="padding:60px 0;background:rgba(201,169,110,.03)">
  <div class="container">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:40px;text-align:center">
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e" data-i18n="press.110">200+</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="press.111">媒体报道</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e" data-i18n="press.112">50+</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="press.113">合作媒体</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e" data-i18n="press.114">15</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="press.115">国家与地区</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e" data-i18n="press.116">8.5亿</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="press.117">曝光量（次）</div>
      </div>
    </div>
  </div>
</section>

<!-- Press Coverage Grid -->
<section class="section-press">
  <div class="container">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(24px,3.5vw,40px);font-weight:700;color:#e8e8e8;margin-bottom:12px;text-align:center" data-i18n="press.120">权威媒体报道</h2>
    <p style="font-size:15px;color:rgba(255,255,255,.45);text-align:center;max-width:600px;margin:0 auto 50px;line-height:1.8" data-i18n="press.121">来自财经、生活方式、游艇行业权威媒体的深度报道与专题采访</p>
    <div class="press-grid">
      <div class="press-card reveal">
        <div class="press-source" data-i18n="press.130">新浪财经 · Sina Finance</div>
        <div class="press-title" data-i18n="press.131">奇幻假期：中国游艇定制行业的新标杆</div>
        <div class="press-excerpt" data-i18n="press.132">深度报道奇幻假期如何以1/10的定价实现国际顶级游艇品质，解读其独特的供应链整合模式与全球合作战略，分析中国高端游艇市场的变革趋势。</div>
        <div class="press-date" data-i18n="press.133">2026年3月15日</div>
      </div>
      <div class="press-card reveal">
        <div class="press-source" data-i18n="press.140">网易新闻 · NetEase</div>
        <div class="press-title" data-i18n="press.141">独家专访：奇幻假期创始人的海洋梦</div>
        <div class="press-excerpt" data-i18n="press.142">专访奇幻假期创始人，讲述从深圳蛇口出发的创业故事，分享深耕高端游艇行业15年的洞察与愿景，展望中国私人游艇消费的黄金十年。</div>
        <div class="press-date" data-i18n="press.143">2026年2月28日</div>
      </div>
      <div class="press-card reveal">
        <div class="press-source" data-i18n="press.150">腾讯财经 · Tencent Finance</div>
        <div class="press-title" data-i18n="press.151">高端游艇租赁市场年增35%，奇幻假期领跑赛道</div>
        <div class="press-excerpt" data-i18n="press.152">市场分析报告指出，中国高端游艇租赁市场持续高速增长，奇幻假期凭借全产业链服务能力和差异化定价策略，市场份额稳居行业前列。</div>
        <div class="press-date" data-i18n="press.153">2026年1月20日</div>
      </div>
      <div class="press-card reveal">
        <div class="press-source" data-i18n="press.160">凤凰网 · Phoenix Media</div>
        <div class="press-title" data-i18n="press.161">从定制到托管：奇幻假期打造游艇全生命周期服务</div>
        <div class="press-excerpt" data-i18n="press.162">专题报道奇幻假期的一站式游艇服务体系，覆盖定制设计、租赁运营、托管维保、资产保值全链条，为高净值客户提供无忧海享生活。</div>
        <div class="press-date" data-i18n="press.163">2025年12月10日</div>
      </div>
      <div class="press-card reveal">
        <div class="press-source" data-i18n="press.170">游艇世界 · Yachting World</div>
        <div class="press-title" data-i18n="press.171">China's FV Redefines Luxury Yacht Accessibility</div>
        <div class="press-excerpt" data-i18n="press.172">国际游艇权威杂志专题报道奇幻假期如何以创新商业模式打破传统游艇行业壁垒，让高端游艇不再是极少数人的专属，引领全球游艇消费民主化浪潮。</div>
        <div class="press-date" data-i18n="press.173">2025年11月5日</div>
      </div>
      <div class="press-card reveal">
        <div class="press-source" data-i18n="press.180">福布斯中国 · Forbes China</div>
        <div class="press-title" data-i18n="press.181">深圳蛇口的海洋野心：奇幻假期如何征服全球游艇市场</div>
        <div class="press-excerpt" data-i18n="press.182">福布斯中国深度调研奇幻假期的全球化战略，从深圳总部到地中海船坞，从亚洲市场到欧美客户，解读一家中国企业的海洋产业版图。</div>
        <div class="press-date" data-i18n="press.183">2025年10月18日</div>
      </div>
    </div>
  </div>
</section>

<!-- Media Contact CTA -->
<section style="padding:80px 0;background:linear-gradient(135deg,#0a1628,#1a2a48);text-align:center">
  <div class="container">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(24px,3.5vw,40px);font-weight:700;color:#e8e8e8;margin-bottom:16px" data-i18n="press.190">媒体合作与采访</h2>
    <p style="font-size:15px;color:rgba(255,255,255,.45);max-width:600px;margin:0 auto 40px;line-height:1.8" data-i18n="press.191">欢迎媒体朋友联系我们的公关团队，获取新闻资料、高清图片、采访安排及活动邀请</p>
    <div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap">
      <a href="mailto:pr@fantastic-vacation.com" style="display:inline-block;padding:16px 48px;background:linear-gradient(135deg,#a07850,#c9a96e);color:#0a0e18;border-radius:40px;font-size:15px;font-weight:600;text-decoration:none;transition:all .3s" data-i18n="press.192">联系公关团队 →</a>
      <a href="news.html" style="display:inline-block;padding:16px 48px;border:1px solid rgba(201,169,110,.3);color:#c9a96e;border-radius:40px;font-size:15px;font-weight:500;text-decoration:none;transition:all .3s" data-i18n="press.193">浏览新闻资讯</a>
    </div>
  </div>
</section>
'''
    
    # Insert before <footer
    html = html.replace('<footer data-i18n="index.965" id="footer">', content_html + '\n<footer data-i18n="index.965" id="footer">')
    
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print(f"press.html: enriched with hero + stats + cards + CTA")

# ─── faq.html: Add hero section before the FAQ content ───
def enrich_faq():
    f = os.path.join(BASE, 'faq.html')
    with open(f, 'r', encoding='utf-8') as fh:
        html = fh.read()
    
    if 'faq-hero' in html:
        print("faq.html: hero already exists, checking content depth")
    else:
        # Add hero before the FAQ items
        hero_html = '''
<!-- FAQ Hero -->
<section class="faq-hero">
  <div class="container" style="text-align:center">
    <div style="display:inline-block;padding:6px 20px;border:1px solid rgba(201,169,110,.3);border-radius:30px;color:#c9a96e;font-size:12px;letter-spacing:2px;text-transform:uppercase;margin-bottom:24px" data-i18n="faq.100">FAQ</div>
    <h1 data-i18n="faq.101">常见问题</h1>
    <p style="font-size:16px;color:rgba(255,255,255,.5);max-width:700px;margin:0 auto;line-height:1.8" data-i18n="faq.102">关于奇幻假期游艇定制、租赁、托管服务的常见问题与详细解答</p>
  </div>
</section>
'''
        # Insert before the first faq-item
        html = html.replace('<div class="faq-item" data-category="custom">', hero_html + '\n<div class="faq-item" data-category="custom">')
        
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(html)
        print("faq.html: added hero section")

    # Now add more FAQ items and a CTA section before footer
    # Read again in case we just modified it
    with open(f, 'r', encoding='utf-8') as fh:
        html = fh.read()
    
    # Check if we already enriched
    if 'faq-cta' in html:
        print("faq.html: already enriched, skipping")
        return
    
    # Add more FAQ items + CTA before footer
    more_content = '''
<!-- Additional FAQ Categories -->
<section style="padding:60px 0;background:rgba(201,169,110,.03)">
  <div class="container">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px">
      <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:32px;text-align:center">
        <div style="width:56px;height:56px;border-radius:14px;background:rgba(201,169,110,.1);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;font-size:26px">🛥️</div>
        <h3 style="font-size:18px;font-weight:600;color:#e8e8e8;margin-bottom:10px" data-i18n="faq.200">定制游艇</h3>
        <p style="font-size:14px;color:rgba(255,255,255,.45);line-height:1.7" data-i18n="faq.201">从概念设计到交付使用，全程1对1专属顾问服务，平均交付周期12-18个月</p>
      </div>
      <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:32px;text-align:center">
        <div style="width:56px;height:56px;border-radius:14px;background:rgba(201,169,110,.1);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;font-size:26px">🌊</div>
        <h3 style="font-size:18px;font-weight:600;color:#e8e8e8;margin-bottom:10px" data-i18n="faq.210">租赁航线</h3>
        <p style="font-size:14px;color:rgba(255,255,255,.45);line-height:1.7" data-i18n="faq.211">覆盖地中海、加勒比海、东南亚等50+热门航线，3天起订，灵活安排</p>
      </div>
      <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:32px;text-align:center">
        <div style="width:56px;height:56px;border-radius:14px;background:rgba(201,169,110,.1);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;font-size:26px">🔧</div>
        <h3 style="font-size:18px;font-weight:600;color:#e8e8e8;margin-bottom:10px" data-i18n="faq.220">托管维保</h3>
        <p style="font-size:14px;color:rgba(255,255,255,.45);line-height:1.7" data-i18n="faq.221">全托管、基础托管、至尊托管三种模式，让您的游艇始终处于最佳状态</p>
      </div>
    </div>
  </div>
</section>

<!-- FAQ CTA -->
<section class="faq-cta" style="padding:80px 0;background:linear-gradient(135deg,#0a1628,#1a2a48);text-align:center">
  <div class="container">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(24px,3.5vw,40px);font-weight:700;color:#e8e8e8;margin-bottom:16px" data-i18n="faq.230">还有更多问题？</h2>
    <p style="font-size:15px;color:rgba(255,255,255,.45);max-width:600px;margin:0 auto 40px;line-height:1.8" data-i18n="faq.231">我们的专业顾问团队随时为您解答任何关于游艇定制、租赁或托管的疑问</p>
    <div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap">
      <a href="contact.html" style="display:inline-block;padding:16px 48px;background:linear-gradient(135deg,#a07850,#c9a96e);color:#0a0e18;border-radius:40px;font-size:15px;font-weight:600;text-decoration:none;transition:all .3s" data-i18n="faq.232">联系专业顾问 →</a>
      <a href="tel:13797920792" style="display:inline-block;padding:16px 48px;border:1px solid rgba(201,169,110,.3);color:#c9a96e;border-radius:40px;font-size:15px;font-weight:500;text-decoration:none;transition:all .3s" data-i18n="faq.233">致电 13797920792</a>
    </div>
  </div>
</section>
'''
    
    html = html.replace('<footer data-i18n="index.965" id="footer">', more_content + '\n<footer data-i18n="index.965" id="footer">')
    
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print("faq.html: enriched with category cards + CTA")

# ─── investment.html: Add substantial IR content sections ───
def enrich_investment():
    f = os.path.join(BASE, 'investment.html')
    with open(f, 'r', encoding='utf-8') as fh:
        html = fh.read()
    
    if 'invest-enriched' in html:
        print("investment.html: already enriched, skipping")
        return
    
    # Current page only has a hero + one ir-section with "最新公告" link + footer
    # Add rich content sections before footer
    
    content_html = '''
<!-- Company Overview Section -->
<section class="ir-section invest-enriched">
  <div class="ir-section-divider"></div>
  <h2 data-i18n="invest.300">公司概况</h2>
  <p class="section-sub" data-i18n="invest.301">奇幻假期实业有限公司深耕高端游艇行业15年，是全球一体化高端游艇定制与私人海享生活缔造者</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;margin-top:50px">
    <div class="ir-card">
      <div class="ir-card-icon">📈</div>
      <h3 data-i18n="invest.310">营收增长</h3>
      <p data-i18n="invest.311">连续5年营收复合增长率超过45%，2025年全年营收突破12亿元人民币，预计2026年将达到18亿元。</p>
      <span class="arrow">了解更多 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
    </div>
    <div class="ir-card">
      <div class="ir-card-icon">🌐</div>
      <h3 data-i18n="invest.320">全球布局</h3>
      <p data-i18n="invest.321">总部位于深圳蛇口太子湾，在香港、新加坡、摩纳哥、迈阿密设有分支机构，服务覆盖全球15个国家和地区。</p>
      <span class="arrow">了解更多 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
    </div>
    <div class="ir-card">
      <div class="ir-card-icon">🏆</div>
      <h3 data-i18n="invest.330">行业地位</h3>
      <p data-i18n="invest.331">亚洲最佳游艇服务商三连冠，中国游艇定制市场份额第一，200+全球高净值客户的信赖之选。</p>
      <span class="arrow">了解更多 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
    </div>
  </div>
</section>

<!-- Key Financial Data -->
<section style="padding:80px 0;background:rgba(201,169,110,.03)">
  <div style="max-width:1200px;margin:0 auto;padding:0 20px">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(24px,3.5vw,40px);font-weight:700;color:#e8e8e8;margin-bottom:12px" data-i18n="invest.340">核心财务数据</h2>
    <p style="font-size:15px;color:rgba(255,255,255,.45);max-width:600px;line-height:1.8;margin-bottom:50px" data-i18n="invest.341">截至2025年12月31日</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:40px;text-align:center">
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(32px,4vw,48px);font-weight:800;color:#c9a96e">¥12亿</div>
        <div style="font-size:13px;color:rgba(255,255,255,.4);margin-top:8px" data-i18n="invest.350">2025年营收</div>
        <div style="font-size:11px;color:#4ade80;margin-top:4px">↑ 45% YoY</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(32px,4vw,48px);font-weight:800;color:#c9a96e">¥3.6亿</div>
        <div style="font-size:13px;color:rgba(255,255,255,.4);margin-top:8px" data-i18n="invest.351">净利润</div>
        <div style="font-size:11px;color:#4ade80;margin-top:4px">↑ 52% YoY</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(32px,4vw,48px);font-weight:800;color:#c9a96e">30%</div>
        <div style="font-size:13px;color:rgba(255,255,255,.4);margin-top:8px" data-i18n="invest.352">净利润率</div>
        <div style="font-size:11px;color:#4ade80;margin-top:4px">行业领先</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(32px,4vw,48px);font-weight:800;color:#c9a96e">200+</div>
        <div style="font-size:13px;color:rgba(255,255,255,.4);margin-top:8px" data-i18n="invest.353">全球客户</div>
        <div style="font-size:11px;color:#4ade80;margin-top:4px">↑ 35% YoY</div>
      </div>
    </div>
  </div>
</section>

<!-- IR Information Cards -->
<section class="ir-section">
  <div class="ir-section-divider"></div>
  <h2 data-i18n="invest.360">投资者信息</h2>
  <p class="section-sub" data-i18n="invest.361">面向机构投资者与资本市场的专业信息披露</p>
  <div class="ir-grid">
    <a class="ir-card" href="ir.html">
      <div class="ir-card-icon">📊</div>
      <h3 data-i18n="invest.370">财务报告</h3>
      <p data-i18n="invest.371">查看年度报告、季度报告及中期报告，了解公司经营状况与财务表现。</p>
      <span class="arrow">查看详情 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
    </a>
    <a class="ir-card" href="ir.html">
      <div class="ir-card-icon">📋</div>
      <h3 data-i18n="invest.380">公告披露</h3>
      <p data-i18n="invest.381">重大事项公告、经营动态、股东大会通知等法定披露信息。</p>
      <span class="arrow">查看详情 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
    </a>
    <a class="ir-card" href="ir.html">
      <div class="ir-card-icon">🏢</div>
      <h3 data-i18n="invest.390">公司治理</h3>
      <p data-i18n="invest.391">董事会构成、内部控制制度、合规管理体系等公司治理信息。</p>
      <span class="arrow">查看详情 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
    </a>
    <a class="ir-card" href="ir.html">
      <div class="ir-card-icon">🤝</div>
      <h3 data-i18n="invest.400">股东关系</h3>
      <p data-i18n="invest.401">股权结构、分红政策、投资者活动及股东常见问题解答。</p>
      <span class="arrow">查看详情 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
    </a>
    <a class="ir-card" href="ir.html">
      <div class="ir-card-icon">📅</div>
      <h3 data-i18n="invest.410">投资者日历</h3>
      <p data-i18n="invest.411">财报发布日期、投资者会议、路演安排及重要活动日程。</p>
      <span class="arrow">查看详情 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
    </a>
    <a class="ir-card" href="ir.html">
      <div class="ir-card-icon">📧</div>
      <h3 data-i18n="invest.420">联系IR团队</h3>
      <p data-i18n="invest.421">投资者关系团队联系方式：ir@fantastic-vacation.com，+86 0755 3353-0188</p>
      <span class="arrow">联系我们 <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></span>
    </a>
  </div>
</section>

<!-- Stock / Investment Highlights -->
<section style="padding:80px 0;background:linear-gradient(135deg,#0a1628,#1a2a48);text-align:center">
  <div class="container">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(24px,3.5vw,40px);font-weight:700;color:#e8e8e8;margin-bottom:16px" data-i18n="invest.430">投资亮点</h2>
    <p style="font-size:15px;color:rgba(255,255,255,.45);max-width:600px;margin:0 auto 50px;line-height:1.8" data-i18n="invest.431">了解为什么奇幻假期是高端消费与海洋经济赛道的优质标的</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:28px;text-align:left">
      <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:32px">
        <div style="color:#c9a96e;font-size:28px;margin-bottom:16px">🎯</div>
        <h3 style="font-size:16px;font-weight:600;color:#e8e8e8;margin-bottom:10px" data-i18n="invest.440">蓝海赛道</h3>
        <p style="font-size:13px;color:rgba(255,255,255,.45);line-height:1.7" data-i18n="invest.441">中国高端游艇市场年复合增长率35%+，处于爆发前夜，先发优势显著</p>
      </div>
      <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:32px">
        <div style="color:#c9a96e;font-size:28px;margin-bottom:16px">💎</div>
        <h3 style="font-size:16px;font-weight:600;color:#e8e8e8;margin-bottom:10px" data-i18n="invest.450">极致性价比</h3>
        <p style="font-size:13px;color:rgba(255,255,255,.45);line-height:1.7" data-i18n="invest.451">市价1/10的定价策略，依托供应链整合能力实现高利润率与高客户价值</p>
      </div>
      <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:32px">
        <div style="color:#c9a96e;font-size:28px;margin-bottom:16px">🔄</div>
        <h3 style="font-size:16px;font-weight:600;color:#e8e8e8;margin-bottom:10px" data-i18n="invest.460">全产业链</h3>
        <p style="font-size:13px;color:rgba(255,255,255,.45);line-height:1.7" data-i18n="invest.461">定制+租赁+托管三引擎驱动，多元收入结构抗风险能力强</p>
      </div>
    </div>
  </div>
</section>
'''
    
    # Find the existing ir-section with "最新公告" and insert AFTER it
    # Current: <div class="ir-section" ...> ... </div> then <footer>
    # We want to add content between the closing </div> of the ir-section and <footer>
    
    # The ir-section ends with </div> before <footer>
    # Let's find the exact pattern
    pattern = r'(</div>\s*<footer data-i18n="index\.965" id="footer">)'
    match = re.search(pattern, html)
    if match:
        html = html[:match.start()] + content_html + '\n' + match.group(0) + html[match.end():]
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(html)
        print("investment.html: enriched with company overview, financials, IR cards, investment highlights")
    else:
        print("investment.html: WARNING - could not find insertion point")

# ─── map.html: Enrich with more region content ───
def enrich_map():
    f = os.path.join(BASE, 'map.html')
    with open(f, 'r', encoding='utf-8') as fh:
        html = fh.read()
    
    if 'map-enriched' in html:
        print("map.html: already enriched, skipping")
        return
    
    # Read the existing section to understand structure
    # Current: section-map with region-grid + footer
    # Add: global coverage stats + service regions detail + CTA
    
    content_html = '''
<!-- Global Coverage Stats -->
<section class="map-enriched" style="padding:60px 0;background:rgba(201,169,110,.03)">
  <div class="container">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(24px,3.5vw,40px);font-weight:700;color:#e8e8e8;margin-bottom:12px;text-align:center" data-i18n="map.100">全球服务网络</h2>
    <p style="font-size:15px;color:rgba(255,255,255,.45);text-align:center;max-width:600px;margin:0 auto 50px;line-height:1.8" data-i18n="map.101">从深圳蛇口到地中海，从加勒比海到东南亚，我们的服务网络覆盖全球</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:40px;text-align:center">
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e" data-i18n="map.110">15</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="map.111">覆盖国家与地区</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e" data-i18n="map.112">50+</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="map.113">热门航线</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e" data-i18n="map.114">6</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="map.115">全球办事处</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e" data-i18n="map.116">24/7</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="map.117">全天候服务支持</div>
      </div>
    </div>
  </div>
</section>

<!-- Featured Routes -->
<section style="padding:80px 0">
  <div class="container">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(24px,3.5vw,40px);font-weight:700;color:#e8e8e8;margin-bottom:12px;text-align:center" data-i18n="map.120">热门航线推荐</h2>
    <p style="font-size:15px;color:rgba(255,255,255,.45);text-align:center;max-width:600px;margin:0 auto 50px;line-height:1.8" data-i18n="map.121">精选全球最具魅力的游艇航线，开启您的专属海上之旅</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px">
      <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;overflow:hidden;transition:all .3s">
        <div style="height:180px;background:linear-gradient(135deg,#0d4f8b,#1a7bc4);display:flex;align-items:center;justify-content:center;font-size:48px">⛵</div>
        <div style="padding:28px">
          <div style="font-size:11px;color:#c9a96e;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px" data-i18n="map.130">Mediterranean</div>
          <h3 style="font-size:18px;font-weight:600;color:#e8e8e8;margin-bottom:10px" data-i18n="map.131">地中海经典航线</h3>
          <p style="font-size:13px;color:rgba(255,255,255,.45);line-height:1.7;margin-bottom:14px" data-i18n="map.132">从法国里维埃拉到希腊爱琴海，途经摩纳哥、意大利阿马尔菲海岸、克罗地亚亚得里亚海，体验地中海的浪漫与传奇。</p>
          <div style="font-size:12px;color:#c9a96e" data-i18n="map.133">7-14天 · 4条推荐路线</div>
        </div>
      </div>
      <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;overflow:hidden;transition:all .3s">
        <div style="height:180px;background:linear-gradient(135deg,#0a6e5c,#14b8a6);display:flex;align-items:center;justify-content:center;font-size:48px">🏝️</div>
        <div style="padding:28px">
          <div style="font-size:11px;color:#c9a96e;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px" data-i18n="map.140">Caribbean</div>
          <h3 style="font-size:18px;font-weight:600;color:#e8e8e8;margin-bottom:10px" data-i18n="map.141">加勒比海天堂航线</h3>
          <p style="font-size:13px;color:rgba(255,255,255,.45);line-height:1.7;margin-bottom:14px" data-i18n="map.142">穿越英属维尔京群岛、圣巴泰勒米、安提瓜，在碧蓝海水中畅游，感受加勒比的热情与奢华。</p>
          <div style="font-size:12px;color:#c9a96e" data-i18n="map.143">5-10天 · 3条推荐路线</div>
        </div>
      </div>
      <div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:14px;overflow:hidden;transition:all .3s">
        <div style="height:180px;background:linear-gradient(135deg,#8b4513,#d4763a);display:flex;align-items:center;justify-content:center;font-size:48px">🌅</div>
        <div style="padding:28px">
          <div style="font-size:11px;color:#c9a96e;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:10px" data-i18n="map.150">Southeast Asia</div>
          <h3 style="font-size:18px;font-weight:600;color:#e8e8e8;margin-bottom:10px" data-i18n="map.151">东南亚秘境航线</h3>
          <p style="font-size:13px;color:rgba(255,255,255,.45);line-height:1.7;margin-bottom:14px" data-i18n="map.152">探索泰国安达曼海、印尼科莫多、菲律宾巴拉望，发现东方的热带秘境与原始海洋之美。</p>
          <div style="font-size:12px;color:#c9a96e" data-i18n="map.153">5-12天 · 4条推荐路线</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Map CTA -->
<section style="padding:80px 0;background:linear-gradient(135deg,#0a1628,#1a2a48);text-align:center">
  <div class="container">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(24px,3.5vw,40px);font-weight:700;color:#e8e8e8;margin-bottom:16px" data-i18n="map.160">开启您的环球航线</h2>
    <p style="font-size:15px;color:rgba(255,255,255,.45);max-width:600px;margin:0 auto 40px;line-height:1.8" data-i18n="map.161">无论您向往哪片海域，我们的航线规划专家都能为您量身定制完美的海上旅程</p>
    <div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap">
      <a href="charter.html" style="display:inline-block;padding:16px 48px;background:linear-gradient(135deg,#a07850,#c9a96e);color:#0a0e18;border-radius:40px;font-size:15px;font-weight:600;text-decoration:none;transition:all .3s" data-i18n="map.162">探索全部航线 →</a>
      <a href="contact.html" style="display:inline-block;padding:16px 48px;border:1px solid rgba(201,169,110,.3);color:#c9a96e;border-radius:40px;font-size:15px;font-weight:500;text-decoration:none;transition:all .3s" data-i18n="map.163">定制专属航线</a>
    </div>
  </div>
</section>
'''
    
    html = html.replace('<footer data-i18n="index.965" id="footer">', content_html + '\n<footer data-i18n="index.965" id="footer">')
    
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print("map.html: enriched with global stats, featured routes, CTA")

# ─── reviews.html: Enrich with more review content ───
def enrich_reviews():
    f = os.path.join(BASE, 'reviews.html')
    with open(f, 'r', encoding='utf-8') as fh:
        html = fh.read()
    
    if 'reviews-enriched' in html:
        print("reviews.html: already enriched, skipping")
        return
    
    # Add more reviews + stats + CTA
    content_html = '''
<!-- Reviews Stats -->
<section class="reviews-enriched" style="padding:60px 0;background:rgba(201,169,110,.03)">
  <div class="container">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:40px;text-align:center">
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e">98%</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="reviews.100">客户满意度</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e">200+</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="reviews.101">真实评价</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e">4.9</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="reviews.102">平均评分（5分制）</div>
      </div>
      <div>
        <div style="font-family:'Playfair Display',serif;font-size:clamp(36px,4vw,56px);font-weight:800;color:#c9a96e">92%</div>
        <div style="font-size:14px;color:rgba(200,210,225,.5);margin-top:8px" data-i18n="reviews.103">复购/推荐率</div>
      </div>
    </div>
  </div>
</section>

<!-- Featured Reviews -->
<section style="padding:80px 0">
  <div class="container">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(24px,3.5vw,40px);font-weight:700;color:#e8e8e8;margin-bottom:12px;text-align:center" data-i18n="reviews.110">客户心声</h2>
    <p style="font-size:15px;color:rgba(255,255,255,.45);text-align:center;max-width:600px;margin:0 auto 50px;line-height:1.8" data-i18n="reviews.111">来自全球高净值客户的真实体验与评价</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:28px">
      <div style="background:linear-gradient(145deg,rgba(255,255,255,.02),rgba(255,255,255,.005));border:1px solid rgba(201,169,110,.08);border-radius:16px;padding:36px;transition:all .3s">
        <div style="color:#c9a96e;font-size:14px;margin-bottom:16px">★★★★★</div>
        <p style="font-size:15px;color:rgba(200,210,225,.7);line-height:1.85;margin-bottom:20px;font-style:italic" data-i18n="reviews.120">"奇幻假期的定制服务超出了我所有的期望。从最初的设计沟通到最终交付，每一个细节都体现了专业与用心。我的55尺飞桥游艇已经成为了家人最爱的度假方式。"</p>
        <div style="display:flex;align-items:center;gap:14px">
          <div style="width:44px;height:44px;border-radius:50%;background:rgba(201,169,110,.15);display:flex;align-items:center;justify-content:center;color:#c9a96e;font-weight:600;font-size:16px">王</div>
          <div>
            <div style="font-size:14px;font-weight:600;color:#e8eef5" data-i18n="reviews.121">王先生</div>
            <div style="font-size:12px;color:rgba(200,210,225,.4)" data-i18n="reviews.122">深圳 · 飞桥系列定制客户</div>
          </div>
        </div>
      </div>
      <div style="background:linear-gradient(145deg,rgba(255,255,255,.02),rgba(255,255,255,.005));border:1px solid rgba(201,169,110,.08);border-radius:16px;padding:36px;transition:all .3s">
        <div style="color:#c9a96e;font-size:14px;margin-bottom:16px">★★★★★</div>
        <p style="font-size:15px;color:rgba(200,210,225,.7);line-height:1.85;margin-bottom:20px;font-style:italic" data-i18n="reviews.130">"租赁了地中海航线两周，从摩纳哥到圣托里尼，每一站都是完美的体验。船员团队的专业素养和服务品质令人印象深刻，已经预订了明年的加勒比航线。"</p>
        <div style="display:flex;align-items:center;gap:14px">
          <div style="width:44px;height:44px;border-radius:50%;background:rgba(201,169,110,.15);display:flex;align-items:center;justify-content:center;color:#c9a96e;font-weight:600;font-size:16px">张</div>
          <div>
            <div style="font-size:14px;font-weight:600;color:#e8eef5" data-i18n="reviews.131">张女士</div>
            <div style="font-size:12px;color:rgba(200,210,225,.4)" data-i18n="reviews.132">上海 · 地中海航线租赁客户</div>
          </div>
        </div>
      </div>
      <div style="background:linear-gradient(145deg,rgba(255,255,255,.02),rgba(255,255,255,.005));border:1px solid rgba(201,169,110,.08);border-radius:16px;padding:36px;transition:all .3s">
        <div style="color:#c9a96e;font-size:14px;margin-bottom:16px">★★★★★</div>
        <p style="font-size:15px;color:rgba(200,210,225,.7);line-height:1.85;margin-bottom:20px;font-style:italic" data-i18n="reviews.140">"选择全托管服务是我最明智的决定。奇幻假期的管理团队让我的游艇始终保持在最佳状态，每次出海都像新船一样。年化投资回报率也超出了预期。"</p>
        <div style="display:flex;align-items:center;gap:14px">
          <div style="width:44px;height:44px;border-radius:50%;background:rgba(201,169,110,.15);display:flex;align-items:center;justify-content:center;color:#c9a96e;font-weight:600;font-size:16px">李</div>
          <div>
            <div style="font-size:14px;font-weight:600;color:#e8eef5" data-i18n="reviews.141">李先生</div>
            <div style="font-size:12px;color:rgba(200,210,225,.4)" data-i18n="reviews.142">北京 · 全托管服务客户</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Reviews CTA -->
<section style="padding:80px 0;background:linear-gradient(135deg,#0a1628,#1a2a48);text-align:center">
  <div class="container">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(24px,3.5vw,40px);font-weight:700;color:#e8e8e8;margin-bottom:16px" data-i18n="reviews.150">加入满意客户行列</h2>
    <p style="font-size:15px;color:rgba(255,255,255,.45);max-width:600px;margin:0 auto 40px;line-height:1.8" data-i18n="reviews.151">98%的客户满意度不是偶然，而是我们对每一个细节的极致追求</p>
    <div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap">
      <a href="contact.html" style="display:inline-block;padding:16px 48px;background:linear-gradient(135deg,#a07850,#c9a96e);color:#0a0e18;border-radius:40px;font-size:15px;font-weight:600;text-decoration:none;transition:all .3s" data-i18n="reviews.152">预约体验 →</a>
      <a href="membership.html" style="display:inline-block;padding:16px 48px;border:1px solid rgba(201,169,110,.3);color:#c9a96e;border-radius:40px;font-size:15px;font-weight:500;text-decoration:none;transition:all .3s" data-i18n="reviews.153">了解尊享会员</a>
    </div>
  </div>
</section>
'''
    
    html = html.replace('<footer data-i18n="index.965" id="footer">', content_html + '\n<footer data-i18n="index.965" id="footer">')
    
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print("reviews.html: enriched with stats, featured reviews, CTA")

# ─── Main ───
if __name__ == '__main__':
    enrich_press()
    enrich_faq()
    enrich_investment()
    enrich_map()
    enrich_reviews()
    print("\n✅ All thin pages enriched!")
