```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [g[i][j] for i in range(22) for j in range(22)]
    return Counter(flat).most_common(1)[0][0]

def count_neighbors(g: List[List[int]], i: int, j: int, color: int) -> int:
    n = 22
    count = 0
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        ni = i + di
        nj = j + dj
        if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == color:
            count += 1
    return count

def program(g: List[List[int]]) -> List[List[int]]:
    n = 22
    background = get_background(g)
    out = [row[:] for row in g]
    for i in range(n):
        for j in range(n):
            if g[i][j] != background:
                if count_neighbors(g, i, j, g[i][j]) < 2:
                    out[i][j] = background
    return out
```