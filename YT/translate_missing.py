#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import time

# Load missing keys
with open('/tmp/missing_keys.json', 'r', encoding='utf-8') as f:
    missing_keys = json.load(f)

print(f"Need to translate {len(missing_keys)} keys")

def translate_text(text, target_lang='en'):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl={target_lang}&dt=t&q={urllib.parse.quote(text)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result and len(result) > 0 and len(result[0]) > 0:
                return result[0][0][0]
    except Exception as e:
        print(f"Translation error: {e}")
    return None

# Translate all missing keys
translations = {}
for i, (key, zh_text) in enumerate(missing_keys.items()):
    print(f"Translating {i+1}/{len(missing_keys)}: {key}")
    en_text = translate_text(zh_text)
    if en_text:
        translations[key] = {
            'zh': zh_text,
            'en': en_text
        }
        print(f"  EN: {en_text[:60]}")
    else:
        translations[key] = {
            'zh': zh_text,
            'en': zh_text
        }
    time.sleep(0.2)

# Save translations
with open('/tmp/missing_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(translations)} translations to /tmp/missing_translations.json")
