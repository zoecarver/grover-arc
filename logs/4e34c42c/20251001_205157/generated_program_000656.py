```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def has_non_bg(row: List[int], bg: int) -> bool:
    return any(cell != bg for cell in row)

def trim_right(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    if h == 0:
        return sub
    mid_idx = h // 2
    while len(sub) > 0 and len(sub[0]) > 1:
        right_col = [row[-1] for row in sub]
        fg_count = sum(1 for c in right_col if c != bg)
        if fg_count != h:
            break
        mid_right = right_col[mid_idx]
        if mid_right == bg:
            break
        mid_left = sub[mid_idx][-2]
        if mid_left == bg:
            break
        if mid_right != mid_left:
            sub = [row[:-1] for row in sub]
        else:
            break
    return sub

def pad_to_5(sub: List[List[int]], bg: int) -> List[List[int]]:
    h = len(sub)
    w = len(sub[0]) if sub and h > 0 else 0
    pad_top = (5 - h) // 2
    pad_bottom = 5 - h - pad_top
    bg_row = [bg] * w
    padded = [bg_row[:] for _ in range(pad_top)] + [row[:] for row in sub] + [bg_row[:] for _ in range(pad_bottom)]
    return padded

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    bg = get_background(g)
    n_rows = len(g)
    if n_rows == 0:
        return []
    n_cols = len(g[0])
    patterns = []
    current = 0
    while current < n_rows:
        start_r = next((r for r in range(current, n_rows) if has_non_bg(g[r], bg)), None)
        if start_r is None:
            break
        end_r = start_r
        while end_r < n_rows - 1 and end_r - start_r + 1 < 5 and has_non_bg(g[end_r + 1], bg):
            end_r += 1
        h = end_r - start_r + 1
        if h < 3:
            current = end_r + 1
            continue
        col_has_fg = [False] * n_cols
        for j in range(n_cols):
            for r in range(start_r, end_r + 1):
                if g[r][j] != bg:
                    col_has_fg[j] = True
                    break
        i = 0
        while i < n_cols:
            if not col_has_fg[i]:
                i += 1
                continue
            run_start = i
            while i < n_cols and col_has_fg[i]:
                i += 1
            run_end = i - 1
            run_w = run_end - run_start + 1
            if run_w < 3:
                continue
            sub = [[g[r][j] for j in range(run_start, run_end + 1)] for r in range(start_r, end_r + 1)]
            h_sub = len(sub)
            if h_sub > 0 and len(sub[0]) > 0:
                left_col = [row[0] for row in sub]
                fg_c = sum(1 for c in left_col if c != bg)
                colors_set = set(c for c in left_col if c != bg)
                num_c = len(colors_set)
                if fg_c >= 3 and ((num_c > 1 and fg_c == h_sub) or fg_c < h_sub):
                    sub = [row[1:] for row in sub]
            sub = trim_right(sub, bg)
            fg_total = sum(1 for row in sub for cell in row if cell != bg)
            if fg_total < 10:
                continue
            padded = pad_to_5(sub, bg)
            patterns.append((start_r, padded))
        current = end_r + 1
    if not patterns:
        bg_row = [bg] * n_cols
        return [bg_row[:] for _ in range(5)]
    patterns.sort(key=lambda p: p[0])
    result = [row[:] for row in patterns[0][1]]
    for _, p in patterns[1:]:
        for k in range(5):
            result[k].extend(p[k])
    return result
```