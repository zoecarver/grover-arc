```python
import copy
from collections import defaultdict
from typing import List

def fill_backslash(grid: List[List[int]], diff: int, min_r: int, max_r: int, color: int, bg: int, nrows: int, ncols: int, overwrite_1: bool = False) -> None:
    for r in range(max(0, min_r), min(nrows, max_r + 1)):
        c = r - diff
        if 0 <= c < ncols:
            cell = grid[r][c]
            if cell == bg or (overwrite_1 and cell == 1):
                grid[r][c] = color

def fill_slash(grid: List[List[int]], s: int, min_r: int, max_r: int, color: int, bg: int, nrows: int, ncols: int, overwrite_1: bool = False) -> None:
    for r in range(max(0, min_r), min(nrows, max_r + 1)):
        c = s - r
        if 0 <= c < ncols:
            cell = grid[r][c]
            if cell == bg or (overwrite_1 and cell == 1):
                grid[r][c] = color

def program(g: List[List[int]]) -> List[List[int]]:
    nrows = len(g)
    if nrows == 0:
        return []
    ncols = len(g[0])
    grid = copy.deepcopy(g)
    bg = grid[0][0] if nrows > 0 and ncols > 0 else 0

    orig_ones = [(r, c) for r in range(nrows) for c in range(ncols) if g[r][c] == 1]
    orig_sixes = [(r, c) for r in range(nrows) for c in range(ncols) if g[r][c] == 6]

    # Group and fill 1 backslash segments
    ones_back = defaultdict(list)
    for r, c in orig_ones:
        ones_back[r - c].append((r, c))
    back_1_keys = {k for k, pos in ones_back.items() if len(pos) >= 2}
    for k, pos in ones_back.items():
        if len(pos) >= 2:
            minr = min(r for r, _ in pos)
            maxr = max(r for r, _ in pos)
            fill_backslash(grid, k, minr, maxr, 1, bg, nrows, ncols, False)

    # Group and fill 1 slash segments
    ones_slash = defaultdict(list)
    for r, c in orig_ones:
        ones_slash[r + c].append((r, c))
    slash_1_keys = {k for k, pos in ones_slash.items() if len(pos) >= 2}
    for k, pos in ones_slash.items():
        if len(pos) >= 2:
            minr = min(r for r, _ in pos)
            maxr = max(r for r, _ in pos)
            fill_slash(grid, k, minr, maxr, 1, bg, nrows, ncols, False)

    # Group and fill 6 backslash segments (overwrite 1s)
    six_back = defaultdict(list)
    for r, c in orig_sixes:
        six_back[r - c].append((r, c))
    for k, pos in six_back.items():
        if len(pos) >= 2:
            minr = min(r for r, _ in pos)
            maxr = max(r for r, _ in pos)
            fill_backslash(grid, k, minr, maxr, 6, bg, nrows, ncols, True)

    # Group and fill 6 slash segments (overwrite 1s)
    six_slash = defaultdict(list)
    for r, c in orig_sixes:
        six_slash[r + c].append((r, c))
    for k, pos in six_slash.items():
        if len(pos) >= 2:
            minr = min(r for r, _ in pos)
            maxr = max(r for r, _ in pos)
            fill_slash(grid, k, minr, maxr, 6, bg, nrows, ncols, True)

    # Full fills for 6s on conflicting 1 diagonals (prioritize 6s)
    for r, c in orig_sixes:
        d = r - c
        s = r + c
        if d in back_1_keys:
            minr = max(0, d)
            maxr = min(nrows - 1, ncols - 1 + d)
            fill_backslash(grid, d, minr, maxr, 6, bg, nrows, ncols, True)
        if s in slash_1_keys:
            minr = max(0, s - (ncols - 1))
            maxr = min(nrows - 1, s)
            fill_slash(grid, s, minr, maxr, 6, bg, nrows, ncols, True)

    return grid
```