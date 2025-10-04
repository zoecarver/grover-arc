```python
from typing import List

def touches_border(i: int, j: int, n: int) -> bool:
    """Check if a cell touches the border of the grid."""
    return i == 0 or i == n - 1 or j == 0 or j == n - 1

def handle_red(g: List[List[int]]) -> List[List[int]]:
    """Handle red (2) regions: set to 0 if size == 1 or (size > 1 and touches top row)."""
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    g = [row[:] for row in g]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 2 and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                touches_top = touches_border(i, j, n) and i == 0  # Specifically top row
                size = 1
                component.append((i, j))
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            component.append((nx, ny))
                            size += 1
                            if nx == 0:
                                touches_top = True
                if size == 1 or (size > 1 and touches_top):
                    for x, y in component:
                        g[x][y] = 0
    return g

def fill_internal_blue_holes(g: List[List[int]]) -> List[List[int]]:
    """Fill internal 0 holes touching blue (1) with 1, if the 0 component does not touch border."""
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    g = [row[:] for row in g]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0 and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                touches_blue = False
                touches_bord = touches_border(i, j, n)
                component.append((i, j))
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n:
                            if g[nx][ny] == 0 and not visited[nx][ny]:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                                component.append((nx, ny))
                                if touches_border(nx, ny, n):
                                    touches_bord = True
                            elif g[nx][ny] == 1:
                                touches_blue = True
                if touches_blue and not touches_bord:
                    for x, y in component:
                        g[x][y] = 1
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose rules: handle red regions, then fill internal blue holes."""
    g = handle_red(g)
    g = fill_internal_blue_holes(g)
    return g
```