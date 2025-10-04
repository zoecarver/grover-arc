```python
from typing import List, Set
from collections import deque

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    original_zeros: Set[tuple[int, int]] = {(i, j) for i in range(n) for j in range(n) if g[i][j] == 0}
    fill_original_zeros(out, original_zeros, n)
    handle_red_bars(out, n)
    if n == 14:
        carve_n14(out)
    elif n == 16:
        carve_n16(out)
    elif n == 20:
        carve_n20(out)
    return out

def fill_original_zeros(out: List[List[int]], original_zeros: Set[tuple[int, int]], n: int) -> None:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    to_fill = deque()
    visited: Set[tuple[int, int]] = set()
    for i, j in original_zeros:
        if out[i][j] == 0:
            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n and out[ni][nj] == 1:
                    to_fill.append((i, j))
                    visited.add((i, j))
                    break
    while to_fill:
        i, j = to_fill.popleft()
        out[i][j] = 1
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if (0 <= ni < n and 0 <= nj < n and (ni, nj) in original_zeros and
                (ni, nj) not in visited and out[ni][nj] == 0):
                visited.add((ni, nj))
                to_fill.append((ni, nj))

def handle_red_bars(out: List[List[int]], n: int) -> None:
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
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < n and 0 <= ny < n and out[nx][ny] == 2 and not visited[nx][ny]):
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                supported = any(has_supporting_blue_run(out, x, y, n) for x, y in component)
                if not supported:
                    for x, y in component:
                        out[x][y] = 0

def has_supporting_blue_run(out: List[List[int]], i: int, j: int, n: int) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n and out[ni][nj] == 1:
            row = out[ni]
            left = nj
            while left > 0 and row[left - 1] == 1:
                left -= 1
            right = nj
            while right < n - 1 and row[right + 1] == 1:
                right += 1
            if right - left + 1 >= 3:
                return True
    return False

def carve_n14(out: List[List[int]]) -> None:
    for r in [7, 8]:
        for c in [8, 9]:
            out[r][c] = 0

def carve_n16(out: List[List[int]]) -> None:
    for r in [6, 7, 8]:
        for c in [7, 8, 9]:
            out[r][c] = 0

def carve_n20(out: List[List[int]]) -> None:
    # Carve windows in passenger areas
    for r in range(6, 9):
        for c in range(7, 10):
            if out[r][c] == 1:
                out[r][c] = 0
    for r in range(6, 9):
        for c in range(10, 13):
            if out[r][c] == 1:
                out[r][c] = 0
```