```python
from typing import List, Tuple, Set
import collections
from collections import Counter

def count_colors(g: List[List[int]]) -> Counter:
    """Count frequency of each color in the grid."""
    return Counter(c for row in g for c in row)

def identify_protected(g: List[List[int]]) -> int:
    """Identify the most frequent color as protected."""
    counts = count_colors(g)
    if not counts:
        return 0
    return counts.most_common(1)[0][0]

def get_neighbors(i: int, j: int, g: List[List[int]], n: int, m: int, protected: int) -> List[int]:
    """Get all adjacent colors, excluding protected."""
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighbors = []
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < m and g[ni][nj] != protected:
            neighbors.append(g[ni][nj])
    return neighbors if neighbors else [g[i][j]]  # Fallback to self if isolated

def update_grid(g: List[List[int]], protected: int) -> List[List[int]]:
    """Update the grid iteratively using max non-protected neighbor until stable."""
    n, m = len(g), len(g[0])
    while True:
        new_g = [row[:] for row in g]
        changed = False
        for i in range(n):
            for j in range(m):
                if g[i][j] == protected:
                    continue
                neighbors = get_neighbors(i, j, g, n, m, protected)
                if neighbors:
                    new_val = max(neighbors)
                    if new_val != g[i][j]:
                        new_g[i][j] = new_val
                        changed = True
        g = new_g
        if not changed:
            break
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: protect most frequent color, update others to max non-protected neighbor iteratively."""
    protected = identify_protected(g)
    return update_grid(g, protected)
```