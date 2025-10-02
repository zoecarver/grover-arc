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

def get_existing_slot(g: List[List[int]], bg: int, n: int) -> Tuple[int, int, int, int, int, int, List[Tuple[int, int, int]], int]:
    min_r = n
    max_r = -1
    for r in range(n):
        has_non_bg = any(g[r][c] != bg for c in range(7, n))
        if has_non_bg:
            min_r = min(min_r, r)
            max_r = max(max_r, r)
    h_existing = max_r - min_r + 1 if max_r >= 0 else 0
    start_s = min_r
    if h_existing == 0:
        return min_r, max_r, h_existing, 7, 0, 1, [], 0
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
    return min_r, max_r, h_existing, first_start, w, s_gap, groups, m

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

def place_group(g_out: List[List[int]], start_r: int, h: int, start_c: int, width: int, color: int, bg: int, n: int):
    for rr in range(start_r, min(start_r + h, n)):
        for cc in range(start_c, min(start_c + width, n)):
            if g_out[rr][cc] == bg:
                g_out[rr][cc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    n = len(g)
    instr_rows = get_instruction_rows(g, bg, n)
    k = len(instr_rows)
    if k == 0:
        return [row[:] for row in g]
    sequence = []
    left_cols = [1, 3, 5]
    for i in range(k):
        row_seq = []
        for j in range(3):
            c = left_cols[j]
            col = g[instr_rows[i]][c] if c < n else bg
            row_seq.append(col)
        sequence.append(row_seq)
    min_r, max_r, h_existing, first_start, w, s_gap, groups, m = get_existing_slot(g, bg, n)
    if m == 0:
        return [row[:] for row in g]
    h_place = w
    step = w + s_gap
    stage, second_channel = find_stage(g, instr_rows, bg, n, groups, m)
    skipped_i = stage - 1
    g_out = [row[:] for row in g]
    partial_non_boundary = (h_existing < h_place) and (max_r < n - 1)
    partial_boundary = (max_r == n - 1)
    shift = 0
    if partial_non_boundary:
        shift = h_place - h_existing
    elif partial_boundary:
        shift = 1
    effective_start = min_r - shift
    def place_for_i(i_val: int, start_row_val: int):
        color1 = sequence[i_val][0]
        if color1 == bg:
            return
        place_group(g_out, start_row_val, h_place, first_start, w, color1, bg, n)
        if m >= 2:
            ch_second = second_channel - 1
            color2 = sequence[i_val][ch_second]
            if color2 != bg:
                start_c2 = groups[1][1]
                w2 = groups[1][2]
                place_group(g_out, start_row_val, h_place, start_c2, w2, color2, bg, n)
            ch_third = 3 - ch_second
            color3 = sequence[i_val][ch_third]
            if color3 != bg:
                start_c3 = groups[1][1] + groups[1][2] + s_gap
                w3 = w
                place_group(g_out, start_row_val, h_place, start_c3, w3, color3, bg, n)
    for i in range(k):
        if i == skipped_i:
            continue
        start_row = effective_start + (i - skipped_i) * step
        if start_row < 0 or start_row + h_place > n:
            continue
        place_for_i(i, start_row)
    if partial_boundary:
        start_row = effective_start
        place_for_i(skipped_i, start_row)
        sticking_start = effective_start + h_place
        for r in range(sticking_start, max_r + 1):
            if r >= n:
                break
            for grp in groups:
                sc = grp[1]
                ww = grp[2]
                for cc in range(sc, min(sc + ww, n)):
                    g_out[r][cc] = bg
    return g_out
```