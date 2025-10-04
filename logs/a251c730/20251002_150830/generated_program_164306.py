```python
from typing import List
import collections

def find_longest_horizontal_run(g: List[List[int]]) -> tuple:
    height = len(g)
    width = len(g[0]) if height > 0 else 0
    max_length = 0
    best_y = 0
    best_x1 = 0
    best_x2 = 0
    best_color = 0
    for i in range(height):
        j = 0
        while j < width:
            color = g[i][j]
            start = j
            while j < width and g[i][j] == color:
                j += 1
            length = j - start
            if length > max_length:
                max_length = length
                best_y = i
                best_x1 = start
                best_x2 = j - 1
                best_color = color
    return best_color, best_y, best_x1, best_x2, max_length

def get_connected_component(g: List[List[int]], start_i: int, start_j: int) -> list:
    height = len(g)
    width = len(g[0]) if height > 0 else 0
    visited = [[False] * width for _ in range(height)]
    color = g[start_i][start_j]
    component = []
    stack = [(start_i, start_j)]
    visited[start_i][start_j] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.pop()
        component.append((x, y))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny] and g[nx][ny] == color:
                visited[nx][ny] = True
                stack.append((nx, ny))
    return component

def get_inner_color(component: list, g: List[List[int]], frame_color: int) -> int:
    if not component:
        return 0
    min_i = min(p[0] for p in component)
    max_i = max(p[0] for p in component)
    min_j = min(p[1] for p in component)
    max_j = max(p[1] for p in component)
    color_count = {}
    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            col = g[i][j]
            if col != frame_color:
                color_count[col] = color_count.get(col, 0) + 1
    if color_count:
        return max(color_count, key=color_count.get)
    return 0

def is_open_bottom(component: list, g: List[List[int]], min_i: int, max_i: int, min_j: int, max_j: int) -> bool:
    sub_h = max_i - min_i + 1
    sub_w = max_j - min_j + 1
    sub_g = [[0] * sub_w for _ in range(sub_h)]
    frame_color = g[component[0][0]][component[0][1]]
    for x, y in component:
        sub_g[x - min_i][y - min_j] = 1
    visited = [[False] * sub_w for _ in range(sub_h)]
    queue = collections.deque()
    for j in range(sub_w):
        i = sub_h - 1
        if sub_g[i][j] == 0 and not visited[i][j]:
            queue.append((i, j))
            visited[i][j] = True
            sub_g[i][j] = 2
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    reached_inner = False
    while queue:
        x, y = queue.popleft()
        if x < sub_h - 1:  # reached above bottom row
            reached_inner = True
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < sub_h and 0 <= ny < sub_w and sub_g[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                sub_g[nx][ny] = 2
                queue.append((nx, ny))
    return reached_inner

def get_components(g: List[List[int]]) -> List[dict]:
    height = len(g)
    width = len(g[0]) if height > 0 else 0
    visited = [[False] * width for _ in range(height)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(height):
        for j in range(width):
            if not visited[i][j] and g[i][j] != 0:
                color = g[i][j]
                component_pos = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component_pos.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append({
                    'color': color,
                    'pixels': len(component_pos),
                    'positions': component_pos
                })
    return components

def calculate_holes(component: dict, g: List[List[int]]) -> int:
    # Flood without bottom to count holes assuming closed bottom
    positions = component['positions']
    if not positions:
        return 0
    min_i = min(p[0] for p in positions)
    max_i = max(p[0] for p in positions)
    min_j = min(p[1] for p in positions)
    max_j = max(p[1] for p in positions)
    sub_h = max_i - min_i + 1
    sub_w = max_j - min_j + 1
    sub_g = [[0] * sub_w for _ in range(sub_h)]
    for x, y in positions:
        sub_g[x - min_i][y - min_j] = 1
    visited = [[False] * sub_w for _ in range(sub_h)]
    queue = collections.deque()
    # Flood from top, left, right borders, but not bottom
    for i in range(sub_h):
        # left
        if sub_g[i][0] == 0:
            queue.append((i, 0))
            visited[i][0] = True
            sub_g[i][0] = 2
        # right
        if sub_g[i][sub_w - 1] == 0:
            queue.append((i, sub_w - 1))
            visited[i][sub_w - 1] = True
            sub_g[i][sub_w - 1] = 2
    for j in range(1, sub_w - 1):  # top, exclude corners already added
        if sub_g[0][j] == 0:
            queue.append((0, j))
            visited[0][j] = True
            sub_g[0][j] = 2
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < sub_h and 0 <= ny < sub_w and sub_g[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                sub_g[nx][ny] = 2
                queue.append((nx, ny))
    # Count remaining 0 components
    hole_count = 0
    for i in range(sub_h):
        for j in range(sub_w):
            if sub_g[i][j] == 0 and not visited[i][j]:
                hole_count += 1
                stack = [(i, j)]
                visited[i][j] = True
                sub_g[i][j] = 2
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < sub_h and 0 <= ny < sub_w and sub_g[nx][ny] == 0 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            sub_g[nx][ny] = 2
                            stack.append((nx, ny))
    return hole_count

def create_output_grid(w: int, h: int, frame_color: int, inner_color: int) -> List[List[int]]:
    grid = [[frame_color for _ in range(w)] for _ in range(h)]
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            grid[i][j] = inner_color
    return grid

def overlay_main_anomalies(grid: List[List[int]], g: List[List[int]], min_i: int, max_i: int, min_j: int, max_j: int, inner_color: int, frame_color: int, w: int, h: int):
    for i in range(min_i, min(max_i + 1, len(g))):
        rel_i = i - min_i
        if rel_i >= h:
            continue
        for j in range(min_j, min(max_j + 1, len(g[0]))):
            rel_j = j - min_j
            if rel_j >= w:
                continue
            col = g[i][j]
            if col != inner_color and col != frame_color:
                grid[rel_i][rel_j] = col

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    frame_color, y0, x1, x2, run_length = find_longest_horizontal_run(g)
    component = get_connected_component(g, y0, x1)
    if not component:
        return []
    min_i = min(p[0] for p in component)
    max_i = max(p[0] for p in component)
    min_j = min(p[1] for p in component)
    max_j = max(p[1] for p in component)
    inner_color = get_inner_color(component, g, frame_color)
    open_bottom = is_open_bottom(component, g, min_i, max_i, min_j, max_j)
    h = max_i - min_i + 1
    if open_bottom:
        h += 1
    w = run_length
    grid = create_output_grid(w, h, frame_color, inner_color)
    # Overlay main anomalies 1:1 shifted
    overlay_main_anomalies(grid, g, min_i, max_i, min_j, min_j + w - 1, inner_color, frame_color, w, h)
    # If added bottom, the last row is already frame_color all
    # Now partial preservation for other large high-hole components
    all_components = get_components(g)
    inner_min_i = 1
    inner_max_i = h - 2
    inner_min_j = 1
    inner_max_j = w - 2
    for comp in all_components:
        if comp['pixels'] <= 100 or comp['color'] == frame_color or comp['color'] == inner_color:
            continue
        holes = calculate_holes(comp, g)
        if holes < 2:
            continue
        c_min_i = min(p[0] for p in comp['positions'])
        c_max_i = max(p[0] for p in comp['positions'])
        c_min_j = min(p[1] for p in comp['positions'])
        c_max_j = max(p[1] for p in comp['positions'])
        c_orig_h = c_max_i - c_min_i
        c_orig_w = c_max_j - c_min_j
        scale_h = inner_max_i - inner_min_i
        scale_w = inner_max_j - inner_min_j
        c_color = comp['color']
        for i in range(c_min_i, c_max_i + 1):
            for j in range(c_min_j, c_max_j + 1):
                col = g[i][j]
                if col != c_color and col != 0 and col != frame_color and col != inner_color:
                    rel_i = i - c_min_i
                    rel_j = j - c_min_j
                    new_i = inner_min_i + (rel_i * scale_h // c_orig_h if c_orig_h > 0 else 0)
                    new_j = inner_min_j + (rel_j * scale_w // c_orig_w if c_orig_w > 0 else 0)
                    new_i = max(inner_min_i, min(inner_max_i, new_i))
                    new_j = max(inner_min_j, min(inner_max_j, new_j))
                    grid[new_i][new_j] = col
    return grid
```