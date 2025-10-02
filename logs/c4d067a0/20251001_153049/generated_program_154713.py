```python
from typing import List

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

def get_sequence(g: List[List[int]], bg: int, instruction_rows: List[int], left_cols: List[int], k: int) -> List[List[int]]:
    sequence = [[] for _ in left_cols]
    for i in range(k):
        r = instruction_rows[i]
        for j in range(len(left_cols)):
            c = left_cols[j]
            if c < len(g[0]) and g[r][c] != bg:
                sequence[j].append(g[r][c])
    return sequence

def get_existing_slot(g: List[List[int]], bg: int, n: int) -> tuple:
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
    first_start = groups[0][1] if m > 0 else 0
    return start_s, h, first_start, w, s_gap, groups, m

def find_stage(sequence: List[List[int]], groups: List, m: int) -> tuple:
    if m == 0:
        return 1, 2
    first_color = groups[0][0]
    second_color = groups[1][0] if m > 1 else None
    for i in range(len(sequence[0])):
        if sequence[0][i] == first_color:
            match_j2 = m <= 1 or (len(sequence[1]) > i and sequence[1][i] == second_color)
            if match_j2:
                return i + 1, 2
            match_j3 = m <= 1 or (len(sequence[2]) > i and sequence[2][i] == second_color)
            if match_j3:
                return i + 1, 3
    return 1, 2

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = get_background(g)
    instruction_rows = get_instruction_rows(g, bg, n)
    k = len(instruction_rows)
    left_cols = [1, 3, 5]
    sequence = get_sequence(g, bg, instruction_rows, left_cols, k)
    start_s, h, first_start, w, s_gap, groups, m = get_existing_slot(g, bg, n)
    stage, second_j = find_stage(sequence, groups, m)
    out = [row[:] for row in g]
    step = h + 2
    for i in range(1, k + 1):
        if i == stage:
            continue
        start_row = start_s + (i - stage) * step
        if start_row < 0 or start_row + h > n:
            continue
        current_c = first_start
        for jj in range(m):
            j = 1 if jj == 0 else second_j
            color = bg
            seq = sequence[j - 1]
            if len(seq) > i - 1:
                color = seq[i - 1]
            if color != bg:
                for rr in range(start_row, start_row + h):
                    for cc in range(current_c, current_c + w):
                        if 0 <= rr < n and 0 <= cc < n:
                            out[rr][cc] = color
            current_c += w + s_gap
    return out
```