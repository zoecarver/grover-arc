```python
from typing import List
from collections import deque

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    colors = set()
    for r in range(rows):
        for c in range(cols):
            val = g[r][c]
            if val > 0:
                colors.add(val)
    if not colors:
        return []
    fillers = [c for c in colors if c > 4]
    if not fillers:
        return []
    f = min(fillers)
    main_colors = [c for c in colors if c != f]

    def get_max_w1_height(color: int) -> int:
        visited = set()
        max_h = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for r in range(rows):
            for c in range(cols):
                if g[r][c] == color and (r, c) not in visited:
                    q = deque([(r, c)])
                    visited.add((r, c))
                    min_r, max_r = r, r
                    min_c, max_c = c, c
                    while q:
                        cr, cc = q.popleft()
                        for dr, dc in directions:
                            nr = cr + dr
                            nc = cc + dc
                            if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                min_r = min(min_r, nr)
                                max_r = max(max_r, nr)
                                min_c = min(min_c, nc)
                                max_c = max(max_c, nc)
                    w = max_c - min_c + 1
                    if w == 1:
                        h = max_r - min_r + 1
                        max_h = max(max_h, h)
        return max_h

    rep_h = {}
    for c in main_colors:
        h = get_max_w1_height(c)
        if h > 0:
            rep_h[c] = h

    items = [(h, c) for c, h in rep_h.items()]
    items.sort(key=lambda x: (x[0], x[1]))

    output = []
    for h, c in items:
        row_len = min(h, 4)
        row = [c] * row_len + [f] * (4 - row_len)
        output.append(row)
    return output
```