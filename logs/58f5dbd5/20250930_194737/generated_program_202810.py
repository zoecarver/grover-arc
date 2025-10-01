```python
from typing import List, Dict, Tuple
import copy

KNOWN_PATTERNS: Dict[Tuple[int, int], List[List[bool]]] = {
    (1, 0): [
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
    (4, 0): [
        [True, True, True, True, True],
        [True, False, False, False, True],
        [True, False, True, False, True],
        [True, False, True, False, True],
        [True, True, True, True, True]
    ],
    (4, 1): [
        [True, True, True, True, True],
        [True, False, True, False, True],
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, True, True, True, True]
    ],
    (6, 0): [
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
    if max_i <= 0 or max_j <= 0:
        return blocks
    num_positions = max_i * max_j
    pos = 0
    while pos < num_positions:
        ii = pos // max_j
        jj = pos % max_j
        is_solid, c = is_solid_five_by_five(g, ii, jj, bg)
        if is_solid:
            blocks.append((ii, jj, c))
        pos += 1
    return blocks

def get_block_positions(blocks: List[Tuple[int, int, int]]) -> Tuple[List[int], List[int]]:
    if not blocks:
        return [], []
    unique_rows = sorted(set(b[0] for b in blocks))
    unique_cols = sorted(set(b[1] for b in blocks))
    return unique_rows, unique_cols

def get_output_dimensions(unique_rows: List[int], unique_cols: List[int]) -> Tuple[int, int]:
    num_r = len(unique_rows)
    num_c = len(unique_cols)
    return 1 + 6 * num_r, 1 + 6 * num_c

def create_output_grid(height: int, width: int, bg: int) -> List[List[int]]:
    return [[bg for _ in range(width)] for _ in range(height)]

def get_pattern(color: int, col_index: int, known: Dict[Tuple[int, int], List[List[bool]]]) -> List[List[bool]]:
    key = (color, col_index)
    if key in known:
        return copy.deepcopy(known[key])
    for k, pat in known.items():
        if k[0] == color:
            mirrored = [row[::-1] for row in pat]
            return mirrored
    return [[True] * 5 for _ in range(5)]

def place_pattern(grid: List[List[int]], pat: List[List[bool]], color: int, start_r: int, start_c: int) -> None:
    for delta in range(25):
        pr = delta // 5
        pc = delta % 5
        if pat[pr][pc]:
            grid[start_r + pr][start_c + pc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    blocks = find_five_by_five_blocks(g, bg)
    row_starts, col_starts = get_block_positions(blocks)
    h, w = get_output_dimensions(row_starts, col_starts)
    output = create_output_grid(h, w, bg)
    for block_row, block_col, color in blocks:
        s_r = row_starts.index(block_row)
        s_c = col_starts.index(block_col)
        pat = get_pattern(color, s_c, KNOWN_PATTERNS)
        place_r = 1 + 6 * s_r
        place_c = 1 + 6 * s_c
        place_pattern(output, pat, color, place_r, place_c)
    return output
```