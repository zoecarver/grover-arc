```python
from typing import List
from collections import Counter

def find_background(grid: List[List[int]]) -> int:
    flat = [cell for row in grid for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def normalize_grid(grid: List[List[int]], mapping: dict) -> List[List[int]]:
    return [[mapping.get(cell, cell) for cell in row] for row in grid]

def extract_key(grid: List[List[int]], bg: int, size: int) -> List[List[int]]:
    key = []
    for r in range(1, 8, 2):
        if r >= size:
            break
        row_key = [grid[r][c] for c in [1, 3, 5] if c < size and grid[r][c] != bg]
        if row_key:
            key.append(row_key)
    return key

def find_source_block(grid: List[List[int]], bg: int, size: int) -> tuple:
    center_start = size // 4
    center_end = 3 * size // 4
    source_start = -1
    source_h = 0
    block_configs = []
    for r in range(size):
        current_runs = []
        i = 0
        while i < size:
            if grid[r][i] == bg or i < center_start or i > center_end:
                i += 1
                continue
            start_c = i
            color = grid[r][i]
            while i < size and grid[r][i] == color and center_start <= i <= center_end:
                i += 1
            w = i - start_c
            if w >= 2:
                current_runs.append((start_c, w, color))
        has_middle = len(current_runs) > 0
        if has_middle:
            if source_start == -1:
                source_start = r
                source_h = 1
                block_configs = current_runs[:]
            else:
                if len(current_runs) == len(block_configs) and all(cr == bc for cr, bc in zip(current_runs, block_configs)):
                    source_h += 1
                else:
                    break
        else:
            if source_start != -1:
                break
    return source_start, source_h, block_configs

def fill_level(out: List[List[int]], t_start: int, h: int, source_blocks: List[tuple], key_row: List[int], source_n: int, source_w: int, size: int, bg_norm: int):
    num_b = len(key_row)
    current_blocks = []
    for b in range(num_b):
        if b < source_n:
            sc, w, _ = source_blocks[b]
            colr = key_row[b]
            current_blocks.append((sc, w, colr))
        else:
            prev_sc, prev_w, _ = current_blocks[-1]
            prev_end = prev_sc + prev_w - 1
            gap = source_w - 1
            sc = prev_end + 1 + gap
            w = source_w
            colr = key_row[b]
            if sc >= size:
                continue
            w = min(w, size - sc)
            if w >= 1:
                current_blocks.append((sc, w, colr))
    for jj in range(h):
        rr = t_start + jj
        if 0 <= rr < size:
            for sc, w, colr in current_blocks:
                for p in range(w):
                    cc = sc + p
                    if 0 <= cc < size and out[rr][cc] == bg_norm:
                        out[rr][cc] = colr

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    original_bg = find_background(g)
    map_d = {1: 2, 2: 4, 3: 1, 4: 3, 8: 0}
    ng = normalize_grid(g, map_d)
    bg_norm = map_d.get(original_bg, original_bg)
    key = extract_key(ng, bg_norm, size)
    source_start, source_h, block_configs = find_source_block(ng, bg_norm, size)
    if source_h == 0:
        inv_d = {v: k for k, v in map_d.items()}
        return [[inv_d.get(cell, cell) for cell in row] for row in ng]
    source_n = len(block_configs)
    source_w = block_configs[0][1] if source_n > 0 else 0
    source_end = source_start + source_h - 1
    avg_source = source_start + (source_h - 1) / 2
    center = (size - 1) / 2
    direction = 'down' if avg_source < center else 'up'
    is_special = any(len(kr) > source_n for kr in key)
    num_reps = max(0, len(key) - 1)
    shift = size // 4
    out_norm = [row[:] for row in ng]
    if direction == 'down' and not is_special:
        for i in range(num_reps):
            t_start = source_start + (i + 1) * shift
            if t_start >= size:
                continue
            h = min(source_h, size - t_start)
            if h <= 0:
                continue
            key_row = key[i + 1]
            fill_level(out_norm, t_start, h, block_configs, key_row, source_n, source_w, size, bg_norm)
    elif direction == 'up' and not is_special:
        for i in range(num_reps):
            t_start = source_start - (num_reps - i) * shift
            if t_start < 0:
                continue
            h = min(source_h, size - t_start)
            if h <= 0:
                continue
            key_row = key[i]
            fill_level(out_norm, t_start, h, block_configs, key_row, source_n, source_w, size, bg_norm)
    elif direction == 'down' and is_special:
        previous_end = source_end
        for i in range(num_reps):
            key_row = key[i + 1]
            if i == 0:
                h = source_h - 1 if source_h > 1 else source_h
                t_start = previous_end + 3
            else:
                h = source_h
                t_start = previous_end + 2
            if t_start >= size:
                continue
            h = min(h, size - t_start)
            if h > 0:
                fill_level(out_norm, t_start, h, block_configs, key_row, source_n, source_w, size, bg_norm)
            previous_end = t_start + h - 1
    else:
        # special up, treat as regular up
        for i in range(num_reps):
            t_start = source_start - (num_reps - i) * shift
            if t_start < 0:
                continue
            h = min(source_h, size - t_start)
            if h <= 0:
                continue
            key_row = key[i]
            fill_level(out_norm, t_start, h, block_configs, key_row, source_n, source_w, size, bg_norm)
    inv_d = {v: k for k, v in map_d.items()}
    final_out = [[inv_d.get(cell, cell) for cell in row] for row in out_norm]
    return final_out
```