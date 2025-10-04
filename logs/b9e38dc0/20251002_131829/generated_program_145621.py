```python
from collections import deque, Counter
from copy import deepcopy
from typing import List, Tuple

def is_border_connected(grid: List[List[int]], color: int, h: int, w: int) -> bool:
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        for c in [0, w - 1]:
            if grid[r][c] == color and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
    for c in range(w):
        if grid[0][c] == color and not visited[0][c]:
            q.append((0, c))
            visited[0][c] = True
        if grid[h - 1][c] == color and not visited[h - 1][c]:
            q.append((h - 1, c))
            visited[h - 1][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and grid[nr][nc] == color:
                visited[nr][nc] = True
                q.append((nr, nc))
    total_count = sum(1 for row in grid for cell in row if cell == color)
    visited_count = sum(1 for row in visited for cell in row if cell)
    return visited_count == total_count

def get_background(grid: List[List[int]]) -> int:
    h = len(grid)
    if h == 0:
        return 0
    w = len(grid[0])
    flat = [cell for row in grid for cell in row]
    counter = Counter(flat)
    candidates = []
    for color in counter:
        if is_border_connected(grid, color, h, w):
            candidates.append((counter[color], color))
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    return 0

def get_freq(grid: List[List[int]]) -> Counter:
    flat = [cell for row in grid for cell in row]
    return Counter(flat)

def program(g: List[List[int]]) -> List[List[int]]:
    grid = deepcopy(g)
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    bg = get_background(grid)
    if bg == 0:
        freq = get_freq(grid)
        non_zero = [c for c in freq if c != 0]
        if not non_zero:
            return grid
        fill_color = min(non_zero)
        visited = [[False] * w for _ in range(h)]
        q = deque()
        for r in range(h):
            if grid[r][0] == 0 and not visited[r][0]:
                q.append((r, 0))
                visited[r][0] = True
            if grid[r][w - 1] == 0 and not visited[r][w - 1]:
                q.append((r, w - 1))
                visited[r][w - 1] = True
        for c in range(w):
            if grid[0][c] == 0 and not visited[0][c]:
                q.append((0, c))
                visited[0][c] = True
            if grid[h - 1][c] == 0 and not visited[h - 1][c]:
                q.append((h - 1, c))
                visited[h - 1][c] = True
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while q:
            r, c = q.popleft()
            grid[r][c] = fill_color
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and grid[nr][nc] == 0:
                    visited[nr][nc] = True
                    q.append((nr, nc))
        return grid
    # For other cases, find enclosed bg and fill with 0
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        if grid[r][0] == bg and not visited[r][0]:
            q.append((r, 0))
            visited[r][0] = True
        if grid[r][w - 1] == bg and not visited[r][w - 1]:
            q.append((r, w - 1))
            visited[r][w - 1] = True
    for c in range(w):
        if grid[0][c] == bg and not visited[0][c]:
            q.append((0, c))
            visited[0][c] = True
        if grid[h - 1][c] == bg and not visited[h - 1][c]:
            q.append((h - 1,