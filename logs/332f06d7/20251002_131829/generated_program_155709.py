```python
from typing import List
from copy import deepcopy

def fill_holes(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h, w = len(out), len(out[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    changed = True
    while changed:
        changed = False
        for i in range(h):
            for j in range(w):
                if out[i][j] == 2:
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < h and 0 <= nj < w and out[ni][nj] == 1:
                            out[i][j] = 1
                            changed = True
                            break
    return out

def handle_red(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h, w = len(out), len(out[0])
    visited = [[False] * w for _ in range(h)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for si in range(h):
        for sj in range(w):
            if out[si][sj] == 3 and not visited[si][sj]:
                component = []
                stack = [(si, sj)]
                visited[si][sj] = True
                size = 1
                touches_top = si < 2
                touches_left = sj == 0
                touches_right = sj == w - 1
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for di, dj in directions:
                        nx, ny = x + di, y + dj
                        if 0 <= nx < h and 0 <= ny < w and out[nx][ny] == 3 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            size += 1
                            if nx < 2:
                                touches_top = True
                            if ny == 0:
                                touches_left = True
                            if ny == w - 1:
                                touches_right = True
                if size <= 1 or (touches_top and not touches_left and not touches_right):
                    for x, y in component:
                        out[x][y] = 2
    return out

def remove_2x2_protrusions(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h, w = len(out), len(out[0])
    for i in range(1, h - 1):
        for j in range(w - 1):
            if (out[i][j] == 1 and out[i][j + 1] == 1 and
                out[i + 1][j] == 1 and out[i + 1][j + 1] == 1 and
                out[i - 1][j] == 0 and out[i - 1][j + 1] == 0):
                out[i][j] = 2
                out[i][j + 1] = 2
                out[i + 1][j] = 2
                out[i + 1][j + 1] = 2
    return out

def remove_3x3_protrusions(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h, w = len(out), len(out[0])
    for i in range(2, h - 2):
        for j in range(1, w - 2):
            is_pattern = (out[i][j] == 1 and out[i][j + 1] == 1 and out[i][j + 2] == 1 and
                          out[i + 1][j] == 1 and out[i + 1][j + 1] == 1 and out[i + 1][j + 2] == 1 and
                          out[i + 2][j] == 1 and out[i + 2][j + 1] == 1 and out[i + 2][j + 2] == 1 and
                          out[i + 2][j - 1] == 0)
            if is_pattern:
                for di in range(3):
                    for dj in range(3):
                        out[i + di][j + dj] = 2
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = fill_holes(g)
    out = handle_red(out)
    out = remove_2x2_protrusions(out)
    out = remove_3x3_protrusions(out)
    return out
```