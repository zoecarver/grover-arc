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

def get_sequence(g: List[List[int]], bg: int, instruction_rows: List[int], left_cols: List[int], k: int, n: int) -> List[List[int]]:
    sequence = [[] for _ in left_cols]
    for i in range(k):
        r = instruction_rows[i]
        for j, c in enumerate(left_cols):
            color = g[r][c] if c < n else bg
            sequence[j].append(color)
    return sequence

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
    if max_r < 0:
        return 0, 0, 7, 0, 1, [], 0
    h = max_r - min_r + 1
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
    first_start = groups[0][1] if m > 0 else 7
    w = groups[0][2] if m > 0 else 0
    s_gap = groups[1][1] - groups[0][1] - groups[0][2] if m > 1 else 1
    return start_s, h, first_start, w, s_gap, groups, m

def find_stage(sequence: List[List[int]], groups: List[Tuple[int, int, int]], m: int, k: int, bg: int) -> Tuple[int, int]:
    if m == 0:
        return 0, 2
    first_color = groups[0][0]
    for i in range(k):
        if sequence[0][i] == first_color:
            if m <= 1:
                return i, 2
            second_color = groups[1][0]
            if sequence[1][i] == second_color:
                return i, 2
            if sequence[2][i] == second_color:
                return i, 3
    return 0, 2

def place_group(g_out: List[List[int]], start_r: int, h: int, start_c: int, width: int, color: int, bg: int, n: int):
    end_r = min(n, start_r + h)
    end_c = min(n, start_c + width)
    for rr in range(max(0, start_r), end_r):
        for cc in range(max(0, start_c), end_c):
            if g_out[rr][cc] == bg:
                g_out[rr][cc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = get_background(g)
    instr_rows = get_instruction_rows(g, bg, n)
    k = len(instr_rows)
    left_cols = [1, 3, 5]
    sequence = get_sequence(g, bg, instr_rows, left_cols, k, n)
    start_s, h, first_start, w, s_gap, groups, m = get_existing_slot(g, bg, n)
    if h == 0 or m == 0:
        return [row[:] for row in g]
    skipped_i, second_channel = find_stage(sequence, groups, m, k, bg)
    step = h + s_gap
    g_out = [row[:] for row in g]
    sec_idx = 1 if second_channel == 2 else 2
    ter_idx = 2 if second_channel == 2 else 1
    for i in range(k):
        if i == skipped_i:
            continue
        start_r = start_s + (i - skipped_i) * step
        if start_r < 0 or start_r >= n:
            continue
        color0 = sequence[0][i]
        if color0 != bg:
            place_group(g_out, start_r, h, first_start, w, color0, bg, n)
        color_sec = sequence[sec_idx][i]
        if color_sec != bg:
            sec_start = first_start + w + s_gap
            place_group(g_out, start_r, h, sec_start, w, color_sec, bg, n)
        color_ter = sequence[ter_idx][i]
        if color_ter != bg:
            ter_start = sec_start + w + s_gap
            place_group(g_out, start_r, h, ter_start, w, color_ter, bg, n)
    return g_out
```