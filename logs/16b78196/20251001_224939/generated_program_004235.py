```python
from typing import List, Tuple
from collections import deque

def find_components(g: List[List[int]]) -> List[Tuple[int, int, int, int, int, int, int, List[Tuple[int, int]]]]:
    n = 30
    visited = [[False] * n for _ in range(n)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    flat_positions = [(i, j) for i in range(n) for j in range(n)]
    for pos in flat_positions:
        i, j = pos
        if g[i][j] != 0 and not visited[i][j]:
            color = g[i][j]
            size = 0
            positions = []
            queue = deque([(i, j)])
            visited[i][j] = True
            while queue:
                x, y = queue.popleft()
                if 0 <= x < n and 0 <= y < n and g[x][y] == color and not visited[x][y]:
                    visited[x][y] = True
                    size += 1
                    positions.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        queue.append((nx, ny))
            if size > 0:
                min_row = min(p[0] for p in positions)
                max_row = max(p[0] for p in positions)
                min_col = min(p[1] for p in positions)
                max_col = max(p[1] for p in positions)
                components.append((color, size, min_col, max_col, min_row, max_row, positions))
    return components

def get_large(components: List[Tuple]) -> Tuple:
    return max(components, key=lambda c: c[1])

def get_small(components: List[Tuple], large: Tuple) -> List[Tuple]:
    large_size = large[1]
    return [c for c in components if c[1] < 20 and c[1] != large_size]

def is_horizontal(large: Tuple) -> bool:
    _, _, min_col, max_col, min_row, max_row = large[:6]
    dx = max_col - min_col + 1
    dy = max_row - min_row + 1
    return dx > dy

def sort_small_by_color(small: List[Tuple]) -> List[Tuple]:
    return sorted(small, key=lambda c: c[0])

def compute_common_width(small: List[Tuple]) -> int:
    if not small:
        return 0
    widths = [c[3] - c[2] + 1 for c in small]
    return max(widths)

def place_vertical_stack(h: List[List[int]], small: List[Tuple], large: Tuple):
    if not small:
        return
    sorted_small = sort_small_by_color(small)
    common_width = compute_common_width(sorted_small)
    common_min_col = large[2]  # large min_col
    current_row = large[5] + 1  # start below large max_row
    n = 30
    for c in sorted_small:
        c_color, _, c_min_col, c_max_col, c_min_row, c_max_row, c_pos = c
        dx = common_min_col - c_min_col  # left align to common
        dy = current_row - c_min_row
        for row, col in c_pos:
            new_row = row + dy
            new_col = col + dx
            if 0 <= new_row < n and 0 <= new_col < n and 0 <= new_col < common_min_col + common_width:
                h[new_row][new_col] = c_color
        current_row += (c_max_row - c_min_row + 1)

def place_horizontal_stack(h: List[List[int]], small: List[Tuple], large: Tuple):
    if not small:
        return
    sorted_small = sort_small_by_color(small)
    common_height = 4  # assuming all ~4
    center_row = 13  # center around row 15
    common_min_row = max(0, center_row - common_height // 2)
    current_col = large[3] + 1  # start right of large max_col
    n = 30
    for c in sorted_small:
        c_color, _, c_min_col, c_max_col, c_min_row, c_max_row, c_pos = c
        dy = common_min_row - c_min_row  # align to common y
        dx = current_col - c_min_col
        for row, col in c_pos:
            new_row = row + dy
            new_col = col + dx
            if 0 <= new_row < n and 0 <= new_col < n and new_row >= common_min_row and new_row < common_min_row + common_height:
                h[new_row][new_col] = c_color
        current_col += (c_max_col - c_min_col + 1)

def remove_original_small(h: List[List[int]], small: List[Tuple]):
    n = 30
    for c in small:
        _, _, _, _, _, _, c_pos = c
        for row, col in c_pos:
            if 0 <= row < n and 0 <= col < n:
                h[row][col] = 0

def program(g: List[List[int]]) -> List[List[int]]:
    h = [row[:] for row in g]
    components = find_components(g)
    if not components:
        return h
    large = get_large(components)
    small = get_small(components, large)
    if is_horizontal(large):
        place_vertical_stack(h, small, large)
    else:
        place_horizontal_stack(h, small, large)
    remove_original_small(h, small)
    return h
```