#!/usr/bin/env python3
"""
全站网格布局全面自动修复 v3
基于审计报告，修复所有不对称网格布局
"""
import re, glob, json

# Load audit report
with open('grid-audit-report.json') as f:
    issues = json.load(f)

# Read all HTML files into memory
file_contents = {}
html_files = glob.glob('**/*.html', recursive=True)
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fh:
        file_contents[f] = fh.read()

total_fixes = 0
files_modified = set()

def fix_grid_class(content, class_name, old_minmax, new_minmax):
    """Fix a grid class definition in <style> tag or inline."""
    # Fix in <style> tag
    pattern1 = f'.{class_name}{{display:grid;grid-template-columns:repeat(auto-fit,minmax({old_minmax}px,1fr))'
    replacement1 = f'.{class_name}{{display:grid;grid-template-columns:repeat(auto-fit,minmax({new_minmax}px,1fr))'
    content = content.replace(pattern1, replacement1)
    
    # Also try auto-fill variant
    pattern2 = f'.{class_name}{{display:grid;grid-template-columns:repeat(auto-fill,minmax({old_minmax}px,1fr))'
    replacement2 = f'.{class_name}{{display:grid;grid-template-columns:repeat(auto-fill,minmax({new_minmax}px,1fr))'
    content = content.replace(pattern2, replacement2)
    
    # Fix in inline style (class on element)
    pattern3 = f'repeat(auto-fit,minmax({old_minmax}px,1fr))'
    replacement3 = f'repeat(auto-fit,minmax({new_minmax}px,1fr))'
    # Only replace within context of the right class element
    # This is risky for inline styles, so we'll be more targeted
    
    return content

def fix_inline_grid(content, context_pattern, old_minmax, new_minmax):
    """Fix inline style grid matching a context pattern."""
    # Find the inline style near the context
    pattern = rf'({context_pattern}[^>]*style="[^"]*grid-template-columns:repeat\(auto-fit,minmax\(){old_minmax}(px,1fr\))'
    replacement = rf'\g<1>{new_minmax}\g<2>'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Also try auto-fill
    pattern2 = rf'({context_pattern}[^>]*style="[^"]*grid-template-columns:repeat\(auto-fill,minmax\(){old_minmax}(px,1fr\))'
    replacement2 = rf'\g<1>{new_minmax}\g<2>'
    new_content = re.sub(pattern2, replacement2, new_content, flags=re.DOTALL)
    
    return new_content

# Strategy: For each issue type, determine the best minmax value
# Key principle: prefer symmetric layouts (equal rows)
# For odd card counts, accept the best near-symmetric layout

# Group issues by (class_name, card_count, current_minmax) for batch fixes
fix_groups = {}
for issue in issues:
    key = (issue['class'], issue['cards'], issue['current_minmax'])
    if key not in fix_groups:
        fix_groups[key] = {
            'files': [],
            'recommended_minmax': issue['recommended_minmax'],
            'best_cols': issue['best_cols'],
            'current_cols': issue['current_cols'],
        }
    fix_groups[key]['files'].append(issue['file'])

print(f"Fix groups: {len(fix_groups)}")
print()

for (cls, cards, old_min), info in sorted(fix_groups.items()):
    new_min = info['recommended_minmax']
    best_cols = info['best_cols']
    current_cols = info['current_cols']
    file_list = info['files']
    
    # Sanity check: don't make minmax too wide or too narrow
    if new_min > 600:
        new_min = 600
    if new_min < 200 and cards > 4:
        new_min = 200
    
    # For logo-wall (20+ items), keep smaller minmax - logo walls are OK asymmetric
    if cls == 'logo-wall':
        continue
    
    # For gallery grids, a bit of asymmetry is acceptable for visual interest
    # But the last row should have at least 2 items
    if cls in ('gallery-grid', 'gallery-grid-c') and cards % current_cols >= 2:
        continue
    
    # For info-grid with many items (16+), some asymmetry is expected
    if cls == 'info-grid' and cards >= 16:
        # Check if current layout is close to symmetric
        last_row = cards % current_cols
        if last_row == 0 or last_row >= current_cols - 1:
            continue
    
    print(f"Fix: {cls} with {cards} cards: minmax {old_min}px→{new_min}px (target {best_cols} cols)")
    
    for f in file_list:
        if f not in file_contents:
            continue
        
        content = file_contents[f]
        original = content
        
        if cls == 'inline-grid':
            # Need more context to fix inline grids
            # We'll handle these separately
            continue
        
        content = fix_grid_class(content, cls, old_min, new_min)
        
        if content != original:
            file_contents[f] = content
            files_modified.add(f)
            total_fixes += 1

# Now handle inline-grid fixes separately
# These are services-grid or other grids with inline styles
inline_fix_items = {}
for (cls, cards, old_min), info in fix_groups.items():
    if cls != 'inline-grid':
        continue
    key = (cards, old_min)
    if key not in inline_fix_items:
        inline_fix_items[key] = {
            'files': [],
            'recommended_minmax': info['recommended_minmax'],
            'best_cols': info['best_cols'],
        }
    inline_fix_items[key]['files'].extend(info['files'])

print(f"\nInline grid fix groups: {len(inline_fix_items)}")

for (cards, old_min), info in inline_fix_items.items():
    new_min = info['recommended_minmax']
    best_cols = info['best_cols']
    
    if new_min > 600:
        new_min = 600
    if new_min < 200 and cards > 4:
        new_min = 200
    
    print(f"Fix inline: {cards} cards: minmax {old_min}px→{new_min}px (target {best_cols} cols)")
    
    for f in info['files']:
        if f not in file_contents:
            continue
        
        content = file_contents[f]
        original = content
        
        # Replace all inline grid minmax in this file that match
        # Be specific: only replace in style attributes
        pattern = f'repeat(auto-fit,minmax({old_min}px,1fr))'
        replacement = f'repeat(auto-fit,minmax({new_min}px,1fr))'
        content = content.replace(pattern, replacement)
        
        # Also auto-fill variant
        pattern2 = f'repeat(auto-fill,minmax({old_min}px,1fr))'
        replacement2 = f'repeat(auto-fill,minmax({new_min}px,1fr))'
        content = content.replace(pattern2, replacement2)
        
        if content != original:
            file_contents[f] = content
            files_modified.add(f)
            total_fixes += 1

# Special fixes for specific grids
print("\n=== Special targeted fixes ===")

# series-gallery in YT/ files: 4 cards at minmax(350px) -> 3+1
# Fix: change to minmax(500px) for 2+2
for f in ['YT/yachts-flybridge.html', 'YT/yachts-expedition.html', 'YT/yachts-daycruiser.html']:
    if f in file_contents:
        content = file_contents[f]
        original = content
        # The series-gallery in these files has minmax(350px) inline
        content = content.replace(
            'series-gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr))',
            'series-gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(500px,1fr))'
        )
        if content != original:
            file_contents[f] = content
            files_modified.add(f)
            total_fixes += 1
            print(f"  Fixed series-gallery in {f}")

# YT/en/yachts-sovereign.html: series-gallery 6 cards at minmax(250px) -> 4+2
# Fix: change to minmax(350px) for 3+3
for f in ['YT/en/yachts-sovereign.html']:
    if f in file_contents:
        content = file_contents[f]
        original = content
        content = content.replace(
            'series-gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr))',
            'series-gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr))'
        )
        if content != original:
            file_contents[f] = content
            files_modified.add(f)
            total_fixes += 1
            print(f"  Fixed series-gallery in {f}")

# Write all modified files
for f in files_modified:
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(file_contents[f])

print(f"\n=== FINAL SUMMARY ===")
print(f"Total fixes applied: {total_fixes}")
print(f"Files modified: {len(files_modified)}")
