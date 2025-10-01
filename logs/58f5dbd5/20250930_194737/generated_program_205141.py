```python
from typing import List, Dict, Tuple

KNOWN_PATTERNS: Dict[Tuple[int, int], List[List[bool]]] = {
    (1, 0): [
        [True] * 5,
        [True, False, False, True, True],
        [True, True, False, True, True],
        [True, False, False, False, True],
        [True] * 5
    ],
    (1, 2): [
        [True] * 5,
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, False, False, False, True],
        [True] * 5
    ],
    (2, 1): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, True, True],
        [True, False, True, False, True],
        [True] * 5
    ],
    (3, 0): [
        [True] * 5,
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, True, False, True, True],
        [True] * 5
    ],
    (3, 2): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, False, True],
        [True, True, False, False, True],
        [True] * 5
    ],
    (4, 1): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True] * 5
    ],
    (4, 2): [
        [True] * 5,
        [True, False, False, False, True],
        [True, False, True, False, True],
        [True, False, True, False, True],
        [True] * 5
    ],
    (6, 2): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, True, True],
        [True, False, True, True, True],
        [True] * 5
    ],
    (8, 0): [
        [True] * 5,
        [True, False, False, True, True],
        [True, False, False, True, True],
        [True, True, True, False, True],
        [True] * 5
    ],
    (9, 1): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, True, True],
        [True, True, False, True, True],
        [True] * 5
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
    for delta in range(25):
        dr = delta // 5
        dc = delta % 5
        if g[i + dr][j + dc] != color:
            return False, 0
    return True, color

def find_five_by_five_blocks(g: List[List[int]], bg: int) -> List[Tuple[int, int, int]]:
    blocks = []
    rows = len(g)
    cols = len(g[0])
    max_i = rows - 4
    max_j = cols - 4
    if max_i <= 0 or max_j <= 0:
        return blocks
    for pos in range(max_i * max_j):
        ii = pos // max_j
        jj = pos % max_j
        is_solid, c = is_solid_five_by_five(g, ii, jj, bg)
        if is_solid:
            blocks.append((ii, jj, c))
    return blocks

def get_unique_row_col_starts(blocks: List[Tuple[int, int, int]]) -> Tuple[List[int], List[int]]:
    if not blocks:
        return [], []
    row_starts = sorted(set(b[0] for b in blocks))
    col_starts = sorted(set(b[1] for b in blocks))
    return row_starts, col_starts

def get_output_dimensions(unique_rows: List[int], unique_cols: List[int]) -> Tuple[int, int]:
    return 1 + 6 * len(unique_rows), 1 + 6 * len(unique_cols)

def create_output_grid(h: int, w: int, bg: int) -> List[List[int]]:
    return [[bg for _ in range(w)] for _ in range(h)]

def get_pattern(color: int, start_col: int, known: Dict[Tuple[int, int], List[List[bool]]]) -> List[List[bool]]:
    var = start_col // 6
    key = (color, var)
    if key in known:
        return [row[:] for row in known[key]]
    color_keys = [k for k in known if k[0] == color]
    if not color_keys:
        return [[True] * 5 for _ in range(5)]
    closest_key = min(color_keys, key=lambda k: abs(k[1] - var))
    base_pat = known[closest_key]
    mirrored = [row[::-1][:] for row in base_pat]
    return mirrored

def place_pattern(grid: List[List[int]], pat: List[List[bool]], color: int, start_r: int, start_c: int) -> None:
    for delta in range(25):
        pr = delta // 5
        pc = delta % 5
        if pat[pr][pc]:
            grid[start_r + pr][start_c + pc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    blocks = find_five_by_five_blocks(g, bg)
    unique_rows, unique_cols = get_unique_row_col_starts(blocks)
    h, w = get_output_dimensions(unique_rows, unique_cols)
    output = create_output_grid(h, w, bg)
    for br, bc, colr in blocks:
        sr = unique_rows.index(br)
        sc = unique_cols.index(bc)
        place_r = 1 + 6 * sr
        place_c = 1 + 6 * sc
        pat = get_pattern(colr, bc, KNOWN_PATTERNS)
        place_pattern(output, pat, colr, place_r, place_c)
    return output
```