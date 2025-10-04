```python
from typing import List
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return g
    h = len(g)
    w = len(g[0])
    # Assume background is the color of the first row (all same)
    b = g[0][0]
    out = [row[:] for row in g]
    visited = [[False] * w for _ in range(h)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(h):
        for j in range(w):
            if out[i][j] != b and not visited[i][j]:
                stack = [(i, j)]
                visited[i][j] = True
                component = []
                color_count = defaultdict(int)
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    c = out[x][y]
                    color_count[c] += 1
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and out[nx][ny] != b:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                colors = list(color_count.keys())
                if len(colors) != 2:
                    continue
                c1, c2 = colors
                if 1 in color_count:
                    # Wall present (1), fill non-1 cells with the other color
                    other = c1 if c1 != 1 else c2
                    for x, y in component:
                        if out[x][y] != 1:
                            out[x][y] = other
                else:
                    # No wall, fill all with minority color
                    if color_count[c1] < color_count[c2]:
                        minority = c1
                    else:
                        minority = c2
                    for x, y in component:
                        out[x][y] = minority
    return out
```