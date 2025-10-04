```python
from collections import deque, Counter
from typing import List, Tuple

def is_border_connected(grid: List[List[int]], color: int, h: int, w: int) -> bool:
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        for c in [0, w - 1]:
            if grid[r][c] == color and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
    for c in range(w):
        if grid[0][c] == color and not visited[0][c]:
            q.append((0, c))
            visited[0][c] = True
        if grid[h - 1][c] == color and not visited[h - 1][c]:
            q.append((h - 1, c))
            visited[h - 1][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and grid[nr][nc] == color:
                visited[nr][nc] = True
                q.append((nr, nc))
    total_count = sum(1 for row in grid for cell in row if cell == color)
    visited_count = sum(sum(row_visited) for row_visited in visited)
    return visited_count == total_count

def get_background(grid: List[List[int]]) -> int:
    h = len(grid)
    if h == 0:
        return 0
    w = len(grid[0])
    flat = [cell for row in grid for cell in row]
    counter = Counter(flat)
    candidates = []
    for color in counter:
        if color != 0 and is_border_connected(grid, color, h, w):
            candidates.append((counter[color], color))
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    return 0

def get_non_bg_components(grid: List[List[int]], bg: int) -> List[List[Tuple[int, int]]]:
    h = len(grid)
    if h == 0:
        return []
    w = len(grid[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if grid[i][j] != bg and not visited[i][j]:
                component = []
                stack = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    if 0 <= x < h and 0 <= y < w and grid[x][y] != bg and not visited[x][y]:
                        visited[x][y] = True
                        component.append((x, y))
                        for dx, dy in dirs:
                            stack.append((x + dx, y + dy))
                if component:
                    components.append(component)
    return components

def get_component_color(grid: List[List[int]], component: List[Tuple[int, int]]) -> int:
    colors = [grid[r][c] for r, c in component]
    counter = Counter(colors)
    return counter.most_common(1)[0][0] if counter else 0

def fill_holes_proper(grid: List[List[int]], component: List[Tuple[int, int]], bg: int, fill_color: int, h: int, w: int) -> List[List[int]]:
    if not component:
        return grid
    min_r = min(r for r, c in component)
    max_r = max(r for r, c in component)
    min_c = min(c for r, c in component)
    max_c = max(c for r, c in component)
    touch_bottom = any(r == h - 1 for r, c in component)
    visited = [[False] * w for _ in range(h)]
    q = deque()
    # Left edge
    for r in range(min_r, max_r + 1):
        c = min_c
        if 0 <= c < w and grid[r][c] == bg and not visited[r][c]:
            q.append((r, c))
            visited[r][c] = True
    # Right edge
    for r in range(min_r, max_r + 1):
        c = max_c
        if 0 <= c < w and grid[r][c] == bg and not visited[r][c]:
            q.append((r, c))
            visited[r][c] = True
    # Top edge
    for c in range(min_c, max_c + 1):
        r = min_r
        if 0 <= r < h and grid[r][c] == bg and not visited[r][c]:
            q.append((r, c))
            visited[r][c] = True
    # Bottom edge only if touching bottom
    if touch_bottom:
        for c in range(min_c, max_c + 1):
            r = max_r
            if 0 <= r < h and grid[r][c] == bg and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if min_r <= nr <= max_r and min_c <= nc <= max_c and 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and grid[nr][nc] == bg:
                visited[nr][nc] = True
                q.append((nr, nc))
    new_grid = [row[:] for row in grid]
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] == bg and not visited[r][c]:
                new_grid[r][c] = fill_color
    return new_grid

def grow_small_components(grid: List[List[int]], components: List[List[Tuple[int, int]]], bg: int, h: int, w: int) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    for comp in components:
        if len(comp) <= 1:
            if not comp:
                continue
            r, c = comp[0]
            color = grid[r][c]
            visited = [[False] * w for _ in range(h)]
            q = deque([(r, c)])
            visited[r][c] = True
            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            while q:
                cr, cc = q.popleft()
                for dr, dc in dirs:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc]:
                        if new_grid[nr][nc] == bg:
                            new_grid[nr][nc] = color
                            visited[nr][nc] = True
                            q.append((nr, nc))
                        elif new_grid[nr][nc] != color:
                            visited[nr][nc] = True  # block other
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return g
    w = len(g[0])
    bg = get_background(g)
    components = get_non_bg_components(g, bg)
    new_grid = [row[:] for row in g]
    # Grow small components first
    new_grid = grow_small_components(new_grid, components, bg, h, w)
    # Then fill holes in large components with 0
    for comp in components:
        if len(comp) > 3:
            new_grid = fill_holes_proper(new_grid, comp, bg, 0, h, w)
    return new_grid
```