```python
from typing import List, Dict, Tuple
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or len(g) < 2:
        return [list(row) for row in g]
    n_rows = len(g)
    n_cols = len(g[0]) if g else 0
    out = [list(row) for row in g]
    b = get_background(g)
    key_pos, key_colors = get_key(g, b, n_cols)
    if not key_colors:
        return out
    key_set = set(key_colors)
    empty_color = get_empty_color(g, b, key_set, n_rows - 2, n_cols)
    slots_per_color = get_slots_per_color(key_colors)
    assigned_count = defaultdict(int)
    blocks = find_blocks(g, b, n_rows)
    block_infos = []
    for blk_start, blk_end in blocks:
        seed_rows = find_seed_rows(g, key_set, blk_start, blk_end, n_cols)
        if not seed_rows:
            slotmap = [-1] * n_cols
            block_infos.append((blk_start, blk_end, slotmap))
            continue
        rep = select_rep_row(g, key_set, seed_rows, n_cols)
        seed_strips = process_horizontal_assign(out[rep], empty_color, key_set, 1, assigned_count, slots_per_color, key_colors, n_cols)
        process_horizontal_gapfill(out[rep], empty_color, key_set, 1, seed_strips, key_colors, n_cols)
        slotmap = create_slotmap(seed_strips, n_cols)
        block_infos.append((blk_start, blk_end, slotmap))
        for i in range(blk_start, blk_end):
            fill_seed_strips(out[i], seed_strips, key_colors, empty_color)
            process_horizontal_gapfill(out[i], empty_color, key_set, 1, seed_strips, key_colors, n_cols)
    process_vertical_gaps(out, blocks, block_infos, key_colors, n_rows, n_cols)
    for i in range(n_rows - 2, n_rows):
        out[i] = list(g[i])
    return out

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
    slots_per_color = defaultdict(list)
    for k, color in enumerate(key_colors):
        slots_per_color[color].append(k)
    return slots_per_color

def get_empty_color(g: List[List[int]], b: int, key_set: set, n_rows: int, n_cols: int) -> int:
    color_count = defaultdict(int)
    for i in range(n_rows):
        for j in range(n_cols):
            c = g[i][j]
            if c != 1 and c != b and c not in key_set:
                color_count[c] += 1
    if color_count:
        return max(color_count, key=lambda item: item[1])
    return b

def find_blocks(g: List[List[int]], b: int, n_rows: int) -> List[Tuple[int, int]]:
    blocks = []
    i = 0
    while i < n_rows - 2:
        if all(c == b for c in g[i]):
            i += 1
            continue
        start = i
        while i < n_rows - 2 and not all(c == b for c in g[i]):
            i += 1
        blocks.append((start, i))
    return blocks

def find_seed_rows(g: List[List[int]], key_set: set, start: int, end: int, n_cols: int) -> List[int]:
    return [i for i in range(start, end) if any(g[i][j] in key_set for j in range(n_cols))]

def select_rep_row(g: List[List[int]], key_set: set, seed_rows: List[int], n_cols: int) -> int:
    counts = [(i, sum(1 for j in range(n_cols) if g[i][j] in key_set)) for i in seed_rows]
    return max(counts, key=lambda x: x[1])[0]

def process_horizontal_assign(out_row: List[int], empty_color: int, key_set: set, border_val: int, assigned_count: Dict[int, int], slots_per_color: Dict[int, List[int]], key_colors: List[int], n_cols: int) -> List[Tuple[int, int, int]]:
    border_js = [-1] + [j for j in range(n_cols) if out_row[j] == border_val] + [n_cols]
    seed_strips = []
    k = 0
    while k < len(border_js) - 1:
        l = border_js[k] + 1
        r = border_js[k + 1] - 1
        if l > r:
            k += 1
            continue
        candidates = [out_row[j] for j in range(l, r + 1) if out_row[j] != empty_color and out_row[j] != border_val and out_row[j] in key_set]
        if candidates and len(set(candidates)) == 1:
            s = candidates[0]
            slist = slots_per_color.get(s, [])
            if slist:
                slot = slist[assigned_count[s] % len(slist)]
                assigned_count[s] += 1
                for j in range(l, r + 1):
                    if out_row[j] == empty_color or out_row[j] == s:
                        out_row[j] = s
                seed_strips.append((l, r, slot))
        k += 1
    return seed_strips

def create_slotmap(seed_strips: List[Tuple[int, int, int]], n_cols: int) -> List[int]:
    slotmap = [-1] * n_cols
    for l, r, slot in seed_strips:
        for j in range(l, r + 1):
            slotmap[j] = slot
    return slotmap

def process_horizontal_gapfill(out_row: List[int], empty_color: int, key_set: set, border_val: int, seed_strips: List[Tuple[int, int, int]], key_colors: List[int], n_cols: int):
    border_js = [-1] + [j for j in range(n_cols) if out_row[j] == border_val] + [n_cols]
    bays = []
    k = 0
    while k < len(border_js) - 1:
        l = border_js[k] + 1
        r = border_js[k + 1] - 1
        if l > r:
            k += 1
            continue
        assigned_slot = None
        for sl, sr, sslot in seed_strips:
            if sl == l and sr == r:
                assigned_slot = sslot
                break
        is_ass = assigned_slot is not None
        bays.append((l, r, is_ass, assigned_slot))
        k += 1
    for kk in range(1, len(bays) - 1):
        l, r, is_ass, slot = bays[kk]
        if is_ass:
            continue
        left_is_ass = bays[kk - 1][2]
        right_is_ass = bays[kk + 1][2]
        if left_is_ass and right_is_ass:
            slot_l = bays[kk - 1][3]
            slot_r = bays[kk + 1][3]
            if abs(slot_l - slot_r) == 1:
                min_slot = min(slot_l, slot_r)
                fill_c = key_colors[min_slot]
                for j in range(l, r + 1):
                    if out_row[j] == empty_color:
                        out_row[j] = fill_c

def fill_seed_strips(out_row: List[int], seed_strips: List[Tuple[int, int, int]], key_colors: List[int], empty_color: int):
    for l, r, slot in seed_strips:
        c = key_colors[slot]
        for j in range(l, r + 1):
            if out_row[j] == empty_color:
                out_row[j] = c

def process_vertical_gaps(out: List[List[int]], blocks: List[Tuple[int, int]], block_infos: List[Tuple[int, int, List[int]]], key_colors: List[int], n_rows: int, n_cols: int):
    m = len(blocks)
    if m < 2:
        return
    for k in range(m - 1):
        blk1_end = blocks[k][1]
        blk2_start = blocks[k + 1][0]
        if blk1_end + 1 == blk2_start:
            continue
        v_start = blk1_end
        v_end = blk2_start - 1
        _, _, slotmap_a = block_infos[k]
        _, _, slotmap_b = block_infos[k + 1]
        for j in range(n_cols):
            sa = slotmap_a[j]
            sb = slotmap_b[j]
            if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                min_s = min(sa, sb)
                fill_c = key_colors[min_s]
                for rr in range(v_start, v_end + 1):
                    out[rr][j] = fill_c
```