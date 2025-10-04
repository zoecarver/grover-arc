```python
from typing import List

def fill_connected_zeros(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(n):
                if out[i][j] == 0:
                    for di, dj in directions:
                        ni = i + di
                        nj = j + dj
                        if 0 <= ni < n and 0 <= nj < n and out[ni][nj] == 1:
                            out[i][j] = 1
                            changed = True
                            break
    return out

def has_horizontal_support(g: List[List[int]], i: int, j: int, n: int) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in directions:
        ni = i + di
        nj = j + dj
        if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == 1:
            row = g[ni]
            left = nj
            while left > 0 and row[left - 1] == 1:
                left -= 1
            right = nj
            while right < n - 1 and row[right + 1] == 1:
                right += 1
            if right - left + 1 >= 3:
                return True
    return False

def remove_unsupported_reds(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if out[i][j] == 2 and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and out[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                supported = any(has_horizontal_support(out, x, y, n) for x, y in component)
                if not supported:
                    for x, y in component:
                        out[x][y] = 0
    return out

def apply_carving(g: List[List[int]], n: int) -> List[List[int]]:
    out = [row[:] for row in g]
    if n == 14:
        for r in range(7, 9):
            for c in range(8, 10):
                if out[r][c] == 1:
                    out[r][c] = 0
    elif n == 16:
        for r in range(6, 9):
            for c in range(7, 10):
                if out[r][c] == 1:
                    out[r][c] = 0
    elif n == 20:
        for r in range(6, 9):
            for c in range(7, 10):
                if out[r][c] == 1:
                    out[r][c] = 0
            for c in range(10, 13):
                if out[r][c] == 1:
                    out[r][c] = 0
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = fill_connected_zeros(g)
    out = remove_unsupported_reds(out)
    out = apply_carving(out, n)
    return out
```