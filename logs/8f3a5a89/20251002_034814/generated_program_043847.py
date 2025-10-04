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

def get_valid_ones(g: List[List[int]]) -> Set[Tuple[int, int]]:
    n = len(g)
    if n == 0:
        return set()
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
                touches_border = any(x == 0 or x == n - 1 or y == 0 or y == n - 1 for x, y in comp)
                if touches_border:
                    for x, y in comp:
                        valid_ones.add((x, y))
    return valid_ones

def get_minj_after(grid: List[List[int]], row: int, start: int) -> int:
    n = len(grid[0])
    for j in range(start, n):
        if grid[row][j] == 1:
            return j
    return n

def get_maxj(grid: List[List[int]], row: int) -> int:
    n = len(grid[0])
    mx = -1
    for j in range(n):
        if grid[row][j] == 1:
            mx = max(mx, j)
    return mx

def apply_dilation(out: List[List[int]], g: List[List[int]], valid_ones: Set[Tuple[int, int]], n: int):
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

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    has_spine, k = has_full_spine(g)
    out = copy_grid(g)
    if has_spine:
        # Clean non-spine 1s
        for i in range(n):
            for j in range(n):
                if j != k and out[i][j] == 1:
                    out[i][j] = 8
        # Left border
        for i in range(n):
            if out[i][0] == 8:
                out[i][0] = 7
        # Left of spine
        if k > 0:
            for i in range(n):
                if out[i][k - 1] == 8:
                    out[i][k - 1] = 7
        # Top row fill left only
        minj = get_minj_after(out, 0, 0)
        for j in range(minj):
            if out[0][j] == 8:
                out[0][j] = 7
        # Bottom row fill left only
        i_bot = n - 1
        jstart = 1 if out[i_bot][0] == 6 else 0
        minj = get_minj_after(out, i_bot, jstart)
        for j in range(jstart, minj):
            if out[i_bot][j] == 8:
                out[i_bot][j] = 7
    else:
        # No spine
        has_right = any(g[i][n - 1] == 1 for i in range(n - 1))
        # Left border
        for i in range(n):
            if out[i][0] == 8:
                out[i][0] = 7
        # Right border
        if has_right:
            for i in range(n):
                if out[i][n - 1] == 8:
                    out[i][n - 1] = 7
        # Top row
        minj = get_minj_after(g, 0, 0)
        maxj = get_maxj(g, 0)
        for j in range(minj):
            if out[0][j] == 8:
                out[0][j] = 7
        if has_right and maxj != -1:
            for j in range(maxj + 1, n):
                if out[0][j] == 8:
                    out[0][j] = 7
        # Bottom row
        i_bot = n - 1
        jstart = 1 if g[i_bot][0] == 6 else 0
        minj = get_minj_after(g, i_bot, jstart)
        maxj = get_maxj(g, i_bot)
        for j in range(jstart, minj):
            if out[i_bot][j] == 8:
                out[i_bot][j] = 7
        if has_right and maxj != -1:
            for j in range(maxj + 1, n):
                if out[i_bot][j] == 8:
                    out[i_bot][j] = 7
        # Dilation for middle rows
        valid_ones = get_valid_ones(g)
        apply_dilation(out, g, valid_ones, n)
    return out
```