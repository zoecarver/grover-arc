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

def find_seed_regions(row: List[int], b: int, n_cols: int, key_set: set, placeholder: int = None) -> List[Tuple[int, int, int, int]]:
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

def is_fillable(c: int, b: int, key_set: set, all_b_row: bool, placeholder: int = None) -> bool:
    if c == 1:
        return all_b_row
    if c in key_set:
        return False
    return True

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n_rows = len(g) - 2
    n_cols = len(g[0])
    b = get_background(g)
    key_pos, key_colors = get_key(g, b, n_cols)
    if not key_colors:
        return [list(row) for row in g]
    slots_per_color = get_slots_per_color(key_colors)
    key_set = set(key_colors)
    flat = [c for row in g[:-2] for c in row]
    possible_ph = {c for c in set(flat) if c != b and c != 1 and c not in key_set}
    placeholder = next(iter(possible_ph)) if len(possible_ph) == 1 else None
    out = [list(row) for row in g]
    slotmaps = [[-1] * n_cols for _ in range(n_rows)]
    assigned_count = defaultdict(int)
    for i in range(n_rows):
        regions = find_seed_regions(g[i], b, n_cols, key_set, placeholder)
        region_slots = {}
        for s, l, r, center in regions:
            if s not in slots_per_color:
                continue
            slist = slots_per_color[s]
            k = assigned_count[s]
            slot_i = slist[k % len(slist)]
            assigned_count[s] += 1
            region_slots[center] = slot_i
            for jj in range(l, r + 1):
                slotmaps[i][jj] = slot_i
        for kk in range(len(regions) - 1):
            s1, l1, r1, c1 = regions[kk]
            s2, l2, r2, c2 = regions[kk + 1]
            slot1 = region_slots.get(c1, -1)
            slot2 = region_slots.get(c2, -1)
            if slot1 != -1 and slot2 != -1 and abs(slot1 - slot2) == 1:
                fill_c = key_colors[min(slot1, slot2)]
                for jj in range(r1 + 1, l2):
                    if is_fillable(out[i][jj], b, key_set, False, placeholder):
                        out[i][jj] = fill_c
        for s, l, r, _ in regions:
            for jj in range(l, r + 1):
                if is_fillable(out[i][jj], b, key_set, False, placeholder):
                    out[i][jj] = s
    i = 0
    while i < n_rows:
        if all(c == b for c in g[i]):
            i += 1
            continue
        start = i
        while i < n_rows and not all(c == b for c in g[i]):
            i += 1
        block_end = i - 1
        max_c = -1
        hint = -1
        for rr in range(start, block_end + 1):
            cnt = sum(1 for j in range(n_cols) if g[rr][j] in key_set)
            if cnt > max_c:
                max_c = cnt
                hint = rr
        if hint == -1 or max_c == 0:
            continue
        regions = find_seed_regions(g[hint], b, n_cols, key_set, placeholder)
        for s, l, r, _ in regions:
            for rr in range(start, block_end + 1):
                allb = all(gg == b for gg in g[rr])
                for jj in range(l, r + 1):
                    if is_fillable(out[rr][jj], b, key_set, allb, placeholder):
                        out[rr][jj] = s
    i = 0
    while i < n_rows:
        start_gap = -1
        curr_i = i
        while curr_i < n_rows:
            if all(c == b for c in g[curr_i]):
                if start_gap == -1:
                    start_gap = curr_i
                curr_i += 1
            else:
                if start_gap != -1 and start_gap < curr_i:
                    for rr in range(start_gap, curr_i):
                        for j in range(n_cols):
                            sa = -1
                            for k in range(rr - 1, -1, -1):
                                if slotmaps[k][j] != -1:
                                    sa = slotmaps[k][j]
                                    break
                            sb = -1
                            for k in range(rr + 1, n_rows):
                                if slotmaps[k][j] != -1:
                                    sb = slotmaps[k][j]
                                    break
                            if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                                fill_c = key_colors[min(sa, sb)]
                                if is_fillable(out[rr][j], b, key_set, True, placeholder):
                                    out[rr][j] = fill_c
                    start_gap = -1
                curr_i += 1
        i = curr_i
    if start_gap != -1 and start_gap < n_rows:
        for rr in range(start_gap, n_rows):
            for j in range(n_cols):
                sa = -1
                for k in range(rr - 1, -1, -1):
                    if slotmaps[k][j] != -1:
                        sa = slotmaps[k][j]
                        break
                sb = -1
                for k in range(rr + 1, n_rows):
                    if slotmaps[k][j] != -1:
                        sb = slotmaps[k][j]
                        break
                if sa != -1 and sb != -1 and abs(sa - sb) == 1:
                    fill_c = key_colors[min(sa, sb)]
                    if is_fillable(out[rr][j], b, key_set, True, placeholder):
                        out[rr][j] = fill_c
    return out
```