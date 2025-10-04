```python
from typing import List, Tuple
from collections import deque

def find_largest_component_bbox(g: List[List[int]]) -> Tuple[int, int, int, int]:
    rows = len(g)
    if rows == 0:
        return 0, 0, 0, 0
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    max_size = 0
    best_min_r = best_max_r = best_min_c = best_max_c = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # 8-connected
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != 0 and not visited[r][c]:
                q = deque([(r, c)])
                visited[r][c] = True
                size = 1
                min_r = max_r = r
                min_c = max_c = c
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] != 0 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            size += 1
                            min_r = min(min_r, nx)
                            max_r = max(max_r, nx)
                            min_c = min(min_c, ny)
                            max_c = max(max_c, ny)
                if size > max_size:
                    max_size = size
                    best_min_r, best_max_r, best_min_c, best_max_c = min_r, max_r, min_c, max_c
    return best_min_r, best_max_r, best_min_c, best_max_c

def crop_and_pad(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    s = max(h, w)
    new_g = [[0] * s for _ in range(s)]
    for i in range(h):
        for j in range(w):
            if min_r + i < rows and min_c + j < cols:
                new_g[i][j] = g[min_r + i][min_c + j]
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    min_r, max_r, min_c, max_c = find_largest_component_bbox(g)
    return crop_and_pad(g, min_r, max_r, min_c, max_c)
```