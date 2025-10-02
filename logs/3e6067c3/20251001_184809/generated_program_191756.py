```python
from typing import List, Dict, Tuple
from collections import defaultdict

def get_background(g: List[List[int]]) -> int:
    return g[-1][0] if g else 0

def get_key(g: List[List[int]], b: int, n_cols: int) -> Tuple[List[int], List[int]]:
    key_row = g[-2]
    key_pos = [j for j in range(n_cols) if key_row[j] != b]
    key_colors = [key_row[j] for j in key_pos]
    return key_pos, key_colors

def get_slots_per_color(key_colors: List[int]) -> Dict[int, List[int]]:
    slots_per_color = defaultdict(list)
    for k, color in enumerate(key_colors):
        slots_per_color[color].append(k)
    return slots_per_color

def find_regions_in_row(row: List[int], b: int, n_cols: int, border: int = 1) -> List[Tuple[int, int, int, int]]:
    border_js = [-1] + [j for j in range(n_cols) if row[j] == border] + [n_cols]
    regions = []
    for bk in range(len(border_js) - 1):
        l = border_js[bk] + 1
        r = border_js[bk + 1] - 1
        if l > r:
            continue
        bay = row[l:r + 1]
        non_b_colors = [c for c in bay if c != b and c != border]
        if non_b_colors:
            s = non_b_colors[0]
            if all(c == s for c in non_b_colors):
                center = (l + r) // 2
                regions.append((s, l, r, center))
    return regions

def find_all_bays(row: List[int], border: int, n_cols: int, b: int) -> List[Tuple[int, int, int]]:
    border_js = [-1] + [j for j in range(n_cols) if row[j] == border] + [n_cols]
    bays = []
    for bk in range(len(border_js) - 1):
        l = border_js[bk] + 1
        r = border_js[bk + 1] - 1
        if l > r:
            continue
        bay = row[l:r + 1]
        if all(c == b for c in bay):
            bt = b
        elif all(c == border for c in bay):
            bt = border
        else:
            non_border = [c for c in bay if c != border]
            if non_border and all(c == non_border[0] for c in non_border) and non_border[0] != b:
                bt = non_border[0]
            else:
                bt = None
        bays.append((l, r, bt))
    return bays

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    out = [row[:] for row in g]
    n_rows = len(out)
    if n_rows == 0:
        return out
    n_cols = len(out[0])
    b = get_background(out)
    border_color = 1
    key_pos, key_colors = get_key(out, b, n_cols)
    slots_per_color = get_slots_per_color(key_colors)
    assigned_count = defaultdict(int)
    slot_grid = [[-1] * n_cols for _ in range(n_rows)]
    # find structure blocks
    structure_blocks = []
    i = 0
    while i < n_rows - 2:
        if all(c == b for c in out[i]):
            i += 1
            continue
        start = i
        i += 1
        while i < n_rows - 2 and not all(c == b for c in out[i]):
            i += 1
        end = i - 1
        structure_blocks.append((start, end))
    # horizontal fill
    for start, end in structure_blocks:
        seed_rows = [r for r in range(start, end + 1) if any(c != b and c != border_color for c in out[r])]
        if not seed_rows:
            continue
        r0 = seed_rows[0]
        regions = find_regions_in_row(out[r0], b, n_cols, border_color)
        regions = sorted(regions, key=lambda x: x[3])
        region_assign = {}
        for idx, (s, l, r, center) in enumerate(regions):
            k = assigned_count[s]
            if s in slots_per_color and slots_per_color[s]:
                slot_i = slots_per_color[s][k % len(slots_per_color[s])]
                region_assign[center] = (s, slot_i)
                assigned_count[s] += 1
        filled_row = out[r0][:]
        # fill seeded
        for s, l, r, center in regions:
            if center in region_assign:
                _, slot_i = region_assign[center]
                for j in range(l, r + 1):
                    filled_row[j] = s
                    slot_grid[r0][j] = slot_i
        # fill gaps
        for k in range(len(regions) - 1):
            left_reg = regions[k]
            right_reg = regions[k + 1]
            left_center = left_reg[3]
            right_center = right_reg[3]
            if left_center not in region_assign or right_center not in region_assign:
                continue
            left_slot = region_assign[left_center][1]
            right_slot = region_assign[right_center][1]
            if abs(left_slot - right_slot) == 1:
                fill_slot = min(left_slot, right_slot)
                fill_c = key_colors[fill_slot]
                left_r = left_reg[2]
                right_l = right_reg[1]
                for j in range(left_r + 1, right_l):
                    if filled_row[j] == b:
                        filled_row[j] = fill_c
                        slot_grid[r0][j] = fill_slot
        # apply to seed rows
        for r in seed_rows:
            for j in range(n_cols):
                if out[r][j] != border_color:
                    out[r][j] = filled_row[j]
                    slot_grid[r][j] = slot_grid[r0][j]
    # vertical fill
    all_b_blocks = []
    i = 0
    while i < n_rows:
        if not all(c == b for c in out[i]):
            i += 1
            continue
        block_start = i
        i += 1
        while i < n_rows and all(c == b for c in out[i]):
            i += 1
        block_end = i - 1
        all_b_blocks.append((block_start, block_end))
    for start, end in all_b_blocks:
        # find above_r
        above_r = -1
        for r in range(start - 1, -1, -1):
            if any(c != b and c != border_color for c in out[r]):
                above_r = r
                break
        # find below_r
        below_r = -1
        for r in range(end + 1, n_rows):
            if any(c != b and c != border_color for c in out[r]):
                below_r = r
                break
        if above_r == -1 or below_r == -1:
            continue
        for j in range(n_cols):
            ca = out[above_r][j]
            sa = slot_grid[above_r][j]
            has_above = ca != b and ca != border_color and sa != -1
            cb = out[below_r][j]
            sb = slot_grid[below_r][j]
            has_below = cb != b and cb != border_color and sb != -1
            if has_above and has_below and abs(sa - sb) == 1:
                fill_slot = min(sa, sb)
                fill_c = key_colors[fill_slot]
                for r in range(start, end + 1):
                    out[r][j] = fill_c
    return out
```