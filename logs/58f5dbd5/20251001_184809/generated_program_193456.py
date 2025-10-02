```python
from typing import List, Tuple
import collections

def get_background(grid: List[List[int]]) -> int:
    """Extract the background color from the top-left cell."""
    return grid[0][0] if grid and grid[0] else 0

def extract_solid_5x5_blocks(grid: List[List[int]]) -> List[Tuple[int, int, int]]:
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

def group_into_rows(blocks: List[Tuple[int, int, int]]) -> List[List[Tuple[int, int, int]]]:
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

def compute_output_dimensions(groups: List[List[Tuple[int, int, int]]]) -> Tuple[int, int]:
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

def render_digit_pattern(pattern: List[List[int]], color: int, bg: int, start_row: int, start_col: int, grid: List[List[int]]) -> None:
    """Renders a 5x5 digit pattern into the grid at the given position, using color for 1s and bg for 0s."""
    for k in range(5):
        for l in range(5):
            val = color if pattern[k][l] == 1 else bg
            grid[start_row + k][start_col + l] = val

def compute_pattern(grid: List[List[int]], sr: int, sc: int, c: int, all_blocks: List[Tuple[int, int, int]]) -> List[List[int]]:
    """Computes the 5x5 binary pattern for the block by carving based on small pixels."""
    n = len(grid)
    m = len(grid[0]) if grid and grid[0] else 0
    covered = set()
    for br, bc, _ in all_blocks:
        for dr in range(5):
            rr = br + dr
            if 0 <= rr < n:
                for dc in range(5):
                    cc = bc + dc
                    if 0 <= cc < m:
                        covered.add((rr, cc))
    small = [(r, cc) for r in range(n) for cc in range(m) if grid[r][cc] == c and (r, cc) not in covered]
    # special skip
    special_r = sr + 5
    skip_positions = set()
    if 0 <= special_r < n:
        full = all(0 <= sc + dc < m and grid[special_r][sc + dc] == c for dc in range(5))
        if full:
            for dc in range(5):
                skip_positions.add((special_r, sc + dc))
    small_filtered = [pos for pos in small if pos not in skip_positions]
    if not small_filtered:
        return [[1] * 5 for _ in range(5)]
    row_to_cols = collections.defaultdict(list)
    for r, cc in small_filtered:
        row_to_cols[r].append(cc)
    unique_rows = sorted(row_to_cols)
    k = len(unique_rows)
    min_col = min(cc for _, ccs in row_to_cols.items() for cc in ccs)
    pat = [[1] * 5 for _ in range(5)]
    row_to_llset = {}
    for r in unique_rows:
        llset = set()
        for cc in row_to_cols[r]:
            rel = cc - min_col + 1
            ll = rel % 5
            llset.add(ll)
        row_to_llset[r] = llset
    for jj in range(k):
        pat_idx = jj + 1
        if pat_idx > 4:
            break
        this_r = unique_rows[jj]
        for ll in row_to_llset[this_r]:
            pat[pat_idx][ll] = 0
    if k == 2:
        r0 = unique_rows[0]
        r1 = unique_rows[1]
        sets1 = row_to_llset[r0]
        sets2 = row_to_llset[r1]
        is_above = r1 < sr
        if is_above:
            if len(sets1) >= 2:
                min_l = min(sets1)
                max_l = max(sets1)
                mid = (min_l + max_l) // 2
                pat[3][mid] = 0
        else:
            for ll in sets1:
                pat[3][ll] = 0
    return pat

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    blocks = extract_solid_5x5_blocks(g)
    groups = group_into_rows(blocks)
    if not groups:
        return [[bg]]
    num_groups = len(groups)
    max_per = max((len(group) for group in groups), default=0)
    height = 6 * num_groups + 1
    width = 6 * max_per + 1
    out = initialize_output_grid(height, width, bg)
    cur_row = 1
    for group in groups:
        for idx, (sr, sc, c) in enumerate(group):
            out_col = 1 + 6 * idx
            pat = compute_pattern(g, sr, sc, c, blocks)
            render_digit_pattern(pat, c, bg, cur_row, out_col, out)
        cur_row += 6
    return out
```