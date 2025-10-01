```python
from typing import List
import copy

def find_background(g: List[List[int]]) -> int:
    count = {}
    for row in g:
        for cell in row:
            count[cell] = count.get(cell, 0) + 1
    return max(count, key=count.get)

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    h, w = len(g), len(g[0])
    new_g = copy.deepcopy(g)
    changed = True
    while changed:
        changed = False
        temp_g = [row[:] for row in new_g]
        for i in range(h):
            for j in range(w):
                if new_g[i][j] == bg:
                    continue
                c = new_g[i][j]
                count = 0
                dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < h and 0 <= nj < w and new_g[ni][nj] == c:
                        count += 1
                if count < 2:
                    temp_g[i][j] = bg
                    changed = True
        new_g = temp_g
    return new_g
```