```python
import collections
from copy import deepcopy
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    g = deepcopy(g)
    h = len(g)
    if h == 0:
        return g
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    cycle = [4, 3, 1, 2]
    component_index = 0
    dirs = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
    for r in range(h):
        for c in range(w):
            if g[r][c] > 4 and not visited[r][c]:
                col = cycle[component_index % 4]
                q = collections.deque([(r, c)])
                visited[r][c] = True
                g[r][c] = col
                while q:
                    x, y = q.popleft()
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] > 4 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            g[nx][ny] = col
                            q.append((nx, ny))
                component_index += 1
    return g
```