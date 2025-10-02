```python
from typing import List
from collections import Counter, deque

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    grid = [row[:] for row in g]
    flat = [grid[i][j] for i in range(rows) for j in range(cols)]
    c = Counter(flat)
    background = c.most_common(1)[0][0]
    non_bg = [k for k in c if k != background and c[k] > 0]
    if not non_bg:
        return grid
    special = min(non_bg, key=lambda k: c[k])
    special_cells = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == special]
    if not special_cells:
        return grid
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    ref = None
    for r, c in special_cells:
        is_isolated = True
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != background:
                is_isolated = False
                break
        if is_isolated:
            ref = (r, c)
            break
    if ref is None:
        return grid
    ref_r, ref_c = ref
    visited = [[False] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == background or visited[i][j]:
                continue
            component = []
            queue = deque([(i, j)])
            visited[i][j] = True
            component.append((i, j, grid[i][j]))
            while queue:
                r, c = queue.popleft()
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] != background:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
                        component.append((nr, nc, grid[nr][nc]))
            special_in_comp = [(r, c) for r, c, col in component if col == special]
            cs = set(c for _, c, _ in component)
            if special_in_comp:
                s_r, s_c = special_in_comp[0]
                if len(cs) == 1 and len(component) > 1:
                    delta_r = ref_r - s_r
                    delta_c = 0
                else:
                    delta_r = 0
                    delta_c = ref_c - s_c
            else:
                if not component:
                    continue
                sum_c = sum(c for _, c, _ in component)
                n = len(component)
                avg_c = sum_c / n
                delta_c = round(ref_c - avg_c)
                delta_r = 0
            for r, c, col in component:
                grid[r][c] = background
            for r, c, col in component:
                new_r = r + delta_r
                new_c = c + delta_c
                if 0 <= new_r < rows and 0 <= new_c < cols:
                    grid[new_r][new_c] = col
    return grid
```