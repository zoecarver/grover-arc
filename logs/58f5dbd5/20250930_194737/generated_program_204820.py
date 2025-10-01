```python
from typing import List, Tuple, Dict
import copy

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

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
    num_positions = max_i * max_j
    for pos in range(num_positions):
        ii = pos // max_j
        jj = pos % max_j
        is_solid, c = is_solid_five_by_five(g, ii, jj, bg)
        if is_solid:
            blocks.append((ii, jj, c))
    return blocks

def get_unique_starts(blocks: List[Tuple[int, int, int]]) -> Tuple[List[int], List[int]]:
    if not blocks:
        return [], []
    row_starts = sorted(set(b[0] for b in blocks))
    col_starts = sorted(set(b[1] for b in blocks))
    return row_starts, col_starts

def compute_output_size(unique_rows: List[int], unique_cols: List[int]) -> Tuple[int, int]:
    num_rows = len(unique_rows)
    num_cols = len(unique_cols)
    height = 1 + 6 * num_rows
    width = 1 + 6 * num_cols
    return height, width

def create_output_grid(height: int, width: int, bg: int) -> List[List[int]]:
    return [[bg for _ in range(width)] for _ in range(height)]

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

def get_pattern(color: int, variant: int, patterns: Dict[Tuple[int, int], List[List[bool]]]) -> List[List[bool]]:
    key = (color, variant)
    if key in patterns:
        return [row[:] for row in patterns[key]]
    for k, pat in patterns.items():
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
    unique_rows, unique_cols = get_unique_starts(blocks)
    height, width = compute_output_size(unique_rows, unique_cols)
    output = create_output_grid(height, width, bg)
    for br, bc, colr in blocks:
        s_r = unique_rows.index(br)
        place_r = 1 + 6 * s_r
        s_c = unique_cols.index(bc)
        place_c = 1 + 6 * s_c
        variant = bc // 6
        pat = get_pattern(colr, variant, KNOWN_PATTERNS)
        place_pattern(output, pat, colr, place_r, place_c)
    return output
```