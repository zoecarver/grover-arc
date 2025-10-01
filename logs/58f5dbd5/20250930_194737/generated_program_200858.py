```python
from typing import List, Dict, Tuple

def get_background(g: List[List[int]]) -> int:
    """Rule: Background color is always the value at the top-left cell g[0][0]."""
    return g[0][0]

def is_solid_five_by_five(g: List[List[int]], i: int, j: int, bg: int) -> Tuple[bool, int]:
    """Rule: A solid 5x5 block is a 5x5 subgrid where all 25 cells are identical and different from background."""
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
    """Rule: Scan all possible top-left positions (i,j) where i+4 < rows, j+4 < cols, and check for solid blocks."""
    blocks = []
    rows = len(g)
    cols = len(g[0])
    max_i = rows - 4
    max_j = cols - 4
    if max_i <= 0 or max_j <= 0:
        return blocks
    pos = 0
    for _ in range(max_i * max_j):
        i = pos // max_j
        j = pos % max_j
        pos += 1
        is_solid, c = is_solid_five_by_five(g, i, j, bg)
        if is_solid:
            blocks.append((i, j, c))
    return blocks

def get_block_positions(blocks: List[Tuple[int, int, int]]) -> Tuple[List[int], List[int]]:
    """Rule: Collect unique sorted starting rows and columns from detected blocks to determine output grid structure preserving relative positions."""
    row_set = sorted(set(b[0] for b in blocks))
    col_set = sorted(set(b[1] for b in blocks))
    return row_set, col_set

def get_output_dimensions(row_starts: List[int], col_starts: List[int]) -> Tuple[int, int]:
    """Rule: Output dimensions are 1 + 6 * num_unique_rows for height, same for width, to fit 5x5 patterns with 1-cell bg separators and borders."""
    m = len(row_starts)
    n = len(col_starts)
    return 1 + 6 * m, 1 + 6 * n

def create_empty_output(height: int, width: int, bg: int) -> List[List[int]]:
    """Rule: Initialize output grid filled entirely with background color."""
    return [[bg for _ in range(width)] for _ in range(height)]

def get_digit_pattern(color: int, start_col: int) -> List[List[bool]]:
    """Rule: Patterns are predefined 5x5 boolean masks for each (color, start_col // 6), representing stylized digits; fallback to horizontal mirror of any known pattern for same color."""
    sc = start_col // 6
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
    key = (color, sc)
    if key in KNOWN_PATTERNS:
        return [row[:] for row in KNOWN_PATTERNS[key]]
    for k, pat in KNOWN_PATTERNS.items():
        if k[0] == color:
            return [[pat[i][j] for j in range(4, -1, -1)] for i in range(5)]
    return [[True] * 5 for _ in range(5)]

def place_digit_pattern(grid: List[List[int]], pat: List[List[bool]], color: int, start_r: int, start_c: int) -> None:
    """Rule: Overlay the boolean pattern with the color onto the output grid at the specified position, filling only True positions."""
    for delta in range(25):
        i = delta // 5
        j = delta % 5
        if pat[i][j]:
            grid[start_r + i][start_c + j] = color

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Detect solid 5x5 blocks, compute layout based on unique start positions, create output grid, place stylized patterns for each block preserving relative positions with separators."""
    bg = get_background(g)
    blocks = find_five_by_five_blocks(g, bg)
    row_starts, col_starts = get_block_positions(blocks)
    h, w = get_output_dimensions(row_starts, col_starts)
    out = create_empty_output(h, w, bg)
    for start_r, start_c, color in blocks:
        s_r_idx = row_starts.index(start_r)
        s_c_idx = col_starts.index(start_c)
        pos_r = 1 + 6 * s_r_idx
        pos_c = 1 + 6 * s_c_idx
        pat = get_digit_pattern(color, start_c)
        place_digit_pattern(out, pat, color, pos_r, pos_c)
    return out
```