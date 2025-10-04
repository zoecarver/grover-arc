```python
from typing import List

def erase_small_red(g: List[List[int]]) -> List[List[int]]:
    h = [row[:] for row in g]
    n = len(h)
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if h[i][j] == 2 and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and h[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                good = False
                for x, y in component:
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and h[nx][ny] == 1:
                            row = h[nx]
                            left = ny
                            while left > 0 and row[left - 1] == 1:
                                left -= 1
                            right = ny
                            while right < n - 1 and row[right + 1] == 1:
                                right += 1
                            run_len = right - left + 1
                            if run_len >= 3:
                                good = True
                                break
                    if good:
                        break
                if not good:
                    for x, y in component:
                        h[x][y] = 0
    return h

def fill_blue_holes(g: List[List[int]]) -> List[List[int]]:
    h = [row[:] for row in g]
    n = len(h)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(n):
                if h[i][j] == 0:
                    for dx, dy in directions:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < n and 0 <= nj < n and h[ni][nj] == 1:
                            h[i][j] = 1
                            changed = True
                            break
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    h = erase_small_red(g)
    h = fill_blue_holes(h)
    return h
```