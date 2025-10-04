```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def count_4_neighbors(g: List[List[int]], i: int, j: int, c: int) -> int:
    h, w = len(g), len(g[0])
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    count = 0
    for di, dj in dirs:
        ni, nj = i + di, j + dj
        if 0 <= ni < h and 0 <= nj < w and g[ni][nj] == c:
            count += 1
    return count

def remove_low_connectivity_iterative(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    out = [row[:] for row in g]
    changed = True
    while changed:
        changed = False
        for i in range(len(out)):
            for j in range(len(out[0])):
                if out[i][j] != bg:
                    c = out[i][j]
                    if count_4_neighbors(out, i, j, c) < 2:
                        out[i][j] = bg
                        changed = True
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    return remove_low_connectivity_iterative(g)
```