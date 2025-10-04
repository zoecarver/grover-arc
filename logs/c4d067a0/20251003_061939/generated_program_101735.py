```python
from typing import List, Tuple
from collections import Counter

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_runs(row: List[int], bg: int) -> List[Tuple[int, int, int]]:
    runs = []
    i = 0
    n = len(row)
    while i < n:
        if row[i] == bg:
            i += 1
            continue
        start = i
        col = row[i]
        while i < n and row[i] == col:
            i += 1
        leng = i - start
        if leng >= 2:
            runs.append((start, leng, col))
    return runs

def is_subsequence(sub: List[int], full: List[int]) -> bool:
    if not sub:
        return True
    i = 0
    for val in full:
        if i < len(sub) and val == sub[i]:
            i += 1
            if i == len(sub):
                return True
    return i == len(sub)

def get_key_cols(g: List[List[int]], bg: int, size: int) -> List[int]:
    key_cols = []
    for c in range(1, min(10, size), 2):
        if any(g[r][c] != bg for r in range(min(8, size))):
            key_cols.append(c)
    return key_cols

def get_key_rows(g: List[List[int]], bg: int, key_cols: List[int], size: int) -> List[int]:
    rows = []
    for r in range(min(8, size)):
        if any(g[r][c] != bg for c in key_cols):
            rows.append(r)
    return rows

def get_key_colors(g: List[List[int]], key_rows: List[int], key_cols: List[int], bg: int) -> List[List[int]]:
    key_colors_list = []
    for r in key_rows:
        row_c = [g[r][c] for c in key_cols if g[r][c] != bg and g[r][c] != 8]
        if row_c:
            key_colors_list.append(row_c)
    return key_colors_list

def find_anchor(g: List[List[int]], bg: int, size: int, key_colors_list: List[List[int]]) -> Tuple[int, int, int, List[int], int, int, int]:
    best_h = 0
    best_s = -1
    best_ki = -1
    best_starts = []
    best_diff = 0
    best_w = 0
    for s in range(size):
        anchor_runs = get_runs(g[s], bg)
        if not anchor_runs:
            continue
        h = 1
        for next_r in range(s + 1, size):
            this_runs = get_runs(g[next_r], bg)
            if this_runs != anchor_runs:
                break
            h += 1
        if h < 2:
            continue
        block_starts = [st for st, _, _ in anchor_runs]
        block_colors = [c for _, _, c in anchor_runs]
        w_set = {l for _, l, _ in anchor_runs}
        if len(w_set) != 1 or next(iter(w_set)) < 2:
            continue
        w = next(iter(w_set))
        if len(block_starts) < 1:
            continue
        diff = block_starts[1] - block_starts[0] if len(block_starts) >= 2 else w + 2
        for ki, kc in enumerate(key_colors_list):
            if is_subsequence(block_colors, kc):
                if h > best_h or (h == best_h and s < best_s):
                    best_h = h
                    best_s = s
                    best_ki = ki
                    best_starts = block_starts
                    best_diff = diff
                    best_w = w
    if best_h == 0:
        return -1, -1, -1, [], 0, 0, 0
    return best_h, best_s, best_ki, best_starts, best_diff, best_w, best_h  # last is h again? No, return h,s,ki,starts,diff,w

def place_block(out: List[List[int]], start_r: int, h: int, start_c: int, w: int, col: int, bg: int, size: int):
    for r in range(start_r, min(start_r + h, size)):
        for c in range(start_c, min(start_c + w, size)):
            if out[r][c] == bg:
                out[r][c] = col

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    bg = get_background(g)
    key_cols = get_key_cols(g, bg, size)
    key_rows = get_key_rows(g, bg, key_cols, size)
    key_colors_list = get_key_colors(g, key_rows, key_cols, bg)
    if not key_colors_list:
        return copy_grid(g)
    anchor_h, anchor_s, anchor_ki, anchor_starts, anchor_diff, anchor_w = find_anchor(g, bg, size, key_colors_list)[:6]
    if anchor_ki == -1:
        return copy_grid(g)
    step_down = 2 * anchor_h - 1
    step_up = 2 * anchor_h + 1
    out = copy_grid(g)
    for ki in range(len(key_colors_list)):
        if ki == anchor_ki:
            continue
        delta = ki - anchor_ki
        if delta > 0:
            place_s = anchor_s + delta * step_down
        else:
            place_s = anchor_s + delta * step_up
        if place_s < 0 or place_s + anchor_h > size:
            continue
        key_seq = key_colors_list[ki]
        m = len(key_seq)
        temp_starts = anchor_starts[:]
        num_b = len(temp_starts)
        while num_b < m:
            last = temp_starts[-1]
            new_st = last + anchor_diff
            if new_st + anchor_w > size:
                break
            temp_starts.append(new_st)
            num_b += 1
        for j in range(min(len(temp_starts), m)):
            col = key_seq[j]
            st = temp_starts[j]
            place_block(out, place_s, anchor_h, st, anchor_w, col, bg, size)
    return out
```