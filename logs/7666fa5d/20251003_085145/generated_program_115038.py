```python
from collections import deque
from typing import List, Tuple, Set

def is_open(row: int, col: int, g: List[List[int]], n: int) -> bool:
    if not (0 <= row < n and 0 <= col < n):
        return True
    return g[row][col] == 8

def allow_vertical_move(cr: int, cc: int, g: List[List[int]], n: int) -> bool:
    left_open = is_open(cr, cc - 1, g, n)
    right_open = is_open(cr, cc + 1, g, n)
    return left_open and right_open

def allow_horizontal_move(cr: int, cc: int, nc: int, g: List[List[int]], n: int) -> bool:
    source_up = is_open(cr - 1, cc, g, n)
    source_down = is_open(cr + 1, cc, g, n)
    target_up = is_open(cr - 1, nc, g, n)
    target_down = is_open(cr + 1, nc, g, n)
    return source_up and source_down and target_up and target_down

def allow_move(cr: int, cc: int, dr: int, dc: int, g: List[List[int]], n: int) -> bool:
    nr = cr + dr
    nc = cc + dc
    if dr != 0:
        return allow_vertical_move(cr, cc, g, n)
    else:
        return allow_horizontal_move(cr, cc, nc, g, n)

def get_border_starts(g: List[List[int]], n: int) -> List[Tuple[int, int]]:
    starts: List[Tuple[int, int]] = []
    for c in range(n):
        if g[0][c] == 8:
            starts.append((0, c))
        if g[n - 1][c] == 8:
            starts.append((n - 1, c))
    for r in range(1, n - 1):
        if g[r][0] == 8:
            starts.append((r, 0))
        if g[r][n - 1] == 8:
            starts.append((r, n - 1))
    return starts

def flood_reachable(starts: List[Tuple[int, int]], g: List[List[int]], n: int) -> Set[Tuple[int, int]]:
    visited: Set[Tuple[int, int]] = set()
    queue = deque()
    for r, c in starts:
        pos = (r, c)
        if pos not in visited:
            visited.add(pos)
            queue.append(pos)
    dirs: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        cr, cc = queue.popleft()
        for dr, dc in dirs:
            nr = cr + dr
            nc = cc + dc
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 8 and (nr, nc) not in visited:
                if allow_move(cr, cc, dr, dc, g, n):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
    return visited

def fill_enclosed(g: List[List[int]], reachable: Set[Tuple[int, int]]) -> List[List[int]]:
    n = len(g)
    new_g = [row[:] for row in g]
    for r in range(n):
        for c in range(n):
            if new_g[r][c] == 8 and (r, c) not in reachable:
                new_g[r][c] = 2
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    starts = get_border_starts(g, n)
    reachable = flood_reachable(starts, g, n)
    return fill_enclosed(g, reachable)
```