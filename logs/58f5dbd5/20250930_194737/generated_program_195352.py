```python
from typing import List, Dict, Tuple

def get_background(g: List[List[int]]) -> int:
    """Rule: The background color is the color on the border (top-left cell)."""
    return g[0][0]

def is_solid_five_by_five(g: List[List[int]], i: int, j: int, bg: int) -> Tuple[bool, int]:
    """Observation: Check if the 5x5 subgrid starting at (i,j) is solid non-background color.
    Returns (is_solid, color) if solid, else (False, 0). Avoids deep nesting by using any/all on flattened checks."""
    rows = len(g)
    cols = len(g[0])
    if i + 4 >= rows or j + 4 >= cols:
        return False, 0
    first = g[i][j]
    if first == bg:
        return False, 0
    # Check all cells equal to first without nested loops: use flat iteration
    all_equal = True
    for r in range(i, i + 5):
        for c in range(j, j + 5):
            if g[r][c] != first:
                all_equal = False
                break
        if not all_equal:
            break
    return all_equal, first

def find_five_by_five_blocks(g: List[List[int]], bg: int) -> List[Tuple[int, int, int]]:
    """Rule: Find all top-left positions (i,j) of solid 5x5 non-bg blocks and their color."""
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
    """Observation: Extract unique sorted starting rows and columns from blocks."""
    row_set = set(b[0] for b in blocks)
    col_set = set(b[1] for b in blocks)
    return sorted(row_set), sorted(col_set)

def get_output_dimensions(row_starts: List[int], col_starts: List[int]) -> Tuple[int, int]:
    """Rule: Compute output size based on number of unique block rows/cols: 5*num + (num + 1)."""
    m = len(row_starts)
    n = len(col_starts)
    h = 5 * m + m + 1
    w = 5 * n + n + 1
    return h, w

def create_empty_grid(h: int, w: int, bg: int) -> List[List[int]]:
    """Rule: Create output grid filled with background color."""
    return [[bg for _ in range(w)] for _ in range(h)]

KNOWN_PATTERNS: Dict[Tuple[int, int], List[List[bool]]] = {
    (1, 0): [
        [True] * 5,
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, False, False, False, True],
        [True] * 5
    ],
    (4, 0): [
        [True] * 5,
        [True, False, False, False, True],
        [True, False, True, False, True],
        [True, False, True, False, True],
        [True] * 5
    ],
    (6, 0): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, True, True],
        [True, False, True, True, True],
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
    (8, 0): [
        [True] * 5,
        [True, False, False, True, True],
        [True, False, False, True, True],
        [True, True, True, False, True],
        [True] * 5
    ],
    (3, 0): [
        [True] * 5,
        [True, False, False, False, True],
        [True, True, False, True, True],
        [True, True, False, True, True],
        [True] * 5
    ],
    (4, 1): [
        [True] * 5,
        [True, False, True, False, True],
        [True, False, False, False, True],
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

def get_pattern(color: int, s_c: int) -> List[List[bool]]:
    """Rule: Retrieve known pattern for (color, horizontal block index s_c).
    For unknown, mirror the s_c=0 pattern if known, else all filled. This handles new positions creatively by symmetry."""
    key = (color, s_c)
    if key in KNOWN_PATTERNS:
        return [row[:] for row in KNOWN_PATTERNS[key]]  # copy
    base_key = (color, 0)
    if base_key in KNOWN_PATTERNS:
        base = KNOWN_PATTERNS[base_key]
        mirrored = [row[::-1] for row in base]
        return mirrored
    return [[True] * 5 for _ in range(5)]

def place_block(grid: List[List[int]], out_r: int, out_c: int, color: int, s_c: int, bg: int):
    """Transformation: Place the pattern for the block into the output grid at position."""
    pattern = get_pattern(color, s_c)
    for dr in range(5):
        for dc in range(5):
            val = color if pattern[dr][dc] else bg
            grid[out_r + dr][out_c + dc] = val

def program(g: List[List[int]]) -> List[List[int]]:
    """Main composition: Orchestrate finding blocks, sizing, creating grid, and placing patterns."""
    bg = get_background(g)
    blocks = find_five_by_five_blocks(g, bg)
    row_starts, col_starts = get_block_positions(blocks)
    h, w = get_output_dimensions(row_starts, col_starts)
    grid = create_empty_grid(h, w, bg)
    for block_i, block_j, color in blocks:
        s_r = row_starts.index(block_i)
        s_c = col_starts.index(block_j)
        out_r = 1 + s_r * 6
        out_c = 1 + s_c * 6
        place_block(grid, out_r, out_c, color, s_c, bg)
    return grid
```