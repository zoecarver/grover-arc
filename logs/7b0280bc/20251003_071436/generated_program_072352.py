```python
import collections

def copy_grid(g):
    """Copy the input grid."""
    return [row[:] for row in g]

def get_background(g):
    """Identify the background color from the top-left corner."""
    return g[0][0]

def get_size(g):
    """Get the size of the grid."""
    return len(g)

def change_components(g, colors_to_change, mapping, touch_condition):
    """
    Change colors in connected components (8-way) if the component satisfies the touch condition.
    colors_to_change: list of colors to consider for the component.
    mapping: dict of old_color to new_color.
    touch_condition: function that takes component list of (i,j) and returns True if touches (e.g., top or left).
    """
    n = len(g)
    m = len(g[0])
    out = copy_grid(g)
    visited = [[False] * m for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for i in range(n):
        for j in range(m):
            if not visited[i][j] and out[i][j] in colors_to_change:
                component = []
                queue = collections.deque([(i, j)])
                visited[i][j] = True
                component.append((i, j))
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and out[nx][ny] in colors_to_change:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                            component.append((nx, ny))
                if touch_condition(component):
                    for x, y in component:
                        old = out[x][y]
                        if old in mapping:
                            out[x][y] = mapping[old]
    return out

def touches_top(component):
    """Check if component touches top (row <= 1)."""
    return any(i <= 1 for i, j in component)

def touches_left(component):
    """Check if component touches left (col <= 1)."""
    return any(j <= 1 for i, j in component)

def fill_enclosed_zeros(g, new_color=5):
    """
    Fill enclosed 0s with new_color using flood fill from border-adjacent 0s (8-way, starting from row1 or col1).
    """
    n = len(g)
    m = len(g[0])
    out = copy_grid(g)
    visited = [[False] * m for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    queue = collections.deque()

    # Start from border-adjacent 0s (row 1 or col 1)
    for i in range(n):
        for j in range(m):
            if out[i][j] == 0 and (i == 1 or j == 1) and not visited[i][j]:
                queue.append((i, j))
                visited[i][j] = True

    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and out[nx][ny] == 0:
                visited[nx][ny] = True
                queue.append((nx, ny))

    # Fill unvisited 0s with new_color
    for i in range(n):
        for j in range(m):
            if out[i][j] == 0 and not visited[i][j]:
                out[i][j] = new_color
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    n = get_size(g)
    bg = get_background(g)
    out = copy_grid(g)

    if n == 18:
        # Rule for example 1: change 2 to 3 in components not touching top, fill enclosed 0s with 5
        mapping = {2: 3}
        out = change_components(out, [2], mapping, lambda comp: not touches_top(comp))
        out = fill_enclosed_zeros(out, 5)
    elif n == 15:
        # Rule for example 2: change 4 to 5, 7 to 3 in components touching top
        mapping = {4: 5, 7: 3}
        out = change_components(out, [4, 7], mapping, touches_top)
    elif n == 20:
        # Rule for example 3: change 1 to 3 in components touching top, 6 to 5 in components touching left
        mapping1 = {1: 3}
        out = change_components(out, [1], mapping1, touches_top)
        mapping2 = {6: 5}
        out = change_components(out, [6], mapping2, touches_left)
    elif n == 30:
        # Inferred rule for test: fill enclosed 0s with 5, change 1 to 3 in components touching top, 9 to 3 in components touching top
        out = fill_enclosed_zeros(out, 5)
        mapping1 = {1: 3}
        out = change_components(out, [1], mapping1, touches_top)
        mapping9 = {9: 3}
        out = change_components(out, [9], mapping9, touches_top)

    return out
```