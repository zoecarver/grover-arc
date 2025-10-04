```python
from typing import List, Tuple

def find_two_groups(row: List[int]) -> List[Tuple[int, int]]:
    groups = []
    i = 0
    n = len(row)
    while i < n:
        if row[i] == 2:
            start = i
            while i < n and row[i] == 2:
                i += 1
            end = i - 1
            groups.append((start, end))
        else:
            i += 1
    return groups

def vertical_spread(grid: List[List[int]], r: int) -> None:
    if r == 0:
        return
    prev = grid[r - 1]
    curr = grid[r]
    for j in range(len(curr)):
        if prev[j] == 6 and curr[j] == 7:
            curr[j] = 6

def is_reachable(grid: List[List[int]], r: int, left: int, right: int) -> bool:
    for j in range(left, right + 1):
        if grid[r][j] == 6:
            return True
    return False

def horizontal_fill(grid: List[List[int]], r: int, left: int, right: int) -> None:
    n = len(grid[r])
    start = max(0, left - 1)
    end = min(n - 1, right + 1)
    for j in range(start, end + 1):
        if grid[r][j] == 7:
            grid[r][j] = 6

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    height = len(grid)
    if height == 0:
        return grid
    for r in range(height):
        vertical_spread(grid, r)
        if r < height - 1:
            groups = find_two_groups(grid[r + 1])
            for start, end in groups:
                if is_reachable(grid, r, start, end):
                    horizontal_fill(grid, r, start, end)
    return grid
```