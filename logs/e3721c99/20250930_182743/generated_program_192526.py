```python
from typing import List, Dict, Tuple
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def find_same_color_components(g: List[List[int]], min_col: int, max_col: int) -> List[Dict[str, any]]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components: List[Dict[str, any]] = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            val = g[r][c]
            if min_col <= val <= max_col and not visited[r][c]:
                color = val
                cells: List[Tuple[int, int]] = []
                min_r, max_r, min_c, max_c = r, r, c, c
                q = deque([(r, c)])
                visited[r][c] = True
                cells.append((r, c))
                while q:
                    x, y = q.popleft()
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            cells.append((nx, ny))
                components.append({
                    'cells': cells,
                    'color': color,
                    'min_r': min_r,
                    'min_c': min_c,
                    'max_r': max_r,
                    'max_c': max_c
                })
    return components

def find_orange_blobs(g: List[List[int]]) -> List[Dict[str, any]]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    blobs: List[Dict[str, any]] = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] > 4 and not visited[r][c]:
                cells: List[Tuple[int, int]] = []
                min_r, max_r, min_c, max_c = r, r, c, c
                q = deque([(r, c)])
                visited[r][c] = True
                cells.append((r, c))
                while q:
                    x, y = q.popleft()
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] > 4:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            cells.append((nx, ny))
                blobs.append({
                    'cells': cells,
                    'min_r': min_r,
                    'min_c': min_c,
                    'max_r': max_r,
                    'max_c': max_c
                })
    return blobs

def is_legend(comp: Dict[str, any]) -> bool:
    height = comp['max_r'] - comp['min_r'] + 1
    width = comp['max_c'] - comp['min_c'] + 1
    return height > 1 and width > 1

def get_legends(g: List[List[int]]) -> List[Dict[str, any]]:
    all_comps = find_same_color_components(g, 1, 4)
    return [comp for comp in all_comps if is_legend(comp)]

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
    for r in (0, rows - 1):
        for c in range(cols):
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

def build_hole_to_color_mapping(legends: List[Dict[str, any]], g: List[List[int]]) -> Dict[int, int]:
    sorted_legends = sorted(legends, key=lambda l: (l['min_r'], l['min_c']))
    mapping: Dict[int, int] = {}
    for leg in sorted_legends:
        h = count_holes(g, leg['cells'])
        if h not in mapping:
            mapping[h] = leg['color']
    return mapping

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    legends = get_legends(g)
    mapping = build_hole_to_color_mapping(legends, g)
    blobs = find_orange_blobs(g)
    for blob in blobs:
        h = count_holes(g, blob['cells'])
        if h in mapping:
            col = mapping[h]
            for r, c in blob['cells']:
                out[r][c] = col
        else:
            for r, c in blob['cells']:
                out[r][c] = 0
    return out
```