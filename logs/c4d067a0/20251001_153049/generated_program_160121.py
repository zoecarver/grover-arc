```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def get_instruction_rows(g: List[List[int]], bg: int, n: int) -> List[int]:
    left_cols = [1, 3, 5]
    instruction_rows = []
    for r in range(1, n, 2):
        has_non_bg = False
        for c in left_cols:
            if c < n and g[r][c] != bg:
                has_non_bg = True
                break
        if has_non_bg:
            instruction_rows.append(r)
    return instruction_rows

def get_existing_slot(g: List[List[int]], bg: int, n: int) -> Tuple[int, int, int, int, int, List[Tuple[int, int, int]], int]:
    min_r = n
    max_r = -1
    for r in range(n):
        has_non_bg = False
        for c in range(7, n):
            if g[r][c] != bg:
                has_non_bg = True
                break
        if has_non_bg:
            min_r = min(min_r, r)
            max_r = max(max_r, r)
    h = max_r - min_r + 1 if max_r >= 0 else 0
    start_s = min_r
    row = g[start_s]
    groups = []
    i = 7
    while i < n:
        if row[i] != bg:
            color = row[i]
            start_c = i
            while i < n and row[i] == color:
                i += 1
            width = i - start_c
            groups.append((color, start_c, width))
        else:
            i += 1
    m = len(groups)
    w = groups[0][2] if m > 0 else 0
    s_gap = groups[1][1] - groups[0][1] - w if m > 1 else 1
    first_start = groups[0][1] if m > 0 else 7
    return start_s, h, first_start, w, s_gap, groups, m

def find_stage(g: List[List[int]], instr_rows: List[int], bg: int, n: int, groups: List[Tuple[int, int, int]], m: int) -> Tuple[int, int]:
    if m == 0:
        return 1, 2
    first_color = groups[0][0]
    k = len(instr_rows)
    for i in range(k):
        r = instr_rows[i]
        col0 = g[r][1] if 1 < n else bg
        if col0 == bg or col0 != first_color:
            continue
        if m <= 1:
            return i + 1, 2
        second_color = groups[1][0]
        col1 = g[r][3] if 3 < n else bg
        if col1 != bg and col1 == second_color:
            return i + 1, 2
        col2 = g[r][5] if 5 < n else bg
        if col2 != bg and col2 == second_color:
            return i + 1, 3
    return 1, 2

def compute_start(start_s: int, skipped_i: int, j: int, h: int, s_gap: int) -> int:
    if j < skipped_i:
        dist = 0
        for t in range(j, skipped_i):
            empty = s_gap + t
            step = h + empty
            dist += step
        sr = start_s - dist
        return sr if sr >= 0 else -1
    else:
        dist = 0
        for t in range(skipped_i, j):
            empty = s_gap + t
            step = h + empty
            dist += step
        sr = start_s + dist
        return sr if sr + h <= len(g) else -1  # n is len(g)

def place_group(g_out: List[List[int]], start_r: int, h: int, start_c: int, width: int, color: int, bg: int, n: int):
    for rr in range(start_r, min(start_r + h, n)):
        for cc in range(start_c, min(start_c + width, n)):
            if g_out[rr][cc] == bg:
                g_out[rr][cc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    g_out = [row[:] for row in g]
    bg = get_background(g)
    instr_rows = get_instruction_rows(g, bg, n)
    k = len(instr_rows)
    if k == 0:
        return g_out
    slot_info = get_existing_slot(g, bg, n)
    start_s, h, _, w, s_gap, groups, m = slot_info
    if h == 0:
        return g_out
    stage, second_channel = find_stage(g, instr_rows, bg, n, groups, m)
    skipped_i = stage - 1
    secondary_index = second_channel - 1
    tertiary_index = 1 if second_channel == 3 else 2
    left_cols = [1, 3, 5]
    for j in range(k):
        if j == skipped_i:
            continue
        start_row = compute_start(start_s, skipped_i, j, h, s_gap)
        if start_row == -1:
            continue
        r = instr_rows[j]
        color0 = g[r][left_cols[0]] if left_cols[0] < n and g[r][left_cols[0]] != bg else bg
        color1 = g[r][left_cols[1]] if left_cols[1] < n and g[r][left_cols[1]] != bg else bg
        color2 = g[r][left_cols[2]] if left_cols[2] < n and g[r][left_cols[2]] != bg else bg
        color_first = color0
        if color_first == bg:
            continue
        place_group(g_out, start_row, h, groups[0][1], groups[0][2], color_first, bg, n)
        if m >= 2:
            color_sec = color1 if secondary_index == 1 else color2
            if color_sec != bg:
                place_group(g_out, start_row, h, groups[1][1], groups[1][2], color_sec, bg, n)
            color_ter = color2 if secondary_index == 1 else color1
            if color_ter != bg:
                last_start = groups[1][1]
                last_w = groups[1][2]
                third_start_c = last_start + last_w + s_gap
                third_w = w
                if third_start_c + third_w <= n:
                    place_group(g_out, start_row, h, third_start_c, third_w, color_ter, bg, n)
    return g_out
```