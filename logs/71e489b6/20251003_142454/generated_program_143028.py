```python
from typing import List
import collections

def remove_thin_protrusions(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 1:
                num_zero = 0
                for dr, dc in dirs4:
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 0:
                        num_zero += 1
                if num_zero >= 3:
                    new_g[r][c] = 0
    return new_g

def remove_isolated(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 1:
                num_one = 0
                for dr, dc in dirs4:
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
                        num_one += 1
                if num_one == 0:
                    new_g[r][c] = 0
    return new_g

def color_adjacent_to_small_zeros(g: List[List[int]], modified_g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    new_g = [row[:] for row in modified_g]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 0 and not visited[r][c]:
                q = collections.deque([(r, c)])
                visited[r][c] = True
                component_size = 1
                while q:
                    cr, cc = q.popleft()
                    for dr, dc in dirs4:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 0 and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                            component_size += 1
                if component_size <= 2:
                    # find all cells in component? But to avoid storing, we can re-BFS or store
                    # but to simplify, since small, we can re do BFS to collect positions
                    # wait, to avoid second BFS, let's collect during first
    # Redo with collection
    visited = [[False] * cols for _ in range(rows)]  # reset
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 0 and not visited[r][c]:
                component = []
                q = collections.deque([(r, c)])
                visited[r][c] = True
                component.append((r, c))
                component_size = 1
                while q:
                    cr, cc = q.popleft()
                    for dr, dc in dirs4:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 0 and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                            component.append((nr, nc))
                            component_size += 1
                if component_size <= 2:
                    for pr, pc in component:
                        for dr in range(-1, 2):
                            for dc in range(-1, 2):
                                if dr == 0 and dc == 0:
                                    continue
                                nr = pr + dr
                                nc = pc + dc
                                if 0 <= nr < rows and 0 <= nc < cols and new_g[nr][nc] == 1:
                                    new_g[nr][nc] = 7
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    temp_g = remove_thin_protrusions(g)
    temp_g = remove_isolated(temp_g)
    result = color_adjacent_to_small_zeros(g, temp_g)
    return result
```