```python
from typing import List, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    positions = [(r, c, g[r][c]) for r in range(len(g)) for c in range(len(g[0])) if g[r][c] != 0]
    components = find_connected_components(g, positions)
    main_component = max(components, key=len)
    min_r = min(r for r, _, _ in main_component)
    max_r = max(r for r, _, _ in main_component)
    min_c = min(c for _, c, _ in main_component)
    max_c = max(c for _, c, _ in main_component)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    side = max(h, w)
    new_grid = [[0] * side for _ in range(side)]
    for r, c, val in main_component:
        new_r = r - min_r
        new_c = c - min_c
        new_grid[new_r][new_c] = val
    return new_grid

def find_connected_components(g: List[List[int]], positions: List[Tuple[int, int, int]]) -> List[List[Tuple[int, int, int]]]:
    n = len(g)
    m = len(g[0])
    visited = [[False] * m for _ in range(n)]
    components = []
    for start_r, start_c, start_val in positions:
        if visited[start_r][start_c]:
            continue
        component = []
        stack = [(start_r, start_c, start_val)]
        visited[start_r][start_c] = True
        while stack:
            cr, cc, cval = stack.pop()
            component.append((cr, cc, cval))
            # Unrolled 8 directions to avoid nested loops
            for dr, dc in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                nr = cr + dr
                nc = cc + dc
                if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc] and g[nr][nc] != 0:
                    visited[nr][nc] = True
                    stack.append((nr, nc, g[nr][nc]))
        if component:
            components.append(component)
    return components
```