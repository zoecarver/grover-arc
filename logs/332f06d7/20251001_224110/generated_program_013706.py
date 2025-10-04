```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    n = len(grid)
    if n == 0:
        return []
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    red_h = None
    red_w = None
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 3 and not visited[i][j]:
                component = []
                min_r = max_r = i
                min_c = max_c = j
                touches_top = (i == 0)
                stack = [(i, j)]
                visited[i][j] = True
                size = 1
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    if x == 0:
                        touches_top = True
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 3 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            size += 1
                if size == 1 or touches_top:
                    for x, y in component:
                        grid[x][y] = 2
                else:
                    if red_h is None:
                        red_h = max_r - min_r + 1
                        red_w = max_c - min_c + 1
    visited = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 2 and not visited[i][j]:
                comp = []
                touches_border = False
                touches_blue = False
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    if x == 0 or x == n - 1 or y == 0 or y == n - 1:
                        touches_border = True
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n:
                            if grid[nx][ny] == 1:
                                touches_blue = True
                            elif grid[nx][ny] == 2 and not visited[nx][ny]:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                if not touches_border and touches_blue:
                    for x, y in comp:
                        grid[x][y] = 1
    if red_h is not None and red_w is not None:
        half = n // 2
        max_sr = min(n - red_h, half)
        found = False
        for start_r in range(max_sr, -1, -1):
            for start_c in range(n - red_w + 1)[::-1]:
                all_one = True
                for dx in range(red_h):
                    for dy in range(red_w):
                        rr = start_r + dx
                        cc = start_c + dy
                        if grid[rr][cc] != 1:
                            all_one = False
                            break
                    if not all_one:
                        break
                if all_one:
                    for dx in range(red_h):
                        for dy in range(red_w):
                            grid[start_r + dx][start_c + dy] = 2
                    found = True
                    break
            if found:
                break
    return grid
```