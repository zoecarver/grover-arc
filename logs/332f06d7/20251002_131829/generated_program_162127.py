```python
from typing import List
from collections import deque

def program(g: List[List[int]]) -> List[List[int]]:
    g = fill_zeros(g)
    g = handle_red_bars(g)
    g = trim_overhang(g)
    g = separation_trim(g)
    return g

def fill_zeros(g: List[List[int]]) -> List[List[int]]:
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
                        ni, nj = i + di, j + dj
                        if 0 <= ni < n and 0 <= nj < n and out[ni][nj] == 1:
                            out[i][j] = 1
                            changed = True
                            break
    return out

def handle_red_bars(g: List[List[int]]) -> List[List[int]]:
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
                touches_left = (j == 0)
                touches_bottom = (i == n - 1)
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and out[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            if ny == 0:
                                touches_left = True
                            if nx == n - 1:
                                touches_bottom = True
                if not (touches_left or touches_bottom):
                    for x, y in component:
                        out[x][y] = 0
    return out

def trim_overhang(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    running_min = n - 1
    for i in range(n):
        # trim 1's at j >= running_min + 2
        for j in range(running_min + 2, n):
            if out[i][j] == 1:
                out[i][j] = 0
        # compute this_max
        this_max = -1
        for j in range(n - 1, -1, -1):
            if out[i][j] == 1:
                this_max = j
                break
        if this_max != -1 and this_max >= 4:
            running_min = min(running_min, this_max)
    return out

def separation_trim(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    for i in range(n - 2, -1, -1):
        j = 0
        while j < n - 1:
            if out[i][j] == 3 and j + 1 < n and out[i][j + 1] == 1:
                start_j = j + 1
                k = start_j
                l = 0
                while k < n and out[i][k] == 1:
                    l += 1
                    k += 1
                if l >= 3:
                    # compute left_l
                    left_l = 0
                    m = j - 1
                    while m >= 0 and out[i][m] == 1:
                        left_l += 1
                        m -= 1
                    if left_l >= 4:
                        # erase run in current row
                        for kk in range(start_j, start_j + l):
                            out[i][kk] = 0
                        # propagate up l-1 rows
                        for h in range(1, l):
                            if i - h < 0:
                                break
                            for kk in range(start_j, start_j + l):
                                if out[i - h][kk] == 1:
                                    out[i - h][kk] = 0
                j = k
            else:
                j += 1
    return out
```