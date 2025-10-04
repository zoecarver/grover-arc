```python
from typing import List
from collections import deque

def get_distinct_colors(g: List[List[int]]) -> set:
    return {cell for row in g for cell in row if cell > 0}

def flood_fill_size(g: List[List[int]], start_r: int, start_c: int, c: int, visited: List[List[bool]]) -> int:
    height = len(g)
    width = len(g[0])
    queue = deque([(start_r, start_c)])
    visited[start_r][start_c] = True
    size = 1
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while queue:
        r, colu = queue.popleft()
        for dr, dc in directions:
            nr = r + dr
            nc = colu + dc
            if 0 <= nr < height and 0 <= nc < width and g[nr][nc] == c and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc))
                size += 1
    return size

def get_max_component_size(g: List[List[int]], c: int) -> int:
    height = len(g)
    if height == 0:
        return 0
    width = len(g[0])
    visited = [[False] * width for _ in range(height)]
    max_size = 0
    for r in range(height):
        for colu in range(width):
            if g[r][colu] == c and not visited[r][colu]:
                size = flood_fill_size(g, r, colu, c, visited)
                if size > max_size:
                    max_size = size
    return max_size

def identify_filler(g: List[List[int]], colors: set) -> int:
    if not colors:
        return 0
    max_sizes = {col: get_max_component_size(g, col) for col in colors}
    return min(max_sizes, key=max_sizes.get)

def get_average_row_for_color(g: List[List[int]], c: int) -> float:
    total_cells = sum(row.count(c) for row in g)
    if total_cells == 0:
        return 0.0
    sum_row = sum(r * row.count(c) for r, row in enumerate(g))
    return sum_row / total_cells

def program(g: List[List[int]]) -> List[List[int]]:
    colors = get_distinct_colors(g)
    if not colors:
        return []
    filler = identify_filler(g, colors)
    main_colors = [col for col in colors if col != filler]
    main_colors.sort(key=lambda col: get_average_row_for_color(g, col))
    k = len(main_colors)
    if k == 0:
        return []
    widths = []
    for i in range(k):
        if i < 3:
            widths.append(i + 1)
        elif i < k - 1:
            widths.append(3)
        else:
            widths.append(4)
    out = []
    for i in range(k):
        w = widths[i]
        row = [main_colors[i]] * w + [filler] * (4 - w)
        out.append(row)
    return out
```