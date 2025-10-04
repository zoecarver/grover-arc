```python
from typing import List
from collections import deque

def get_special_color(g: List[List[int]]) -> int:
    colors = set()
    for row in g:
        for val in row:
            if val != 8:
                colors.add(val)
    return max(colors) if colors else 8

def create_binary(g: List[List[int]], special: int, n: int) -> List[List[int]]:
    return [[1 if g[r][c] == special else 0 for c in range(n)] for r in range(n)]

def dilate(b: List[List[int]], n: int, iterations: int) -> List[List[int]]:
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for _ in range(iterations):
        new_b = [[0 for _ in range(n)] for _ in range(n)]
        for r in range(n):
            for c in range(n):
                if b[r][c] == 1:
                    new_b[r][c] = 1
                    continue
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and b[nr][nc] == 1:
                        new_b[r][c] = 1
                        break
        b = new_b
    return b

def flood_exterior(b: List[List[int]], n: int) -> List[List[bool]]:
    visited = [[False for _ in range(n)] for _ in range(n)]
    q = deque()
    dirs_flood = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(n):
        for c in [0, n - 1]:
            if b[r][c] == 0 and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    for c in range(1, n - 1):
        for r in [0, n - 1]:
            if b[r][c] == 0 and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in dirs_flood:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and b[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                q.append((nr, nc))
    return visited

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    n = len(g)
    special = get_special_color(g)
    if special == 8:
        return [row[:] for row in g]
    b = create_binary(g, special, n)
    b = dilate(b, n, 3)
    visited = flood_exterior(b, n)
    result = [row[:] for row in g]
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(n):
        for c in range(n):
            if g[r][c] != 8:
                continue
            if b[r][c] == 0 and not visited[r][c]:
                result[r][c] = 2
                continue
            if b[r][c] == 1:
                has_exterior = False
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < n and 0 <= nc < n):
                        has_exterior = True
                        break
                    if visited[nr][nc]:
                        has_exterior = True
                        break
                if not has_exterior:
                    result[r][c] = 2
    return result
```