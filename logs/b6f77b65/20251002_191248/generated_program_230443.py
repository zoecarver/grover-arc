```python
from typing import List

def remove_color(g: List[List[int]], c: int) -> List[List[int]]:
    n = len(g)
    new_g = [row[:] for row in g]
    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            if new_g[i][j] == c:
                new_g[i][j] = 0
    return new_g

def apply_gravity(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    new_g = [[0] * n for _ in range(n)]
    for j in range(n):
        non_zeros = [g[i][j] for i in range(n) if g[i][j] != 0]
        start = n - len(non_zeros)
        for i in range(start):
            new_g[i][j] = 0
        for idx, val in enumerate(non_zeros):
            new_g[start + idx][j] = val
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    c = g[0][0]
    g = remove_color(g, c)
    g = apply_gravity(g)
    return g
```