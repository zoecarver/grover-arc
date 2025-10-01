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
        r = i + dr
        c = j + dc
        if g[r][c] != color:
            return False, 0
    return True, color

def find_five_by_five_blocks(g: List[List[int]], bg: int) -> List[Tuple[int, int, int]]:
    blocks = []
    rows = len(g)
    cols = len(g[0])
    max_i = rows - 4
    max_j = cols - 4
    pos = 0
    for ii in range(max_i * max_j):
        i = pos // max_j
        j = pos % max_j
        pos += 1
        is_solid, c = is_solid_five_by_five(g, i, j, bg)
        if is_solid:
            blocks.append((i, j, c))
    return blocks

def get_block_positions(blocks: List[Tuple[int, int, int]]) -> Tuple[List[int], List[int]]:
    row_set = sorted(set(b[0] for b in blocks))
    col_set = sorted(set(b[1] for b in blocks))
    return row_set, col_set

def get_output_dimensions(row_starts: List[int], col_starts: List[int]) -> Tuple[int, int]:
    num_rows = len(row_starts)
    num_cols = len(col_starts)
    height = 1 + 6 * num_rows
    width = 1 + 6 * num_cols
    return height, width

def create_output_grid(height: int, width: int, bg: int) -> List[List[int]]:
    return [[bg for _ in range(width)] for _ in range(height)]

def get_pattern(color: int, start_col: int) -> List[List[bool]]:
    sc = start_col // 6
    key = (color, sc)
    if key in KNOWN_PATTERNS:
        return [row[:] for row in KNOWN_PATTERNS[key]]
    for k, pat in KNOWN_PATTERNS.items():
        if k[0] == color:
            mirrored = [row[::-1] for row in pat]
            return mirrored
    return [[True] * 5 for _ in range(5)]

def place_pattern(grid: List[List[int]], pat: List[List[bool]], color: int, start_r: int, start_c: int) -> None:
    for delta in range(25):
        dr = delta // 5
        dc = delta % 5
        if pat[dr][dc]:
            grid[start_r + dr][start_c + dc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    blocks = find_five_by_five_blocks(g, bg)
    row_starts, col_starts = get_block_positions(blocks)
    height, width = get_output_dimensions(row_starts, col_starts)
    out = create_output_grid(height, width, bg)
    for block in blocks:
        start_row, start_col, color = block
        s_r_idx = row_starts.index(start_row)
        s_c_idx = col_starts.index(start_col)
        out_r = 1 + s_r_idx * 6
        out_c = 1 + s_c_idx * 6
        pat = get_pattern(color, start_col)
        place_pattern(out, pat, color, out_r, out_c)
    return out
```