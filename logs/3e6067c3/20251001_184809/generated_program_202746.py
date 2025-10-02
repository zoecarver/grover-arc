```python
from typing import List, Dict, Tuple
from collections import defaultdict

def get_background(g: List[List[int]]) -> int:
    return g[-1][0] if g else 0

def get_key(g: List[List[int]], b: int, n_cols: int) -> Tuple[List[int], List[int]]:
    if len(g) < 2:
        return [], []
    key_row = g[-2]
    key_pos = [j for j in range(n_cols) if key_row[j] != b]
    key_colors = [key_row[j] for j in key_pos]
    return key_pos, key_colors

def get_slots_per_color(key_colors: List[int]) -> Dict[int, List[int]]:
    slots_per_color: Dict[int, List[int]] = defaultdict(list)
    for k, color in enumerate(key_colors):
        slots_per_color[color].append(k)
    return slots_per_color

def is_all_b(row: List[int], b: int) -> bool:
    return all(c == b for c in row)

def is_fillable(c: int, b: int, key_set: set, all_b_row: bool = False) -> bool:
    if c == 1 and not all_b_row:
        return False
    if c in key_set:
        return False
    return True

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    out = [list(row) for row in g]
    n_rows = len(g)
    n_cols = len(g[0]) if n_rows > 0 else 0
    if n_rows < 2:
        return out
    b = get_background(g)
    key_pos, key_colors = get_key(g, b, n_cols)
    if not key_colors:
        return out
    key_set = set(key_colors)
    slots_per_color = get_slots_per_color(key_colors)
    assigned_count = defaultdict(int)
    blocks = []
    i = 0
    while i < n_rows - 2:
        if is_all_b(g[i], b):
            i += 1
            continue
        start = i
        while i < n_rows - 2 and not is_all_b(g[i], b):
            i += 1
        blocks.append((start, i - 1))
    block_slotmaps = []
    for start, end in blocks:
        slotmap = [-1] * n_cols
        for r in range(start, end + 1):
            border_js = [-1] + [j for j in range(n_cols) if out[r][j] == 1] + [n_cols]
            regions = []
            for bk in range(len(border_js) - 1):
                l = border_js[bk] + 1
                r_ = border_js[bk + 1] - 1
                if l > r_:
                    continue
                candidates = [out[r][j] for j in range(l, r_ + 1) if out[r][j] != b and out[r][j] != 1 and out[r][j] in key_set]
                if candidates and len(set(candidates)) == 1:
                    s = candidates[0]
                    slist = slots_per_color.get(s, [])
                    if slist:
                        k = assigned_count[s]
                        slot_i = slist[k % len(slist)]
                        regions.append((l, r_, slot_i))
                        assigned_count[s] += 1
            regions.sort(key=lambda x: x[0])
            temp_slot = [-1] * n_cols
            for l, r_, slot_i in regions:
                fill_c = key_colors[slot_i]
                for j in range(l, r_ + 1):
                    if is_fillable(out[r][j], b, key_set, False):
                        out[r][j] = fill_c
                    temp_slot[j] = slot_i
            for ii in range(len(regions) - 1):
                l1, r1, s1 = regions[ii]
                l2, r2, s2 = regions[ii + 1]
                if abs(s1 - s2) == 1:
                    gap_l = r1 + 1
                    gap_r = l2 - 1
                    if gap_l <= gap_r:
                        min_s = min(s1, s2)
                        fill_c = key_colors[min_s]
                        for j in range(gap_l, gap_r + 1):
                            if is_fillable(out[r][j], b, key_set, False):
                                out[r][j] = fill_c
                            temp_slot[j] = min_s
            for j in range(n_cols):
                if temp_slot[j] != -1:
                    slotmap[j] = temp_slot[j]
        block_slotmaps.append(slotmap)
    for k in range(1, len(blocks)):
        gap_start = blocks[k - 1][1] + 1
        gap_end = blocks[k][0] - 1
        if gap_start > gap_end:
            continue
        above_sm = block_slotmaps[k - 1]
        below_sm = block_slotmaps[k]
        for j in range(n_cols):
            sa = above_sm[j]
            sb = below_sm[j]
            if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                min_s = min(sa, sb)
                fill_c = key_colors[min_s]
                for rr in range(gap_start, gap_end + 1):
                    if is_fillable(out[rr][j], b, key_set, True):
                        out[rr][j] = fill_c
    return out
```