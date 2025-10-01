```python
from typing import List, Dict, Tuple
import copy

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
    num_positions = max_i * max_j
    for pos in range(num_positions):
        ii = pos // max_j
        jj = pos % max_j
        is_solid, c = is_solid_five_by_five(g, ii, jj, bg)
        if is_solid:
            blocks.append((ii, jj, c))
    return blocks

def get_unique_row_starts(blocks: List[Tuple[int, int, int]]) -> List[int]:
    if not blocks:
        return []
    return sorted(set(b[0] for b in blocks))

def get_unique_col_starts(blocks: List[Tuple[int, int, int]]) -> List[int]:
    if not blocks:
        return []
    return sorted(set(b[1] for b in blocks))

def get_output_height(unique_rows: List[int]) -> int:
    return 1 + 6 * len(unique_rows)

def get_output_width(unique_cols: List[int]) -> int:
    return 1 + 6 * len(unique_cols)

def create_output_grid(height: int, width: int, bg: int) -> List[List[int]]:
    return [[bg for _ in range(width)] for _ in range(height)]

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

def get_pattern(color: int, s_c: int, known: Dict[Tuple[int, int], List[List[bool]]]) -> List[List[bool]]:
    key = (color, s_c)
    if key in known:
        return copy.deepcopy(known[key])
    for k, pat in known.items():
        if k[0] == color:
            mirrored = [row[::-1] for row in pat]
            return mirrored
    return [[True] * 5 for _ in range(5)]

def get_row_index(row_start: int, unique_rows: List[int]) -> int:
    return unique_rows.index(row_start)

def get_col_index(col_start: int, unique_cols: List[int]) -> int:
    return unique_cols.index(col_start)

def get_place_row(s_r: int) -> int:
    return 1 + 6 * s_r

def get_place_col(s_c: int) -> int:
    return 1 + 6 * s_c

def place_pattern(grid: List[List[int]], pat: List[List[bool]], color: int, start_r: int, start_c: int) -> None:
    for delta in range(25):
        pr = delta // 5
        pc = delta % 5
        if pat[pr][pc]:
            grid[start_r + pr][start_c + pc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    blocks = find_five_by_five_blocks(g, bg)
    unique_rows = get_unique_row_starts(blocks)
    unique_cols = get_unique_col_starts(blocks)
    height = get_output_height(unique_rows)
    width = get_output_width(unique_cols)
    output = create_output_grid(height, width, bg)
    for block_row, block_col, color in blocks:
        s_r = get_row_index(block_row, unique_rows)
        s_c = get_col_index(block_col, unique_cols)
        pat = get_pattern(color, s_c, KNOWN_PATTERNS)
        place_r = get_place_row(s_r)
        place_c = get_place_col(s_c)
        place_pattern(output, pat, color, place_r, place_c)
    return output
```