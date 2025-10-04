```python
from typing import List, Tuple
from collections import deque

def find_separator(g: List[List[int]]) -> Tuple[str, int]:
    n = len(g)
    # Check for horizontal separator
    for r in range(n):
        if all(g[r][c] == 1 for c in range(n)):
            return 'h', r
    # Check for vertical separator
    for c in range(n):
        if all(g[r][c] == 1 for r in range(n)):
            return 'v', c
    return None, -1

def get_picture_left(v_sep_index: int, g: List[List[int]]) -> bool:
    n = len(g)
    num_left = sum(1 for r in range(n) for c in range(v_sep_index) if g[r][c] == 5)
    num_right = sum(1 for r in range(n) for c in range(v_sep_index + 1, n) if g[r][c] == 5)
    return num_left >= num_right

def find_pre_components(g: List[List[int]]) -> List[Tuple[int, int, int]]:
    n = len(g)
    label = [[0] * n for _ in range(n)]
    components: List[Tuple[int, int, int]] = []
    next_label = 1
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(n):
        for j in range(n):
            if label[i][j] == 0 and g[i][j] != 0 and g[i][j] != 5:
                color = g[i][j]
                q = deque([(i, j)])
                label[i][j] = next_label
                size = 1
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and label[nx][ny] == 0 and g[nx][ny] != 0 and g[nx][ny] != 5:
                            label[nx][ny] = next_label
                            size += 1
                            q.append((nx, ny))
                components.append((next_label, color, size))
                next_label += 1
    return components

def get_legend_colors(components: List[Tuple[int, int, int]]) -> List[int]:
    if not components:
        return []
    # Find largest color 1 component to exclude
    max_size = 0
    excluded_label = -1
    for lid, col, sz in components:
        if col == 1 and sz > max_size:
            max_size = sz
            excluded_label = lid
    # Build unique colors in discovery order, skipping excluded
    color_set = set()
    legend = []
    # Sort by label to ensure discovery order
    components.sort(key=lambda x: x[0])
    for lid, col, sz in components:
        if lid != excluded_label and col not in color_set:
            color_set.add(col)
            legend.append(col)
    return legend

def flood_fill_region(output: List[List[int]], g: List[List[int]], visited: List[List[int]], sr: int, sc: int, color: int, in_picture: callable):
    n = len(g)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    stack = [(sr, sc)]
    visited[sr][sc] = True
    output[sr][sc] = color
    while stack:
        x, y = stack.pop()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 5 and not visited[nx][ny] and in_picture(nx, ny):
                visited[nx][ny] = True
                output[nx][ny] = color
                stack.append((nx, ny))

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    sep_type, sep_index = find_separator(g)
    has_sep = sep_type is not None
    picture_left = False
    if sep_type == 'v':
        picture_left = get_picture_left(sep_index, g)
    components = find_pre_components(g)
    legend_colors = get_legend_colors(components)
    output = [row[:] for row in g]
    if not legend_colors:
        return output
    visited = [[False] * n for _ in range(n)]
    component_id = 0
    num_colors = len(legend_colors)

    def in_picture_func(r: int, c: int) -> bool:
        if not has_sep:
            return True
        if sep_type == 'h':
            return r > sep_index
        else:
            return (c < sep_index) if picture_left else (c > sep_index)

    if sep_type == 'h' or not has_sep:
        start_r = sep_index + 1 if has_sep else 0
        for r in range(start_r, n):
            for c in range(n):
                if g[r][c] == 5 and not visited[r][c]:
                    col = legend_colors[component_id % num_colors]
                    flood_fill_region(output, g, visited, r, c, col, in_picture_func)
                    component_id += 1
    else:  # vertical
        start_c = 0 if picture_left else sep_index + 1
        end_c = sep_index if picture_left else n
        for r in range(n):
            for c in range(start_c, end_c):
                if g[r][c] == 5 and not visited[r][c]:
                    col = legend_colors[component_id % num_colors]
                    flood_fill_region(output, g, visited, r, c, col, in_picture_func)
                    component_id += 1
    return output
```