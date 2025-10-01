```python
from typing import List, Tuple
from collections import deque, defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    def copy_grid(grid: List[List[int]]) -> List[List[int]]:
        return [row[:] for row in grid]

    def count_holes(grid: List[List[int]], component_cells: List[Tuple[int, int]]) -> int:
        rows, cols = len(grid), len(grid[0])
        is_barrier = [[False] * cols for _ in range(rows)]
        for r, c in component_cells:
            is_barrier[r][c] = True
        visited = [[False] * cols for _ in range(rows)]
        q = deque()
        # Enqueue border non-barrier cells
        for r in range(rows):
            for c in (0, cols - 1):
                if not is_barrier[r][c] and not visited[r][c]:
                    visited[r][c] = True
                    q.append((r, c))
            if r in (0, rows - 1):
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
        # Count connected components of internal 0 cells
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

    def find_key_components(grid: List[List[int]]) -> List[dict]:
        rows, cols = len(grid), len(grid[0])
        visited = [[False] * cols for _ in range(rows)]
        components = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for r in range(rows):
            for c in range(cols):
                if 1 <= grid[r][c] <= 4 and not visited[r][c]:
                    color = grid[r][c]
                    cells: List[Tuple[int, int]] = []
                    stack = deque([(r, c)])
                    visited[r][c] = True
                    cells.append((r, c))
                    min_r, max_r, min_c, max_c = r, r, c, c
                    while stack:
                        x, y = stack.popleft()
                        min_r = min(min_r, x)
                        max_r = max(max_r, x)
                        min_c = min(min_c, y)
                        max_c = max(max_c, y)
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == color:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                                cells.append((nx, ny))
                    height = max_r - min_r + 1
                    if height == 3:
                        num_holes = count_holes(grid, cells)
                        components.append({
                            'color': color,
                            'holes': num_holes,
                            'min_r': min_r,
                            'min_c': min_c,
                            'cells': cells
                        })
        return components

    def find_orange_blobs(grid: List[List[int]]) -> List[List[Tuple[int, int]]]:
        rows, cols = len(grid), len(grid[0])
        visited = [[False] * cols for _ in range(rows)]
        blobs = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] > 4 and not visited[r][c]:
                    cells: List[Tuple[int, int]] = []
                    stack = deque([(r, c)])
                    visited[r][c] = True
                    cells.append((r, c))
                    while stack:
                        x, y = stack.popleft()
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] > 4:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                                cells.append((nx, ny))
                    blobs.append(cells)
        return blobs

    grid = copy_grid(g)
    key_components = find_key_components(g)
    hole_to_keys = defaultdict(list)
    for comp in key_components:
        hole_to_keys[comp['holes']].append(comp)
    key_map = {}
    for h, klist in hole_to_keys.items():
        if klist:
            best = min(klist, key=lambda k: (k['min_r'], k['min_c']))
            key_map[h] = best['color']
    orange_blobs = find_orange_blobs(g)
    for blob_cells in orange_blobs:
        if not blob_cells:
            continue
        num_holes = count_holes(g, blob_cells)
        if num_holes in key_map:
            new_color = key_map[num_holes]
            for r, c in blob_cells:
                grid[r][c] = new_color
        else:
            for r, c in blob_cells:
                grid[r][c] = 0
    return grid
```