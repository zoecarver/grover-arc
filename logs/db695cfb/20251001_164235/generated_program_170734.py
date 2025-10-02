```python
from collections import defaultdict
from copy import deepcopy
from typing import List

def detect_bg(grid: List[List[int]]) -> int:
    """Detects the background color from the top-left cell."""
    return grid[0][0] if grid else 0

def extract_seeds(grid: List[List[int]]) -> tuple[List[tuple[int, int]], List[tuple[int, int]]]:
    """Extracts positions of 1s and 6s from the grid."""
    nrows = len(grid)
    ncols = len(grid[0]) if nrows else 0
    ones = [(r, c) for r in range(nrows) for c in range(ncols) if grid[r][c] == 1]
    sixes = [(r, c) for r in range(nrows) for c in range(ncols) if grid[r][c] == 6]
    return ones, sixes

def group_by_backslash(positions: List[tuple[int, int]]) -> defaultdict[int, List[int]]:
    """Groups positions by backslash diagonal key (r - c)."""
    groups = defaultdict(list)
    for r, c in positions:
        groups[r - c].append(r)
    return groups

def group_by_slash(positions: List[tuple[int, int]]) -> defaultdict[int, List[int]]:
    """Groups positions by slash diagonal key (r + c)."""
    groups = defaultdict(list)
    for r, c in positions:
        groups[r + c].append(r)
    return groups

def fill_backslash(grid: List[List[int]], diff: int, min_r: int, max_r: int, color: int, bg: int, nrows: int, ncols: int, overwrite_1: bool = False) -> None:
    """Fills a backslash diagonal from min_r to max_r with color, overwriting bg or (if flag) 1s."""
    for r in range(max(0, min_r), min(nrows, max_r + 1)):
        c = r - diff
        if 0 <= c < ncols:
            cell = grid[r][c]
            if cell == bg or (overwrite_1 and cell == 1):
                grid[r][c] = color

def fill_slash(grid: List[List[int]], s: int, min_r: int, max_r: int, color: int, bg: int, nrows: int, ncols: int, overwrite_1: bool = False) -> None:
    """Fills a slash diagonal from min_r to max_r with color, overwriting bg or (if flag) 1s."""
    for r in range(max(0, min_r), min(nrows, max_r + 1)):
        c = s - r
        if 0 <= c < ncols:
            cell = grid[r][c]
            if cell == bg or (overwrite_1 and cell == 1):
                grid[r][c] = color

def fill_segments(grid: List[List[int]], groups: defaultdict[int, List[int]], color: int, bg: int, nrows: int, ncols: int, fill_func, overwrite_1: bool = False) -> None:
    """Fills segments for groups with >=2 positions using the provided fill function."""
    for key, rs in groups.items():
        if len(rs) >= 2:
            min_r = min(rs)
            max_r = max(rs)
            fill_func(grid, key, min_r, max_r, color, bg, nrows, ncols, overwrite_1)

def handle_conflicts(grid: List[List[int]], sixes: List[tuple[int, int]], one_back_keys: set[int], one_slash_keys: set[int], bg: int, nrows: int, ncols: int) -> None:
    """Handles full fills for conflicting 6s on perpendicular diagonals, overwriting 1s."""
    for r, c in sixes:
        diff = r - c
        s = r + c
        if diff in one_back_keys:
            # Full fill slash
            min_r = max(0, s - (ncols - 1))
            max_r = min(nrows - 1, s)
            fill_slash(grid, s, min_r, max_r, 6, bg, nrows, ncols, overwrite_1=True)
        if s in one_slash_keys:
            # Full fill backslash
            min_r = max(0, diff)
            max_r = min(nrows - 1, ncols + diff - 1)
            fill_backslash(grid, diff, min_r, max_r, 6, bg, nrows, ncols, overwrite_1=True)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    grid = deepcopy(g)
    nrows = len(grid)
    if nrows == 0:
        return grid
    ncols = len(grid[0])
    bg = detect_bg(grid)
    ones, sixes = extract_seeds(grid)
    # Process 1s backslash
    back_groups1 = group_by_backslash(ones)
    one_back_keys = {k for k, rs in back_groups1.items() if len(rs) >= 2}
    fill_segments(grid, back_groups1, 1, bg, nrows, ncols, fill_backslash, overwrite_1=False)
    # Process 1s slash
    slash_groups1 = group_by_slash(ones)
    one_slash_keys = {k for k, rs in slash_groups1.items() if len(rs) >= 2}
    fill_segments(grid, slash_groups1, 1, bg, nrows, ncols, fill_slash, overwrite_1=False)
    # Process 6s backslash
    back_groups6 = group_by_backslash(sixes)
    fill_segments(grid, back_groups6, 6, bg, nrows, ncols, fill_backslash, overwrite_1=False)
    # Process 6s slash
    slash_groups6 = group_by_slash(sixes)
    fill_segments(grid, slash_groups6, 6, bg, nrows, ncols, fill_slash, overwrite_1=False)
    # Handle conflicts
    handle_conflicts(grid, sixes, one_back_keys, one_slash_keys, bg, nrows, ncols)
    return grid
```