```python
from typing import List, Tuple, Set
from collections import deque

def get_border_8_positions(g: List[List[int]]) -> List[Tuple[int, int]]:
    n = len(g)
    positions: List[Tuple[int, int]] = []
    # Top row
    for j in range(n):
        if g[0][j] == 8:
            positions.append((0, j))
    # Bottom row
    for j in range(n):
        if g[n-1][j] == 8:
            positions.append((n-1, j))
    # Left column, excluding corners already added
    for i in range(1, n-1):
        if g[i][0] == 8:
            positions.append((i, 0))
    # Right column, excluding corners
    for i in range(1, n-1):
        if g[i][n-1] == 8:
            positions.append((i, n-1))
    return positions

def flood_reachable_8s(g: List[List[int]], starts: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    n = len(g)
    reachable: Set[Tuple[int, int]] = set()
    q = deque()
    for pos in starts:
        r, c = pos
        if pos not in reachable:
            reachable.add(pos)
            q.append(pos)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        cr, cc = q.popleft()
        for dr, dc in directions:
            nr = cr + dr
            nc = cc + dc
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 8 and (nr, nc) not in reachable:
                reachable.add((nr, nc))
                q.append((nr, nc))
    return reachable

def create_output_grid(g: List[List[int]], reachable: Set[Tuple[int, int]]) -> List[List[int]]:
    n = len(g)
    output = [row[:] for row in g]
    for i in range(n):
        for j in range(n):
            if output[i][j] == 8 and (i, j) not in reachable:
                output[i][j] = 2
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    starts = get_border_8_positions(g)
    reachable = flood_reachable_8s(g, starts)
    return create_output_grid(g, reachable)
```