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

def find_seed_regions(row: List[int], b: int, n_cols: int, key_set: set) -> List[Tuple[int, int, int, int]]:
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
    return regions

def is_empty(c: int, b: int, key_set: set) -> bool:
    return c == b or (c != 1 and c not in key_set)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n_rows, n_cols = len(g), len(g[0])
    b = get_background(g)
    _, key_colors = get_key(g, b, n_cols)
    key_set = set(key_colors)
    slots_per_color = get_slots_per_color(key_colors)
    out = [row[:] for row in g]
    assigned_count = defaultdict(int)
    blocks = []
    i = 0
    while i < n_rows - 2:
        if all(g[i][j] == b for j in range(n_cols)):
            i += 1
            continue
        start = i
        i += 1
        while i < n_rows - 2 and not all(g[i][j] == b for j in range(n_cols)):
            i += 1
        blocks.append(list(range(start, i)))
    block_slotmaps = []
    for blk in blocks:
        seed_rows_in_blk = [rr for rr in blk if any(g[rr][j] in key_set for j in range(n_cols))]
        assigned = {}
        for rr in seed_rows_in_blk:
            regs = find_seed_regions(g[rr], b, n_cols, key_set)
            for s, l, r, center in regs:
                if center not in assigned:
                    slots_list = slots_per_color.get(s, [])
                    if slots_list:
                        k = assigned_count[s]
                        slot_i = slots_list[k % len(slots_list)]
                        assigned[center] = (l, r, s, slot_i)
                        assigned_count[s] += 1
        slot_per_col = [-1] * n_cols
        for center, (l, r, s, slot_i) in assigned.items():
            for j in range(l, r + 1):
                slot_per_col[j] = slot_i
        block_slotmaps.append(slot_per_col)
        # horizontal fill for this block
        for rr in blk:
            # fill assigned cols
            for j in range(n_cols):
                if slot_per_col[j] != -1:
                    s_fill = key_colors[slot_per_col[j]]
                    if is_empty(out[rr][j], b, key_set):
                        out[rr][j] = s_fill
            # gap filling
            border_js = [-1] + [j for j in range(n_cols) if out[rr][j] == 1] + [n_cols]
            bay_list = []
            for bk_ in range(len(border_js) - 1):
                ll = border_js[bk_] + 1
                rr_ = border_js[bk_ + 1] - 1
                if ll > rr_:
                    continue
                is_emp = all(is_empty(out[rr][k], b, key_set) for k in range(ll, rr_ + 1))
                is_asg = any(slot_per_col[k] != -1 for k in range(ll, rr_ + 1))
                bay_center = (ll + rr_) // 2
                bay_slot = slot_per_col[bay_center] if is_asg else -1
                bay_list.append((ll, rr_, is_asg, bay_slot))
            for ii in range(1, len(bay_list) - 1):
                prev = bay_list[ii - 1]
                curr = bay_list[ii]
                nxt = bay_list[ii + 1]
                if not curr[2] and prev[2] and nxt[2]:
                    sl = prev[3]
                    sr = nxt[3]
                    if abs(sl - sr) == 1:
                        fill_c = key_colors[min(sl, sr)]
                        cl, cr = curr[0], curr[1]
                        for k in range(cl, cr + 1):
                            out[rr][k] = fill_c
    # now vertical fills
    verticals = []
    prev_end = -1
    for bb in blocks:
        blk_end = bb[-1] + 1
        blk_start = bb[0]
        if prev_end + 1 < blk_start:
            verticals.append((prev_end + 1, blk_start - 1))
        prev_end = blk_end
    if prev_end < n_rows - 2:
        verticals.append((prev_end, n_rows - 3))
    for v_start, v_end in verticals:
        if v_start > v_end:
            continue
        # find above_ib
        above_ib = -1
        for ib in range(len(blocks)):
            if blocks[ib][-1] < v_start:
                above_ib = ib
            else:
                break
        below_ib = -1
        for ib in range(above_ib + 1, len(blocks)):
            if blocks[ib][0] > v_end:
                below_ib = ib
                break
        if above_ib == -1 or below_ib == -1:
            continue
        slotmap_a = block_slotmaps[above_ib]
        slotmap_b = block_slotmaps[below_ib]
        for j in range(n_cols):
            sa = slotmap_a[j]
            sb = slotmap_b[j]
            if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                fill_c = key_colors[min(sa, sb)]
                for rr in range(v_start, v_end + 1):
                    if out[rr][j] == b:
                        out[rr][j] = fill_c
    return out
```