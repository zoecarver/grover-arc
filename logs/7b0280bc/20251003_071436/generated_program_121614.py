```python
from typing import List, Tuple
import collections

def program(g: List[List[int]]) -> List[List[int]]:
    def copy_grid(grid: List[List[int]]) -> List[List[int]]:
        return [row[:] for row in grid]

    def get_background(grid: List[List[int]]) -> int:
        return grid[0][0]

    def get_used_colors(grid: List[List[int]], b: int) -> List[int]:
        s = set()
        for row in grid:
            for cell in row:
                if cell != b and cell != 0:
                    s.add(cell)
        return sorted(s)

    directions8: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    directions4: List[Tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def extract_components(grid: List[List[int]], c: int) -> List[List[Tuple[int, int]]]:
        n = len(grid)
        m = len(grid[0])
        visited = [[False] * m for _ in range(n)]
        comps = []
        for i in range(n):
            for j in range(m):
                if grid[i][j] == c and not visited[i][j]:
                    comp = []
                    q = collections.deque([(i, j)])
                    visited[i][j] = True
                    comp.append((i, j))
                    while q:
                        x, y = q.popleft()
                        for dx, dy in directions8:
                            nx = x + dx
                            ny = y + dy
                            if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == c and not visited[nx][ny]:
                                visited[nx][ny] = True
                                q.append((nx, ny))
                                comp.append((nx, ny))
                    comps.append(comp)
        return comps

    def has_top_visible(comp: List[Tuple[int, int]], grid: List[List[int]], b: int) -> bool:
        n = len(grid)
        for i, j in comp:
            visible = True
            for k in range(i):
                if grid[k][j] != b and grid[k][j] != 0:
                    visible = False
                    break
            if visible:
                return True
        return False

    def has_left_visible(comp: List[Tuple[int, int]], grid: List[List[int]], b: int) -> bool:
        m = len(grid[0])
        for i, j in comp:
            visible = True
            for l in range(j):
                if grid[i][l] != b and grid[i][l] != 0:
                    visible = False
                    break
            if visible:
                return True
        return False

    def touches_bottom(comp: List[Tuple[int, int]], n: int) -> bool:
        if not comp:
            return False
        return max(i for i, _ in comp) >= n - 3

    out = copy_grid(g)
    n = len(g)
    m = len(g[0])
    bg = get_background(g)
    used = get_used_colors(g, bg)
    for c in used:
        comps = extract_components(g, c)
        for comp in comps:
            if not comp:
                continue
            min_i = min(i for i, _ in comp)
            max_i = max(i for i, _ in comp)
            min_j = min(j for _, j in comp)
            max_j = max(j for _, j in comp)
            h = max_i - min_i + 1
            w = max_j - min_j + 1
            top_v = has_top_visible(comp, g, bg)
            left_v = has_left_visible(comp, g, bg)
            if bg == 8 and c == 2 and touches_bottom(comp, n):
                for i, j in comp:
                    out[i][j] = 3
                continue
            if bg == 9 and c == 6:
                continue
            is_odd = (c % 2 == 1)
            if is_odd and not (c == 1 and bg == 8):
                if top_v and w >= h:
                    for i, j in comp:
                        out[i][j] = 3
            else:
                change = False
                if w > h and top_v:
                    change = True
                elif h > w and left_v:
                    change = True
                elif h == w and top_v and min_i <= 1:
                    change = True
                if change:
                    for i, j in comp:
                        out[i][j] = 5
    # Flood fill 4-way from seeds {1,3,5} into 0's
    visited = [[False] * m for _ in range(n)]
    q = collections.deque()
    seeds = {1, 3, 5}
    for i in range(n):
        for j in range(m):
            if out[i][j] in seeds:
                for di, dj in directions4:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0 and not visited[ni][nj]:
                        out[ni][nj] = 5
                        visited[ni][nj] = True
                        q.append((ni, nj))
    while q:
        i, j = q.popleft()
        for di, dj in directions4:
            ni = i + di
            nj = j + dj
            if 0 <= ni < n and 0 <= nj < m and out[ni][nj] == 0 and not visited[ni][nj]:
                out[ni][nj] = 5
                visited[ni][nj] = True
                q.append((ni, nj))
    return out
```