```python
from typing import List, Set, Tuple
from collections import deque

def get_one_components(grid: List[List[int]]) -> List[Set[Tuple[int, int]]]:
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1 and not visited[i][j]:
                comp: Set[Tuple[int, int]] = set()
                stack = [(i, j)]
                visited[i][j] = True
                comp.add((i, j))
                while stack:
                    x, y = stack.pop()
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 1 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            comp.add((nx, ny))
                components.append(comp)
    return components

def remove_small_components(grid: List[List[int]], min_size: int = 2) -> List[List[int]]:
    out = [row[:] for row in grid]
    comps = get_one_components(grid)
    for comp in comps:
        if len(comp) < min_size:
            for i, j in comp:
                out[i][j] = 0
    return out

def get_background_positions(grid: List[List[int]]) -> Set[Tuple[int, int]]:
    rows = len(grid)
    if rows == 0:
        return set()
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    background: Set[Tuple[int, int]] = set()
    q = deque()
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Enqueue border 0s
    for i in range(rows):
        for j in (0, cols - 1):
            if grid[i][j] == 0 and not visited[i][j]:
                visited[i][j] = True
                q.append((i, j))
                background.add((i, j))
    for j in range(1, cols - 1):
        for i in (0, rows - 1):
            if grid[i][j] == 0 and not visited[i][j]:
                visited[i][j] = True
                q.append((i, j))
                background.add((i, j))
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
                background.add((nx, ny))
    return background

def get_zero_components(enclosed: Set[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    if not enclosed:
        return []
    rows = max(r for r, _ in enclosed) + 1 if enclosed else 0
    cols = max(c for _, c in enclosed) + 1 if enclosed else 0
    visited: Set[Tuple[int, int]] = set()
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for pos in list(enclosed):
        if pos in visited:
            continue
        comp: Set[Tuple[int, int]] = set()
        stack = [pos]
        visited.add(pos)
        comp.add(pos)
        while stack:
            x, y = stack.pop()
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                npos = (nx, ny)
                if npos in enclosed and npos not in visited:
                    visited.add(npos)
                    stack.append(npos)
                    comp.add(npos)
        components.append(comp)
    return components

def get_border_single_zeros(grid: List[List[int]]) -> List[Set[Tuple[int, int]]]:
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    border_singles = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Check sides
    for i in range(rows):
        for j in (0, cols - 1):
            if grid[i][j] == 0 and not visited[i][j]:
                # Check if single (no adjacent 0)
                is_single = all(
                    not (0 <= i + dx < rows and 0 <= j + dy < cols and grid[i + dx][j + dy] == 0)
                    for dx, dy in dirs
                )
                if is_single:
                    border_singles.append({(i, j)})
                visited[i][j] = True
    # Check top and bottom, excluding corners already checked
    for j in range(1, cols - 1):
        for i in (0, rows - 1):
            if grid[i][j] == 0 and not visited[i][j]:
                is_single = all(
                    not (0 <= i + dx < rows and 0 <= j + dy < cols and grid[i + dx][j + dy] == 0)
                    for dx, dy in dirs
                )
                if is_single:
                    border_singles.append({(i, j)})
                visited[i][j] = True
    return border_singles

def dilate_small_holes(grid: List[List[int]], small_hole_comps: List[Set[Tuple[int, int]]]) -> List[List[int]]:
    out = [row[:] for row in grid]
    if not small_hole_comps:
        return out
    all_hole_pixels: Set[Tuple[int, int]] = set()
    for comp in small_hole_comps:
        all_hole_pixels.update(comp)
    rows = len(grid)
    cols = len(grid[0])
    to_change: Set[Tuple[int, int]] = set()
    for comp in small_hole_comps:
        for r, c in comp:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        to_change.add((nr, nc))
    for r, c in to_change:
        if (r, c) not in all_hole_pixels:
            out[r][c] = 7
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = remove_small_components(g, min_size=2)
    background = get_background_positions(g)
    enclosed: Set[Tuple[int, int]] = set()
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 0 and (i, j) not in background:
                enclosed.add((i, j))
    hole_comps = get_zero_components(enclosed)
    small_internal = [comp for comp in hole_comps if len(comp) <= 3]
    border_singles = get_border_single_zeros(g)
    small_hole_comps = small_internal + border_singles
    out = dilate_small_holes(out, small_hole_comps)
    return out
```