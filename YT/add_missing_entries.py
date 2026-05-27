#!/usr/bin/env python3
import json
import re

# Load missing keys
with open('/tmp/missing_keys.json', 'r', encoding='utf-8') as f:
    missing_keys = json.load(f)

print(f"Need to translate {len(missing_keys)} keys")

# For now, let me add them with Chinese text as placeholder
# In production, these should be translated
new_entries = {}
for key, zh_text in missing_keys.items():
    new_entries[key] = {
        'zh': zh_text,
        'en': zh_text  # TODO: translate
    }

# Load existing i18n.js dict
with open('i18n.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Find dict end
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

# Add new entries
added = 0
for key, value in new_entries.items():
    if key not in dict_obj:
        dict_obj[key] = value
        added += 1

print(f"Added {added} new entries")

# Now we need to translate them
# Let me write a translation script
print("\nTransating missing keys...")

# Simple translation using a mapping for common terms
# For now, let me just flag these for manual translation
print(f"\nMissing keys need English translation:")
for key, zh in missing_keys.items():
    print(f"  {key}: {zh[:60]}")
