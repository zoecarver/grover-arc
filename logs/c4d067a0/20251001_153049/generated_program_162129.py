```python
from typing import List, Tuple
import copy

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
        for j in range(len(left_cols)):
            c = left_cols[j]
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
    h = max_r - min_r + 1 if max_r >= 0 else 0
    start_s = min_r
    if h == 0:
        return start_s, h, 7, 0, 1, [], 0
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
    m_ = len(groups)
    w = groups[0][2] if m_ > 0 else 0
    s_gap_ = groups[1][1] - groups[0][1] - groups[0][2] if m_ > 1 else 1
    first_start_ = groups[0][1] if m_ > 0 else 7
    return start_s, h, first_start_, w, s_gap_, groups, m_

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
    for rr in range(start_r, min(start_r + h, n)):
        for cc in range(start_c, min(start_c + width, n)):
            if g_out[rr][cc] == bg:
                g_out[rr][cc] = color

def compute_start_row(skipped_i: int, i: int, start_s: int, h: int, s_gap: int, m_list: List[int], first_three: int, k: int) -> int:
    if i == skipped_i:
        return start_s
    base_step = h + s_gap
    if first_three is None:
        is_special = lambda jj: False
    else:
        is_special = lambda jj: (jj + 1 == first_three)
    if i > skipped_i:
        cum = 0
        for jj in range(skipped_i, i):
            step = base_step + (1 if is_special(jj) else 0)
            cum += step
        return start_s + cum
    else:
        cum = 0
        for jj in range(i, skipped_i):
            step = base_step + (1 if is_special(jj) else 0)
            cum += step
        return start_s - cum

def place_for_i(g_out: List[List[int]], i: int, start_r: int, h: int, sequence: List[List[int]], bg: int, n: int,
                second_channel: int, first_start: int, w: int, s_gap: int, groups: List[Tuple[int, int, int]], m: int):
    if start_r < 0 or start_r + h > n:
        return
    colr0 = sequence[0][i]
    if colr0 == bg:
        return
    c = first_start
    wid = w
    place_group(g_out, start_r, h, c, wid, colr0, bg, n)
    last_c = c + wid
    last_wid = wid
    if second_channel == 2:
        colr1 = sequence[1][i]
        if colr1 != bg:
            if m >= 2:
                c = groups[1][1]
                wid = groups[1][2]
            else:
                c = last_c + s_gap
                wid = w
            place_group(g_out, start_r, h, c, wid, colr1, bg, n)
            last_c = c + wid
            last_wid = wid
        colr2 = sequence[2][i]
        if colr2 != bg:
            c = last_c + s_gap
            wid = w
            place_group(g_out, start_r, h, c, wid, colr2, bg, n)
    else:
        colr2 = sequence[2][i]
        placed_second = False
        if colr2 != bg:
            if m >= 2:
                c = groups[1][1]
                wid = groups[1][2]
            else:
                c = last_c + s_gap
                wid = w
            place_group(g_out, start_r, h, c, wid, colr2, bg, n)
            last_c = c + wid
            last_wid = wid
            placed_second = True
        colr1 = sequence[1][i]
        if colr1 != bg:
            if placed_second:
                c = last_c + s_gap
                wid = w
            else:
                if m >= 2:
                    c = groups[1][1]
                    wid = groups[1][2]
                else:
                    c = last_c + s_gap
                    wid = w
            place_group(g_out, start_r, h, c, wid, colr1, bg, n)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = get_background(g)
    instr_rows = get_instruction_rows(g, bg, n)
    k = len(instr_rows)
    if k == 0:
        return [row[:] for row in g]
    left_cols = [1, 3, 5]
    sequence = get_sequence(g, bg, instr_rows, left_cols, k, n)
    slot_info = get_existing_slot(g, bg, n)
    start_s, h, first_start, w, s_gap, groups, m = slot_info
    if h == 0 or m == 0:
        return [row[:] for row in g]
    skipped_i, second_channel = find_stage(sequence, groups, m, k, bg)
    m_list = [sum(1 for j in range(3) if sequence[j][ii] != bg) for ii in range(k)]
    first_three = next((ii for ii in range(k) if m_list[ii] == 3), None)
    g_out = [row[:] for row in g]
    for i in range(k):
        start_r = compute_start_row(skipped_i, i, start_s, h, s_gap, m_list, first_three, k)
        place_for_i(g_out, i, start_r, h, sequence, bg, n, second_channel, first_start, w, s_gap, groups, m)
    return g_out
```