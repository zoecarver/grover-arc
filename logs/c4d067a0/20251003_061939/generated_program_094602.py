```python
from typing import List

def get_bg(g: List[List[int]]) -> int:
    return g[0][0]

def get_left_cols(g: List[List[int]], bg: int) -> List[int]:
    left_cols = [1, 3]
    if any(g[r][5] != bg for r in range(len(g))):
        left_cols.append(5)
    return left_cols

def get_sample_rows(g: List[List[int]], bg: int, left_cols: List[int]) -> List[int]:
    n = len(g)
    first_r = min((r for r in range(n) if any(g[r][c] != bg for c in left_cols)), default=0)
    sample_rows = []
    r = first_r
    while r < n:
        if any(g[r][c] != bg for c in left_cols):
            sample_rows.append(r)
            r += 2
        else:
            break
    return sample_rows

def get_palette(g: List[List[int]], sample_rows: List[int], left_cols: List[int], bg: int) -> List[List[int]]:
    return [[g[r][c] for c in left_cols] for r in sample_rows]

def get_b_start_and_s(g: List[List[int]], bg: int) -> tuple:
    n = len(g)
    has_non_right = [any(c != bg for c in row[n // 2:]) for row in g]
    b_start = 0
    s = 0
    current_start = 0
    for r in range(n):
        if has_non_right[r]:
            if s == 0:
                b_start = r
                current_start = r
            s = r - current_start + 1
        else:
            if s > 0:
                break
            s = 0
            current_start = r + 1
    if s == 0:
        b_start = current_start
    return b_start, s

def get_sub_starts(g: List[List[int]], b_start: int, s: int, bg: int) -> List[int]:
    n = len(g[0])
    row = g[b_start]
    sub_starts = []
    i = 0
    while i < n:
        if row[i] != bg:
            start = i
            color = row[i]
            width = 0
            while i < n and row[i] == color:
                width += 1
                i += 1
            if width == s:
                sub_starts.append(start)
        else:
            i += 1
    return sub_starts

def find_j(palette: List[List[int]], sub_colors: List[int], m: int, len_left: int) -> int:
    k = len(palette)
    for l in range(k):
        match = True
        for i in range(m):
            if palette[l][i] == bg or palette[l][i] != sub_colors[i]:
                match = False
                break
        if match:
            return l
        if m == 2 and len_left == 3 and palette[l][0] == palette[l][1] and palette[l][0] != bg and palette[l][2] != bg and sub_colors[0] == palette[l][0] and sub_colors[1] == palette[l][2]:
            return l
    return 0  # fallback

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = get_bg(g)
    out = [row[:] for row in g]
    left_cols = get_left_cols(g, bg)
    sample_rows = get_sample_rows(g, bg, left_cols)
    palette = get_palette(g, sample_rows, left_cols, bg)
    k = len(sample_rows)
    b_start, s = get_b_start_and_s(g, bg)
    sub_starts = get_sub_starts(g, b_start, s, bg)
    m = len(sub_starts)
    row = g[b_start]
    sub_colors = [row[sub_starts[i]] for i in range(m)]
    j = find_j(palette, sub_colors, m, len(left_cols))
    first_sample_zero = sample_rows[0] == 0 if sample_rows else False
    d_forward = 2 * s - 1
    d_backward = 2 * s + 1
    sep = 1
    for l in range(k):
        if l == j:
            continue
        if l > j:
            num_step = l - j
            if first_sample_zero:
                step_sum = 2 * s + (num_step - 1) * d_forward
            else:
                step_sum = num_step * d_forward
            b_s = b_start + step_sum
        else:
            num_step = j - l
            step_sum = num_step * d_backward
            b_s = b_start - step_sum
        if b_s < 0 or b_s + s > n:
            continue
        for rr in range(s):
            r = b_s + rr
            if r >= n:
                break
            row_out = out[r]
            for i in range(m):
                c = palette[l][i]
                if c != bg:
                    start_c = sub_starts[i]
                    for cc in range(s):
                        if start_c + cc < n:
                            row_out[start_c + cc] = c
            if len(left_cols) == 3 and m == 2 and palette[l][2] != bg:
                start_c = sub_starts[1] + s + sep
                for cc in range(s):
                    if start_c + cc < n:
                        row_out[start_c + cc] = palette[l][2]
    return out
```