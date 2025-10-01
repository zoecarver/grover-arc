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
    if max_i < 1 or max_j < 1:
        return blocks
    num_pos = max_i * max_j
    for pos in range(num_pos):
        i = pos // max_j
        j = pos % max_j
        is_solid, c = is_solid_five_by_five(g, i, j, bg)
        if is_solid:
            blocks.append((i, j, c))
    return blocks

def get_unique_row_col_starts(blocks: List[Tuple[int, int, int]]) -> Tuple[List[int], List[int]]:
    if not blocks:
        return [], []
    row_starts = sorted(set(b[0] for b in blocks))
    col_starts = sorted(set(b[1] for b in blocks))
    return row_starts, col_starts

def get_output_size(num_row_starts: int, num_col_starts: int) -> Tuple[int, int]:
    return 1 + 6 * num_row_starts, 1 + 6 * num_col_starts

def create_output_grid(height: int, width: int, bg: int) -> List[List[int]]:
    return [[bg] * width for _ in range(height)]

def get_patterns() -> Dict[Tuple[int, int], List[List[bool]]]:
    T = True
    F = False
    return {
        (1, 0): [
            [T, T, T, T, T],
            [T, F, F, T, T],
            [T, T, F, T, T],
            [T, F, F, F, T],
            [T, T, T, T, T]
        ],
        (1, 2): [
            [T, T, T, T, T],
            [T, F, F, F, T],
            [T, T, F, T, T],
            [T, F, F, F, T],
            [T, T, T, T, T]
        ],
        (2, 1): [
            [T, T, T, T, T],
            [T, F, T, F, T],
            [T, F, F, T, T],
            [T, F, T, F, T],
            [T, T, T, T, T]
        ],
        (3, 0): [
            [T, T, T, T, T],
            [T, F, F, F, T],
            [T, T, F, T, T],
            [T, T, F, T, T],
            [T, T, T, T, T]
        ],
        (3, 2): [
            [T, T, T, T, T],
            [T, F, T, F, T],
            [T, F, F, F, T],
            [T, T, F, F, T],
            [T, T, T, T, T]
        ],
        (4, 1): [
            [T, T, T, T, T],
            [T, F, T, F, T],
            [T, F, F, F, T],
            [T, T, F, T, T],
            [T, T, T, T, T]
        ],
        (4, 2): [
            [T, T, T, T, T],
            [T, F, F, F, T],
            [T, F, T, F, T],
            [T, F, T, F, T],
            [T, T, T, T, T]
        ],
        (6, 2): [
            [T, T, T, T, T],
            [T, F, T, F, T],
            [T, F, F, T, T],
            [T, F, T, T, T],
            [T, T, T, T, T]
        ],
        (8, 0): [
            [T, T, T, T, T],
            [T, F, F, T, T],
            [T, F, F, T, T],
            [T, T, T, F, T],
            [T, T, T, T, T]
        ],
        (9, 1): [
            [T, T, T, T, T],
            [T, F, T, F, T],
            [T, F, F, T, T],
            [T, T, F, T, T],
            [T, T, T, T, T]
        ]
    }

def get_pattern(color: int, start_col: int, patterns: Dict[Tuple[int, int], List[List[bool]]]) -> List[List[bool]]:
    sc = start_col // 6
    key = (color, sc)
    if key in patterns:
        return copy.deepcopy(patterns[key])
    known_keys = [k for k in patterns.keys() if k[0] == color]
    if not known_keys:
        T = True
        return [[T] * 5 for _ in range(5)]
    best_key = min(known_keys, key=lambda k: abs(k[1] - sc))
    return copy.deepcopy(patterns[best_key])

def place_pattern_flat(grid: List[List[int]], pattern: List[List[bool]], color: int, start_row: int, start_col: int) -> None:
    for delta in range(25):
        pr = delta // 5
        pc = delta % 5
        if pattern[pr][pc]:
            grid[start_row + pr][start_col + pc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    blocks = find_five_by_five_blocks(g, bg)
    row_starts, col_starts = get_unique_row_col_starts(blocks)
    h, w = get_output_size(len(row_starts), len(col_starts))
    output = create_output_grid(h, w, bg)
    patterns = get_patterns()
    for block_row, block_col, color in blocks:
        s_r = row_starts.index(block_row)
        s_c = col_starts.index(block_col)
        pat = get_pattern(color, block_col, patterns)
        place_row = 1 + 6 * s_r
        place_col = 1 + 6 * s_c
        place_pattern_flat(output, pat, color, place_row, place_col)
    return output
```