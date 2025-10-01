```python
from typing import List, Tuple
from collections import Counter
import itertools

def find_background(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    flat = [cell for row in grid for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_positions(grid: List[List[int]], color: int) -> List[Tuple[int, int]]:
    positions = []
    rows = len(grid)
    if rows == 0:
        return positions
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == color:
                positions.append((r, c))
    return positions

def is_aligned(p1: Tuple[int, int], p2: Tuple[int, int]) -> bool:
    r1, c1 = p1
    r2, c2 = p2
    dr = abs(r1 - r2)
    dc = abs(c1 - c2)
    return dr == dc and dr > 0

def fill_perp_line(out: List[List[int]], pos: Tuple[int, int], perp_sdc: int, rows: int, cols: int, bg: int, color: int):
    r, c = pos
    # Direction 1: +row, +perp_sdc col
    cr, cc = r, c
    while 0 <= cr < rows and 0 <= cc < cols:
        if out[cr][cc] == bg:
            out[cr][cc] = color
        cr += 1
        cc += perp_sdc
    # Direction 2: -row, -perp_sdc col
    cr, cc = r, c
    while 0 <= cr < rows and 0 <= cc < cols:
        if out[cr][cc] == bg:
            out[cr][cc] = color
        cr -= 1
        cc -= perp_sdc

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    bg = find_background(g)
    out = [row[:] for row in g]
    ones = find_positions(g, 1)
    hit_to_dir = {}
    for p1, p2 in itertools.combinations(ones, 2):
        if not is_aligned(p1, p2):
            continue
        # Ensure p1 has smaller row
        if p1[0] > p2[0]:
            p1, p2 = p2, p1
        r1, c1 = p1
        r2, c2 = p2
        steps = r2 - r1
        sdc = 1 if c2 > c1 else -1
        cr = r1
        cc = c1
        for i in range(steps + 1):
            if out[cr][cc] == bg:
                out[cr][cc] = 1
            if out[cr][cc] == 6:
                hit_to_dir[(cr, cc)] = (1, sdc)
            if i < steps:
                cr += 1
                cc += sdc
    # Extend hit 6's perpendicular
    for pos, (sdr, sdc) in hit_to_dir.items():
        perp_sdc = -sdc
        fill_perp_line(out, pos, perp_sdc, rows, cols, bg, 6)
    return out
```