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
    slots_per_color: Dict[int, List[int]] = defaultdict(list)
    for k, color in enumerate(key_colors):
        slots_per_color[color].append(k)
    return slots_per_color

def find_seed_regions(row: List[int], b: int, n_cols: int, key_set: set) -> List[Tuple[int, int, int, int]]:
    border_js = [-1] + [j for j in range(n_cols) if row[j] == 1] + [n_cols]
    regions = []
    for bk in range(len(border_js) - 1):
        l = border_js[bk] + 1
        r = border_js[bk + 1] - 1
        if l > r:
            continue
        candidates = [c for c in row[l:r + 1] if c != b and c != 1 and c in key_set]
        if candidates and len(set(candidates)) == 1:
            s = candidates[0]
            center = (l + r) // 2
            regions.append((s, l, r, center))
    return regions

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n_rows = len(g)
    n_cols = len(g[0])
    b = get_background(g)
    _, key_colors = get_key(g, b, n_cols)
    if not key_colors:
        return [row[:] for row in g]
    key_set = set(key_colors)
    slots_per_color = get_slots_per_color(key_colors)
    out = [row[:] for row in g]
    assigned_count = defaultdict(int)
    blocks = []
    current_block = []
    for i in range(n_rows - 2):
        is_all_b = all(c == b for c in g[i])
        if is_all_b:
            if current_block:
                blocks.append(current_block)
                current_block = []
        else:
            current_block.append(i)
    if current_block:
        blocks.append(current_block)
    slotmaps = []
    for block in blocks:
        seed_row = None
        best_regions = []
        for ri in block:
            temp_regions = find_seed_regions(g[ri], b, n_cols, key_set)
            if len(temp_regions) > len(best_regions):
                best_regions = temp_regions
                seed_row = ri
        if not seed_row:
            slotmap = [-1] * n_cols
            slotmaps.append(slotmap)
            continue
        regions = best_regions
        assigned = {}
        for s, l, r, center in regions:
            slots_list = slots_per_color.get(s, [])
            if not slots_list:
                continue
            k = assigned_count[s]
            slot = slots_list[k % len(slots_list)]
            assigned[center] = slot
            assigned_count[s] += 1
        slotmap = [-1] * n_cols
        for s, l, r, center in regions:
            if center in assigned:
                sl = assigned[center]
                for j in range(l, r + 1):
                    slotmap[j] = sl
        slotmaps.append(slotmap)
        seed_rows_in_block = [ri for ri in block if any(c != b and c != 1 for c in g[ri])]
        for ri in seed_rows_in_block:
            for s, l, r, center in regions:
                if center not in assigned:
                    continue
                fill_c = key_colors[assigned[center]]
                for j in range(l, r + 1):
                    c = out[ri][j]
                    if c == b or c == fill_c or (c != 1 and c not in key_set):
                        out[ri][j] = fill_c
        for kk in range(len(regions) - 1):
            s1, l1, r1, center1 = regions[kk]
            s2, l2, r2, center2 = regions[kk + 1]
            if center1 not in assigned or center2 not in assigned:
                continue
            slot1 = assigned[center1]
            slot2 = assigned[center2]
            if abs(slot1 - slot2) != 1:
                continue
            fill_c = key_colors[min(slot1, slot2)]
            gap_start = r1 + 1
            gap_end = l2 - 1
            if gap_start > gap_end:
                continue
            for ri in seed_rows_in_block:
                for j in range(gap_start, gap_end + 1):
                    if out[ri][j] == b:
                        out[ri][j] = fill_c
    gaps = []
    prev_end = -1
    for blk in blocks:
        start = blk[0]
        if start > prev_end + 1:
            gaps.append((prev_end + 1, start - 1))
        prev_end = blk[-1]
    if prev_end < n_rows - 3:
        gaps.append((prev_end + 1, n_rows - 3))
    for v_start, v_end in gaps:
        if v_start > v_end:
            continue
        above_ib = -1
        for ii in range(len(blocks)):
            if blocks[ii][-1] < v_start:
                above_ib = ii
            else:
                break
        below_ib = -1
        for ii in range(above_ib + 1, len(blocks)):
            if blocks[ii][0] > v_end:
                below_ib = ii
                break
        if above_ib == -1 or below_ib == -1:
            continue
        above_slot = slotmaps[above_ib]
        below_slot = slotmaps[below_ib]
        for j in range(n_cols):
            sa = above_slot[j]
            sb = below_slot[j]
            if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                fill_c = key_colors[min(sa, sb)]
                for rr in range(v_start, v_end + 1):
                    if out[rr][j] == b:
                        out[rr][j] = fill_c
    return out
```