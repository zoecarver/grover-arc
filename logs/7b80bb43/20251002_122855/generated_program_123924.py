```python
from typing import List
from collections import deque, Counter

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    colors = list(c.keys())
    bg = min(colors)
    fg = max(colors)
    h = len(g)
    w = len(g[0])
    grid = [row[:] for row in g]
    protected = set()
    # Horizontal fills
    for r in range(h):
        row = grid[r]
        i = 0
        while i < w:
            if row[i] != fg:
                i += 1
                continue
            start = i
            while i < w and row[i] == fg:
                i += 1
            len_left = i - start
            if i + 3 <= w and all(row[k] == bg for k in range(i, i + 3)) and row[i + 3] == fg:
                j = i + 3
                while j < w and row[j] == fg:
                    j += 1
                len_right = j - (i + 3)
                if len_left >= 5 and len_right >= 1:
                    for k in range(i, i + 3):
                        row[k] = fg
                    for k in range(i + 3, j):
                        protected.add((r, k))
                    i = j
                    continue
            i += 1
    # Vertical fills
    for c in range(w):
        i = 0
        while i < h:
            if grid[i][c] != fg:
                i += 1
                continue
            start = i
            while i < h and grid[i][c] == fg:
                i += 1
            len_upper = i - start
            if i + 3 <= h and all(grid[k][c] == bg for k in range(i, i + 3)) and grid[i + 3][c] == fg:
                j = i + 3
                while j < h and grid[j][c] == fg:
                    j += 1
                len_lower = j - (i + 3)
                if len_upper >= 5 and len_lower >= 1:
                    for k in range(i, i + 3):
                        grid[k][c] = fg
                    for k in range(i + 3, j):
                        protected.add((k, c))
                    i = j
                    continue
            i += 1
    # Original fg positions
    original_fg = set()
    for r in range(h):
        for cc in range(w):
            if g[r][cc] == fg:
                original_fg.add((r, cc))
    # Connected components on original
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for sr, sc in list(original_fg):
        if (sr, sc) in visited:
            continue
        component = []
        q = deque([(sr, sc)])
        visited.add((sr, sc))
        component.append((sr, sc))
        while q:
            cr, cc = q.popleft()
            for dr, dc in directions:
                nr = cr + dr
                nc = cc + dc
                if 0 <= nr < h and 0 <= nc < w and (nr, nc) in original_fg and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
                    component.append((nr, nc))
        size = len(component)
        if size <= 3 and not any(p in protected for p in component):
            for pr, pc in component:
                grid[pr][pc] = bg
    return grid
```