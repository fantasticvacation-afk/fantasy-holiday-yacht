#!/usr/bin/env python3
import re
import json
import os

BASE_DIR = "/Users/stone/.qclaw/workspace/fantasy-holiday-yacht"

with open(os.path.join(BASE_DIR, "news_content_cn.json"), "r", encoding="utf-8") as f:
    NEWS_CN = json.load(f)

with open(os.path.join(BASE_DIR, "news_content_en.json"), "r", encoding="utf-8") as f:
    NEWS_EN = json.load(f)

FILES = {
    "news.html": NEWS_CN,
    "en/news.html": NEWS_EN,
    "YT/news.html": NEWS_CN,
    "YT/en/news.html": NEWS_EN,
}

I18N_KEYS = [
    "news.298", "news.312", "news.326", "news.340", "news.354",
    "news.368", "news.382", "news.396", "news.410", "news.424",
]

for filename, paragraphs in FILES.items():
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    assert len(paragraphs) == 10, f"Expected 10 paragraphs, got {len(paragraphs)} for {filename}"

    for idx, key in enumerate(I18N_KEYS):
        # Match the entire <p data-i18n="KEY">...</p> including nested <p> tags
        # We need to replace the WHOLE <p data-i18n="KEY">...</p> block
        # But since there may be nested <p> tags now, we need a smarter approach
        
        # First, let's find the start of the tag
        start_marker = '<p data-i18n="' + key + '">'
        start_pos = content.find(start_marker)
        if start_pos == -1:
            print(f"WARNING: No match for {key} in {filename}")
            continue
        
        # Find the matching </p> - we need to account for nested <p> tags
        search_from = start_pos + len(start_marker)
        depth = 1
        pos = search_from
        while depth > 0 and pos < len(content):
            next_open = content.find('<p', pos)
            next_close = content.find('</p>', pos)
            
            if next_close == -1:
                print(f"WARNING: Could not find closing tag for {key} in {filename}")
                break
            
            if next_open != -1 and next_open < next_close:
                # Check if it's a <p> tag (not <param> or something)
                after_open = content[next_open:next_open+3]
                if after_open == '<p>':
                    depth += 1
                pos = next_open + 3
            else:
                depth -= 1
                if depth == 0:
                    end_pos = next_close + len('</p>')
                    # Replace the entire block
                    new_paragraphs_html = "\n".join("<p>{}</p>".format(p) for p in paragraphs[idx])
                    content = content[:start_pos] + new_paragraphs_html + content[end_pos:]
                    break
                pos = next_close + 4

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {filename}")

print("\nAll files updated successfully!")
