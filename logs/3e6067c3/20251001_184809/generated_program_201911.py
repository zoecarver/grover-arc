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

def process_row(row: List[int], block_slotmap: List[int], b: int, key_set: set, slots_per_color: Dict[int, List[int]], assigned_count: defaultdict) -> None:
    n_cols = len(row)
    border_js = [-1] + [j for j in range(n_cols) if row[j] == 1] + [n_cols]
    assigned_regions: List[Tuple[int, int, int]] = []
    for bk in range(len(border_js) - 1):
        l = border_js[bk] + 1
        r = border_js[bk + 1] - 1
        if l > r:
            continue
        candidates = [row[j] for j in range(l, r + 1) if row[j] != b and row[j] != 1 and row[j] in key_set]
        if candidates and len(set(candidates)) == 1:
            s = candidates[0]
            slist = slots_per_color[s]
            if slist:
                k = assigned_count[s]
                slot = slist[k % len(slist)]
                assigned_count[s] += 1
                for j in range(l, r + 1):
                    if is_fillable(row[j], b, key_set, False):
                        row[j] = s
                    if row[j] != 1:
                        block_slotmap[j] = slot
                assigned_regions.append((l, r, slot))
    assigned_regions.sort(key=lambda x: x[0])
    for ii in range(len(assigned_regions) - 1):
        l1, r1, slot1 = assigned_regions[ii]
        l2, _, slot2 = assigned_regions[ii + 1]
        if abs(slot1 - slot2) == 1:
            min_slot = min(slot1, slot2)
            fill_c = slots_per_color  # Wait, no: need key_colors, but passed? Wait, error.
Wait, process_row needs key_colors passed.

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n_rows = len(g)
    if n_rows < 2:
        return [list(row) for row in g]
    n_cols = len(g[0])
    b = get_background(g)
    _, key_colors = get_key(g, b, n_cols)
    if not key_colors:
        return [list(row) for row in g]
    key_set = set(key_colors)
    slots_per_color = get_slots_per_color(key_colors)
    out = [list(row) for row in g]
    assigned_count = defaultdict(int)
    # Find blocks
    blocks: List[Tuple[int, int]] = []
    i = 0
    while i < n_rows - 2:
        if is_all_b(out[i], b):
            i += 1
            continue
        start = i
        while i < n_rows - 2 and not is_all_b(out[i], b):
            i += 1
        end = i - 1
        blocks.append((start, end))
    block_slotmaps: List[List[int]] = []
    for start, end in blocks:
        block_slotmap = [-1] * n_cols
        for r in range(start, end + 1):
            process_row(out[r], block_slotmap, b, key_set, key_colors, slots_per_color, assigned_count)
        block_slotmaps.append(block_slotmap)
    # Process gaps
    for kk in range(len(blocks) - 1):
        gap_start = blocks[kk][1] + 1
        gap_end = blocks[kk + 1][0] - 1
        if gap_start > gap_end:
            continue
        above_s = block_slotmaps[kk]
        below_s = block_slotmaps[kk + 1]
        for j in range(n_cols):
            sa