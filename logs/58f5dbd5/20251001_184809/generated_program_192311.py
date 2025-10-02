```python
import typing as tp
from typing import List
from collections import defaultdict

def get_background(grid: List[List[int]]) -> int:
    """Extract the background color from the top-left cell."""
    return grid[0][0] if grid and grid[0] else 0

def extract_solid_5x5_blocks(grid: List[List[int]]) -> List[tp.Tuple[int, int, int]]:
    """Extracts 5x5 solid blocks as (start_row, start_col, color) tuples.
    A solid block is a 5x5 region where all cells are the same non-background color."""
    if not grid or not grid[0]:
        return []
    bg = get_background(grid)
    n = len(grid)
    m = len(grid[0]) if grid[0] else 0
    blocks = []
    for i in range(n - 4):
        for j in range(m - 4):
            c = grid[i][j]
            if c == bg:
                continue
            is_solid = True
            for k in range(5):
                if not is_solid:
                    break
                for l in range(5):
                    if grid[i + k][j + l] != c:
                        is_solid = False
                        break
            if is_solid:
                blocks.append((i, j, c))
    return blocks

def group_into_rows(blocks: List[tp.Tuple[int, int, int]]) -> List[List[tp.Tuple[int, int, int]]]:
    """Groups blocks into rows based on starting row proximity (within 5 units).
    Sorts groups by starting row and blocks within groups by starting column."""
    if not blocks:
        return []
    # Sort by starting row, then column
    sorted_blocks = sorted(blocks, key=lambda b: (b[0], b[1]))
    groups = []
    current_group = [sorted_blocks[0]]
    for block in sorted_blocks[1:]:
        if block[0] <= current_group[-1][0] + 5:
            current_group.append(block)
        else:
            # Sort current group by column
            current_group.sort(key=lambda b: b[1])
            groups.append(current_group)
            current_group = [block]
    # Sort last group by column
    current_group.sort(key=lambda b: b[1])
    groups.append(current_group)
    return groups

def compute_output_dimensions(groups: List[List[tp.Tuple[int, int, int]]]) -> tp.Tuple[int, int]:
    """Computes the height and width of the output grid based on number of groups and max blocks per group."""
    if not groups:
        return 1, 1
    num_groups = len(groups)
    max_blocks_per_row = max(len(group) for group in groups)
    height = 6 * num_groups + 1
    width = 6 * max_blocks_per_row + 1
    return height, width

def initialize_output_grid(height: int, width: int, bg: int) -> List[List[int]]:
    """Initializes the output grid filled with background color."""
    return [[bg for _ in range(width)] for _ in range(height)]

def compute_pattern(grid: List[List[int]], covered: set, color: int, n: int, m: int) -> List[List[int]]:
    """Computes the 5x5 binary pattern for the block of given color based on small pixels of that color."""
    small = []
    for r in range(n):
        for c in range(m):
            if grid[r][c] == color and (r, c) not in covered:
                small.append((r, c))
    if not small:
        return [[1] * 5 for _ in range(5)]
    group: dict[int, list[int]] = defaultdict(list)
    for r, c in small:
        group[r].append(c)
    sorted_rs = sorted(group)
    pat = [[1] * 5 for _ in range(5)]
    # Note: sr, sc not used here, but shift depends on sc; wait, error, need sc for shift
    # Wait, this func needs sc for shift, but in call pass sc
    # Wait, adjust: def compute_pattern(..., sc: int, ...)

# Correction: move sc to params
# But since in main we have it, fine, but to define properly.

# Redefine with sc
# But for the code, I'll include in program.

def render_digit_pattern(pattern: List[List[int]], color: int, bg: int, start_row: int, start_col: int, grid: List[List[int]]) -> None:
    """Renders a 5x5 digit pattern into the grid at the given position, using color for 1s and bg for 0s."""
    for k in range(5):
        for l in range(5):
            val = color if pattern[k][l] == 1 else bg
            grid[start_row + k][start_col + l] = val

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    bg = get_background(g)
    n = len(g)
    m = len(g[0]) if g[0] else 0
    blocks = extract_solid_5x5_blocks(g)
    covered = set()
    for sr, sc, c in blocks:
        for dr in range(5):
            for dc in range(5):
                rr = sr + dr
                cc = sc + dc
                if 0 <= rr < n and 0 <= cc < m:
                    covered.add((rr, cc))
    groups = group_into_rows(blocks)
    if not groups:
        return [[bg]]
    num_groups = len(groups)
    max_per_row = max(len(group) for group in groups)
    height = 6 * num_groups + 1
    width = 6 * max_per_row + 1
    out_grid = initialize_output_grid(height, width, bg)
    current_row = 1
    for grp in groups:
        grp = sorted(grp, key=lambda b: b[1])
        for d_idx, (sr, sc, color) in enumerate(grp):
            start_c_out = 1 + 6 * d_idx
            # compute pattern for this block
            small = []
            for r in range(n):
                for c in range(m):
                    if g[r][c] == color and (r, c) not in covered:
                        small.append((r, c))
            pat = [[1] * 5 for _ in range(5)]
            if small:
                group_d = defaultdict(list)
                for r, c in small:
                    group_d[r].append(c)
                sorted_rs = sorted(group_d)
                block_col1 = sc + 1  # 1-based start col index sc is 0-based
                sh = 0 if (block_col1 % 5 == 3) else -1
                for ii, r in enumerate(sorted_rs):
                    pat_r = ii + 1
                    if pat_r > 4:
                        continue
                    offs = set()
                    for ccc in group_d[r]:
                        col1 = ccc + 1
                        raw = col1 % 5
                        ll = (raw + sh + 5) % 5
                        offs.add(ll)
                    for ll in offs:
                        pat[pat_r][ll] = 0
            render_digit_pattern(pat, color, bg, current_row, start_c_out, out_grid)
        current_row += 6
    return out_grid
```