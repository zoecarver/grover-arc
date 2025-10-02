```python
from typing import List, Dict, Tuple
from collections import defaultdict

def get_background(g: List[List[int]]) -> int:
    return g[-1][0] if g else 0

def get_key(g: List[List[int]], b: int, n_cols: int) -> Tuple[List[int], List[int]]:
    key_row = g[-2]
    key_pos: List[int] = [j for j in range(n_cols) if key_row[j] != b]
    key_colors: List[int] = [key_row[j] for j in key_pos]
    return key_pos, key_colors

def get_slots_per_color(key_colors: List[int]) -> Dict[int, List[int]]:
    slots_per_color: Dict[int, List[int]] = defaultdict(list)
    for k, color in enumerate(key_colors):
        slots_per_color[color].append(k)
    return slots_per_color

def find_regions_in_row(row: List[int], b: int, n_cols: int) -> List[Tuple[int, int, int, int]]:
    border_js = [-1] + [j for j in range(n_cols) if row[j] == 1] + [n_cols]
    regions = []
    for bk in range(len(border_js) - 1):
        l = border_js[bk] + 1
        r = border_js[bk + 1] - 1
        if l > r:
            continue
        bay = row[l:r + 1]
        non_b_colors = [c for c in bay if c != b]
        if non_b_colors:
            s = non_b_colors[0]
            if all(c == s for c in non_b_colors):
                center = (l + r) // 2
                regions.append((s, l, r, center))
    return regions

def assign_slots_to_regions(regions_per_level: List[List[Tuple[int, int, int, int]]], slots_per_color: Dict[int, List[int]]) -> Dict[Tuple[int, int], Tuple[int, int]]:
    assigned_count = defaultdict(int)
    region_assign: Dict[Tuple[int, int], Tuple[int, int]] = {}
    for level_id, level_regions in enumerate(regions_per_level):
        for s, l, r, center in level_regions:
            k = assigned_count[s]
            slots_list = slots_per_color[s]
            if slots_list:
                slot_i = slots_list[k % len(slots_list)]
                region_assign[(level_id, center)] = (s, slot_i)
                assigned_count[s] += 1
    return region_assign

def fill_horizontal(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    n_rows = len(g)
    if n_rows < 2:
        return out
    n_cols = len(out[0])
    b = get_background(g)
    _, key_colors = get_key(g, b, n_cols)
    slots_per_color = get_slots_per_color(key_colors)

    # Collect regions for assignment, one per level
    regions_per_level = []
    i = 0
    while i < n_rows - 2:
        row = g[i]
        has_seed = any(c != 1 and c != b for c in row)
        if has_seed:
            # Start of level, collect regions from this row
            level_regions = find_regions_in_row(row, b, n_cols)
            regions_per_level.append(level_regions)
            # Skip to next level, after this seed row, but to find end of level, skip while has_seed
            i += 1
            while i < n_rows - 2 and any(c != 1 and c != b for c in g[i]):
                i += 1
        else:
            i += 1

    region_assign = assign_slots_to_regions(regions_per_level, slots_per_color)

    # Now fill all seed rows
    level_id = 0
    in_level = False
    for i in range(n_rows - 2):
        row = out[i]  # use out, but since we fill out
        has_seed = any(c != 1 and c != b for c in row)
        if has_seed:
            if not in_level:
                in_level = True
                current_level = level_id
                level_id += 1
            # Fill this row
            border_js = [-1] + [j for j in range(n_cols) if row[j] == 1] + [n_cols]
            for bk in range(len(border_js) - 1):
                l = border_js[bk] + 1
                r = border_js[bk + 1] - 1
                if l > r:
                    continue
                bay = row[l : r + 1]
                is_gap = all(c == b for c in bay)
                if is_gap and bk > 0 and bk < len(border_js) - 1:
                    # gap, check left and right rooms
                    # left bay
                    left_bk = bk - 1
                    left_l = border_js[left_bk - 1] + 1 if left_bk > 0 else -1
                    left_r = border_js[left_bk] - 1
                    left_bay = row[left_l : left_r + 1] if left_l <= left_r else []
                    left_has_seed = left_l <= left_r and not all(c == b for c in left_bay)
                    if not left_has_seed:
                        continue
                    left_center = (left_l + left_r) // 2
                    left_key = (current_level, left_center)
                    if left_key not in region_assign:
                        continue
                    s1, i1 = region_assign[left_key]
                    # right bay
                    right_l = border_js[bk] + 1
                    right_r = border_js[bk + 1] - 1
                    right_bay = row[right_l : right_r + 1] if right_l <= right_r else []
                    right_has_seed = right_l <= right_r and not all(c == b for c in right_bay)
                    if not right_has_seed:
                        continue
                    right_center = (right_l + right_r) // 2
                    right_key = (current_level, right_center)
                    if right_key not in region_assign:
                        continue
                    s2, i2 = region_assign[right_key]
                    if abs(i1 - i2) == 1:
                        fill_color = s1 if i1 < i2 else s2
                        for jj in range(l, r + 1):
                            out[i][jj] = fill_color
                else:
                    # normal bay
                    counts = defaultdict(int)
                    for c in bay:
                        if c != 1 and c != b:
                            counts[c] += 1
                    if counts:
                        min_cnt = min(counts.values())
                        cands = [c for c, cnt in counts.items() if cnt == min_cnt]
                        if len(cands) == 1:
                            s = cands[0]
                            for jj in range(l, r + 1):
                                if out[i][jj] != 1:
                                    out[i][jj] = s
        else:
            in_level = False

    return out

def program(g: List[List[int]]) -> List[List[int]]:
    return fill_horizontal(g)
```