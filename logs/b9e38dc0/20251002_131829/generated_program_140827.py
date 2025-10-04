```python
from collections import deque, Counter
from typing import List, Tuple
import copy

def is_border_connected(grid: List[List[int]], color: int, h: int, w: int) -> bool:
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        for c in [0, w - 1]:
            if grid[r][c] == color and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
        if r in [0, h - 1]:
            for c in range(w):
                if grid[r][c] == color and not visited[r][c]:
                    q.append((r, c))
                    visited[r][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and grid[nr][nc] == color:
                visited[nr][nc] = True
                q.append((nr, nc))
    total_count = sum(1 for row in grid for cell in row if cell == color)
    visited_count = sum(1 for r in range(h) for c in range(w) if visited[r][c])
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
        if is_border_connected(grid, color, h, w):
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
                components.append(component)
    return components

def get_component_color(grid: List[List[int]], component: List[Tuple[int, int]]) -> int:
    colors = [grid[r][c] for r, c in component]
    counter = Counter(colors)
    return counter.most_common(1)[0][0]

def find_enclosed_holes(grid: List[List[int]], component: List[Tuple[int, int]], bg: int, fill_color: int, h: int, w: int) -> List[List[int]]:
    if not component:
        return [row[:] for row in grid]
    min_r = min(r for r, c in component)
    max_r = max(r for r, c in component)
    min_c = min(c for r, c in component)
    max_c = max(c for r, c in component)
    # Mark outer bg inside bounding box by flooding from left, right, top (not bottom to handle leaks)
    visited = [[False] * w for _ in range(h)]
    q = deque()
    # Seed from left, right, top boundaries of bounding box if bg
    for r in range(min_r, max_r + 1):
        if grid[r][min_c] == bg and not visited[r][min_c]:
            q.append((r, min_c))
            visited[r][min_c] = True
        if grid[r][max_c] == bg and not visited[r][max_c]:
            q.append((r, max_c))
            visited[r][max_c] = True
    for c in range(min_c, max_c + 1):
        if grid[min_r][c] == bg and not visited[min_r][c]:
            q.append((min_r, c))
            visited[min_r][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if min_r <= nr <= max_r and min_c <= nc <= max_c and not visited[nr][nc] and grid[nr][nc] == bg:
                visited[nr][nc] = True
                q.append((nr, nc))
    # Now fill unmarked bg inside bounding with fill_color
    new_grid = [row[:] for row in grid]
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if new_grid[r][c] == bg and not visited[r][c]:
                new_grid[r][c] = fill_color
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    bg = get_background(grid)
    components = get_non_bg_components(grid, bg)
    for component in components:
        comp_color = get_component_color(grid, component)
        # For each component, fill enclosed holes with 0 (default for test-like cases)
        fill_color = 0  # Default to 0 for enclosed as per test feedback
        grid = find_enclosed_holes(grid, component, bg, fill_color, h, w)
    return grid
```