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

def get_row_info(component: List[Tuple[int, int]]) -> Tuple[int, int, Dict[int, Tuple[int, int, int]], int]:
    if not component:
        return 0, 0, {}, 0
    row_positions = {}
    min_r = min(p[0] for p in component)
    max_r = max(p[0] for p in component)
    max_width = 0
    for r in range(min_r, max_r + 1):
        cols = [p[1] for p in component if p[0] == r]
        if cols:
            min_c = min(cols)
            max_c = max(cols)
            width = max_c - min_c + 1
            row_positions[r] = (min_c, max_c, width)
            if width > max_width:
                max_width = width
    return min_r, max_r, row_positions, max_width

def detect_holes(g: List[List[int]], component: List[Tuple[int, int]], h: int, w: int) -> Tuple[bool, set]:
    comp_set = set(component)
    # Flood fill exterior 4's from edges (4-connect)
    exterior = set()
    visited = set()
    q = deque()
    # Add edge 4's
    for r in range(h):
        if g[r][0] == 4:
            pos = (r, 0)
            if pos not in visited:
                q.append(pos)
                visited.add(pos)
                exterior.add(pos)
        if g[r][w - 1] == 4:
            pos = (r, w - 1)
            if pos not in visited:
                q.append(pos)
                visited.add(pos)
                exterior.add(pos)
    for c in range(w):
        if g[0][c] == 4:
            pos = (0, c)
            if pos not in visited:
                q.append(pos)
                visited.add(pos)
                exterior.add(pos)
        if g[h - 1][c] == 4:
            pos = (h - 1, c)
            if pos not in visited:
                q.append(pos)
                visited.add(pos)
                exterior.add(pos)
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
    # Flood fill each unvisited adj start for holes
    has_hole = len(adj_starts) > 0
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
    # Process holed components first
    for comp in components:
        has_hole, holes = detect_holes(g, comp, h, w)
        if has_hole:
            for r, c in comp:
                out[r][c] = 8
            for r, c in holes:
                out[r][c] = 6
    # Global bordering: set 4's adjacent (8-way) to 1 or 8 to 2
    dirs8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(h):
        for c in range(w):
            if out[r][c] == 4:
                for dx, dy in dirs8:
                    nr, nc = r + dx, c + dy
                    if 0 <= nr < h and 0 <= nc < w and out[nr][nc] in (1, 8):
                        out[r][c] = 2
                        break
    # Cap top row of solid components if narrower
    for comp in components:
        # Check if still solid (has 1's)
        if not any(out[r][c] == 1 for r, c in comp):
            continue
        min_r, max_r, row_dict, max_width = get_row_info(comp)
        if min_r in row_dict:
            top_min_c, top_max_c, top_width = row_dict[min_r]
            if top_width < max_width:
                # Set original 1 positions in top row to 2
                for rr, cc in comp:
                    if rr == min_r and g[rr][cc] == 1:
                        out[rr][cc] = 2
    return out
```