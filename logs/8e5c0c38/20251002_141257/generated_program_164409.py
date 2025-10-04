```python
from typing import List, Tuple, Set
from collections import Counter, deque

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_color_components(g: List[List[int]], bg: int) -> List[Set[Tuple[int, int]]]:
    h, w = len(g), len(g[0])
    visited = [[False for _ in range(w)] for _ in range(h)]
    components = []
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != bg and not visited[i][j]:
                component = set()
                queue = deque([(i, j)])
                visited[i][j] = True
                component.add((i, j))
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == g[i][j]:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                            component.add((nx, ny))
                if len(component) > 0:
                    components.append(component)
    return components

def get_bbox(component: Set[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    min_i = min(p[0] for p in component)
    max_i = max(p[0] for p in component)
    min_j = min(p[1] for p in component)
    max_j = max(p[1] for p in component)
    return min_i, min_j, max_i, max_j

def has_hole(g: List[List[int]], component: Set[Tuple[int, int]], bg: int, h: int, w: int) -> bool:
    # Simple check for enclosed bg, using flood fill from border to see if all bg are connected to border
    visited = [[False for _ in range(w)] for _ in range(h)]
    queue = deque()
    for i in range(h):
        for j in [0, w-1]:
            if g[i][j] == bg and not visited[i][j]:
                queue.append((i, j))
                visited[i][j] = True
    for j in range(w):
        for i in [0, h-1]:
            if g[i][j] == bg and not visited[i][j]:
                queue.append((i, j))
                visited[i][j] = True
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while queue:
        x, y = queue.popleft()
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == bg and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append((nx, ny))
    # Check if there is bg inside the component not visited (hole)
    for i, j in component:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                ni, nj = i + dx, j + dy
                if 0 <= ni < h and 0 <= nj < w and g[ni][nj] == bg and not visited[ni][nj]:
                    return True
    return False

def adjust_single_hole(g: List[List[int]], component: Set[Tuple[int, int]], hole_pos: Tuple[int, int], fg: int, bg: int) -> List[List[int]]:
    i, j = hole_pos
    new_g = [row[:] for row in g]
    # Left swap if possible
    if j - 1 in [p[1] for p in component if p[0] == i] and g[i][j - 2] == bg if j - 2 >= 0 else False:
        new_g[i][j - 2] = fg
        new_g[i][j - 1] = bg
    # Right swap
    if j + 1 in [p[1] for p in component if p[0] == i]:
        new_g[i][j] = fg
        new_g[i][j + 1] = bg
    return new_g

def find_single_hole(g: List[List[int]], component: Set[Tuple[int, int]], bg: int, h: int, w: int) -> Tuple[bool, Tuple[int, int]]:
    # Simple search for single pixel hole inside bbox
    min_i, min_j, max_i, max_j = get_bbox(component)
    for ci in range(min_i, max_i + 1):
        for cj in range(min_j, max_j + 1):
            if (ci, cj) not in component and g[ci][cj] == bg:
                # Check if enclosed single
                enclosed = True
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        ni, nj = ci + dx, cj + dy
                        if not (0 <= ni < h and 0 <= nj < w):
                            enclosed = False
                        elif (ni, nj) not in component and g[ni][nj] == bg:
                            enclosed = False
                if enclosed:
                    return True, (ci, cj)
    return False, None

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    h, w = len(g), len(g[0])
    new_g = [row[:] for row in g]
    components = get_color_components(new_g, bg)
    for comp in components:
        fg = g[list(comp)[0][0]][list(comp)[0][1]]
        has_h, hole_pos = find_single_hole(new_g, comp, bg, h, w)
        if has_h:
            new_g = adjust_single_hole(new_g, comp, hole_pos, fg, bg)
        # Remove single pixel in min_x if applicable
        min_i, min_j, _, _ = get_bbox(comp)
        candidates = [(p[0], p[1]) for p in comp if p[1] == min_j]
        if len(candidates) == 1:
            i, j = candidates[0]
            # Check if horizontal protrusion with 1 neighbor
            n = count_neighbors(new_g, i, j, fg)
            if n == 1:
                # Check if the neighbor is horizontal
                neighbors = []
                for di, dj in [(0,1), (0,-1), (1,0), (-1,0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < h and 0 <= nj < w and new_g[ni][nj] == fg:
                        neighbors.append((di, dj))
                if any(abs(di) == 0 for di, dj in neighbors):  # horizontal
                    if not has_h or i != hole_pos[0]:  # not in hole row
                        new_g[i][j] = bg
    return new_g

def count_neighbors(g: List[List[int]], i: int, j: int, color: int) -> int:
    h, w = len(g), len(g[0])
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    count = 0
    for di, dj in dirs:
        ni, nj = i + di, j + dj
        if 0 <= ni < h and 0 <= nj < w and g[ni][nj] == color:
            count += 1
    return count
```