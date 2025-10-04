```python
from typing import List

def find_min_r(g: List[List[int]]) -> int:
    min_r = 20
    for i in range(20):
        for j in range(20):
            if g[i][j] != 0 and i < 16:
                min_r = min(min_r, i)
    return min_r if min_r < 20 else 0

def find_max_r(g: List[List[int]]) -> int:
    max_r = -1
    for i in range(20):
        for j in range(20):
            if g[i][j] != 0 and i < 16:
                max_r = max(max_r, i)
    return max_r if max_r >= 0 else 0

def find_min_c(g: List[List[int]]) -> int:
    min_c = 20
    for i in range(20):
        for j in range(20):
            if g[i][j] != 0 and i < 16:
                min_c = min(min_c, j)
    return min_c if min_c < 20 else 0

def find_max_c(g: List[List[int]]) -> int:
    max_c = -1
    for i in range(20):
        for j in range(20):
            if g[i][j] != 0 and i < 16:
                max_c = max(max_c, j)
    return max_c if max_c >= 0 else 0

def compute_size(h: int, w: int) -> int:
    return max(h, w)

def create_empty_grid(s: int) -> List[List[int]]:
    return [[0 for _ in range(s)] for _ in range(s)]

def shift_and_place(g: List[List[int]], new_grid: List[List[int]], min_r: int, min_c: int, s: int) -> None:
    for i in range(20):
        if i >= 16:
            continue
        for j in range(20):
            if g[i][j] != 0:
                ni = i - min_r
                nj = j - min_c
                if 0 <= ni < s and 0 <= nj < s:
                    new_grid[ni][nj] = g[i][j]

def program(g: List[List[int]]) -> List[List[int]]:
    min_r = find_min_r(g)
    max_r = find_max_r(g)
    min_c = find_min_c(g)
    max_c = find_max_c(g)
    h = max_r - min_r + 1 if max_r >= min_r else 0
    w = max_c - min_c + 1 if max_c >= min_c else 0
    s = compute_size(h, w)
    new_grid = create_empty_grid(s)
    shift_and_place(g, new_grid, min_r, min_c, s)
    return new_grid
```