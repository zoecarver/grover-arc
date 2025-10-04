```python
from typing import List
import collections

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def count_one(r: int, c: int) -> int:
        cnt = 0
        for dr, dc in dirs4:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
                cnt += 1
        return cnt

    # Cleaning: remove 1s with <2 one neighbors
    cleaned = [row[:] for row in g]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 1 and count_one(r, c) < 2:
                cleaned[r][c] = 0

    # Find small components
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 0 and not visited[r][c] and count_one(r, c) >= 3:
                component = []
                q = collections.deque([(r, c)])
                visited[r][c] = True
                component.append((r, c))
                size = 1
                expanded = True
                while q and expanded and size <= 3:
                    expanded = False
                    new_q = collections.deque()
                    for cr, cc in list(q):
                        for dr, dc in dirs4:
                            nr = cr + dr
                            nc = cc + dc
                            if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 0 and not visited[nr][nc]:
                                n_one = count_one(nr, nc)
                                if n_one >= 1:
                                    visited[nr][nc] = True
                                    new_q.append((nr, nc))
                                    component.append((nr, nc))
                                    size += 1
                                    expanded = True
                                    if size > 3:
                                        break
                        if size > 3:
                            break
                    q = new_q
                if size <= 3:
                    is_special = (size == 1 and component[0][0] >= rows - 4 and
                                  (component[0][0] + 1 >= rows or g[component[0][0] + 1][component[0][1]] == 0))
                    components.append((component, is_special))

    # Collect to_set
    to_set = set()
    for component, is_special in components:
        for pr, pc in component:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr == 0 and dc == 0:
                        continue
                    if is_special and dr == -1:
                        continue
                    nr = pr + dr
                    nc = pc + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        to_set.add((nr, nc))
        if is_special and len(component) == 1:
            to_set.add(component[0])

    # Set to 7
    for nr, nc in to_set:
        cleaned[nr][nc] = 7

    # Set back non-special components to 0
    for component, is_special in components:
        if not is_special:
            for pr, pc in component:
                cleaned[pr][pc] = 0

    return cleaned
```