```python
from typing import List, Tuple
from collections import deque

def can_reach_border(grid: List[List[int]], comp: List[Tuple[int, int]]) -> bool:
    if not comp:
        return False
    visited = set(comp)
    q = deque(comp)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        if r == 0 or r == 10 or c == 0 or c == 10:
            return True
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 11 and 0 <= nc < 11 and (nr, nc) not in visited and grid[nr][nc] == 7:
                visited.add((nr, nc))
                q.append((nr, nc))
    return False

def has_adjacent_low_col_six(grid: List[List[int]], comp: List[Tuple[int, int]]) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r, c in comp:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 11 and 0 <= nc < 11 and grid[nr][nc] == 6 and nc <= 5:
                return True
    return False

def has_adjacent_six(grid: List[List[int]], pos: Tuple[int, int]) -> bool:
    r, c = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 11 and 0 <= nc < 11 and grid[nr][nc] == 6:
            return True
    return False

def is_protruding(grid: List[List[int]], r: int, c: int) -> bool:
    left_r, left_c = r, c - 1
    up_r, up_c = r - 1, c
    right_r, right_c = r, c + 1
    left_7 = 0 <= left_c < 11 and grid[left_r][left_c] == 7
    up_9 = 0 <= up_r < 11 and grid[up_r][up_c] == 9
    right_9 = 0 <= right_c < 11 and grid[right_r][right_c] == 9
    return left_7 and up_9 and right_9

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    visited = [[False] * 11 for _ in range(11)]
    components = []
    for i in range(11):
        for j in range(11):
            if grid[i][j] == 9 and not visited[i][j]:
                comp = []
                q = deque([(i, j)])
                visited[i][j] = True
                while q:
                    r, c = q.popleft()
                    comp.append((r, c))
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 11 and 0 <= nc < 11 and grid[nr][nc] == 9 and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                components.append(comp)
    n = 0
    for comp in components:
        sz = len(comp)
        if sz == 1:
            r, c = comp[0]
            if r == 5 and not has_adjacent_six(grid, (r, c)):
                continue
            grid[r][c] = 7
            n += 1
        else:
            reach = can_reach_border(grid, comp)
            if reach:
                for r, c in comp:
                    if is_protruding(grid, r, c):
                        grid[r][c] = 7
                        n += 1
            else:
                if has_adjacent_low_col_six(grid, comp):
                    continue
                for r, c in comp:
                    grid[r][c] = 7
                    n += 1
    central = [(4,4), (4,5), (4,6), (5,4), (5,5), (5,6), (6,4), (6,5), (6,6)]
    for k in range(min(n, len(central))):
        rr, cc = central[k]
        grid[rr][cc] = 9
    return grid
```