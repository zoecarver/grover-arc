```python
from typing import List, Dict, Tuple
from collections import deque
import copy

def get_legend_mapping(grid: List[List[int]]) -> Dict[int, int]:
    mapping: Dict[int, int] = {}
    r1 = grid[1]
    r2 = grid[2]
    r3 = grid[3]
    col = 0
    while col < 30:
        while col < 30 and r1[col] == 0 and r2[col] == 0 and r3[col] == 0:
            col += 1
        if col == 30:
            break
        start_col = col
        while col < 30 and (r1[col] != 0 or r2[col] != 0 or r3[col] != 0):
            col += 1
        end_col = col - 1
        width = end_col - start_col + 1
        if width < 3:
            col = end_col + 1
            continue
        first = -1
        last = -1
        for c in range(start_col, end_col + 1):
            if r2[c] != 0:
                if first == -1:
                    first = c
                last = c
        if first == -1 or last == first:
            col = end_col + 1
            continue
        color = r2[first]
        num_holes = 0
        for c in range(first + 1, last):
            if r2[c] == 0:
                num_holes += 1
        mapping[num_holes] = color
        col = end_col + 1
    return mapping

def compute_holes(grid: List[List[int]], component: List[Tuple[int, int]]) -> int:
    if not component:
        return 0
    empty_visited = [[False] * 30 for _ in range(30)]
    hole_count = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for x, y in component:
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 30 and 0 <= ny < 30 and grid[nx][ny] == 0 and not empty_visited[nx][ny]:
                q = deque([(nx, ny)])
                empty_visited[nx][ny] = True
                reaches_border = False
                while q:
                    a, b = q.popleft()
                    if a == 0 or a == 29 or b == 0 or b == 29:
                        reaches_border = True
                    for ddx, ddy in directions:
                        na, nb = a + ddx, b + ddy
                        if 0 <= na < 30 and 0 <= nb < 30 and grid[na][nb] == 0 and not empty_visited[na][nb]:
                            empty_visited[na][nb] = True
                            q.append((na, nb))
                if not reaches_border:
                    hole_count += 1
    return hole_count

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(g)
    mapping = get_legend_mapping(grid)
    visited = [[False] * 30 for _ in range(30)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for r in range(30):
        for c in range(30):
            if grid[r][c] == 5 and not visited[r][c]:
                component = []
                q = deque([(r, c)])
                visited[r][c] = True
                component.append((r, c))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 30 and 0 <= ny < 30 and grid[nx][ny] == 5 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            component.append((nx, ny))
                h = compute_holes(grid, component)
                if h in mapping:
                    color = mapping[h]
                    for x, y in component:
                        grid[x][y] = color
                else:
                    for x, y in component:
                        grid[x][y] = 0
    return grid
```