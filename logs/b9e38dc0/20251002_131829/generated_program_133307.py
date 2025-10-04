```python
import copy
from collections import deque, Counter

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(g)
    if not g or not g[0]:
        return grid
    h = len(grid)
    w = len(grid[0])
    bg = grid[0][0]
    flat = [cell for row in grid for cell in row]
    freq = Counter(flat)
    non_bg = {k: v for k, v in freq.items() if k != bg and v > 0}
    if not non_bg:
        return grid
    barrier = max(non_bg, key=non_bg.get)
    fill = None
    for r in range(h):
        for c in range(w):
            if grid[r][c] != bg and grid[r][c] != barrier:
                adjacent_barrier = any(
                    0 <= r + dr < h and 0 <= c + dc < w and grid[r + dr][c + dc] == barrier
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                )
                if adjacent_barrier:
                    fill = grid[r][c]
                    break
        if fill:
            break
    if not fill:
        return grid
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        for c in range(w):
            if grid[r][c] == fill and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and grid[nr][nc] == bg:
                grid[nr][nc] = fill
                visited[nr][nc] = True
                q.append((nr, nc))
    return grid
```