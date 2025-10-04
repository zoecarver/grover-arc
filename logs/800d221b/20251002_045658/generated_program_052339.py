```python
from typing import List
from collections import defaultdict

def identify_colors(g: List[List[int]]) -> tuple:
    """Identify protected and replaceable colors based on frequency and max."""
    colors = set(c for row in g for c in row)
    if len(colors) < 2:
        return max(colors) if colors else 0, None
    sorted_colors = sorted(colors, reverse=True)
    protected = sorted_colors[0]
    replaceable = sorted_colors[1] if len(sorted_colors) > 1 else None
    return protected, replaceable

def get_non_protected_neighbors(i: int, j: int, g: List[List[int]], n: int, m: int, protected: int) -> List[int]:
    """Get colors of non-protected neighbors."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < m and g[ni][nj] != protected:
            neighbors.append(g[ni][nj])
    return neighbors

def update_replaceable(g: List[List[int]], protected: int, original_replaceable: List[List[bool]], n: int, m: int) -> List[List[int]]:
    """Update one iteration for originally replaceable positions to min non-protected neighbor."""
    new_g = [row[:] for row in g]
    for i in range(n):
        for j in range(m):
            if original_replaceable[i][j]:
                neighbors = get_non_protected_neighbors(i, j, g, n, m, protected)
                if neighbors:
                    new_g[i][j] = min(neighbors)
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: iteratively update originally replaceable cells to the minimum non-protected neighbor color."""
    n = len(g)
    if n == 0:
        return g
    m = len(g[0])
    protected, replaceable = identify_colors(g)
    if replaceable is None:
        return [row[:] for row in g]
    original_replaceable = [[g[i][j] == replaceable for j in range(m)] for i in range(n)]
    current = [row[:] for row in g]
    for _ in range(n):
        new_current = update_replaceable(current, protected, original_replaceable, n, m)
        if new_current == current:
            break
        current = new_current
    return current
```