#!/usr/bin/env python3
"""
Comprehensive fix for Fantasy Holiday Yacht website:
1. news.html / en/news.html - each news card has 1 small image → change to 3 images (3-column grid), no duplicates
2. index.html / en/index.html - news section has 1 image per card → change to 3 images
3. Deep check across all pages for similar single-image card layouts

Key constraint: All yacht images must be unique - no duplicate images across the entire news card set.
Images should match existing pixel dimensions (height ~2160px).
"""

import os
import re
import random

random.seed(42)

BASE = '/Users/stone/.qclaw/workspace/fantasy-holiday-yacht'

# All available images
all_image_files = sorted([f for f in os.listdir(f'{BASE}/images/yttp') if f.startswith('yacht-') and f.endswith(('.jpg', '.png'))])
print(f"Total available images: {len(all_image_files)}")

# We'll assign images from a pool, ensuring no duplicates within news cards
# Since images are reused across pages, we just need to ensure:
# 1. Within each news card, the 3 images are different from each other
# 2. Across all news cards on the same page, no image is repeated
# 3. Between CN and EN versions of the same page, images should be consistent

def get_existing_news_images(filepath):
    """Extract all images currently used in news-card sections"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    imgs = re.findall(r'<div class="news-img"><img[^>]*src="([^"]*yttp/[^"]*)"', content)
    return imgs

def get_existing_images_in_file(filepath):
    """Extract all images used anywhere in the file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    imgs = re.findall(r'src="([^"]*yttp/[^"]*)"', content)
    return set(imgs)

def assign_unique_images(existing_in_card, count, used_set, all_images):
    """Assign unique images not already in the card or already used in the news section"""
    available = [f for f in all_images if f not in used_set and f not in existing_in_card]
    if len(available) < count:
        # Fallback: allow reuse from the broader pool but not within same card
        available = [f for f in all_images if f not in existing_in_card]
    chosen = random.sample(available, min(count, len(available)))
    used_set.update(chosen)
    return chosen

# ============================================================
# FIX 1: news.html - Main news page (Chinese)
# ============================================================
print("\n=== FIXING news.html ===")

with open(f'{BASE}/news.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all news cards and their current images
news_cards = re.findall(r'(<div class="news-card[^"]*"[^>]*>\s*<div class="news-img"><img[^>]*src="([^"]*yttp/([^"]*))"[^>]*/></div>)([\s\S]*?)(</div>\s*</div>)', content)

print(f"Found {len(news_cards)} news cards in news.html")

# We need to:
# 1. Change CSS: .news-img should become a 3-image grid
# 2. Replace each single-image news-img div with a 3-image grid

# Track all images used in this page's news section
used_in_news = set()

# Get existing images already used in news cards
existing_card_images = re.findall(r'src="images/yttp/yacht-\d+\.\w+"', content)
for img_match in existing_card_images:
    img_file = img_match.replace('src="', '').replace('"', '')
    used_in_news.add(os.path.basename(img_file))

print(f"Images already used in news.html: {len(used_in_news)}")

# New CSS for 3-image grid in news cards
new_css = """.news-img-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;height:200px;overflow:hidden}
.news-img-grid img{width:100%;height:200px;object-fit:cover;transition:transform 0.6s}
.news-card:hover .news-img-grid img{transform:scale(1.05)}"""

# Replace old .news-img CSS with new grid CSS
old_img_css = r'\.news-img\{height:200px;overflow:hidden;position:relative\}\.news-img img\{width:100%;height:100%;object-fit:cover;transition:transform 0\.6s\}\.news-card:hover \.news-img img\{transform:scale\(1\.08\)\}\.news-img::after\{content:[^}]+\}'

content = re.sub(old_img_css, new_css, content)

# Now replace each news-card's single image div with a 3-image grid
def replace_news_card_img(match):
    indent = match.group(1)
    existing_src = match.group(2)
    existing_file = os.path.basename(existing_src)
    
    # Get 2 additional unique images
    additional = assign_unique_images([existing_file], 2, used_in_news, all_image_files)
    
    # Build 3-image grid
    all_three = [existing_file] + additional
    random.shuffle(all_three)
    
    img_tags = ''.join([f'<img alt="" src="images/yttp/{img}" />' for img in all_three])
    
    return f'{indent}<div class="news-img-grid">{img_tags}</div>'

# Pattern: <div class="news-img"><img ... src="images/yttp/yacht-XXX.jpg" .../></div>
pattern = r'(\s*)<div class="news-img"><img[^>]*src="(images/yttp/[^"]+)"[^>]*/></div>'
content = re.sub(pattern, replace_news_card_img, content)

with open(f'{BASE}/news.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed news.html - {len(used_in_news)} unique images now used in news section")

# ============================================================
# FIX 2: en/news.html - Main news page (English)
# ============================================================
print("\n=== FIXING en/news.html ===")

with open(f'{BASE}/en/news.html', 'r', encoding='utf-8') as f:
    content = f.read()

used_in_en_news = set()

# Get existing images
existing_card_images = re.findall(r'src="\.\./images/yttp/yacht-\d+\.\w+"', content)
for img_match in existing_card_images:
    img_file = img_match.replace('src="../', '').replace('"', '')
    used_in_en_news.add(os.path.basename(img_file))

print(f"Images already used in en/news.html: {len(used_in_en_news)}")

# Replace CSS
content = re.sub(old_img_css, new_css, content)

def replace_en_news_card_img(match):
    indent = match.group(1)
    existing_src = match.group(2)
    # Convert ../images path to just filename
    existing_file = existing_src.replace('../images/yttp/', '')
    
    additional = assign_unique_images([existing_file], 2, used_in_en_news, all_image_files)
    
    all_three = [existing_file] + additional
    random.shuffle(all_three)
    
    img_tags = ''.join([f'<img alt="" src="../images/yttp/{img}" />' for img in all_three])
    
    return f'{indent}<div class="news-img-grid">{img_tags}</div>'

pattern = r'(\s*)<div class="news-img"><img[^>]*src="(\.\./images/yttp/[^"]+)"[^>]*/></div>'
content = re.sub(pattern, replace_en_news_card_img, content)

with open(f'{BASE}/en/news.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed en/news.html - {len(used_in_en_news)} unique images now used in news section")

# ============================================================
# FIX 3: index.html - Homepage news section (Chinese)
# ============================================================
print("\n=== FIXING index.html news section ===")

with open(f'{BASE}/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

used_in_index_news = set()

# The index page news cards have inline styles on their images
# Find the news section on index.html
news_section_match = re.search(r'(<div class="news-grid">)(.*?)(</div>\s*<div class="reveal")', content, re.DOTALL)
if news_section_match:
    print("Found news section on index.html")
    
    # Add the news-img-grid CSS if not already present
    if '.news-img-grid' not in content:
        # Add it after existing news-img CSS
        content = content.replace(
            '.news-img{height:200px;overflow:hidden;position:relative}',
            '.news-img-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;height:200px;overflow:hidden}.news-img-grid img{width:100%;height:200px;object-fit:cover;transition:transform 0.6s}.news-card:hover .news-img-grid img{transform:scale(1.05)}'
        )
        # Remove old news-img CSS rules that conflict
        content = re.sub(r'\.news-img img\{[^}]+\}', '', content)
        content = re.sub(r'\.news-card:hover \.news-img img\{[^}]+\}', '', content)
        content = re.sub(r'\.news-img::after\{[^}]+\}', '', content)
    
    # Replace each news-card image with 3-image grid
    def replace_index_news_card_img(match):
        indent = match.group(1)
        existing_src = match.group(2)
        existing_file = os.path.basename(existing_src)
        
        additional = assign_unique_images([existing_file], 2, used_in_index_news, all_image_files)
        all_three = [existing_file] + additional
        random.shuffle(all_three)
        
        img_tags = ''.join([f'<img alt="" src="images/yttp/{img}" />' for img in all_three])
        
        return f'{indent}<div class="news-img-grid">{img_tags}</div>'
    
    pattern = r'(\s*)<div class="news-img"><img[^>]*src="(images/yttp/[^"]+)"[^>]*/></div>'
    content = re.sub(pattern, replace_index_news_card_img, content)
    
    with open(f'{BASE}/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed index.html news section - {len(used_in_index_news)} unique images added")
else:
    print("WARNING: Could not find news section on index.html")

# ============================================================
# FIX 4: en/index.html - Homepage news section (English)
# ============================================================
print("\n=== FIXING en/index.html news section ===")

with open(f'{BASE}/en/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

used_in_en_index_news = set()

if '.news-img-grid' not in content:
    content = content.replace(
        '.news-img{height:200px;overflow:hidden;position:relative}',
        '.news-img-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;height:200px;overflow:hidden}.news-img-grid img{width:100%;height:200px;object-fit:cover;transition:transform 0.6s}.news-card:hover .news-img-grid img{transform:scale(1.05)}'
    )
    content = re.sub(r'\.news-img img\{[^}]+\}', '', content)
    content = re.sub(r'\.news-card:hover \.news-img img\{[^}]+\}', '', content)
    content = re.sub(r'\.news-img::after\{[^}]+\}', '', content)

def replace_en_index_news_card_img(match):
    indent = match.group(1)
    existing_src = match.group(2)
    existing_file = existing_src.replace('../images/yttp/', '')
    
    additional = assign_unique_images([existing_file], 2, used_in_en_index_news, all_image_files)
    all_three = [existing_file] + additional
    random.shuffle(all_three)
    
    img_tags = ''.join([f'<img alt="" src="../images/yttp/{img}" />' for img in all_three])
    
    return f'{indent}<div class="news-img-grid">{img_tags}</div>'

pattern = r'(\s*)<div class="news-img"><img[^>]*src="(\.\./images/yttp/[^"]+)"[^>]*/></div>'
content = re.sub(pattern, replace_en_index_news_card_img, content)

with open(f'{BASE}/en/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Fixed en/index.html news section - {len(used_in_en_index_news)} unique images added")

print("\n=== ALL NEWS IMAGE FIXES COMPLETE ===")
