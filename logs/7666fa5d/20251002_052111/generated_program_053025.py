```python
from typing import List
from collections import deque

def get_special_color(g: List[List[int]]) -> int:
    for row in g:
        for cell in row:
            if cell != 8:
                return cell
    return 8

def dilate(boundary: List[List[int]], iterations: int = 1) -> List[List[int]]:
    n = len(boundary)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for _ in range(iterations):
        new_b = [row[:] for row in boundary]
        for r in range(n):
            for c in range(n):
                if boundary[r][c] == 0:
                    for dr, dc in directions:
                        nr = r + dr
                        nc = c + dc
                        if 0 <= nr < n and 0 <= nc < n and boundary[nr][nc] == 1:
                            new_b[r][c] = 1
                            break
        boundary = new_b
    return boundary

def flood_background(boundary: List[List[int]]) -> List[List[bool]]:
    n = len(boundary)
    visited = [[False] * n for _ in range(n)]
    queue = deque()
    for r in range(n):
        for c in (0, n - 1):
            if boundary[r][c] == 0 and not visited[r][c]:
                visited[r][c] = True
                queue.append((r, c))
    for c in range(n):
        for r in (0, n - 1):
            if boundary[r][c] == 0 and not visited[r][c]:
                visited[r][c] = True
                queue.append((r, c))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < n and 0 <= nc < n and boundary[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc))
    return visited

def is_inside(boundary: List[List[int]], visited: List[List[bool]], r: int, c: int) -> bool:
    return boundary[r][c] == 0 and not visited[r][c]

def has_inside_neighbor(r: int, c: int, n: int, boundary: List[List[int]], visited: List[List[bool]]) -> bool:
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < n and 0 <= nc < n and is_inside(boundary, visited, nr, nc):
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    special_color = get_special_color(g)
    result = [row[:] for row in g]
    boundary = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if g[r][c] == special_color:
                boundary[r][c] = 1
    boundary = dilate(boundary)
    visited = flood_background(boundary)
    for r in range(n):
        for c in range(n):
            if g[r][c] == 8 and is_inside(boundary, visited, r, c):
                result[r][c] = 2
    for r in range(n):
        for c in range(n):
            if g[r][c] == 8 and boundary[r][c] == 1 and has_inside_neighbor(r, c, n, boundary, visited):
                result[r][c] = 2
    return result
```