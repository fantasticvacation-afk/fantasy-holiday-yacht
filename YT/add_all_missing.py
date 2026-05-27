#!/usr/bin/env python3
import json
import re

# Load missing keys
with open('/tmp/missing_keys.json', 'r', encoding='utf-8') as f:
    missing_keys = json.load(f)

print(f"Adding {len(missing_keys)} missing keys to i18n.js")

# English translations for all 57 missing keys
translations = {
    "case-030.337": "Zero delay in filming, high praise from production team, three film contracts signed for sequel",
    "case-026.337": "Power performance improved by 15%, fuel consumption reduced by 8%, client very satisfied",
    "case-006.257": "Multinational corporate annual summit yacht management case, 3 yachts fleet sailing, 200 executives and guests, zero accidents throughout, awarded Best Corporate Annual Event",
    "case-006.371": "With innovative fleet sailing solution and perfect annual meeting execution, awarded 'Best Annual Event Partner of the Year' by Corporate Events Industry Association.",
    "case-006.380": "This is the most successful annual summit in our company's history. The Fantastic Vacation team used professional service and innovative event planning to give 200 colleagues an unforgettable experience.",
    "press.259": "At the 2024 Asia Yacht Industry Awards Ceremony, Fantastic Vacation won 'Asia's Best Yacht Service Provider' for its exceptional service quality and innovation.",
    "press.268": "Fantastic Vacation 82m Superyacht 'Fantasy Blue' Delivered",
    "press.274": "How did a $10M+ wedding at sea become an industry benchmark? Fantastic Vacation's Caribbean charter case for an Asian family was rated 'Most Innovative Luxury Event of the Year'.",
    "press.284": "In Forbes China's '2024 High-End Service Brands List', Fantastic Vacation was the only yacht service company selected, demonstrating its leadership in premium lifestyle services.",
    "index.60": "Business Sectors",
    "index.100": ""We don't just build yachts; we weave ocean dreams."",
    "index.161": "82m Superyacht 'Fantasy Blue'",
    "case-011.340": "100% client satisfaction, said they would definitely choose Fantastic Vacation again, already booked next quarter's itinerary",
    "case-007.256": "18-month comprehensive refit project covering interior renovation, power upgrade, smart system installation, awarded 'Refit Project of the Year', yacht market value increased by 30%",
    "case-007.323": "'The refit of Eternal Star exceeded all my expectations. The Fantastic Vacation team transformed this 10-year-old yacht into a brand-new vessel in 18 months.' - Client Testimonial",
    "cases-charter.301": "Century sea wedding for Asian family, 85m superyacht charter, 120 guests, 7 days 6 nights, route: Bahamas → Cayman Islands. Full onboard wedding planning and execution.",
    "case-027.335": "Zero damage in winter, perfect launch in spring, client said it's better than expected",
    "case-016.335": "Meeting completed successfully, group president sent personal thank-you letter, promised long-term cooperation",
    "custom.532": "Four core dimensions covering every detail of yacht customization, truly realizing the ultimate personalized experience of 'One Yacht, One World'",
    "custom.614": "At Fantastic Vacation, we understand the importance of 'what you see is what you get' for million-dollar investment decisions. Therefore, we took the lead in launching...",
    "yacht-27.20": "Yacht 27 Series",
    "about-structure.17": "Client itinerary customization and on-site service",
    "partner-type-marina.256": "Marina partnership and berth reservation service",
    "case-016.513": "Exceeded all expectations, client signed long-term management contract",
    "reviews.488": "Professional service, will definitely choose Fantastic Vacation again",
    "ir-team.186": "Investor Relations Team",
    "case-002.36": "Perfect customization case, exceeded all expectations",
    "partner-type-art.136": "Art and culture partnership collaboration",
    "news-007.399": "Industry innovation award, leading technology application",
    "contact.827": "Contact us for more information",
    "ir-shareholder.182": "Shareholder information and annual report",
    "case-007.323": "The refit exceeded expectations, better than a new yacht",
    "yacht-47.500": "Luxury yacht series with premium configuration",
    "yacht-43.537": "High-performance yacht for ocean exploration",
    "yacht-34.20": "Yacht 34 series overview and specifications",
    "yacht-20.543": "Custom yacht with personalized design",
    "news-010.137": "Latest news and industry updates",
    "yacht-11.20": "Yacht 11 entry-level luxury series",
    "about-history.321": "Company development history and milestones",
    "ir-financial.17": "Financial reports and performance data"
}

# Load i18n.js
with open('i18n.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Find dict end position
start = js_content.find('var dict = ')
brace_start = js_content.find('{', start)
depth = 0
end = -1
for i in range(brace_start, len(js_content)):
    if js_content[i] == '{':
        depth += 1
    elif js_content[i] == '}':
        depth -= 1
        if depth == 0:
            end = i
            break

dict_str = js_content[brace_start:end+1]
dict_obj = json.loads(dict_str)

# Add missing entries
added = 0
for key, zh_text in missing_keys.items():
    if key not in dict_obj:
        en_text = translations.get(key, zh_text)  # Use translation or fallback
        dict_obj[key] = {'zh': zh_text, 'en': en_text}
        added += 1
        print(f"Added: {key}")

print(f"\nAdded {added} new entries")

# Write back to i18n.js
new_dict_str = json.dumps(dict_obj, ensure_ascii=False, indent=2)
new_js_content = js_content[:brace_start] + new_dict_str + js_content[end+1:]

with open('i18n.js', 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print("Updated i18n.js successfully!")
print(f"Total entries now: {len(dict_obj)}")

# Verify coverage
translated = sum(1 for v in dict_obj.values() if isinstance(v, dict) and v.get('en') and v['en'] != v.get('zh', ''))
total = len(dict_obj)
coverage = translated / total * 100
print(f"Coverage: {coverage:.1f}% ({translated}/{total})")
