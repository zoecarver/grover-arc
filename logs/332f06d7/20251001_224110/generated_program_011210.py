```python
from typing import List
from copy import deepcopy

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def handle_red_components(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return copy_grid(g)
    m = len(g[0])
    visited = [[False] * m for _ in range(n)]
    result = copy_grid(g)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(m):
            if g[i][j] == 3 and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                min_r, max_r = i, i
                min_c, max_c = j, j
                size = 1
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < m and g[nx][ny] == 3 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            size += 1
                            min_r = min(min_r, nx)
                            max_r = max(max_r, nx)
                            min_c = min(min_c, ny)
                            max_c = max(max_c, ny)
                touches_border = (min_c == 0 or max_c == m - 1 or max_r == n - 1)
                if size == 1 or not touches_border:
                    for x, y in component:
                        result[x][y] = 2
    return result

def fill_blues(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return copy_grid(g)
    m = len(g[0])
    result = copy_grid(g)
    for _ in range(n):
        # Left to right pass: fill right and down
        new_result = copy_grid(result)
        for i in range(n):
            for j in range(m):
                if result[i][j] == 2:
                    fill = False
                    if i > 0 and result[i - 1][j] == 1:
                        fill = True
                    if j > 0 and result[i][j - 1] == 1:
                        fill = True
                    if fill:
                        new_result[i][j] = 1
        result = new_result
        # Right to left pass: fill left and down
        new_result = copy_grid(result)
        for i in range(n):
            for j in range(m - 1, -1, -1):
                if result[i][j] == 2:
                    fill = False
                    if i > 0 and result[i - 1][j] == 1:
                        fill = True
                    if j < m - 1 and result[i][j + 1] == 1:
                        fill = True
                    if fill:
                        new_result[i][j] = 1
        result = new_result
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    result = handle_red_components(g)
    result = fill_blues(result)
    return result
```