```python
from typing import List

def get_main_component(g: List[List[int]], h: int, w: int) -> List[tuple[int, int]]:
    component = []
    if h == 0 or w == 0 or g[0][0] != 8:
        return component
    visited = [[False] * w for _ in range(h)]
    stack = [(0, 0)]
    visited[0][0] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        r, c = stack.pop()
        component.append((r, c))
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] == 8:
                visited[nr][nc] = True
                stack.append((nr, nc))
    return component

def find_connected_component(g: List[List[int]], start_r: int, start_c: int, color: int, visited: List[List[bool]]) -> List[tuple[int, int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    component = []
    if not (0 <= start_r < h and 0 <= start_c < w) or g[start_r][start_c] != color or visited[start_r][start_c]:
        return component
    stack = [(start_r, start_c)]
    visited[start_r][start_c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        r, c = stack.pop()
        component.append((r, c))
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] == color:
                visited[nr][nc] = True
                stack.append((nr, nc))
    return component

def is_adjacent_to_main(blue_comp: List[tuple[int, int]], main_set: set[tuple[int, int]], g: List[List[int]], h: int, w: int) -> bool:
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r, c in blue_comp:
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == 8 and (nr, nc) in main_set:
                return True
    return False

def is_boundary_pos(r: int, c: int, main_set: set[tuple[int, int]], h: int, w: int) -> bool:
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            nr = r + dr
            nc = c + dc
            if not (0 <= nr < h and 0 <= nc < w) or (nr, nc) not in main_set:
                return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    main_comp = get_main_component(g, h, w)
    main_set = set(main_comp)
    output = [row[:] for row in g]
    visited = [[False] * w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c] == 1 and not visited[r][c]:
                blue_comp = find_connected_component(g, r, c, 1, visited)
                if not is_adjacent_to_main(blue_comp, main_set, g, h, w):
                    for br, bc in blue_comp:
                        output[br][bc] = 8
    for r, c in main_comp:
        if is_boundary_pos(r, c, main_set, h, w):
            output[r][c] = 7
        else:
            output[r][c] = 8
    return output
```