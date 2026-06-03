#!/usr/bin/env python3
"""
Insert rich content sections into all 10 partner-type pages
and update i18n.js with all required dictionary entries.
"""

import re, json

# Import content database
exec(open('build_partner_content.py').read())

# ============================================================
# PHASE 1: Generate i18n entries
# ============================================================

def build_i18n_entries():
    """Build all i18n dictionary entries for partner pages."""
    entries = {}
    for ptype, data in CONTENT.items():
        slug = ptype.replace("partner-type-", "")
        ns = f"partner-type-{slug}"
        
        # Overview
        entries[f"{ns}.600"] = {"zh": data["sections"]["overview"]["zh"], "en": data["sections"]["overview"]["en"]}
        entries[f"{ns}.601"] = {"zh": "合作概述", "en": "Partnership Overview"}
        
        # Benefits
        benefits = data["sections"]["benefits"]
        entries[f"{ns}.610"] = {"zh": benefits["title_zh"], "en": benefits["title_en"]}
        for i, item in enumerate(benefits["items"]):
            entries[f"{ns}.b{i}"] = {"zh": item["zh"], "en": item["en"]}
        
        # Tiers
        tiers = data["sections"]["tiers"]
        entries[f"{ns}.620"] = {"zh": tiers["title_zh"], "en": tiers["title_en"]}
        for i, item in enumerate(tiers["items"]):
            entries[f"{ns}.tier{i}_name"] = {"zh": item["zh"], "en": item["en"]}
            entries[f"{ns}.tier{i}_desc"] = {"zh": item["desc_zh"], "en": item["desc_en"]}
        
        # Process
        process = data["sections"]["process"]
        entries[f"{ns}.640"] = {"zh": process["title_zh"], "en": process["title_en"]}
        for i, step in enumerate(process["steps"]):
            entries[f"{ns}.step{i}_name"] = {"zh": step["zh"], "en": step["en"]}
            entries[f"{ns}.step{i}_desc"] = {"zh": step["desc_zh"], "en": step["desc_en"]}
        
        # FAQ
        faq = data["sections"]["faq"]
        entries[f"{ns}.650"] = {"zh": faq["title_zh"], "en": faq["title_en"]}
        for i, item in enumerate(faq["items"]):
            entries[f"{ns}.faq{i}_q"] = {"zh": item["q_zh"], "en": item["q_en"]}
            entries[f"{ns}.faq{i}_a"] = {"zh": item["a_zh"], "en": item["a_en"]}
    
    return entries


# ============================================================
# PHASE 2: Generate HTML content for insertion
# ============================================================

def build_html_content(ptype, data):
    """Build HTML sections for a partner-type page."""
    slug = ptype.replace("partner-type-", "")
    ns = f"partner-type-{slug}"
    
    # Map pages to their index for icon selection
    idx = list(CONTENT.keys()).index(ptype)
    icons = ['🏭', '⚓', '✈️', '🏨', '🎨', '🏛️', '🤝', '🔧', '🌐', '💻']
    icon = icons[idx]
    
    sections = []
    
    # === 1. Partnership Overview ===
    overview = data["sections"]["overview"]
    sections.append(f'''\n
    <!-- ===== 合作概述 ===== -->
    <section class="section-padding" style="background:var(--dark3)">
      <div class="container" style="max-width:1100px">
        <div class="section-header reveal">
          <span class="section-label gold-gradient" data-i18n="{ns}.601">合作概述</span>
          <h2><span class="gold-gradient" data-i18n="{ns}.601">合作概述</span></h2>
          <div class="divider-gold"></div>
        </div>
        <p data-i18n="{ns}.600" style="color:var(--text-muted);font-size:16px;line-height:1.9;max-width:900px;margin:0 auto;text-align:center">{overview["zh"]}</p>
      </div>
    </section>''')
    
    # === 2. Partnership Benefits ===
    benefits = data["sections"]["benefits"]
    cards = ""
    for i, item in enumerate(benefits["items"]):
        cards += f'''
          <div class="benefit-card reveal" style="background:rgba(255,255,255,0.03);border:1px solid rgba(201,169,110,0.15);border-radius:12px;padding:32px 28px;text-align:center;transition:all .3s ease"
            onmouseenter="this.style.transform='translateY(-4px)';this.style.borderColor='rgba(201,169,110,0.4)';this.style.boxShadow='0 12px 40px rgba(0,0,0,0.3)'"
            onmouseleave="this.style.transform='';this.style.borderColor='';this.style.boxShadow=''">
            <div style="font-size:36px;margin-bottom:18px">{icon}</div>
            <h4 data-i18n="{ns}.b{i}" style="font-size:17px;color:#fff;margin-bottom:10px;font-weight:500">{item["zh"]}</h4>
          </div>'''
    
    sections.append(f'''\n
    <!-- ===== 合作优势 ===== -->
    <section class="section-padding" style="background:var(--dark2)">
      <div class="container" style="max-width:1200px">
        <div class="section-header reveal">
          <span class="section-label gold-gradient" data-i18n="{ns}.610">合作优势</span>
          <h2><span class="gold-gradient" data-i18n="{ns}.610">{benefits["title_zh"]}</span></h2>
          <div class="divider-gold"></div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px;margin-top:40px">{cards}
        </div>
      </div>
    </section>''')
    
    # === 3. Partnership Tiers ===
    tiers = data["sections"]["tiers"]
    tier_cards = ""
    tier_icons_list = ['💎', '⭐', '🔹']
    for i, item in enumerate(tiers["items"]):
        ti = tier_icons_list[i] if i < len(tier_icons_list) else '🔹'
        opacity = 0.25 - i * 0.08
        tier_cards += f'''
          <div class="tier-card reveal" style="background:rgba(255,255,255,0.03);border:1px solid rgba(201,169,110,{opacity:.2f});border-radius:16px;padding:40px 32px;text-align:center;transition:all .3s ease"
            onmouseenter="this.style.transform='translateY(-4px)';this.style.borderColor='rgba(201,169,110,0.5)';this.style.boxShadow='0 12px 40px rgba(0,0,0,0.3)'"
            onmouseleave="this.style.transform='';this.style.borderColor='';this.style.boxShadow=''">
            <div style="font-size:40px;margin-bottom:18px">{ti}</div>
            <h3 data-i18n="{ns}.tier{i}_name" style="font-size:22px;color:var(--gold);margin-bottom:16px;font-family:'Playfair Display',serif">{item["zh"]}</h3>
            <p data-i18n="{ns}.tier{i}_desc" style="color:var(--text-muted);font-size:14px;line-height:1.7">{item["desc_zh"]}</p>
          </div>'''
    
    sections.append(f'''\n
    <!-- ===== 合作层级 ===== -->
    <section class="section-padding" style="background:var(--dark3)">
      <div class="container" style="max-width:1200px">
        <div class="section-header reveal">
          <span class="section-label gold-gradient" data-i18n="{ns}.620">合作层级</span>
          <h2><span class="gold-gradient" data-i18n="{ns}.620">{tiers["title_zh"]}</span></h2>
          <div class="divider-gold"></div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;margin-top:40px">{tier_cards}
        </div>
      </div>
    </section>''')
    
    # === 4. Partnership Process ===
    process = data["sections"]["process"]
    steps = ""
    for i, step in enumerate(process["steps"]):
        steps += f'''
          <div class="process-step reveal" style="display:flex;gap:24px;align-items:flex-start;padding:32px 0;border-bottom:1px solid rgba(201,169,110,0.1)">
            <div style="flex-shrink:0;width:64px;height:64px;border-radius:50%;background:linear-gradient(135deg,rgba(201,169,110,0.25),rgba(201,169,110,0.05));border:2px solid var(--gold);display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:700;color:var(--gold)">{i+1}</div>
            <div style="padding-top:10px">
              <h4 data-i18n="{ns}.step{i}_name" style="font-size:19px;color:#fff;margin-bottom:10px;font-weight:500">{step["zh"]}</h4>
              <p data-i18n="{ns}.step{i}_desc" style="color:var(--text-muted);font-size:15px;line-height:1.7">{step["desc_zh"]}</p>
            </div>
          </div>'''
    
    sections.append(f'''\n
    <!-- ===== 合作流程 ===== -->
    <section class="section-padding" style="background:var(--dark2)">
      <div class="container" style="max-width:900px">
        <div class="section-header reveal">
          <span class="section-label gold-gradient" data-i18n="{ns}.640">合作流程</span>
          <h2><span class="gold-gradient" data-i18n="{ns}.640">{process["title_zh"]}</span></h2>
          <div class="divider-gold"></div>
        </div>
        <div style="margin-top:40px">{steps}
        </div>
      </div>
    </section>''')
    
    # === 5. FAQ ===
    faq = data["sections"]["faq"]
    faq_items = ""
    for i, item in enumerate(faq["items"]):
        faq_id = f"faq_{slug}_{i}"
        faq_items += f'''
          <div class="faq-item reveal" style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:12px;overflow:hidden;margin-bottom:16px">
            <button class="faq-question" onclick="var a=this.parentElement;a.classList.toggle('active')" style="width:100%;text-align:left;background:none;border:none;padding:24px 28px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;color:#fff;font-size:16px;font-weight:500;transition:background .2s"
              onmouseenter="this.style.background='rgba(201,169,110,0.04)'" onmouseleave="this.style.background=''">
              <span data-i18n="{ns}.faq{i}_q">{item["q_zh"]}</span>
              <svg class="faq-arrow" fill="none" height="20" stroke="var(--gold)" stroke-width="2" viewBox="0 0 24 24" width="20" style="transition:transform .3s ease"><path d="m6 9 6 6 6-6"></path></svg>
            </button>
            <div class="faq-answer" style="max-height:0;overflow:hidden;transition:max-height .4s ease">
              <p data-i18n="{ns}.faq{i}_a" style="padding:0 28px 24px;color:var(--text-muted);font-size:15px;line-height:1.8">{item["a_zh"]}</p>
            </div>
          </div>'''
    
    sections.append(f'''\n
    <!-- ===== 常见问题 ===== -->
    <section class="section-padding" style="background:var(--dark3)">
      <div class="container" style="max-width:900px">
        <div class="section-header reveal">
          <span class="section-label gold-gradient" data-i18n="{ns}.650">常见问题</span>
          <h2><span class="gold-gradient" data-i18n="{ns}.650">{faq["title_zh"]}</span></h2>
          <div class="divider-gold"></div>
        </div>
        <div style="margin-top:40px">{faq_items}
        </div>
        <style>.faq-item.active .faq-arrow{{transform:rotate(180deg)}}.faq-item.active .faq-answer{{max-height:800px!important}}</style>
      </div>
    </section>''')
    
    return "".join(sections)


# ============================================================
# PHASE 3: Insert content into HTML files
# ============================================================

def insert_content_into_pages():
    """Insert generated content into all 10 partner-type pages."""
    pages_dir = '/Users/stone/Desktop/www/YT'
    changes = {}
    
    for ptype in CONTENT:
        filepath = f"{pages_dir}/{ptype}.html"
        with open(filepath) as f:
            html = f.read()
        
        # Find insertion point: right before the CTA section
        # The CTA section is the last <section> before <footer>
        footer_pos = html.rfind('<footer')
        if footer_pos < 0:
            print(f"  ERROR: No footer in {ptype}.html")
            continue
        
        # Find all <section> tags before footer
        section_starts = [m.start() for m in re.finditer(r'<section', html) if m.start() < footer_pos]
        
        if len(section_starts) < 2:
            print(f"  ERROR: Not enough sections in {ptype}.html ({len(section_starts)})")
            continue
        
        cta_section_pos = section_starts[-1]  # Last section = CTA
        core_section_pos = section_starts[-2]  # Second-to-last = core partners
        
        # The core partners section closes right before the CTA section starts
        core_close = html.rfind('</section>', core_section_pos, cta_section_pos)
        if core_close < 0:
            print(f"  ERROR: Can't find core section close in {ptype}.html")
            continue
        
        insert_at = core_close + len('</section>')
        
        # Build content
        new_content = build_html_content(ptype, CONTENT[ptype])
        
        # Verify it doesn't break
        if not new_content.strip():
            print(f"  ERROR: Empty content for {ptype}")
            continue
        
        # Insert
        new_html = html[:insert_at] + new_content + html[insert_at:]
        
        # Verify structure integrity
        # Count sections before and after
        sections_before = len(re.findall(r'<section', html))
        sections_after = len(re.findall(r'<section', new_html))
        new_sections = sections_after - sections_before
        
        # Also count closing tags
        closes_before = len(re.findall(r'</section>', html))
        closes_after = len(re.findall(r'</section>', new_html))
        
        # Write
        with open(filepath, 'w') as f:
            f.write(new_html)
        
        changes[ptype] = {
            "size_before": len(html),
            "size_after": len(new_html),
            "sections_added": new_sections,
            "sections_before": sections_before,
            "sections_after": sections_after,
            "closes_before": closes_before,
            "closes_after": closes_after
        }
        
        print(f"  {ptype}: +{len(new_html)-len(html)} chars, "
              f"{new_sections} new sections, "
              f"closes {closes_before}→{closes_after}")
    
    return changes


# ============================================================
# PHASE 4: Update i18n.js
# ============================================================

def update_i18n_js():
    """Add all new dict entries to i18n.js."""
    filepath = '/Users/stone/Desktop/www/YT/i18n.js'
    with open(filepath) as f:
        js = f.read()
    
    entries = build_i18n_entries()
    
    # Build the new dict entries as JS
    new_lines = []
    for key in sorted(entries.keys()):
        zh = entries[key]["zh"].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        en = entries[key]["en"].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        new_lines.append(f'  "{key}": {{ "zh": "{zh}", "en": "{en}" }},')
    
    new_block = "  // === Partner detail page content (auto-generated) ===\n" + "\n".join(new_lines) + "\n"
    
    # Find insertion point: the dict closing `};` — search from end
    lines = js.split('\n')
    insert_line = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == '};':
            insert_line = i
            break
    
    if insert_line is None:
        print("  ERROR: Cannot find dict closing }}; in i18n.js")
        return None
    
    lines.insert(insert_line, new_block.rstrip('\n'))
    new_js = '\n'.join(lines)
    
    with open(filepath, 'w') as f:
        f.write(new_js)
    
    return len(entries)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("=== Phase 1: Generating i18n entries ===")
    entries = build_i18n_entries()
    print(f"  Total new i18n entries: {len(entries)}")
    
    print("\n=== Phase 2: Inserting content into HTML pages ===")
    changes = insert_content_into_pages()
    
    print(f"\n=== Phase 3: Updating i18n.js ===")
    count = update_i18n_js()
    print(f"  Added {count} dictionary entries to i18n.js")
    
    # Verify
    print("\n=== Verification ===")
    for ptype in CONTENT:
        fp = f'/Users/stone/Desktop/www/YT/{ptype}.html'
        with open(fp) as f:
            html = f.read()
        sections = len(re.findall(r'<section', html))
        closes = len(re.findall(r'</section>', html))
        match = "✓" if sections == closes else "✗ MISMATCH"
        print(f"  {ptype}: {len(html)} chars, {sections} sections, {closes} closes {match}")
    
    print("\nDone!")
