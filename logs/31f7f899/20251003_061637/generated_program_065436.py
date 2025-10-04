```python
def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    c_row = n // 2
    center_col = n // 2
    center = g[c_row][:]
    # Find all same-color non-6 groups in center row
    all_groups = []
    i = 0
    while i < n:
        if center[i] != 6:
            colr = center[i]
            st = i
            i += 1
            while i < n and center[i] == colr:
                i += 1
            all_groups.append({'start': st, 'end': i - 1, 'color': colr})
        else:
            i += 1
    # Determine if has main component
    has_main = (center[center_col] != 6)
    left_groups = []
    right_groups = []
    if has_main:
        # Find main_start and main_end
        main_start = center_col
        while main_start > 0 and center[main_start - 1] != 6:
            main_start -= 1
        main_end = center_col
        while main_end < n - 1 and center[main_end + 1] != 6:
            main_end += 1
        # Left groups
        for grp in all_groups:
            if grp['end'] < main_start:
                left_groups.append(grp)
        # Main groups (split by color)
        main_grps = []
        i = main_start
        while i <= main_end:
            colr = center[i]
            st = i
            i += 1
            while i <= main_end and center[i] == colr:
                i += 1
            main_grps.append({'start': st, 'end': i - 1, 'color': colr})
        # Additional right groups
        add_right = [grp for grp in all_groups if grp['start'] > main_end]
        right_groups = main_grps + add_right
    else:
        for grp in all_groups:
            if grp['end'] < center_col:
                left_groups.append(grp)
            elif grp['start'] > center_col:
                right_groups.append(grp)
    # Assign max_d for left groups
    max_left = (n - 1) // 6
    color_to_left_maxd = {}
    for k in range(len(left_groups)):
        grp = left_groups[k]
        md = min(k + 1, max_left)
        grp['max_d'] = md
        color_to_left_maxd[grp['color']] = md
    num_left = len(left_groups)
    # Assign for right groups
    matched_count = 0
    for grp in right_groups:
        if grp['color'] in color_to_left_maxd:
            grp['max_d'] = color_to_left_maxd[grp['color']]
            matched_count += 1
    base = num_left - matched_count
    new_k = 1
    for grp in right_groups:
        if 'max_d' not in grp:
            grp['max_d'] = base + new_k
            new_k += 1
    # All groups with max_d
    all_groups_with_d = left_groups + right_groups
    # Build output
    output = [[8] * n for _ in range(n)]
    # Set center row
    for j in range(n):
        output[c_row][j] = center[j]
    # Fill other rows
    for i in range(n):
        if i == c_row:
            continue
        d = abs(i - c_row)
        for grp in all_groups_with_d:
            if grp['max_d'] >= d:
                for j in range(grp['start'], grp['end'] + 1):
                    output[i][j] = grp['color']
    return output
```