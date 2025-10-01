```python
from typing import List
import collections

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h, w = len(g), len(g[0])
    visited = [[False] * w for _ in range(h)]
    color_cycle = [4, 3, 2, 1]
    color_idx = 0
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for r in range(h):
        for c in range(w):
            if g[r][c] > 4 and not visited[r][c]:
                col = color_cycle[color_idx % 4]
                color_idx += 1
                q = collections.deque([(r, c)])
                visited[r][c] = True
                g[r][c] = col
                while q:
                    x, y = q.popleft()
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] > 4 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            g[nx][ny] = col
                            q.append((nx, ny))
    return g
```