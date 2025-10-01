```python
from typing import List
import copy

def find_background(g: List[List[int]]) -> int:
    count = {}
    for row in g:
        for cell in row:
            count[cell] = count.get(cell, 0) + 1
    return max(count, key=count.get)

def remove_low_connectivity(g: List[List[int]], bg: int) -> List[List[int]]:
    """
    Remove non-background pixels with fewer than 2 same-color 4-neighbors.
    This handles removal of isolated and low-connectivity protrusions.
    """
    h, w = len(g), len(g[0])
    new_g = [row[:] for row in g]
    for i in range(h):
        for j in range(w):
            if g[i][j] == bg:
                continue
            c = g[i][j]
            count = 0
            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for di, dj in dirs:
                ni, nj = i + di, j + dj
                if 0 <= ni < h and 0 <= nj < w and g[ni][nj] == c:
                    count += 1
            if count < 2:
                new_g[i][j] = bg
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    new_g = remove_low_connectivity(g, bg)
    return new_g
```