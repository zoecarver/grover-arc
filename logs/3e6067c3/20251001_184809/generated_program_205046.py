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

def find_bays(row: List[int], n_cols: int) -> List[Tuple[int, int]]:
    borders = [-1] + [j for j in range(n_cols) if row[j] == 1] + [n_cols]
    bays = []
    for k in range(len(borders) - 1):
        l = borders[k] + 1
        r = borders[k + 1] - 1
        if l <= r:
            bays.append((l, r))
    return bays

def process_row_for_seeds(out: List[List[int]], row: int, b: int, key_set: set, slots_per_color: Dict[int, List[int]],
                          assigned_count: Dict[int, int], seed_slotmap: List[int], block_slotmap: List[int],
                          key_colors: List[int], n_cols: int) -> List[Tuple[int, int, int]]:
    assigned_regions = []
    bays = find_bays(out[row], n_cols)
    for l, r in bays:
        cands = [out[row][j] for j in range(l, r + 1) if out[row][j] != 1 and out[row][j] != b and out[row][j] in key_set]
        if len(cands) > 0 and len(set(cands)) == 1:
            s = cands[0]
            slist = slots_per_color.get(s, [])
            if not slist:
                continue
            # Check consistency with seed_slotmap
            col_slots = [seed_slotmap[j] for j in range(l, r + 1) if seed_slotmap[j] != -1]
            if col_slots and len(set(col_slots)) == 1:
                slot = col_slots[0]
                if slot not in slist:
                    continue
                # Reuse, no increment
            else:
                # Assign new
                idx = assigned_count[s] % len(slist)
                slot = slist[idx]
                assigned_count[s] += 1
                # Check consistency
                consistent = all(seed_slotmap[j] == -1 or seed_slotmap[j] == slot for j in range(l, r + 1))
                if not consistent:
                    continue
                # Set seed_slotmap
                for j in range(l, r + 1):
                    if seed_slotmap[j] == -1:
                        seed_slotmap[j] = slot
            # Fill the bay
            for j in range(l, r + 1):
                if is_fillable(out[row][j], b, key_set):
                    out[row][j] = s
                if block_slotmap[j] == -1:
                    block_slotmap[j] = slot
            assigned_regions.append((l, r, slot))
    return assigned_regions

def process_horizontal_gaps(out: List[List[int]], row: int, assigned_regions: List[Tuple[int, int, int]],
                            key_colors: List[int], b: int, key_set: set, block_slotmap: List[int], n_cols: int):
    if len(assigned_regions) < 2:
        return
    assigned_regions = sorted(assigned_regions, key=lambda x: x[0])
    for k in range(len(assigned_regions) - 1):
        l1, r1, slot1 = assigned_regions[k]
        l2, r2, slot2 = assigned_regions[k + 1]
        if abs(slot1 - slot2) == 1:
            gap_l = r1 + 1
            gap_r = l2 - 1
            if gap_l > gap_r:
                continue
            min_slot = min(slot1, slot2)
            fill_c = key_colors[min_slot]
            for j in range(gap_l, gap_r + 1):
                if is_fillable(out[row][j], b, key_set):
                    out[row][j] = fill_c
                if block_slotmap[j] == -1:
                    block_slotmap[j] = min_slot

def propagate_vertical_within_block(out: List[List[int]], start: int, end: int, seed_slotmap: List[int],
                                    key_colors: List[int], b: int, key_set: set, n_cols: int):
    for j in range(n_cols):
        if seed_slotmap[j] != -1:
            s = key_colors[seed_slotmap[j]]
            for r in range(start, end):
                if is_fillable(out[r][j], b, key_set):
                    out[r][j] = s

def fill_vertical_gaps(out: List[List[int]], blocks: List[Tuple[int, int]], block_slotmaps: List[List[int]],
                       key_colors: List[int], b: int, key_set: set, n_rows: int, n_cols: int):
    for bk in range(1, len(blocks)):
        above_start, above_end = blocks[bk - 1]
        below_start, below_end = blocks[bk]
        gap_start = above_end
        gap_end = below_start
        sa = block_slotmaps[bk - 1]
        sb = block_slotmaps[bk]
        for j in range(n_cols):
            if sa[j] != -1 and sb[j] != -1 and abs(sa[j] - sb[j]) == 1:
                min_s = min(sa[j], sb[j])
                fill_c = key_colors[min_s]
                for r in range(gap_start, gap_end):
                    all_b_r = is_all_b(out[r], b)
                    if is_fillable(out[r][j], b, key_set, all_b_r):
                        out[r][j] = fill_c

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n_rows = len(g)
    n_cols = len(g[0]) if n_rows > 0 else 0
    if n_rows < 2:
        return [row[:] for row in g]
    out = [row[:] for row in g]
    b = get_background(out)
    key_pos, key_colors = get_key(out, b, n_cols)
    if not key_colors:
        return out
    key_set = set(key_colors)
    slots_per_color = get_slots_per_color(key_colors)
    assigned_count: Dict[int, int] = defaultdict(int)
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
        blocks.append((start, i))
    block_slotmaps: List[List[int]] = []
    for start, end in blocks:
        seed_slotmap = [-1] * n_cols
        block_slotmap = [-1] * n_cols
        for row in range(start, end):
            assigned_regions = process_row_for_seeds(out, row, b, key_set, slots_per_color, assigned_count,
                                                     seed_slotmap, block_slotmap, key_colors, n_cols)
            process_horizontal_gaps(out, row, assigned_regions, key_colors, b, key_set, block_slotmap, n_cols)
        propagate_vertical_within_block(out, start, end, seed_slotmap, key_colors, b, key_set, n_cols)
        block_slotmaps.append(block_slotmap)
    fill_vertical_gaps(out, blocks, block_slotmaps, key_colors, b, key_set, n_rows, n_cols)
    return out
```