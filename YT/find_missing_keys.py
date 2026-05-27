#!/usr/bin/env python3
import re
import json
from pathlib import Path

# Load i18n.js dict
with open('i18n.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract dict
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

dict_obj = json.loads(js_content[brace_start:end+1])
print(f"Loaded {len(dict_obj)} keys from i18n.js")

# Find all data-i18n keys in HTML files and their Chinese text
html_files = list(Path('.').glob('*.html'))
missing_keys = {}
all_keys_in_html = set()

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all data-i18n="key" and get text content
    # Pattern to match: <tag ... data-i18n="key" ...>text</tag>
    # More robust: find data-i18n="key" then find the text after >
    matches = re.finditer(r'data-i18n="([^"]+)"', content)
    for match in matches:
        key = match.group(1)
        all_keys_in_html.add(key)
        
        if key not in dict_obj and key not in missing_keys:
            # Find the Chinese text for this key
            pos = match.start()
            # Find the next > after this position
            gt_pos = content.find('>', pos)
            if gt_pos != -1:
                # Find the next <
                lt_pos = content.find('<', gt_pos)
                if lt_pos != -1:
                    text = content[gt_pos+1:lt_pos].strip()
                    # Remove nested tags
                    text = re.sub(r'<[^>]+>', '', text).strip()
                    if text and any('\u4e00' <= c <= '\u9fff' for c in text):
                        missing_keys[key] = text

print(f"Found {len(all_keys_in_html)} unique keys in HTML")
print(f"Missing from i18n.js: {len(missing_keys)}")

# Save missing keys with their Chinese text
with open('/tmp/missing_keys.json', 'w', encoding='utf-8') as f:
    json.dump(missing_keys, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(missing_keys)} missing keys to /tmp/missing_keys.json")
print("\nFirst 20 missing keys:")
for i, (key, text) in enumerate(list(missing_keys.items())[:20]):
    print(f"  {key}: {text[:50]}")
