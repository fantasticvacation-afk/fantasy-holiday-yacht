#!/usr/bin/env python3
"""
全站网格布局全面审计 v3
扫描所有HTML文件中的grid布局，检测不对称问题
"""
import re, glob, json

html_files = glob.glob('**/*.html', recursive=True)
issues = []
total_grids = 0

for f in html_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Find ALL grid definitions - both in <style> and inline styles
    # 1. In <style> tags
    style_grids = re.findall(
        r'\.([\w-]+)\s*\{\s*display:grid;\s*grid-template-columns:([^}]+)\}',
        content
    )
    
    for class_name, cols_def in style_grids:
        total_grids += 1
        
        # Skip fixed layouts (not auto-fit/auto-fill)
        if 'auto-fit' not in cols_def and 'auto-fill' not in cols_def:
            continue
        
        # Extract minmax value
        minmax_match = re.search(r'minmax\((\d+)px', cols_def)
        if not minmax_match:
            continue
        
        min_px = int(minmax_match.group(1))
        
        # Extract gap
        gap_match = re.search(r'gap:(\d+)px', cols_def)
        gap = int(gap_match.group(1)) if gap_match else 24
        
        # Find usage and count cards
        usage_pattern = rf'class=\"[^\"]*{class_name}[^\"]*\"'
        usage = re.search(usage_pattern, content)
        if not usage:
            continue
        
        # Count direct children (cards)
        grid_start = usage.end()
        section = content[grid_start:grid_start + 5000]
        
        # Count cards by looking for card/item patterns
        card_class = class_name.replace('-grid', '-card')
        cards = section.count(f'class="{card_class}')
        if cards == 0:
            cards = section.count(f'class="stat-item')
        if cards == 0:
            cards = section.count(f'class="info-item')
        if cards == 0:
            # Generic count - count first-level divs
            # This is approximate
            depth = 0
            first_divs = 0
            i = 0
            while i < len(section) and first_divs < 20:
                if section[i:i+4] == '<div':
                    if depth == 0:
                        first_divs += 1
                    depth += 1
                elif section[i:i+6] == '</div>':
                    depth -= 1
                    if depth < 0:
                        break
                i += 1
            if first_divs > 0:
                cards = first_divs
        
        if cards == 0:
            continue
        
        # Calculate columns at 1200px width
        container_width = 1200
        cols = max(1, (container_width + gap) // (min_px + gap))
        last_row = cards % cols if cards > cols else cards
        if last_row == 0:
            last_row = cols
        
        is_asymmetric = (last_row != cols and cards > cols)
        
        if is_asymmetric:
            # Calculate best fix
            best_cols = None
            for c in range(cols, 1, -1):
                if cards % c == 0:
                    best_cols = c
                    break
            
            if best_cols is None:
                # For numbers that don't divide evenly, find the one with smallest last row
                for c in range(cols, 1, -1):
                    remainder = cards % c
                    if remainder == 0 or remainder >= c - 1:  # nearly full last row
                        best_cols = c
                        break
            
            if best_cols is None:
                best_cols = 2
            
            required_min = int((container_width - (best_cols - 1) * gap) / best_cols)
            required_min = ((required_min + 9) // 10) * 10  # Round to nearest 10
            
            issues.append({
                'file': f,
                'class': class_name,
                'cards': cards,
                'current_cols': cols,
                'current_last_row': last_row,
                'best_cols': best_cols,
                'current_minmax': min_px,
                'recommended_minmax': required_min,
            })

    # 2. Inline style grids
    inline_grids = re.finditer(
        r'style=\"([^\"]*display:grid;[^\"]*grid-template-columns:repeat\(auto-fit,minmax\((\d+)px,1fr\))',
        content
    )
    
    for m in inline_grids:
        total_grids += 1
        min_px = int(m.group(2))
        
        # Get gap from same style
        gap_match = re.search(r'gap:(\d+)px', m.group(1))
        gap = int(gap_match.group(1)) if gap_match else 24
        
        # Count cards after this element
        grid_start = m.end()
        section = content[grid_start:grid_start + 5000]
        
        # Count cards
        cards = section.count('class="service-card')
        if cards == 0:
            cards = section.count('class="cert-card')
        if cards == 0:
            cards = section.count('class="cap-card')
        if cards == 0:
            # Generic
            depth = 0
            first_divs = 0
            i = 0
            while i < len(section) and first_divs < 20:
                if section[i:i+4] == '<div':
                    if depth == 0:
                        first_divs += 1
                    depth += 1
                elif section[i:i+6] == '</div>':
                    depth -= 1
                    if depth < 0:
                        break
                i += 1
            if first_divs > 0:
                cards = first_divs
        
        if cards == 0:
            continue
        
        container_width = 1200
        cols = max(1, (container_width + gap) // (min_px + gap))
        last_row = cards % cols if cards > cols else cards
        if last_row == 0:
            last_row = cols
        
        is_asymmetric = (last_row != cols and cards > cols)
        
        if is_asymmetric:
            best_cols = None
            for c in range(cols, 1, -1):
                if cards % c == 0:
                    best_cols = c
                    break
            if best_cols is None:
                best_cols = 2
            
            required_min = int((container_width - (best_cols - 1) * gap) / best_cols)
            required_min = ((required_min + 9) // 10) * 10
            
            issues.append({
                'file': f,
                'class': 'inline-grid',
                'cards': cards,
                'current_cols': cols,
                'current_last_row': last_row,
                'best_cols': best_cols,
                'current_minmax': min_px,
                'recommended_minmax': required_min,
            })

print(f'Total grids scanned: {total_grids}')
print(f'Asymmetric grids found: {len(issues)}')
print()

# Group by class
by_class = {}
for issue in issues:
    cls = issue['class']
    if cls not in by_class:
        by_class[cls] = []
    by_class[cls].append(issue)

for cls, items in sorted(by_class.items()):
    print(f'\n--- {cls} ({len(items)} files) ---')
    # Show unique configurations
    configs = {}
    for item in items:
        key = f"{item['cards']}cards@{item['current_minmax']}px→{item['current_cols']}col(last:{item['current_last_row']})"
        if key not in configs:
            configs[key] = []
        configs[key].append(item['file'])
    
    for config, files in configs.items():
        print(f'  {config}')
        if len(files) <= 5:
            for f in files:
                print(f'    - {f}')
        else:
            for f in files[:3]:
                print(f'    - {f}')
            print(f'    ... and {len(files)-3} more')

# Save full report
with open('grid-audit-report.json', 'w') as f:
    json.dump(issues, f, indent=2, ensure_ascii=False)
print(f'\nFull report saved to grid-audit-report.json')
