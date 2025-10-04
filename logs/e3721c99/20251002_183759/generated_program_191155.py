```python
from collections import deque
from typing import List

def get_palette(grid: List[List[int]]) -> List[int]:
    palette = []
    seen = set()
    for r in range(30):
        i = 0
        while i < 30:
            if grid[r][i] == 0:
                i += 1
                continue
            c = grid[r][i]
            if c > 4 or c in seen:
                # skip the run
                while i < 30 and grid[r][i] == c:
                    i += 1
                continue
            # c is 1-4, not seen
            start = i
            while i < 30 and grid[r][i] == c:
                i += 1
            length = i - start
            if length >= 3:
                seen.add(c)
                palette.append(c)
    return palette

def fill_components(grid: List[List[int]], palette: List[int]) -> List[List[int]]:
    out = [row[:] for row in grid]
    if not palette:
        return out
    visited = [[False for _ in range(30)] for _ in range(30)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    color_index = 0
    for r in range(30):
        for c in range(30):
            if out[r][c] > 4 and not visited[r][c]:
                fill_c = palette[color_index % len(palette)]
                color_index += 1
                q = deque([(r, c)])
                visited[r][c] = True
                out[r][c] = fill_c
                while q:
                    cr, cc = q.popleft()
                    for dr, dc in directions:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < 30 and 0 <= nc < 30 and out[nr][nc] > 4 and not visited[nr][nc]:
                            visited[nr][nc] = True
                            out[nr][nc] = fill_c
                            q.append((nr, nc))
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    palette = get_palette(g)
    return fill_components(g, palette)
```