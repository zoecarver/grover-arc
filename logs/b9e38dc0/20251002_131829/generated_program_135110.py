```python
from collections import Counter
from typing import List

def find_background(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    flat = [cell for row in grid for cell in row]
    counter = Counter(flat)
    return counter.most_common(1)[0][0]

def find_fill_color(grid: List[List[int]], bg: int) -> int:
    flat = [cell for row in grid for cell in row]
    counter = Counter(flat)
    non_bg = {c: count for c, count in counter.items() if c != bg and count > 0}
    if not non_bg:
        return bg
    min_count = min(non_bg.values())
    candidates = [c for c, count in non_bg.items() if count == min_count]
    return min(candidates)

def fill_gaps_per_row(grid: List[List[int]], f: int, bg: int) -> List[List[int]]:
    if f == bg:
        return [row[:] for row in grid]
    new_grid = [row[:] for row in grid]
    rows = len(new_grid)
    if rows == 0:
        return new_grid
    cols = len(new_grid[0])
    for i in range(rows):
        gaps = []
        j = 0
        while j < cols:
            if new_grid[i][j] != bg:
                j += 1
                continue
            if j > 0 and new_grid[i][j - 1] != bg:
                start = j
                j += 1
                while j < cols and new_grid[i][j] == bg:
                    j += 1
                gaps.append((start, j))
            else:
                j += 1
        for start, end in gaps:
            for k in range(start, end):
                new_grid[i][k] = f
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    f = find_fill_color(g, bg)
    return fill_gaps_per_row(g, f, bg)
```