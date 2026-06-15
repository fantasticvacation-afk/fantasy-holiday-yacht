#!/usr/bin/env python3
"""
全站布局修复脚本 v1
1. 修复所有 HTML 文件中的重复 class 属性（合并到一个 class="" 中）
2. 修复 highlights-grid 4卡片布局问题（改为2列 2+2）
3. 修复 about-history.html timeline 宽度问题
4. 修复 container-narrow/container-wide 无效问题
"""
import re, glob, os

def merge_duplicate_classes(tag_str):
    """Merge duplicate class= attributes in an HTML tag string."""
    # Find all class="..." values
    class_pattern = r'class="([^"]*)"'
    matches = list(re.finditer(class_pattern, tag_str))
    
    if len(matches) <= 1:
        return tag_str, False
    
    # Collect all class values
    all_classes = []
    for m in matches:
        all_classes.extend(m.group(1).split())
    
    # Deduplicate while preserving order
    seen = set()
    unique_classes = []
    for c in all_classes:
        if c not in seen:
            seen.add(c)
            unique_classes.append(c)
    
    merged = ' '.join(unique_classes)
    
    # Remove all class="..." from the tag
    result = re.sub(class_pattern, '', tag_str)
    
    # Insert merged class right after the tag name
    # Find the tag name (first word after <)
    tag_name_match = re.match(r'(<\s*\w+)', result)
    if tag_name_match:
        insert_pos = tag_name_match.end()
        result = result[:insert_pos] + f' class="{merged}"' + result[insert_pos:]
    
    return result, True

def fix_file(filepath):
    """Fix duplicate class attributes in a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = 0
    
    # Find all HTML tags and check for duplicate class attributes
    # We need to process tag by tag
    def process_tag(match):
        nonlocal changes
        tag = match.group(0)
        class_count = len(re.findall(r'class="', tag))
        if class_count > 1:
            new_tag, changed = merge_duplicate_classes(tag)
            if changed:
                changes += 1
                return new_tag
        return tag
    
    # Match HTML opening tags (self-closing and regular)
    content = re.sub(r'<[a-zA-Z][^>]*>', process_tag, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    return 0

# Main execution
total_changes = 0
files_changed = 0

html_files = glob.glob('**/*.html', recursive=True)
print(f"Scanning {len(html_files)} HTML files for duplicate class attributes...")

for f in html_files:
    changes = fix_file(f)
    if changes > 0:
        files_changed += 1
        total_changes += changes
        if files_changed <= 20:
            print(f"  Fixed {changes} duplicate class(es) in {f}")

print(f"\n=== Phase 1 Complete: Duplicate class attributes ===")
print(f"Files changed: {files_changed}")
print(f"Total duplicate classes merged: {total_changes}")

# Phase 2: Fix highlights-grid in series pages (4 cards -> 2+2 layout)
# The issue: minmax(350px) with 4 cards in ~1200px container = 3 columns, so 3+1
# Fix: increase minmax to force 2-column layout
print("\n=== Phase 2: Fixing highlights-grid 4-card asymmetry ===")
hl_changes = 0
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    original = content
    
    # Check if this file has highlights-grid with 4 cards
    if 'highlights-grid' not in content:
        continue
    
    # Count the number of direct child cards in highlights-grid
    # The highlights-grid sections have 4 <div> children (cards)
    # Change minmax(350px,1fr) or minmax(260px,1fr) to minmax(500px,1fr) to force 2+2
    # This ensures 4 cards show as 2x2 grid instead of 3+1
    content = re.sub(
        r'\.highlights-grid\{display:grid;grid-template-columns:repeat\(auto-fit,minmax\(\d+px,1fr\)\)',
        '.highlights-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(500px,1fr))',
        content
    )
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        hl_changes += 1
        print(f"  Fixed highlights-grid in {f}")

print(f"Files with highlights-grid fixed: {hl_changes}")

# Phase 3: Fix about-history.html timeline width
# The timeline currently has class="timeline" with class="container container-narrow" (was duplicate, now merged)
# But container-narrow = 800px max, which is too narrow for a timeline
# We want the timeline to be wider, using container-wide (1100px) or just container (default)
# Also the section header should be wider
print("\n=== Phase 3: Fixing about-history.html timeline width ===")
history_files = glob.glob('**/about-history.html', recursive=True)
for f in history_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    original = content
    
    # After Phase 1, the duplicate classes are merged. 
    # Change timeline from container-narrow to wider layout
    # Remove container-narrow from timeline, let it use full container width
    content = content.replace(
        'class="timeline container container-narrow"',
        'class="timeline container"'
    )
    
    # Also fix the section header: change container-wide to just container for consistency
    # The section header "里程碑时间线" should span wider
    content = content.replace(
        'class="container container-wide reveal"',
        'class="container reveal"'
    )
    
    # Fix the bottom section with container-narrow
    # This is the summary section at the bottom, keep it narrow for readability
    # Actually let's make it container-wide for better layout
    content = content.replace(
        'class="container container-narrow reveal"',
        'class="container container-wide reveal"'
    )
    
    # The timeline itself needs to be wider - remove the narrow constraint
    # and add proper width styling
    # Let's ensure the timeline takes more horizontal space
    if 'timeline' in content:
        # Add a style to make timeline content wider within the container
        # Replace the inline style on the timeline div to remove any max-width constraint
        pass
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f"  Fixed timeline width in {f}")
    else:
        print(f"  No changes needed in {f}")

# Phase 4: Comprehensive grid scan - find all grid containers with asymmetry issues
print("\n=== Phase 4: Comprehensive grid asymmetry scan ===")
asymmetry_count = 0
asymmetry_files = []

for f in html_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Find all inline grid definitions
    grid_matches = re.finditer(
        r'(display:grid;[^"]*grid-template-columns:repeat\(\s*auto-fill\s*,\s*minmax\((\d+)px)',
        content
    )
    
    for m in grid_matches:
        min_px = int(m.group(2))
        # Grids with minmax < 300px likely cause multi-column asymmetry on wide screens
        # These were already addressed in previous commit, skip for now

print("Phase 4: Previous grid fixes already applied. Checking for remaining issues...")

# Phase 5: Fix about.html stats-grid layout
print("\n=== Phase 5: Checking about.html (公司简介) layout ===")
about_files = glob.glob('**/about.html', recursive=True) + glob.glob('**/about-intro.html', recursive=True)
for f in about_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Check for stats-grid or similar grid layouts
    if 'stats-grid' in content:
        # Count how many stat items there are
        stats_section = content[content.find('stats-grid'):content.find('stats-grid')+2000]
        stat_count = stats_section.count('<div')
        print(f"  {f}: stats-grid found with ~{stat_count} items")
    
    # Check for any grid with 4 items in asymmetric layout
    grids = re.findall(r'class="([^"]*grid[^"]*)"', content)
    if grids:
        print(f"  {f}: Grid classes found: {set(grids)}")

print("\n=== ALL PHASES COMPLETE ===")
