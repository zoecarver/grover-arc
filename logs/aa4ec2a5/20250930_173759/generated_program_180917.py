```python
from typing import List, Tuple
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
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-connect
    for r in range(h):
        for c in range(w):
            if g[r][c] == 1 and not visited[r][c]:
                component = []
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 1 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(component)
    return components

def detect_holes(g: List[List[int]], component: List[Tuple[int, int]], h: int, w: int) -> Tuple[bool, set]:
    comp_set = set(component)
    # Flood fill exterior 4's from edges (4-connect)
    exterior = set()
    visited = set()
    q = deque()
    # Add edge 4's
    for r in range(h):
        if g[r][0] == 4 and (r, 0) not in visited:
            q.append((r, 0))
            visited.add((r, 0))
            exterior.add((r, 0))
        if g[r][w - 1] == 4 and (r, w - 1) not in visited:
            q.append((r, w - 1))
            visited.add((r, w - 1))
            exterior.add((r, w - 1))
    for c in range(w):
        if g[0][c] == 4 and (0, c) not in visited:
            q.append((0, c))
            visited.add((0, c))
            exterior.add((0, c))
        if g[h - 1][c] == 4 and (h - 1, c) not in visited:
            q.append((h - 1, c))
            visited.add((h - 1, c))
            exterior.add((h - 1, c))
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in dirs4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and (nx, ny) not in visited and (nx, ny) not in comp_set:
                visited.add((nx, ny))
                exterior.add((nx, ny))
                q.append((nx, ny))
    # Find starting points for holes: 4-adj to component, not exterior
    adj_starts = set()
    for r, c in component:
        for dx, dy in dirs4:
            nr, nc = r + dx, c + dy
            if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 4 and (nr, nc) not in exterior:
                adj_starts.add((nr, nc))
    # Flood fill each unvisited adj start for holes (4-connect)
    hole_positions = set()
    hole_visited = set()
    for start in adj_starts:
        if start in hole_visited:
            continue
        curr_q = deque([start])
        hole_visited.add(start)
        hole_positions.add(start)
        while curr_q:
            x, y = curr_q.popleft()
            for dx, dy in dirs4:
                nx, ny = x + dx, y + dy
                if (0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and
                    (nx, ny) not in exterior and (nx, ny) not in comp_set and (nx, ny) not in hole_visited):
                    hole_visited.add((nx, ny))
                    hole_positions.add((nx, ny))
                    curr_q.append((nx, ny))
    return bool(hole_positions), hole_positions

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    h = len(g)
    if h == 0:
        return out
    w = len(g[0])
    components = find_components(g)
    for comp in components:
        has_hole, holes = detect_holes(g, comp, h, w)
        if has_hole:
            for r, c in comp:
                out[r][c] = 8
            for r, c in holes:
                out[r][c] = 6
    # Bordering using 8-connectivity to 1 or 8
    dirs8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(h):
        for c in range(w):
            if out[r][c] == 4:
                adjacent = any(
                    0 <= r + dr < h and 0 <= c + dc < w and out[r + dr][c + dc] in (1, 8)
                    for dr, dc in dirs8
                )
                if adjacent:
                    out[r][c] = 2
    return out
```