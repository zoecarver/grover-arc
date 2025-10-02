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

def is_fillable(c: int, b: int, key_set: set, all_b_row: bool = False) -> bool:
    if c in key_set:
        return False
    if c == 1:
        return all_b_row
    return True

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n_rows = len(g)
    n_cols = len(g[0])
    b = get_background(g)
    _, key_colors = get_key(g, b, n_cols)
    key_set = set(key_colors)
    slots_per_color = get_slots_per_color(key_colors)
    out = [list(row) for row in g]
    assigned_count = defaultdict(int)
    blocks: List[Tuple[int, int]] = []
    i = 0
    while i < n_rows - 2:
        if all(c == b for c in g[i]):
            i += 1
            continue
        start = i
        while i < n_rows - 2 and not all(c == b for c in g[i + 1]):
            i += 1
        end = i
        blocks.append((start, end))
        i = end + 1
    slotmaps: List[List[int]] = []
    for start, end in blocks:
        rep_row = start
        max_num = sum(1 for j in range(n_cols) if g[start][j] in key_set)
        for r in range(start + 1, end + 1):
            num = sum(1 for j in range(n_cols) if g[r][j] in key_set)
            if num > max_num:
                max_num = num
                rep_row = r
        if max_num == 0:
            slotmaps.append([-1] * n_cols)
            continue
        row = g[rep_row]
        border_js = [-1] + [j for j in range(n_cols) if row[j] == 1] + [n_cols]
        regions = []
        for ib in range(len(border_js) - 1):
            l = border_js[ib] + 1
            r = border_js[ib + 1] - 1
            if l > r:
                continue
            candidates = [row[j] for j in range(l, r + 1) if row[j] in key_set]
            if candidates and len(set(candidates)) == 1:
                s = candidates[0]
                center = (l + r) // 2
                regions.append((s, l, r, center))
        regions.sort(key=lambda x: x[3])
        region_to_slot = {}
        for s, l, r, _ in regions:
            slots_list = slots_per_color.get(s, [])
            if slots_list:
                k = assigned_count[s]
                slot_i = slots_list[k % len(slots_list)]
                region_to_slot[(l, r)] = slot_i
                assigned_count[s] += 1
        slotmap = [-1] * n_cols
        for (l, r), slot_i in region_to_slot.items():
            color = key_colors[slot_i]
            for j in range(l, r + 1):
                if is_fillable(row[j], b, key_set, False):
                    out[rep_row][j] = color
                if out[rep_row][j] == color:
                    slotmap[j] = slot_i
        bay_intervals = []
        bay_slots = []
        for ib in range(len(border_js) - 1):
            l = border_js[ib] + 1
            r = border_js[ib + 1] - 1
            if l > r:
                continue
            bay_intervals.append((l, r))
            sl = region_to_slot.get((l, r), -1)
            bay_slots.append(sl)
        n_bays = len(bay_intervals)
        i = 0
        while i < n_bays:
            if bay_slots[i] != -1:
                i += 1
                continue
            start_bg = i
            while i < n_bays and bay_slots[i] == -1:
                i += 1
            end_bg = i - 1
            if start_bg > 0 and end_bg < n_bays - 1:
                left_slot = bay_slots[start_bg - 1]
                right_slot = bay_slots[end_bg + 1]
                if left_slot != -1 and right_slot != -1 and abs(left_slot - right_slot) == 1:
                    min_slot = min(left_slot, right_slot)
                    color = key_colors[min_slot]
                    for k in range(start_bg, end_bg + 1):
                        ll, rr = bay_intervals[k]
                        for j in range(ll, rr + 1):
                            if is_fillable(row[j], b, key_set, False):
                                out[rep_row][j] = color
                                slotmap[j] = min_slot
        slotmaps.append(slotmap)
        for r in range(start, end + 1):
            for j in range(n_cols):
                if slotmap[j] != -1:
                    color = key_colors[slotmap[j]]
                    if is_fillable(g[r][j], b, key_set, False):
                        out[r][j] = color
    gaps = []
    prev_end = -1
    for bs, be in blocks:
        if bs > prev_end + 1:
            gaps.append((prev_end + 1, bs - 1))
        prev_end = be
    if n_rows - 2 > prev_end:
        gaps.append((prev_end + 1, n_rows - 3))
    for v_start, v_end in gaps:
        if v_start > v_end:
            continue
        above_idx = -1
        for bii in range(len(blocks)):
            if blocks[bii][1] < v_start:
                above_idx = bii
            else:
                break
        below_idx = len(blocks)
        for bii in range(above_idx + 1, len(blocks)):
            if blocks[bii][0] > v_end:
                below_idx = bii
                break
        if above_idx == -1 or below_idx == len(blocks) or below_idx <= above_idx + 1:
            continue
        above_sm = slotmaps[above_idx]
        below_sm = slotmaps[below_idx]
        for j in range(n_cols):
            sa = above_sm[j]
            sb = below_sm[j]
            if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                min_s = min(sa, sb)
                color = key_colors[min_s]
                for r in range(v_start, v_end + 1):
                    if is_fillable(g[r][j], b, key_set, True):
                        out[r][j] = color
    return out
```