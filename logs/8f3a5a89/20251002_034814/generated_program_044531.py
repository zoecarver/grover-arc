```python
from typing import List, Set, Tuple
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    return [row[:] for row in g]

def has_full_spine(g: List[List[int]]) -> Tuple[bool, int]:
    n = len(g)
    if n == 0:
        return False, -1
    for col in range(n):
        if all(g[row][col] == 1 for row in range(n)):
            return True, col
    return False, -1

def clean_other_1s(out: List[List[int]], k: int, n: int) -> None:
    for i in range(n):
        for j in range(n):
            if j != k and out[i][j] == 1:
                out[i][j] = 8

def apply_left_border(out: List[List[int]], n: int) -> None:
    for i in range(n - 1):
        if out[i][0] == 8:
            out[i][0] = 7

def apply_right_border(out: List[List[int]], n: int) -> None:
    for i in range(n):
        if out[i][n - 1] == 8:
            out[i][n - 1] = 7

def apply_column_fill(out: List[List[int]], col: int, n: int) -> None:
    for i in range(n):
        if out[i][col] == 8:
            out[i][col] = 7

def apply_top_fill_left(out: List[List[int]], k: int, n: int) -> None:
    for j in range(k):
        if out[0][j] == 8:
            out[0][j] = 7

def apply_bottom_fill_left(out: List[List[int]], k: int, n: int) -> None:
    j_start = 1 if out[n - 1][0] == 6 else 0
    for j in range(j_start, k):
        if out[n - 1][j] == 8:
            out[n - 1][j] = 7

def get_valid_ones(g: List[List[int]], n: int) -> Set[Tuple[int, int]]:
    visited = [[False] * n for _ in range(n)]
    valid_ones: Set[Tuple[int, int]] = set()
    directions4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for r in range(n):
        for c in range(n):
            if g[r][c] == 1 and not visited[r][c]:
                comp = []
                q = deque([(r, c)])
                visited[r][c] = True
                while q:
                    x, y = q.popleft()
                    comp.append((x, y))
                    for dx, dy in directions4:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 1 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                touches_border = any(xx == 0 or xx == n - 1 or yy == 0 or yy == n - 1 for xx, yy in comp)
                if touches_border:
                    for pos in comp:
                        valid_ones.add(pos)
    return valid_ones

def apply_dilation(out: List[List[int]], valid_ones: Set[Tuple[int, int]], n: int) -> None:
    if n <= 2:
        return
    directions8 = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(1, n - 1):
        for j in range(n):
            if out[i][j] == 8:
                for di, dj in directions8:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < n and 0 <= nj < n and (ni, nj) in valid_ones:
                        out[i][j] = 7
                        break

def find_minj_maxj(g: List[List[int]], row: int, n: int) -> Tuple[int, int]:
    minj = n
    maxj = -1
    for j in range(n):
        if g[row][j] == 1:
            minj = min(minj, j)
            maxj = max(maxj, j)
    return minj, maxj

def apply_top_fill_segments(out: List[List[int]], g: List[List[int]], row: int, n: int) -> None:
    minj, maxj = find_minj_maxj(g, row, n)
    for j in range(minj):
        if out[row][j] == 8:
            out[row][j] = 7
    for j in range(maxj + 1, n):
        if out[row][j] == 8:
            out[row][j] = 7

def apply_bottom_fill_segments(out: List[List[int]], g: List[List[int]], row: int, n: int) -> None:
    j_start = 1 if g[row][0] == 6 else 0
    minj, maxj = find_minj_maxj(g, row, n)
    for j in range(j_start, minj):
        if out[row][j] == 8:
            out[row][j] = 7
    for j in range(maxj + 1, n):
        if out[row][j] == 8:
            out[row][j] = 7

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    out = copy_grid(g)
    has_spine, k = has_full_spine(g)
    if has_spine:
        clean_other_1s(out, k, n)
        apply_left_border(out, n)
        if k > 0:
            apply_column_fill(out, k - 1, n)
        apply_top_fill_left(out, k, n)
        apply_bottom_fill_left(out, k, n)
    else:
        apply_left_border(out, n)
        apply_right_border(out, n)
        valid_ones = get_valid_ones(g, n)
        apply_dilation(out, valid_ones, n)
        apply_top_fill_segments(out, g, 0, n)
        apply_bottom_fill_segments(out, g, n - 1, n)
    return out
```