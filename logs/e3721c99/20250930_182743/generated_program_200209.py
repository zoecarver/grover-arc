```python
from typing import List, Tuple, Dict
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def flood_fill_same(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]], color: int) -> List[Tuple[int, int]]:
    rows, cols = len(g), len(g[0])
    if not (0 <= sr < rows and 0 <= sc < cols) or g[sr][sc] != color or visited[sr][sc]:
        return []
    stack = deque([(sr, sc)])
    visited[sr][sc] = True
    cells = [(sr, sc)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                visited[nx][ny] = True
                stack.append((nx, ny))
                cells.append((nx, ny))
    return cells

def flood_fill_high(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]]) -> List[Tuple[int, int]]:
    rows, cols = len(g), len(g[0])
    if not (0 <= sr < rows and 0 <= sc < cols) or g[sr][sc] <= 4 or visited[sr][sc]:
        return []
    stack = deque([(sr, sc)])
    visited[sr][sc] = True
    cells = [(sr, sc)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] > 4:
                visited[nx][ny] = True
                stack.append((nx, ny))
                cells.append((nx, ny))
    return cells

def count_holes(grid: List[List[int]], component_cells: List[Tuple[int, int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    is_barrier = [[False] * cols for _ in range(rows)]
    for r, c in component_cells:
        is_barrier[r][c] = True
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in (0, cols - 1):
            if not is_barrier[r][c] and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    for c in range(cols):
        for r in (0, rows - 1):
            if not is_barrier[r][c] and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and not is_barrier[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
    hole_count = 0
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and not is_barrier[r][c] and grid[r][c] == 0:
                hole_count += 1
                qq = deque([(r, c)])
                visited[r][c] = True
                while qq:
                    x, y = qq.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and not is_barrier[nx][ny] and grid[nx][ny] == 0:
                            visited[nx][ny] = True
                            qq.append((nx, ny))
    return hole_count

def find_all_low_components(g: List[List[int]]) -> List[Dict[str, int]]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for r in range(rows):
        for c in range(cols):
            if 1 <= g[r][c] <= 4 and not visited[r][c]:
                color = g[r][c]
                cells = flood_fill_same(g, r, c, visited, color)
                if cells:
                    min_r = min(rr for rr, _ in cells)
                    min_c = min(cc for _, cc in cells)
                    size = len(cells)
                    num_holes = count_holes(g, cells)
                    components.append({
                        'color': color,
                        'holes': num_holes,
                        'min_r': min_r,
                        'min_c': min_c,
                        'size': size
                    })
    return components

def build_hole_to_color_mapping(components: List[Dict[str, int]]) -> Dict[int, int]:
    sorted_components = sorted(components, key=lambda d: (-d['size'], d['min_r'], d['min_c']))
    mapping = {}
    for comp in sorted_components:
        h = comp['holes']
        if h not in mapping:
            mapping[h] = comp['color']
    return mapping

def find_all_high_components(g: List[List[int]]) -> List[Dict[str, any]]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] > 4 and not visited[r][c]:
                cells = flood_fill_high(g, r, c, visited)
                if cells:
                    min_r = min(rr for rr, _ in cells)
                    min_c = min(cc for _, cc in cells)
                    components.append({
                        'cells': cells,
                        'min_r': min_r,
                        'min_c': min_c
                    })
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    low_comps = find_all_low_components(g)
    mapping = build_hole_to_color_mapping(low_comps)
    high_comps = find_all_high_components(g)
    for comp in high_comps:
        cells = comp['cells']
        holes = count_holes(g, cells)
        color = mapping.get(holes, 0)
        for r, c in cells:
            out[r][c] = color
    return out
```