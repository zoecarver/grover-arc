```python
from typing import List

def find_separator(n: int, g: List[List[int]]) -> tuple:
    sep_type = None
    sep_index = -1
    for r in range(n):
        if all(g[r][c] == 1 for c in range(n)):
            sep_type = 'h'
            sep_index = r
            break
    if sep_type is None:
        for c in range(n):
            if all(g[r][c] == 1 for r in range(n)):
                sep_type = 'v'
                sep_index = c
                break
    return sep_type, sep_index

def extract_legend_colors(n: int, g: List[List[int]], sep_type: str, sep_index: int) -> List[int]:
    legend_colors = []
    seen = set()
    if sep_type == 'h':
        for r in range(sep_index):
            for c in range(n):
                col = g[r][c]
                if col != 0 and col != 5 and col not in seen:
                    seen.add(col)
                    legend_colors.append(col)
    elif sep_type == 'v':
        for r in range(n):
            for c in range(sep_index + 1, n):
                col = g[r][c]
                if col != 0 and col != 5 and col not in seen:
                    seen.add(col)
                    legend_colors.append(col)
    return legend_colors

def color_picture_side(n: int, g: List[List[int]], output: List[List[int]], legend_colors: List[int], sep_type: str, sep_index: int) -> None:
    if not legend_colors:
        return
    visited = [[False] * n for _ in range(n)]
    component_id = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if sep_type == 'h':
        for r in range(sep_index + 1, n):
            for c in range(n):
                if g[r][c] == 5 and not visited[r][c]:
                    color = legend_colors[component_id % len(legend_colors)]
                    self_fill(n, g, output, visited, color, r, c, directions)
                    component_id += 1
    elif sep_type == 'v':
        for r in range(n):
            for c in range(sep_index):
                if g[r][c] == 5 and not visited[r][c]:
                    color = legend_colors[component_id % len(legend_colors)]
                    self_fill(n, g, output, visited, color, r, c, directions)
                    component_id += 1

def self_fill(n: int, g: List[List[int]], output: List[List[int]], visited: List[List[bool]], color: int, sr: int, sc: int, directions: List[tuple]) -> None:
    stack = [(sr, sc)]
    visited[sr][sc] = True
    output[sr][sc] = color
    while stack:
        x, y = stack.pop()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 5 and not visited[nx][ny]:
                visited[nx][ny] = True
                output[nx][ny] = color
                stack.append((nx, ny))

def program(g: List[List[int]]) -> List[List[int]]:
    n = 30
    output = [row[:] for row in g]
    sep_type, sep_index = find_separator(n, g)
    if sep_type is None:
        return output
    legend_colors = extract_legend_colors(n, g, sep_type, sep_index)
    color_picture_side(n, g, output, legend_colors, sep_type, sep_index)
    return output
```