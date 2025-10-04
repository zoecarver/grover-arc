```python
from typing import List, Dict
from collections import defaultdict, deque

def has_color(g: List[List[int]], c: int) -> bool:
    for row in g:
        if c in row:
            return True
    return False

def remove_yellow_if_pink(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if has_color(g, 6):
        rows = len(new_g)
        cols = len(new_g[0]) if rows > 0 else 0
        for i in range(rows):
            for j in range(cols):
                if new_g[i][j] == 4:
                    new_g[i][j] = 8
    return new_g

def remove_small_blue_if_dark_red(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if not has_color(g, 7):
        return new_g
    rows = len(new_g)
    cols = len(new_g[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if new_g[i][j] == 1 and not visited[i][j]:
                component = []
                q = deque([(i, j)])
                visited[i][j] = True
                component.append((i, j))
                size = 1
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and new_g[nx][ny] == 1:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            component.append((nx, ny))
                            size += 1
                if size <= 2:
                    for px, py in component:
                        new_g[px][py] = 8
    return new_g

def count_colors(g: List[List[int]]) -> Dict[int, int]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    color_count: Dict[int, int] = defaultdict(int)
    for i in range(rows):
        for j in range(cols):
            c = g[i][j]
            if c != 8:
                color_count[c] += 1
    return dict(color_count)

def get_widths(n: int, c: int) -> List[int]:
    if n == 0:
        return [0, 0, 0, 0]
    is_odd = c % 2 == 1
    if n == 2:
        if is_odd:
            return [0, 0, 0, 2]
        else:
            return [2, 0, 0, 0]
    if is_odd:
        a = 2
        b = n // 2 - a
        if b < a:
            a = 1
            b = n // 2 - a
        widths = [a, b, b, a]
        remaining = n - sum(widths)
        if remaining > 0:
            widths[2] += remaining
        return widths
    else:
        a = 1
        b = n // 2 - a
        widths = [a, b, b, a]
        remaining = n - sum(widths)
        if remaining > 0:
            widths[2] += remaining
        return widths

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return g
    cols = len(g[0])
    # Apply removals
    modified_g = remove_yellow_if_pink(g)
    modified_g = remove_small_blue_if_dark_red(modified_g)
    # Count colors after removals
    color_count = count_colors(modified_g)
    # Create output grid all 8s
    out_g = [[8] * cols for _ in range(rows)]
    if not color_count:
        return out_g
    # Sorted colors ascending
    colors = sorted(color_count)
    # Start row for 4-row block
    start_row = (rows - 4) // 2
    # Prepare shape infos
    shape_infos = []
    total_width = 0
    separator = 2
    for c in colors:
        n = color_count[c]
        widths = get_widths(n, c)
        max_w = max([w for w in widths if w > 0] or [0])
        bounding_w = max_w
        shape_infos.append((c, widths, bounding_w))
        total_width += bounding_w
        total_width += separator
    total_width -= separator  # remove last separator
    current_col = (cols - total_width) // 2 if total_width > 0 else 0
    # Place shapes
    for c, widths, bounding_w in shape_infos:
        is_odd = c % 2 == 1
        for i in range(4):
            r = widths[i]
            if r == 0:
                continue
            row = start_row + i
            if row >= rows:
                continue
            if is_odd:
                fill_start = current_col
            else:
                fill_start = current_col + bounding_w - r
            for j in range(r):
                col_pos = fill_start + j
                if 0 <= col_pos < cols:
                    out_g[row][col_pos] = c
        current_col += bounding_w + separator
    return out_g
```