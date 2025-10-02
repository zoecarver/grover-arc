```python
import collections
from typing import List, Tuple

def flood_outer_background(g: List[List[int]], h: int, w: int, directions4: List[Tuple[int, int]]) -> List[List[bool]]:
    outer_visited = [[False] * w for _ in range(h)]
    q = collections.deque()
    # Seed from all border cells that are 4
    for i in range(h):
        for j in (0, w-1):
            if g[i][j] == 4 and not outer_visited[i][j]:
                outer_visited[i][j] = True
                q.append((i, j))
    for j in range(w):
        for i in (0, h-1):
            if g[i][j] == 4 and not outer_visited[i][j]:
                outer_visited[i][j] = True
                q.append((i, j))
    while q:
        x, y = q.popleft()
        for dx, dy in directions4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and not outer_visited[nx][ny]:
                outer_visited[nx][ny] = True
                q.append((nx, ny))
    return outer_visited

def extract_one_components(g: List[List[int]], h: int, w: int, directions4: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    one_visited = [[False] * w for _ in range(h)]
    components = []
    for i in range(h):
        for j in range(w):
            if g[i][j] == 1 and not one_visited[i][j]:
                comp = []
                q = collections.deque([(i, j)])
                one_visited[i][j] = True
                comp.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions4:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 1 and not one_visited[nx][ny]:
                            one_visited[nx][ny] = True
                            q.append((nx, ny))
                            comp.append((nx, ny))
                components.append(comp)
    return components

def extract_holes_for_comp(comp: List[Tuple[int, int]], g: List[List[int]], outer_visited: List[List[bool]], h: int, w: int, directions4: List[Tuple[int, int]], hole_visited: set) -> List[List[Tuple[int, int]]]:
    adjacent_hole_starts = set()
    for x, y in comp:
        for dx, dy in directions4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and not outer_visited[nx][ny] and (nx, ny) not in hole_visited:
                adjacent_hole_starts.add((nx, ny))
    hole_comps = []
    for sx, sy in list(adjacent_hole_starts):
        if (sx, sy) in hole_visited:
            continue
        hole_comp = []
        q = collections.deque([(sx, sy)])
        hole_visited.add((sx, sy))
        hole_comp.append((sx, sy))
        while q:
            ux, uy = q.popleft()
            for dx, dy in directions4:
                nx, ny = ux + dx, uy + dy
                if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and not outer_visited[nx][ny] and (nx, ny) not in hole_visited:
                    hole_visited.add((nx, ny))
                    q.append((nx, ny))
                    hole_comp.append((nx, ny))
        hole_comps.append(hole_comp)
    return hole_comps

def fill_closed_shapes(out: List[List[int]], components: List[List[Tuple[int, int]]], g: List[List[int]], outer_visited: List[List[bool]], h: int, w: int) -> None:
    directions4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    hole_visited = set()
    for comp in components:
        holes = extract_holes_for_comp(comp, g, outer_visited, h, w, directions4, hole_visited)
        if holes:
            for x, y in comp:
                out[x][y] = 8
            for hole_comp in holes:
                for x, y in hole_comp:
                    out[x][y] = 6

def add_borders(out: List[List[int]], h: int, w: int) -> None:
    directions8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i in range(h):
        for j in range(w):
            if out[i][j] == 4:
                for dx, dy in directions8:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < h and 0 <= nj < w and out[ni][nj] in {1, 6, 8}:
                        out[i][j] = 2
                        break

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    out = [row[:] for row in g]
    directions4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    outer_visited = flood_outer_background(g, h, w, directions4)
    components = extract_one_components(g, h, w, directions4)
    fill_closed_shapes(out, components, g, outer_visited, h, w)
    add_borders(out, h, w)
    return out
```