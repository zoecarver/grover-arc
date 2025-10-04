```python
from typing import List

def transpose(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    return [list(col) for col in zip(*g)]

def get_separators(g: List[List[int]]) -> List[int]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    seps = []
    for c in range(w):
        if all(g[r][c] == 1 for r in range(h)):
            seps.append(c)
    return seps

def get_first_section_start_end(seps: List[int]) -> tuple:
    if not seps:
        return 0, 0
    return 0, seps[0]

def get_four_rows(g: List[List[int]], first_start: int, first_end: int) -> List[int]:
    h = len(g)
    four_rows = []
    s = first_end - first_start
    for r in range(h):
        has_four = False
        for c in range(first_start, first_end):
            if g[r][c] == 4:
                has_four = True
                break
        if has_four:
            four_rows.append(r)
    return four_rows

def get_block_colors(g: List[List[int]], h: int, seps: List[int]) -> tuple:
    if len(seps) < 3 or h == 0:
        return 0, 0
    block1_start = seps[1] + 1
    block1_end = seps[2]
    A = 0
    if block1_start < len(g[0]):
        A = g[0][block1_start]
    block2_start = seps[2] + 1
    B = 0
    if block2_start < len(g[0]):
        B = g[0][block2_start]
    return A, B

def build_unit(g: List[List[int]], r: int, first_start: int, s: int, A: int, B: int) -> List[int]:
    subrow = [g[r][first_start + jj] for jj in range(s)]
    unit = []
    for jj in range(1, s):
        val = subrow[jj]
        unit.append(A if val == 4 else B)
    return unit

def build_output_row(unit: List[int], h_out: int, u: int) -> List[int]:
    if u <= 0:
        return []
    full = h_out - 1
    row = unit * full
    prefix_len = u - 1
    row += unit[:prefix_len]
    return row

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    transposed = len(g) > len(g[0])
    if transposed:
        g = transpose(g)
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    seps = get_separators(g)
    first_start, first_end = get_first_section_start_end(seps)
    s = first_end - first_start
    u = s - 1
    four_rows = get_four_rows(g, first_start, first_end)
    h_out = len(four_rows)
    w_out = h_out * u - 1 if u > 0 else 0
    A, B = get_block_colors(g, h, seps)
    out_g = []
    for i in range(h_out):
        r = four_rows[i]
        unit = build_unit(g, r, first_start, s, A, B)
        row = build_output_row(unit, h_out, u)
        out_g.append(row)
    if transposed:
        out_g = transpose(out_g)
    return out_g
```