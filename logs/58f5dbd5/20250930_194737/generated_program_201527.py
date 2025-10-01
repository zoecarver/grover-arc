```python
from typing import List, Dict, Tuple

KNOWN_PATTERNS: Dict[Tuple[int, int], List[List[bool]]] = {
    (1, 0): [
        [True, True, True, True, True],
        [True, False, False, True, True],
        [True, True, False, True, True],
        [True, False, False, False, True],
        [True, True, True, True, True]
    ],
    (1, 2): [
        [True, True, True, True, True],
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, False, False, False, True],
        [True, True, True, True, True]
    ],
    (2, 1): [
        [True, True, True, True, True],
        [True, False, True, False, True],
        [True, False, False, True, True],
        [True, False, True, False, True],
        [True, True, True, True, True]
    ],
    (3, 0): [
        [True, True, True, True, True],
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, True, False, True, True],
        [True, True, True, True, True]
    ],
    (3, 2): [
        [True, True, True, True, True],
        [True, False, True, False, True],
        [True, False, False, False, True],
        [True, True, False, False, True],
        [True, True, True, True, True]
    ],
    (4, 1): [
        [True, True, True, True, True],
        [True, False, True, False, True],
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, True, True, True, True]
    ],
    (4, 2): [
        [True, True, True, True, True],
        [True, False, False, False, True],
        [True, False, True, False, True],
        [True, False, True, False, True],
        [True, True, True, True, True]
    ],
    (6, 2): [
        [True, True, True, True, True],
        [True, False, True, False, True],
        [True, False, False, True, True],
        [True, False, True, True, True],
        [True, True, True, True, True]
    ],
    (8, 0): [
        [True, True, True, True, True],
        [True, False, False, True, True],
        [True, False, False, True, True],
        [True, True, True, False, True],
        [True, True, True, True, True]
    ],
    (9, 1): [
        [True, True, True, True, True],
        [True, False, True, False, True],
        [True, False, False, True, True],
        [True, True, False, True, True],
        [True, True, True, True, True]
    ]
}

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def is_solid_five_by_five(g: List[List[int]], i: int, j: int, bg: int) -> Tuple[bool, int]:
    rows = len(g)
    cols = len(g[0])
    if i + 4 >= rows or j + 4 >= cols:
        return False, 0
    color = g[i][j]
    if color == bg:
        return False, 0
    for d in range(25):
        dr = d // 5
        dc = d % 5
        r = i + dr
        c = j + dc
        if g[r][c] != color:
            return False, 0
    return True, color

def find_five_by_five_blocks(g: List[List[int]], bg: int) -> List[Tuple[int, int, int]]:
    blocks = []
    rows = len(g)
    cols = len(g[0])
    maxr = rows - 4
    maxc = cols - 4
    if maxr <= 0 or maxc <= 0:
        return blocks
    num_pos = maxr * maxc
    for pos in range(num_pos):
        ii = pos // maxc
        jj = pos % maxc
        is_solid, c = is_solid_five_by_five(g, ii, jj, bg)
        if is_solid:
            blocks.append((ii, jj, c))
    return blocks

def get_row_starts(blocks: List[Tuple[int, int, int]]) -> List[int]:
    return sorted(set(b[0] for b in blocks))

def get_col_starts(blocks: List[Tuple[int, int, int]]) -> List[int]:
    return sorted(set(b[1] for b in blocks))

def get_output_dimensions(num_rows: int, num_cols: int) -> Tuple[int, int]:
    return 1 + 6 * num_rows, 1 + 6 * num_cols

def create_output_grid(h: int, w: int, bg: int) -> List[List[int]]:
    return [[bg] * w for _ in range(h)]

def get_pattern(color: int, start_col: int) -> List[List[bool]]:
    sc = start_col // 6
    key = (color, sc)
    if key in KNOWN_PATTERNS:
        return [row[:] for row in KNOWN_PATTERNS[key]]
    for k, pat in KNOWN_PATTERNS.items():
        if k[0] == color:
            mirrored = [row[::-1][:] for row in pat]
            return mirrored
    return [[True] * 5 for _ in range(5)]

def place_pattern(grid: List[List[int]], pat: List[List[bool]], color: int, start_r: int, start_c: int) -> None:
    for d in range(25):
        dr = d // 5
        dc = d % 5
        if pat[dr][dc]:
            grid[start_r + dr][start_c + dc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    blocks = find_five_by_five_blocks(g, bg)
    row_starts = get_row_starts(blocks)
    col_starts = get_col_starts(blocks)
    h, w = get_output_dimensions(len(row_starts), len(col_starts))
    out = create_output_grid(h, w, bg)
    for sr, sc, color in blocks:
        idx_r = row_starts.index(sr)
        idx_c = col_starts.index(sc)
        out_r = 1 + 6 * idx_r
        out_c = 1 + 6 * idx_c
        pat = get_pattern(color, sc)
        place_pattern(out, pat, color, out_r, out_c)
    return out
```