```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    bg = g[0][0]
    h = len(g)
    w = len(g[0])
    new_g = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if new_g[i][j] == bg:
                continue
            c = new_g[i][j]
            n = 0
            for di, dj in directions:
                ni = i + di
                nj = j + dj
                if 0 <= ni < h and 0 <= nj < w and new_g[ni][nj] == c:
                    n += 1
            if n < 2:
                new_g[i][j] = bg
    return new_g
```