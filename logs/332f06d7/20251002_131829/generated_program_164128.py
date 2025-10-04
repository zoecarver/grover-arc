```python
from typing import List

def has_one_neighbor(g: List[List[int]], i: int, j: int, n: int) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in directions:
        ni = i + di
        nj = j + dj
        if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == 1:
            return True
    return False

def fill_pass(g: List[List[int]], n: int) -> List[List[int]]:
    new_g = [row[:] for row in g]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0 and has_one_neighbor(g, i, j, n):
                new_g[i][j] = 1
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    current = [row[:] for row in g]
    for _ in range(n):
        current = fill_pass(current, n)
    return current
```