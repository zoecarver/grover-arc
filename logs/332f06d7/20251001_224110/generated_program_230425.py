```python
from typing import List

def dilate_once(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    new_g = [[g[i][j] for j in range(cols)] for i in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 0:
                for di, dj in directions:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and g[ni][nj] == 1:
                        new_g[i][j] = 1
                        break
    return new_g

def handle_red(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    new_g = [[g[i][j] for j in range(cols)] for i in range(rows)]
    total_red = sum(sum(1 for j in range(cols) if g[i][j] == 2) for i in range(rows))
    top_red = any(g[0][j] == 2 for j in range(cols))
    if total_red == 1 or top_red:
        for i in range(rows):
            for j in range(cols):
                if new_g[i][j] == 2:
                    new_g[i][j] = 0
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    current = [[g[i][j] for j in range(cols)] for i in range(rows)]
    max_passes = rows * 2
    for _ in range(max_passes):
        new_current = dilate_once(current)
        if new_current == current:
            break
        current = new_current
    result = handle_red(current)
    return result
```