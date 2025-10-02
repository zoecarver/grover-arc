```python
from typing import List

def transpose(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    return [list(row) for row in zip(*g)]

def extract_separators(g: List[List[int]]) -> List[int]:
    H = len(g)
    W = len(g[0]) if H > 0 else 0
    return [c for c in range(W) if all(g[r][c] == 1 for r in range(H))]

def get_four_pattern(g: List[List[int]], s1: int) -> List[List[int]]:
    H = len(g)
    wf = s1
    return [[g[r][c] for c in range(wf)] for r in range(H)]

def get_solid_color(g: List[List[int]], start_col: int) -> int:
    return g[0][start_col]

def compute_u(four_pattern: List[List[int]]) -> int:
    H = len(four_pattern)
    wf = len(four_pattern[0]) if H > 0 else 0
    max_consec = 0
    for r in range(H):
        curr = 0
        for c in range(wf):
            if four_pattern[r][c] == 4:
                curr += 1
                max_consec = max(max_consec, curr)
            else:
                curr = 0
    return max_consec + 1

def build_unit(four_pattern: List[List[int]], a_color: int, b_color: int, h_out: int, u: int, wf: int) -> List[List[int]]:
    unit = [[b_color] * u for _ in range(h_out)]
    for k in range(h_out):
        r = k + 1
        a_positions = set()
        for c in range(wf):
            if four_pattern[r][c] == 4:
                if wf > 1:
                    mapped = int(c / (wf - 1) * (u - 1))
                else:
                    mapped = 0
                if 0 <= mapped < u:
                    a_positions.add(mapped)
        for pos in a_positions:
            unit[k][pos] = a_color
    return unit

def build_output(unit: List[List[int]], h_out: int, u: int) -> List[List[int]]:
    out_grid = []
    for k in range(h_out):
        row = []
        for _ in range(h_out - 1):
            row.extend(unit[k])
        row.extend(unit[k][:u - 1])
        out_grid.append(row)
    return out_grid

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    H = len(g)
    W = len(g[0])
    transposed = H > W
    if transposed:
        g = transpose(g)
        H, W = W, H
    seps = extract_separators(g)
    if len(seps) != 3:
        return []
    s1, s2, s3 = seps
    four_p = get_four_pattern(g, s1)
    wf = s1
    starta = s2 + 1
    a_color = get_solid_color(g, starta)
    startb = s3 + 1
    b_color = get_solid_color(g, startb)
    h_out = H - 2
    if h_out <= 0:
        return []
    u = compute_u(four_p)
    unit = build_unit(four_p, a_color, b_color, h_out, u, wf)
    out = build_output(unit, h_out, u)
    if transposed:
        out = transpose(out)
    return out
```