```python
from typing import List
import collections

def count_colors(g: List[List[int]]) -> collections.Counter:
    return collections.Counter(c for row in g for c in row)

def identify_protected(g: List[List[int]]) -> int:
    counts = count_colors(g)
    return counts.most_common(1)[0][0] if counts else 0

def get_non_protected_neighbors(r: int, c: int, g: List[List[int]], protected: int, n: int, m: int) -> List[int]:
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighbors = []
    for dr, dc in directions:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < n and 0 <= nc < m and g[nr][nc] != protected:
            neighbors.append(g[nr][nc])
    return neighbors

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return g
    m = len(g[0])
    protected = identify_protected(g)
    current = [row[:] for row in g]
    while True:
        new_grid = [row[:] for row in current]
        changed = False
        for r in range(n):
            for c in range(m):
                if current[r][c] == protected:
                    continue
                neighbors = get_non_protected_neighbors(r, c, current, protected, n, m)
                if neighbors:
                    new_val = min(neighbors)
                    if new_val != current[r][c]:
                        new_grid[r][c] = new_val
                        changed = True
        current = new_grid
        if not changed:
            break
    return current
```