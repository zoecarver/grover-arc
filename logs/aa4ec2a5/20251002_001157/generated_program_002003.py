```python
from collections import deque
from typing import List, Set, Tuple

def find_enclosed(g: List[List[int]], rows: int, cols: int) -> List[List[int]]:
    temp = [row[:] for row in g]
    visited: Set[Tuple[int, int]] = set()
    q = deque()
    # Add border 4's
    for r in range(rows):
        for c in (0, cols - 1):
            pos = (r, c)
            if temp[r][c] == 4 and pos not in visited:
                visited.add(pos)
                q.append(pos)
    for c in range(1, cols - 1):
        for r in (0, rows - 1):
            pos = (r, c)
            if temp[r][c] == 4 and pos not in visited:
                visited.add(pos)
                q.append(pos)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            pos = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and temp[nr][nc] == 4 and pos not in visited:
                visited.add(pos)
                q.append(pos)
    for r in range(rows):
        for c in range(cols):
            pos = (r, c)
            if temp[r][c] == 4 and pos not in visited:
                temp[r][c] = 6
    return temp

def get_components(g: List[List[int]], rows: int, cols: int) -> List[Set[Tuple[int, int]]]:
    visited: Set[Tuple[int, int]] = set()
    comps: List[Set[Tuple[int, int]]] = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            pos = (r, c)
            if g[r][c] == 1 and pos not in visited:
                comp: Set[Tuple[int, int]] = set()
                q = deque([pos])
                visited.add(pos)
                comp.add(pos)
                while q:
                    cr, cc = q.popleft()
                    for dr, dc in dirs:
                        nr, nc = cr + dr, cc + dc
                        npos = (nr, nc)
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1 and npos not in visited:
                            visited.add(npos)
                            q.append(npos)
                            comp.add(npos)
                comps.append(comp)
    return comps

def has_hole(comp: Set[Tuple[int, int]], temp: List[List[int]], rows: int, cols: int) -> bool:
    for r, c in comp:
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and temp[nr][nc] == 6:
                    return True
    return False

def dilate(comp: Set[Tuple[int, int]], temp: List[List[int]], rows: int, cols: int) -> None:
    to_set: Set[Tuple[int, int]] = set()
    comp_set = comp
    for r, c in comp:
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in comp_set:
                    to_set.add((nr, nc))
    for r, c in to_set:
        if temp[r][c] == 4:
            temp[r][c] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    temp = find_enclosed(g, rows, cols)
    comps = get_components(g, rows, cols)
    for comp in comps:
        if has_hole(comp, temp, rows, cols):
            for r, c in comp:
                temp[r][c] = 8
        else:
            if len(comp) == 1:
                r, c = next(iter(comp))
                temp[r][c] = 2
                if r > 0:
                    for dc in range(-1, 2):
                        nc = c + dc
                        if 0 <= nc < cols and temp[r - 1][nc] == 4:
                            temp[r - 1][nc] = 2
                for dc in (-1, 1):
                    nc = c + dc
                    if 0 <= nc < cols and temp[r][nc] == 4:
                        temp[r][nc] = 2
        if len(comp) != 1:
            dilate(comp, temp, rows, cols)
    return temp
```