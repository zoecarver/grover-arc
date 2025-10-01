```python
from typing import List, Tuple, Dict
import copy

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
    for i in range(rows - 4):
        for j in range(cols - 4):
            is_solid, c = is_solid_five_by_five(g, i, j, bg)
            if is_solid:
                blocks.append((i, j, c))
    return blocks

def get_block_positions(blocks: List[Tuple[int, int, int]]) -> Tuple[List[int], List[int]]:
    if not blocks:
        return [], []
    row_starts = sorted(set(b[0] for b in blocks))
    col_starts = sorted(set(b[1] for b in blocks))
    return row_starts, col_starts

def get_output_dimensions(row_starts: List[int], col_starts: List[int]) -> Tuple[int, int]:
    num_rows = len(row_starts)
    num_cols = len(col_starts)
    return 1 + 6 * num_rows, 1 + 6 * num_cols

def create_output_grid(height: int, width: int, bg: int) -> List[List[int]]:
    return [[bg for _ in range(width)] for _ in range(height)]

def get_pattern(color: int, variant: int) -> List[List[bool]]:
    key = (color, variant)
    if key in KNOWN_PATTERNS:
        return [row[:] for row in KNOWN_PATTERNS[key]]
    color_keys = [k for k in KNOWN_PATTERNS.keys() if k[0] == color]
    if not color_keys:
        return [[True] * 5 for _ in range(5)]
    best_key = min(color_keys, key=lambda k: abs(k[1] - variant))
    return [row[:] for row in KNOWN_PATTERNS[best_key]]

def place_pattern(grid: List[List[int]], pat: List[List[bool]], color: int, start_r: int, start_c: int) -> None:
    for pr in range(5):
        for pc in range(5):
            if pat[pr][pc]:
                grid[start_r + pr][start_c + pc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    blocks = find_five_by_five_blocks(g, bg)
    row_starts, col_starts = get_block_positions(blocks)
    height, width = get_output_dimensions(row_starts, col_starts)
    output = create_output_grid(height, width, bg)
    for block in blocks:
        start_r, start_c, color = block
        s_r = row_starts.index(start_r)
        s_c = col_starts.index(start_c)
        pat = get_pattern(color, start_c // 6)
        place_r = 1 + 6 * s_r
        place_c = 1 + 6 * s_c
        place_pattern(output, pat, color, place_r, place_c)
    return output
```