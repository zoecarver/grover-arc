```python
from typing import List
from collections import defaultdict

def identify_colors(g: List[List[int]]) -> tuple:
    """Identify background, special, and ink colors based on frequency."""
    counts = defaultdict(int)
    n, m = len(g), len(g[0])
    for i in range(n):
        for j in range(m):
            counts[g[i][j]] += 1
    all_colors = list(counts.keys())
    if len(all_colors) < 2:
        return 0, 0, []
    background = max(all_colors, key=lambda c: counts[c])
    remaining = [c for c in all_colors if c != background]
    if not remaining:
        return background, 0, []
    special = max(remaining, key=lambda c: counts[c])
    ink = [c for c in remaining if c != special]
    return background, special, ink

def spread_colors(g: List[List[int]], background: int, special: int, ink: List[int]) -> List[List[int]]:
    """Spread ink colors into special cells iteratively if unique candidate."""
    n, m = len(g), len(g[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    new_g = [row[:] for row in g]
    changed = True
    while changed:
        changed = False
        old_g = [row[:] for row in new_g]
        for i in range(n):
            for j in range(m):
                if old_g[i][j] == special:
                    candidates = set()
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < n and 0 <= nj < m:
                            neigh = old_g[ni][nj]
                            if neigh != special and neigh != background and neigh in ink:
                                candidates.add(neigh)
                    if len(candidates) == 1:
                        new_g[i][j] = next(iter(candidates))
                        changed = True
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: identify colors and spread."""
    background, special, ink = identify_colors(g)
    if special == 0:
        return g  # No special, return as is
    return spread_colors(g, background, special, ink)
```