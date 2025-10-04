```python
from typing import List
from collections import deque

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h, w = len(g), len(g[0])
    out = [row[:] for row in g]
    label = [[0] * w for _ in range(h)]
    next_label = 1
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(h):
        for j in range(w):
            if g[i][j] >= 5 and label[i][j] == 0:
                queue = deque([(i, j)])
                label[i][j] = next_label
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] >= 5 and label[nx][ny] == 0:
                            label[nx][ny] = next_label
                            queue.append((nx, ny))
                next_label += 1
    for i in range(h):
        for j in range(w):
            l = label[i][j]
            if l > 0:
                out[i][j] = ((l - 1) % 4) + 1
    return out
```