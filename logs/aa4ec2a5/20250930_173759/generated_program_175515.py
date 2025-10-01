```python
from typing import List, Tuple, Dict
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def find_components(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] == 1 and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 1 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(comp)
    return components

def get_row_info(component: List[Tuple[int, int]]) -> Tuple[int, int, Dict[int, Tuple[int, int, int]], int]:
    if not component:
        return 0, 0, {}, 0
    rows = {p[0] for p in component}
    min_r = min(rows)
    max_r = max(rows)
    row_dict: Dict[int, Tuple[int, int, int]] = {}
    max_width = 0
    for r in rows:
        cols = [p[1] for p in component if p[0] == r]
        min_c = min(cols)
        max_c = max(cols)
        width = max_c - min_c + 1
        row_dict[r] = (min_c, max_c, width)
        max_width = max(max_width, width)
    return min_r, max_r, row_dict, max_width

def detect_holes(g: List[List[int]], component: List[Tuple[int, int]], h: int, w: int) -> Tuple[bool, set]:
    temp = copy_grid(g)
    for r, c in component:
        temp[r][c] = 3
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for i in range(h):
        for j in range(w):
            if (i == 0 or i == h - 1 or j == 0 or j == w - 1) and temp[i][j] == 4 and not visited[i][j]:
                q.append((i, j))
                visited[i][j] = True
                temp[i][j] = 5
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and temp[nx][ny] == 4 and not visited[nx][ny]:
                visited[nx][ny] = True
                temp[nx][ny] = 5
                q.append((nx, ny))
    hole_visited = [[False] * w for _ in range(h)]
    holes = set()
    for r, c in component:
        for dx, dy in dirs:
            nr, nc = r + dx, c + dy
            if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 4 and temp[nr][nc] == 4 and not hole_visited[nr][nc]:
                qh = deque([(nr, nc)])
                hole_visited[nr][nc] = True
                current_hole = [(nr, nc)]
                while qh:
                    x, y = qh.popleft()
                    for dx2, dy2 in dirs:
                        nx, ny = x + dx2, y + dy2
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and temp[nx][ny] == 4 and not hole_visited[nx][ny]:
                            hole_visited[nx][ny] = True
                            qh.append((nx, ny))
                            current_hole.append((nx, ny))
                holes.update(current_hole)
    has_hole = len(holes) > 0
    return has_hole, holes

def add_global_borders(grid: List[List[int]], h: int, w: int):
    dirs8 = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 4:
                adjacent_obj = any(
                    0 <= r + dr < h and 0 <= c + dc < w and grid[r + dr][c + dc] in {1, 8}
                    for dr, dc in dirs8
                )
                if adjacent_obj:
                    grid[r][c] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy_grid(g)
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    components = find_components(g)
    for comp in components:
        if not comp:
            continue
        has_hole, holes = detect_holes(g, comp, h, w)
        min_r, max_r, row_dict, max_width = get_row_info(comp)
        is_solid = not has_hole
        if has_hole:
            for r, c in comp:
                grid[r][c] = 8
            for r, c in holes:
                grid[r][c] = 6
        # cap top if applicable
        if is_solid and min_r in row_dict:
            top_min_c, top_max_c, top_width = row_dict[min_r]
            if top_width < max_width:
                for c in range(top_min_c, top_max_c + 1):
                    grid[min_r][c] = 2
                if top_min_c > 0 and grid[min_r][top_min_c - 1] == 4:
                    grid[min_r][top_min_c - 1] = 2
                if top_max_c < w - 1 and grid[min_r][top_max_c + 1] == 4:
                    grid[min_r][top_max_c + 1] = 2
        # cap bottom if applicable
        if is_solid and max_r in row_dict:
            bot_min_c, bot_max_c, bot_width = row_dict[max_r]
            if bot_width < max_width:
                for c in range(bot_min_c, bot_max_c + 1):
                    grid[max_r][c] = 2
                if bot_min_c > 0 and grid[max_r][bot_min_c - 1] == 4:
                    grid[max_r][bot_min_c - 1] = 2
                if bot_max_c < w - 1 and grid[max_r][bot_max_c + 1] == 4:
                    grid[max_r][bot_max_c + 1] = 2
    add_global_borders(grid, h, w)
    return grid
```