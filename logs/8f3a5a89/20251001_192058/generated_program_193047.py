```python
import collections

def get_sources(grid: List[List[int]]) -> set:
    sources = set()
    n = len(grid)
    # left border
    for i in range(n):
        if grid[i][0] == 8:
            sources.add((i, 0))
    # top left segment
    j = 0
    while j < n and grid[0][j] == 8:
        sources.add((0, j))
        j += 1
    # bottom left segment
    i = n - 1
    j = 0
    if grid[i][0] == 6:
        j = 1
    while j < n and grid[i][j] == 8:
        sources.add((i, j))
        j += 1
    return sources

def mark_exterior(grid: List[List[int]], sources: set) -> set:
    n = len(grid)
    visited = set(sources)
    queue = collections.deque(sources)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        ci, cj = queue.popleft()
        for di, dj in dirs:
            ni = ci + di
            nj = cj + dj
            if 0 <= ni < n and 0 <= nj < n and grid[ni][nj] == 8 and (ni, nj) not in visited:
                visited.add((ni, nj))
                queue.append((ni, nj))
    return visited

def is_adjacent_to_one(grid: List[List[int]], i: int, j: int) -> bool:
    n = len(grid)
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni = i + di
            nj = j + dj
            if 0 <= ni < n and 0 <= nj < n and grid[ni][nj] == 1:
                return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    sources = get_sources(g)
    exterior = mark_exterior(g, sources)
    for i in range(n):
        for j in range(n):
            if out[i][j] == 8:
                is_source = (i, j) in sources
                is_exterior = (i, j) in exterior
                adj_to_one = is_adjacent_to_one(g, i, j)
                is_top = i == 0
                is_bottom = i == n - 1
                is_left = j == 0
                is_right = j == n - 1
                if is_source or (is_exterior and adj_to_one) or (is_exterior and (is_top or is_bottom or is_left or is_right)):
                    out[i][j] = 7
    return out
```