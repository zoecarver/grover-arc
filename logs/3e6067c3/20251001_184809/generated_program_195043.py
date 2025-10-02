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

def find_seed_regions(row: List[int], b: int, n_cols: int, border: int = 1) -> List[Tuple[int, int, int, int]]:
    border_js = [-1] + [j for j in range(n_cols) if row[j] == border] + [n_cols]
    regions = []
    for bk in range(len(border_js) - 1):
        l = border_js[bk] + 1
        r = border_js[bk + 1] - 1
        if l > r:
            continue
        candidates = [row[j] for j in range(l, r + 1) if row[j] != b and row[j] != border]
        if candidates and len(set(candidates)) == 1:
            s = candidates[0]
            center = (l + r) // 2
            regions.append((s, l, r, center))
    return regions

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    out = [list(row) for row in g]
    b = get_background(g)
    n_rows = len(g)
    n_cols = len(g[0])
    if n_rows < 2:
        return out
    key_pos, key_colors = get_key(g, b, n_cols)
    if not key_colors:
        return out
    slots_per_color = get_slots_per_color(key_colors)
    assigned_count = defaultdict(int)
    border = 1
    # Find content blocks
    blocks = []
    i = 0
    while i < n_rows - 2:
        if all(c == b for c in g[i]):
            i += 1
            continue
        start = i
        i += 1
        while i < n_rows - 2 and not all(c == b for c in g[i]):
            i += 1
        blocks.append((start, i))
    # Process each block
    slot_per_cols = []
    for start, end in blocks:
        seed_rows = [r for r in range(start, end) if any(c != b and c != border for c in g[r])]
        if not seed_rows:
            slot_per_cols.append([-1] * n_cols)
            continue
        best_count = -1
        best_slot_per = None
        prev_seed_r = -1
        for sr_idx, sr in enumerate(seed_rows):
            if sr_idx > 0 and g[sr] == g[seed_rows[sr_idx - 1]]:
                out[sr] = out[seed_rows[sr_idx - 1]][:]
                continue
            # Process this seed row
            regions = find_seed_regions(g[sr], b, n_cols, border)
            slots_assigned = [-1] * len(regions)
            for idx, (s, l, r, center) in enumerate(regions):
                slots_list = slots_per_color.get(s, [])
                if slots_list:
                    k = assigned_count[s]
                    slot_i = slots_list[k % len(slots_list)]
                    assigned_count[s] += 1
                    slots_assigned[idx] = slot_i
                    # Fill seed bay
                    for j in range(l, r + 1):
                        if out[sr][j] == b:
                            out[sr][j] = s
            # Horizontal gap fill
            for ii in range(len(regions) - 1):
                if slots_assigned[ii] == -1 or slots_assigned[ii + 1] == -1:
                    continue
                slot1 = slots_assigned[ii]
                slot2 = slots_assigned[ii + 1]
                if abs(slot1 - slot2) != 1:
                    continue
                r1 = regions[ii][2]
                l2 = regions[ii + 1][1]
                gap_l = r1 + 1
                gap_r = l2 - 1
                if gap_l > gap_r:
                    continue
                fill_c = key_colors[min(slot1, slot2)]
                for j in range(gap_l, gap_r + 1):
                    if out[sr][j] == b:
                        out[sr][j] = fill_c
            # Update best
            current_slot_per = [-1] * n_cols
            num_assigned = 0
            for idx in range(len(regions)):
                if slots_assigned[idx] != -1:
                    num_assigned += 1
                    l = regions[idx][1]
                    r = regions[idx][2]
                    for j in range(l, r + 1):
                        current_slot_per[j] = slots_assigned[idx]
            if num_assigned > best_count:
                best_count = num_assigned
                best_slot_per = current_slot_per
        if best_slot_per is not None:
            slot_per_cols.append(best_slot_per)
        else:
            slot_per_cols.append([-1] * n_cols)
    # Vertical gap fills
    num_blocks = len(blocks)
    for gap_i in range(1, num_blocks):
        above_end = blocks[gap_i - 1][1]
        below_start = blocks[gap_i][0]
        gap_start = above_end
        gap_end = below_start
        if gap_start >= gap_end:
            continue
        sa_list = slot_per_cols[gap_i - 1]
        sb_list = slot_per_cols[gap_i]
        for j in range(n_cols):
            sa = sa_list[j]
            sb = sb_list[j]
            if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                fill_c = key_colors[min(sa, sb)]
                for rr in range(gap_start, gap_end):
                    if out[rr][j] == b:
                        out[rr][j] = fill_c
    return out
```