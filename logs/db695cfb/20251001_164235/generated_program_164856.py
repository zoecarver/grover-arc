```python
import copy
from collections import defaultdict
from typing import List

def fill_backslash(grid: List[List[int]], diff: int, min_r: int, max_r: int, color: int, bg: int, nrows: int, ncols: int):
    for r in range(max(0, min_r), min(nrows, max_r + 1)):
        c = r - diff
        if 0 <= c < ncols and grid[r][c] == bg:
            grid[r][c] = color

def fill_slash(grid: List[List[int]], s: int, min_r: int, max_r: int, color: int, bg: int, nrows: int, ncols: int):
    for r in range(max(0, min_r), min(nrows, max_r + 1)):
        c = s - r
        if 0 <= c < ncols and grid[r][c] == bg:
            grid[r][c] = color

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(g)
    nrows = len(grid)
    if nrows == 0:
        return grid
    ncols = len(grid[0])
    bg = grid[0][0]
    orig_ones = [(r, c) for r in range(nrows) for c in range(ncols) if grid[r][c] == 1]
    orig_sixes = [(r, c) for r in range(nrows) for c in range(ncols) if grid[r][c] == 6]
    
    # Process 1's backslash segments
    diff_to_rs = defaultdict(list)
    for r, c in orig_ones:
        d = r - c
        diff_to_rs[d].append(r)
    for d, rs in diff_to_rs.items():
        if len(rs) >= 2:
            minr = min(rs)
            maxr = max(rs)
            fill_backslash(grid, d, minr, maxr, 1, bg, nrows, ncols)
    
    # Process 1's slash segments
    sum_to_rs = defaultdict(list)
    for r, c in orig_ones:
        s = r + c
        sum_to_rs[s].append(r)
    for s, rs in sum_to_rs.items():
        if len(rs) >= 2:
            minr = min(rs)
            maxr = max(rs)
            fill_slash(grid, s, minr, maxr, 1, bg, nrows, ncols)
    
    # Conflicting diagonals for 1's
    conflicting_diffs = {d for d, rs in diff_to_rs.items() if len(rs) >= 2}
    conflicting_sums = {s for s, rs in sum_to_rs.items() if len(rs) >= 2}
    
    # Process 6's backslash segments
    diff_to_rs6 = defaultdict(list)
    for r, c in orig_sixes:
        d = r - c
        diff_to_rs6[d].append(r)
    for d, rs in diff_to_rs6.items():
        if len(rs) >= 2:
            minr = min(rs)
            maxr = max(rs)
            fill_backslash(grid, d, minr, maxr, 6, bg, nrows, ncols)
    
    # Process 6's slash segments
    sum_to_rs6 = defaultdict(list)
    for r, c in orig_sixes:
        s = r + c
        sum_to_rs6[s].append(r)
    for s, rs in sum_to_rs6.items():
        if len(rs) >= 2:
            minr = min(rs)
            maxr = max(rs)
            fill_slash(grid, s, minr, maxr, 6, bg, nrows, ncols)
    
    # Full fills for conflicted 6's
    for r, c in orig_sixes:
        my_d = r - c
        my_s = r + c
        if my_d in conflicting_diffs:
            min_r_full = max(0, my_s - (ncols - 1))
            max_r_full = min(nrows - 1, my_s)
            fill_slash(grid, my_s, min_r_full, max_r_full, 6, bg, nrows, ncols)
        if my_s in conflicting_sums:
            min_r_full = max(0, my_d)
            max_r_full = min(nrows - 1, ncols - 1 + my_d)
            fill_backslash(grid, my_d, min_r_full, max_r_full, 6, bg, nrows, ncols)
    
    return grid
```