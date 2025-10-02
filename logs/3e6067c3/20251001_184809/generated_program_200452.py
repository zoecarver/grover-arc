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

def is_all_b(row: List[int], b: int) -> bool:
    return all(c == b for c in row)

def is_fillable(c: int, b: int, key_set: set, all_b_row: bool = False) -> bool:
    if c == 1:
        return all_b_row
    if c in key_set:
        return False
    return True

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n_rows = len(g)
    n_cols = len(g[0])
    b = get_background(g)
    _, key_colors = get_key(g, b, n_cols)
    key_set = set(key_colors)
    slots_per_color = get_slots_per_color(key_colors)
    out = [list(row) for row in g]
    assigned_count = defaultdict(int)
    seed_slotmaps = {}
    for i in range(n_rows - 2):
        row = g[i]
        border_js = [-1] + [j for j in range(n_cols) if row[j] == 1] + [n_cols]
        regions = []
        for bk in range(len(border_js) - 1):
            l = border_js[bk] + 1
            r = border_js[bk + 1] - 1
            if l > r:
                continue
            candidates = [row[j] for j in range(l, r + 1) if row[j] in key_set]
            if candidates and len(set(candidates)) == 1:
                s = candidates[0]
                center = (l + r) // 2
                regions.append((s, l, r, center))
        if not regions:
            continue
        regions.sort(key=lambda x: x[3])
        slotmap_row = [-1] * n_cols
        assigned_regions = []
        for s, l, r, center in regions:
            slist = slots_per_color.get(s, [])
            if not slist:
                continue
            idx = assigned_count[s] % len(slist)
            slot = slist[idx]
            assigned_count[s] += 1
            for j in range(l, r + 1):
                if is_fillable(out[i][j], b, key_set, False):
                    out[i][j] = s
                slotmap_row[j] = slot
            assigned_regions.append((center, slot, l, r))
        seed_slotmaps[i] = slotmap_row
        for ii in range(len(assigned_regions) - 1):
            center1, slot1, l1, r1 = assigned_regions[ii]
            center2, slot2, l2, r2 = assigned_regions[ii + 1]
            if abs(slot1 - slot2) == 1:
                min_slot = min(slot1, slot2)
                fill_c = key_colors[min_slot]
                start_j = r1 + 1
                end_j = l2 - 1
                for j in range(start_j, end_j + 1):
                    if 0 <= j < n_cols and is_fillable(out[i][j], b, key_set, False):
                        out[i][j] = fill_c
    blocks = []
    i = 0
    while i < n_rows - 2:
        if is_all_b(g[i], b):
            i += 1
            continue
        start = i
        while i < n_rows - 2 and not is_all_b(g[i], b):
            i += 1
        blocks.append((start, i))
    for start, end in blocks:
        possible_reps = [k for k in range(start, end) if k in seed_slotmaps]
        if not possible_reps:
            continue
        rep = max(possible_reps, key=lambda k: sum(1 for x in seed_slotmaps[k] if x != -1))
        slotmap_rep = seed_slotmaps[rep]
        for k in range(start, end):
            for j in range(n_cols):
                if slotmap_rep[j] != -1:
                    fill_c = out[rep][j]
                    if is_fillable(out[k][j], b, key_set, False):
                        out[k][j] = fill_c
    for i in range(n_rows - 2):
        if not is_all_b(g[i], b):
            continue
        above = -1
        for kk in range(i - 1, -1, -1):
            if kk in seed_slotmaps:
                above = kk
                break
        below = -1
        for kk in range(i + 1, n_rows - 2):
            if kk in seed_slotmaps:
                below = kk
                break
        if above == -1 or below == -1:
            continue
        slotmap_a = seed_slotmaps[above]
        slotmap_b = seed_slotmaps[below]
        all_b_row_flag = is_all_b(g[i], b)
        for j in range(n_cols):
            sa = slotmap_a[j]
            sb = slotmap_b[j]
            if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                min_s = min(sa, sb)
                fill_c = key_colors[min_s]
                if is_fillable(out[i][j], b, key_set, all_b_row_flag):
                    out[i][j] = fill_c
    return out
```