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
    d = defaultdict(list)
    for i, c in enumerate(key_colors):
        d[c].append(i)
    return d

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
    if n_rows < 2:
        return out
    n_cols = len(g[0])
    b = get_background(g)
    _, key_colors = get_key(g, b, n_cols)
    if not key_colors:
        return out
    key_set = set(key_colors)
    slots_per_color = get_slots_per_color(key_colors)
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
    assigned_count = defaultdict(int)
    block_slotmaps = []
    for start, end in blocks:
        block_slotmap = [-1] * n_cols
        for r in range(start, end + 1):
            borders = [-1] + [j for j in range(n_cols) if g[r][j] == 1] + [n_cols]
            assigned_bays = []
            for k in range(len(borders) - 1):
                l = borders[k] + 1
                rr_ = borders[k + 1] - 1
                if l > rr_:
                    continue
                bay_colors = set()
                for j in range(l, rr_ + 1):
                    c = g[r][j]
                    if c != 1 and c != b and c in key_set:
                        bay_colors.add(c)
                if len(bay_colors) == 1:
                    s = next(iter(bay_colors))
                    slist = slots_per_color[s]
                    if slist:
                        idx = assigned_count[s] % len(slist)
                        slot = slist[idx]
                        assigned_count[s] += 1
                        assigned_bays.append((l, rr_, slot))
                        for j in range(l, rr_ + 1):
                            if is_fillable(out[r][j], b, key_set):
                                out[r][j] = s
                        for j in range(l, rr_ + 1):
                            block_slotmap[j] = slot
            if len(assigned_bays) > 1:
                assigned_bays = sorted(assigned_bays, key=lambda x: x[0])
                for ii in range(len(assigned_bays) - 1):
                    l1, r1, slot1 = assigned_bays[ii]
                    l2, r2, slot2 = assigned_bays[ii + 1]
                    if abs(slot1 - slot2) == 1:
                        gap_l = r1 + 1
                        gap_r = l2 - 1
                        if gap_l <= gap_r:
                            min_slot = min(slot1, slot2)
                            fill_c = key_colors[min_slot]
                            for j in range(gap_l, gap_r + 1):
                                if is_fillable(out[r][j], b, key_set):
                                    out[r][j] = fill_c
                            for j in range(gap_l, gap_r + 1):
                                block_slotmap[j] = min_slot
        block_slotmaps.append(block_slotmap)
    m = len(blocks)
    if m > 1:
        for k in range(1, m):
            prev_end = blocks[k - 1][1]
            curr_start = blocks[k][0]
            g_start = prev_end + 1
            g_end = curr_start - 1
            if g_start > g_end:
                continue
            above_sm = block_slotmaps[k - 1]
            below_sm = block_slotmaps[k]
            for j in range(n_cols):
                sa = above_sm[j]
                sb = below_sm[j]
                if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                    min_slot = min(sa, sb)
                    fill_c = key_colors[min_slot]
                    for rr in range(g_start, g_end + 1):
                        if is_fillable(out[rr][j], b, key_set, all_b_row=True):
                            out[rr][j] = fill_c
    return out
```