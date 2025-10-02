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
    out = [list(row) for row in g]
    n_rows = len(out)
    if n_rows < 2:
        return out
    n_cols = len(out[0])
    b = get_background(out)
    _, key_colors = get_key(out, b, n_cols)
    if not key_colors:
        return out
    key_set = set(key_colors)
    slots_per_color = get_slots_per_color(key_colors)
    assigned_count = defaultdict(int)
    blocks = []
    i = 0
    while i < n_rows - 2:
        if is_all_b(out[i], b):
            i += 1
            continue
        start = i
        i += 1
        while i < n_rows - 2 and not is_all_b(out[i], b):
            i += 1
        blocks.append((start, i))
    block_slotmaps = [None] * len(blocks)
    seed_bays_per_block = [[] for _ in blocks]
    for blk_idx, (start, end) in enumerate(blocks):
        block_used_slots = {}
        for i in range(start, end):
            row = out[i]
            border_js = [-1] + [j for j in range(n_cols) if row[j] == 1] + [n_cols]
            bay_list = []
            for bk in range(len(border_js) - 1):
                l = border_js[bk] + 1
                r = border_js[bk + 1] - 1
                if l > r:
                    continue
                candidates = [row[j] for j in range(l, r + 1) if row[j] != b and row[j] != 1 and row[j] in key_set]
                bay_is_seed = False
                bay_slot = None
                if candidates:
                    s_set = set(candidates)
                    if len(s_set) == 1:
                        s = next(iter(s_set))
                        if s in slots_per_color:
                            if s in block_used_slots:
                                bay_slot = block_used_slots[s]
                            else:
                                slist = slots_per_color[s]
                                k = assigned_count[s]
                                bay_slot = slist[k % len(slist)]
                                block_used_slots[s] = bay_slot
                                assigned_count[s] += 1
                            bay_is_seed = True
                            for j in range(l, r + 1):
                                if is_fillable(row[j], b, key_set, False):
                                    row[j] = s
                            seed_bays_per_block[blk_idx].append((l, r, bay_slot))
                bay_list.append((l, r, bay_is_seed, bay_slot))
            for m in range(len(bay_list)):
                l_m, r_m, is_seed_m, slot_m = bay_list[m]
                if is_seed_m:
                    continue
                if m > 0 and bay_list[m - 1][2] and m < len(bay_list) - 1 and bay_list[m + 1][2]:
                    left_slot = bay_list[m - 1][3]
                    right_slot = bay_list[m + 1][3]
                    if abs(left_slot - right_slot) == 1:
                        min_s = min(left_slot, right_slot)
                        fill_c = key_colors[min_s]
                        for j in range(l_m, r_m + 1):
                            if is_fillable(row[j], b, key_set, False):
                                row[j] = fill_c
                        bay_list[m] = (l_m, r_m, False, min_s)
        block_slotmap = [-1] * n_cols
        for j in range(n_cols):
            for ii in range(start, end):
                c = out[ii][j]
                if c in key_set and c in block_used_slots:
                    block_slotmap[j] = block_used_slots[c]
                    break
        block_slotmaps[blk_idx] = block_slotmap
    for k in range(1, len(blocks)):
        above_end = blocks[k - 1][1]
        below_start = blocks[k][0]
        gap_start = above_end
        gap_end = below_start
        if gap_start >= gap_end:
            continue
        sa = block_slotmaps[k - 1]
        sb = block_slotmaps[k]
        for j in range(n_cols):
            if sa[j] != -1 and sb[j] != -1 and abs(sa[j] - sb[j]) == 1:
                min_s = min(sa[j], sb[j])
                fill_c = key_colors[min_s]
                for rr in range(gap_start, gap_end):
                    if is_fillable(out[rr][j], b, key_set, True):
                        out[rr][j] = fill_c
    for blk_idx, (start, end) in enumerate(blocks):
        for l, r, slot in seed_bays_per_block[blk_idx]:
            fill_c = key_colors[slot]
            for j in range(l, r + 1):
                for i in range(start, end):
                    if is_fillable(out[i][j], b, key_set, False):
                        out[i][j] = fill_c
    return out
```