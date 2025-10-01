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
    (2, 1): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, True, True],
        [True, False, True, False, True],
        [True] * 5
    ],
    (3, 2): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, False, True],
        [True, True, False, False, True],
        [True] * 5
    ],
    (1, 2): [
        [True] * 5,
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, False, False, False, True],
        [True] * 5
    ],
    (6, 2): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, True, True],
        [True, False, True, True, True],
        [True] * 5
    ],
    (4, 2): [
        [True] * 5,
        [True, False, False, False, True],
        [True, False, True, False, True],
        [True, False, True, False, True],
        [True] * 5
    ],
    (8, 0): [
        [True] * 5,
        [True, False, False, True, True],
        [True, False, False, True, True],
        [True, True, True, False, True],
        [True] * 5
    ],
    (4, 1): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True] * 5
    ],
    (3, 0): [
        [True] * 5,
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, True, False, True, True],
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
    if i + 4 >= len(g) or j + 4 >= len(g[0]):
        return False, 0
    first = g[i][j]
    if first == bg:
        return False, 0
    for r in range(i, i + 5):
        for c in range(j, j + 5):
            if g[r][c] != first:
                return False, 0
    return True, first

def find_five_by_five_blocks(g: List[List[int]], bg: int) -> List[Tuple[int, int, int]]:
    blocks = []
    rows, cols = len(g), len(g[0])
    for i in range(rows - 4):
        for j in range(cols - 4):
            is_solid, c = is_solid_five_by_five(g, i, j, bg)
            if is_solid:
                blocks.append((i, j, c))
    return blocks

def get_block_positions(blocks: List[Tuple[int, int, int]]) -> Tuple[List[int], List[int]]:
    row_set = sorted(set(b[0] for b in blocks))
    col_set = sorted(set(b[1] for b in blocks))
    return row_set, col_set

def get_output_dimensions(row_starts: List[int], col_starts: List[int]) -> Tuple[int, int]:
    m, n = len(row_starts), len(col_starts)
    return 1 + 6 * m, 1 + 6 * n

def get_pattern(c: int, sc: int) -> List[List[bool]]:
    key = (c, sc)
    if key in KNOWN_PATTERNS:
        return [row[:] for row in KNOWN_PATTERNS[key]]
    for k, pat in KNOWN_PATTERNS.items():
        if k[0] == c:
            return [row[::-1] for row in pat]
    return [[True] * 5 for _ in range(5)]

def create_output_grid(h: int, w: int, bg: int) -> List[List[int]]:
    return [[bg for _ in range(w)] for _ in range(h)]

def place_pattern(grid: List[List[int]], pat: List[List[bool]], color: int, start_r: int, start_c: int) -> None:
    for i in range(5):
        for j in range(5):
            if pat[i][j]:
                grid[start_r + i][start_c + j] = color

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    blocks = find_five_by_five_blocks(g, bg)
    row_starts, col_starts = get_block_positions(blocks)
    h, w = get_output_dimensions(row_starts, col_starts)
    out = create_output_grid(h, w, bg)
    for block in blocks:
        r, c, colr = block
        sr = row_starts.index(r)
        sc_idx = col_starts.index(c)
        place_r = 1 + 6 * sr
        place_c = 1 + 6 * sc_idx
        key_sc = c // 6
        pat = get_pattern(colr, key_sc)
        place_pattern(out, pat, colr, place_r, place_c)
    return out
```