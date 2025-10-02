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

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n_rows = len(g)
    n_cols = len(g[0]) if n_rows else 0
    b = get_background(g)
    _, key_colors = get_key(g, b, n_cols)
    slots_per_color = get_slots_per_color(key_colors)
    key_set = set(key_colors)
    out = [list(row) for row in g]
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
        blocks.append((start, i))
        i += 1
    block_slotmaps = []
    for b_start, b_end in blocks:
        block_slotmap = [-1] * n_cols
        for r in range(b_start, b_end):
            border_js = [-1] + [j for j in range(n_cols) if out[r][j] == 1] + [n_cols]
            assigned_regions = []
            for bk in range(len(border_js) - 1):
                l = border_js[bk] + 1
                rr = border_js[bk + 1] - 1
                if l > rr:
                    continue
                cands = [out[r][j] for j in range(l, rr + 1) if out[r][j] != 1 and out[r][j] != b]
                if not cands:
                    continue
                s_set = set(cands)
                if len(s_set) == 1 and list(s_set)[0] in key_set:
                    s = list(s_set)[0]
                    already_assigned = all(block_slotmap[j] != -1 for j in range(l, rr + 1))
                    slot = -1
                    if not already_assigned:
                        slist = slots_per_color[s]
                        if slist:
                            k = assigned_count[s]
                            slot = slist[k % len(slist)]
                            assigned_count[s] += 1
                            for jj in range(l, rr + 1):
                                block_slotmap[jj] = slot
                    else:
                        slot = block_slotmap[l]
                    assigned_regions.append((l, rr, slot))
                    fill_c = s
                    for j in range(l, rr + 1):
                        if out[r][j] == b:
                            out[r][j] = fill_c
            if assigned_regions:
                assigned_regions.sort(key=lambda x: x[0])
                for ii in range(len(assigned_regions) - 1):
                    l1, rr1, slot1 = assigned_regions[ii]
                    l2, _, slot2 = assigned_regions[ii + 1]
                    if slot1 != -1 and slot2 != -1 and abs(slot1 - slot2) == 1:
                        min_s = min(slot1, slot2)
                        fill_c = key_colors[min_s]
                        for j in range(rr1 + 1, l2):
                            if out[r][j] == b:
                                out[r][j] = fill_c
                                if block_slotmap[j] == -1:
                                    block_slotmap[j] = min_s
        block_slotmaps.append(block_slotmap)
    gap_intervals = []
    prev_end = 0
    for b_start, b_end in blocks:
        if prev_end < b_start:
            gap_intervals.append((prev_end, b_start - 1))
        prev_end = b_end
    if prev_end < n_rows - 2:
        gap_intervals.append((prev_end, n_rows - 3))
    for g_start, g_end in gap_intervals:
        if g_start > g_end:
            continue
        above_idx = -1
        for bi in range(len(blocks)):
            if blocks[bi][1] == g_start:
                above_idx = bi
                break
        below_idx = -1
        for bi in range(len(blocks)):
            if blocks[bi][0] == g_end + 1:
                below_idx = bi
                break
        if above_idx == -1 or below_idx == -1:
            continue
        slotmap_a = block_slotmaps[above_idx]
        slotmap_b = block_slotmaps[below_idx]
        for j in range(n_cols):
            sa = slotmap_a[j]
            sb = slotmap_b[j]
            if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                min_s = min(sa, sb)
                fill_c = key_colors[min_s]
                for rr in range(g_start, g_end + 1):
                    if out[rr][j] == b:
                        out[rr][j] = fill_c
    return out
```