```python
from typing import List, Tuple
from collections import deque

def flood_fill(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]]) -> List[Tuple[int, int]]:
    n = 30
    color = g[sr][sc]
    stack: List[Tuple[int, int]] = [(sr, sc)]
    visited[sr][sc] = True
    comp: List[Tuple[int, int]] = [(sr, sc)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.pop()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == color:
                visited[nx][ny] = True
                stack.append((nx, ny))
                comp.append((nx, ny))
    return comp

def find_legend_components(g: List[List[int]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    n = 30
    visited = [[False] * n for _ in range(n)]
    components = []
    for r in range(n):
        for c in range(n):
            if not visited[r][c] and g[r][c] >= 2 and g[r][c] != 5:
                comp = flood_fill(g, r, c, visited)
                min_r = min(x for x, y in comp)
                max_r = max(x for x, y in comp)
                min_c = min(y for x, y in comp)
                max_c = max(y for x, y in comp)
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                if height > 1 and width > 1:
                    components.append((g[r][c], comp))
    return components

def compute_enclosed_holes(g: List[List[int]], comp: List[Tuple[int, int]]) -> int:
    if not comp:
        return 0
    min_r = min(r for r, c in comp)
    max_r = max(r for r, c in comp)
    min_c = min(c for r, c in comp)
    max_c = max(c for r, c in comp)
    if min_r == max_r or min_c == max_c:
        return 0
    n = 30
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    q = deque()
    # Seed boundary 0s
    for r in [min_r, max_r]:
        for c in range(min_c, max_c + 1):
            if g[r][c] == 0 and 0 <= r < n and 0 <= c < n and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    for c in [min_c, max_c]:
        for r in range(min_r, max_r + 1):
            if g[r][c] == 0 and 0 <= r < n and 0 <= c < n and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    # Flood background 0s within bbox
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if min_r <= nx <= max_r and min_c <= ny <= max_c and 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
    # Count remaining 0 CCs in bbox (holes)
    h = 0
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if g[r][c] == 0 and not visited[r][c]:
                h += 1
                qq = deque([(r, c)])
                visited[r][c] = True
                while qq:
                    xx, yy = qq.popleft()
                    for dx, dy in directions:
                        nxx, nyy = xx + dx, yy + dy
                        if min_r <= nxx <= max_r and min_c <= nyy <= max_c and 0 <= nxx < n and 0 <= nyy < n and g[nxx][nyy] == 0 and not visited[nxx][nyy]:
                            visited[nxx][nyy] = True
                            qq.append((nxx, nyy))
    return h

def build_hole_to_color(g: List[List[int]]) -> dict[int, int]:
    legend_comps = find_legend_components(g)
    hole_to_color = {}
    for color, comp in legend_comps:
        h = compute_enclosed_holes(g, comp)
        hole_to_color[h] = color
    return hole_to_color

def process_five_components(g: List[List[int]], output: List[List[int]], hole_to_color: dict[int, int]):
    n = 30
    visited = [[False] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if g[r][c] == 5 and not visited[r][c]:
                comp = flood_fill(g, r, c, visited)
                h = compute_enclosed_holes(g, comp)
                if h in hole_to_color:
                    fill_color = hole_to_color[h]
                    for x, y in comp:
                        output[x][y] = fill_color
                else:
                    for x, y in comp:
                        output[x][y] = 0

def program(g: List[List[int]]) -> List[List[int]]:
    output = [row[:] for row in g]
    hole_to_color = build_hole_to_color(g)
    process_five_components(g, output, hole_to_color)
    return output
```