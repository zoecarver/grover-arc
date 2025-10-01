```python
import copy
from collections import defaultdict
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    height = len(g)
    width = len(g[0])
    # Find background color
    count = defaultdict(int)
    for row in g:
        for x in row:
            count[x] += 1
    background = max(count, key=count.get)
    # Copy grid
    grid = copy.deepcopy(g)
    # Fill 1 diagonals
    fill_diagonals(grid, height, width, background, 1)
    # Extend perp for 6 blockers on 1 paths
    extend_perp(grid, height, width, background, 1, 6)
    return grid

def fill_diagonals(grid: List[List[int]], height: int, width: int, background: int, color: int):
    pos = [(r, c) for r in range(height) for c in range(width) if grid[r][c] == color]
    # Group by / (r - c)
    groups = defaultdict(list)
    for r, c in pos:
        groups[r - c].append(r)
    for d, rs in groups.items():
        if len(rs) >= 2:
            min_r = min(rs)
            max_r = max(rs)
            for r in range(min_r, max_r + 1):
                c = r - d
                if 0 <= c < width and grid[r][c] == background:
                    grid[r][c] = color
    # Group by \ (r + c)
    groups = defaultdict(list)
    for r, c in pos:
        groups[r + c].append(r)
    for s, rs in groups.items():
        if len(rs) >= 2:
            min_r = min(rs)
            max_r = max(rs)
            for r in range(min_r, max_r + 1):
                c = s - r
                if 0 <= c < width and grid[r][c] == background:
                    grid[r][c] = color

def extend_perp(grid: List[List[int]], height: int, width: int, background: int, path_color: int, perp_color: int):
    pos = [(r, c) for r in range(height) for c in range(width) if grid[r][c] == path_color]
    # For / paths
    groups = defaultdict(list)
    for r, c in pos:
        groups[r - c].append((r, c))
    for d, poss in groups.items():
        if len(poss) >= 2:
            min_r = min(r for r, _ in poss)
            max_r = max(r for r, _ in poss)
            for r in range(min_r, max_r + 1):
                c = r - d
                if 0 <= c < width and grid[r][c] == perp_color:
                    s = r + c  # perp \
                    for rr in range(height):
                        cc = s - rr
                        if 0 <= cc < width and grid[rr][cc] == background:
                            grid[rr][cc] = perp_color
    # For \ paths
    groups = defaultdict(list)
    for r, c in pos:
        groups[r + c].append((r, c))
    for s, poss in groups.items():
        if len(poss) >= 2:
            min_r = min(r for r, _ in poss)
            max_r = max(r for r, _ in poss)
            for r in range(min_r, max_r + 1):
                c = s - r
                if 0 <= c < width and grid[r][c] == perp_color:
                    d = r - c  # perp /
                    for rr in range(height):
                        cc = rr - d
                        if 0 <= cc < width and grid[rr][cc] == background:
                            grid[rr][cc] = perp_color
```