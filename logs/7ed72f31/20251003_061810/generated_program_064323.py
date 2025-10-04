```python
import copy
from collections import deque
from typing import List, Tuple, Dict

def find_red_components(grid: List[List[int]], n: int) -> List[List[Tuple[int, int]]]:
    visited = [[False] * n for _ in range(n)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 2 and not visited[i][j]:
                component = []
                q = deque([(i, j)])
                visited[i][j] = True
                while q:
                    x, y = q.popleft()
                    component.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                components.append(component)
    return components

def classify_red_component(component: List[Tuple[int, int]]) -> str:
    if len(component) == 1:
        return 'point'
    rows = [x for x, y in component]
    cols = [y for x, y in component]
    if len(set(cols)) == 1:
        min_r, max_r = min(rows), max(rows)
        if max_r - min_r + 1 == len(rows) and len(set(rows)) == len(rows):
            return 'vertical'
    if len(set(rows)) == 1:
        min_c, max_c = min(cols), max(cols)
        if max_c - min_c + 1 == len(cols) and len(set(cols)) == len(cols):
            return 'horizontal'
    return 'ignore'

def handle_point_mirror(grid: List[List[int]], pr: int, pc: int, bg: int, n: int, changes: Dict[Tuple[int, int], int]):
    adj_dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    touching_cells = set()
    for dx, dy in adj_dirs:
        nx, ny = pr + dx, pc + dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != bg and grid[nx][ny] != 2:
            touching_cells.add((nx, ny))
    visited_comp = [[False] * n for _ in range(n)]
    dirs8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for tr, tc in touching_cells:
        if not visited_comp[tr][tc]:
            c = grid[tr][tc]
            if c == bg or c == 2:
                continue
            component = []
            q = deque([(tr, tc)])
            visited_comp[tr][tc] = True
            while q:
                x, y = q.popleft()
                component.append((x, y))
                for dx, dy in dirs8:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and not visited_comp[nx][ny] and grid[nx][ny] == c:
                        visited_comp[nx][ny] = True
                        q.append((nx, ny))
            for rr, cc in component:
                nr = 2 * pr - rr
                nc = 2 * pc - cc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == bg:
                    changes[(nr, nc)] = c

def handle_vertical_mirror(grid: List[List[int]], k: int, a: int, b: int, bg: int, n: int, changes: Dict[Tuple[int, int], int]):
    touching_cells = set()
    adj_dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for x in range(a, b + 1):
        for dx, dy in adj_dirs:
            nx, ny = x + dx, k + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != bg and grid[nx][ny] != 2:
                touching_cells.add((nx, ny))
    visited_comp = [[False] * n for _ in range(n)]
    dirs8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for tr, tc in touching_cells:
        if not visited_comp[tr][tc]:
            c = grid[tr][tc]
            if c == bg or c == 2:
                continue
            component = []
            q = deque([(tr, tc)])
            visited_comp[tr][tc] = True
            while q:
                x, y = q.popleft()
                component.append((x, y))
                for dx, dy in dirs8:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and not visited_comp[nx][ny] and grid[nx][ny] == c:
                        visited_comp[nx][ny] = True
                        q.append((nx, ny))
            for rr, cc in component:
                if a <= rr <= b:
                    nc = 2 * k - cc
                    nr = rr
                    if 0 <= nc < n and grid[nr][nc] == bg:
                        changes[(nr, nc)] = c

def handle_horizontal_mirror(grid: List[List[int]], m: int, l: int, r: int, bg: int, n: int, changes: Dict[Tuple[int, int], int]):
    touching_cells = set()
    adj_dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for y in range(l, r + 1):
        for dx, dy in adj_dirs:
            nx, ny = m + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != bg and grid[nx][ny] != 2:
                touching_cells.add((nx, ny))
    visited_comp = [[False] * n for _ in range(n)]
    dirs8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for tr, tc in touching_cells:
        if not visited_comp[tr][tc]:
            c = grid[tr][tc]
            if c == bg or c == 2:
                continue
            component = []
            q = deque([(tr, tc)])
            visited_comp[tr][tc] = True
            while q:
                x, y = q.popleft()
                component.append((x, y))
                for dx, dy in dirs8:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and not visited_comp[nx][ny] and grid[nx][ny] == c:
                        visited_comp[nx][ny] = True
                        q.append((nx, ny))
            for rr, cc in component:
                if l <= cc <= r:
                    nr = 2 * m - rr
                    nc = cc
                    if 0 <= nr < n and grid[nr][nc] == bg:
                        changes[(nr, nc)] = c

def process_mirrors(grid: List[List[int]], n: int, bg: int, changes: Dict[Tuple[int, int], int]):
    components = find_red_components(grid, n)
    for comp in components:
        typ = classify_red_component(comp)
        if typ == 'point':
            pr, pc = comp[0]
            handle_point_mirror(grid, pr, pc, bg, n, changes)
        elif typ == 'vertical':
            k = comp[0][1]
            rows = sorted(set(x for x, _ in comp))
            a, b = rows[0], rows[-1]
            handle_vertical_mirror(grid, k, a, b, bg, n, changes)
        elif typ == 'horizontal':
            m = comp[0][0]
            cols = sorted(set(y for _, y in comp))
            l, r = cols[0], cols[-1]
            handle_horizontal_mirror(grid, m, l, r, bg, n, changes)

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(g)
    n = len(grid)
    if n == 0:
        return grid
    bg = grid[0][0]
    changes: Dict[Tuple[int, int], int] = {}
    process_mirrors(grid, n, bg, changes)
    for (r, c), colr in changes.items():
        grid[r][c] = colr
    return grid
```