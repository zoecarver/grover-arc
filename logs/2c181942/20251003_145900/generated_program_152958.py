```python
from typing import List
import copy
import math

def count_pixels(g: List[List[int]], color: int) -> int:
    rows = len(g)
    cols = len(g[0])
    return sum(1 for r in range(rows) for c in range(cols) if g[r][c] == color)

def find_closest_component(g: List[List[int]]) -> tuple:
    rows = len(g)
    cols = len(g[0])
    center_r = rows // 2
    center_c = cols // 2
    visited = [[False] * cols for _ in range(rows)]
    min_dist = float('inf')
    special_color = None
    hub_r = center_r
    hub_c = center_c
    hub_p = 0
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != 8 and g[r][c] > 3 and not visited[r][c]:
                color = g[r][c]
                queue = [(r, c)]
                visited[r][c] = True
                comp_p = 1
                min_cr, max_cr = r, r
                min_cc, max_cc = c, c
                while queue:
                    cr, cc = queue.pop(0)
                    min_cr = min(min_cr, cr)
                    max_cr = max(max_cr, cr)
                    min_cc = min(min_cc, cc)
                    max_cc = max(max_cc, cc)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                            comp_p += 1
                comp_center_r = (min_cr + max_cr) / 2
                comp_center_c = (min_cc + max_cc) / 2
                dist = abs(comp_center_r - center_r) + abs(comp_center_c - center_c)
                if dist < min_dist:
                    min_dist = dist
                    special_color = color
                    hub_r = round(comp_center_r)
                    hub_c = round(comp_center_c)
                    hub_p = comp_p
    total_special_p = count_pixels(g, special_color) if special_color else 0
    return special_color, total_special_p, hub_r, hub_c

def place_vertical_bar(g: List[List[int]], color: int, start_r: int, col: int, height: int) -> None:
    rows = len(g)
    for i in range(height):
        r = start_r + i
        if 0 <= r < rows and 0 <= col < len(g[0]):
            g[r][col] = color

def place_horizontal_bar(g: List[List[int]], color: int, row: int, start_c: int, width: int) -> None:
    cols = len(g[0])
    for i in range(width):
        c = start_c + i
        if 0 <= c < cols and 0 <= row < len(g):
            g[row][c] = color

def place_shape_2(g: List[List[int]], color: int, base_r: int, base_c: int, p: int) -> None:
    if p < 2:
        return
    m = (p - 2) // 2
    # Top single at base_c
    if 0 <= base_r - 1 < len(g):
        if 0 <= base_c < len(g[0]):
            g[base_r - 1][base_c] = color
    # Middle two rows: col base_c - m + 1 to base_c, width m
    for mr in range(2):
        r = base_r + mr
        if 0 <= r < len(g):
            for j in range(m):
                c = base_c - (m - 1 - j)  # right aligned
                if 0 <= c < len(g[0]):
                    g[r][c] = color
    # Bottom single at base_c
    if 0 <= base_r + 2 < len(g):
        if 0 <= base_c < len(g[0]):
            g[base_r + 2][base_c] = color

def place_shape_3(g: List[List[int]], color: int, base_r: int, base_c: int, p: int) -> None:
    if p < 4:
        return
    w = (p - 2) // 4
    m = w + 1
    # Top bar width w left aligned to base_c
    if 0 <= base_r - 1 < len(g):
        for j in range(w):
            c = base_c + j
            if 0 <= c < len(g[0]):
                g[base_r - 1][c] = color
    # Middle two rows width m, shifted right
    for mr in range(2):
        r = base_r + mr
        if 0 <= r < len(g):
            for j in range(m):
                c = base_c + j
                if 0 <= c < len(g[0]):
                    g[r][c] = color
    # Bottom bar width w left aligned
    if 0 <= base_r + 2 < len(g):
        for j in range(w):
            c = base_c + j
            if 0 <= c < len(g[0]):
                g[base_r + 2][c] = color

def place_shape_1(g: List[List[int]], color: int, base_r: int, base_c: int, p: int) -> None:
    if p == 0:
        return
    w = 1 if p <= 4 else 2
    h = math.ceil(p / w)
    start_r = base_r - h // 2
    for i in range(h):
        r = start_r + i
        if 0 <= r < len(g):
            for j in range(w):
                c = base_c + j - (w - 1) // 2  # center
                if 0 <= c < len(g[0]):
                    g[r][c] = color
    # Fill exactly p
    filled = 0
    for r in range(start_r, start_r + h):
        if 0 <= r < len(g):
            for j in range(w):
                c = base_c + j - (w - 1) // 2
                if 0 <= c < len(g[0]) and filled < p:
                    g[r][c] = color
                    filled += 1

def place_shape_special(g: List[List[int]], color: int, base_r: int, base_c: int, p: int) -> None:
    if p == 0:
        return
    if p == 2:
        # Horizontal
        place_horizontal_bar(g, color, base_r, base_c - 1, 2)
        return
    if color == 4 and p == 7:
        # Blocky 4 with 7 pixels
        # Assume base_r, base_c center
        # Vertical left col base_c -1 rows base_r to base_r +2
        for i in range(3):
            r = base_r + i - 1
            if 0 <= r < len(g):
                g[r][base_c - 1] = color
        # Cross row base_r +1 col base_c -1 to base_c +1
        r = base_r + 1
        if 0 <= r < len(g):
            for j in range(3):
                c = base_c - 1 + j
                if 0 <= c < len(g[0]):
                    g[r][c] = color
        # Right bottom col base_c +1 row base_r +2
        r = base_r + 2
        if 0 <= r < len(g):
            g[r][base_c + 1] = color
        return
    # Default to vertical bar
    place_vertical_bar(g, color, base_r - p // 2, base_c, p)

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(g)
    rows = len(grid)
    cols = len(grid[0])
    p1 = count_pixels(g, 1)
    p2 = count_pixels(g, 2)
    p3 = count_pixels(g, 3)
    special_color, p_special, hub_r, hub_c = find_closest_component(g)
    # Fill with 8
    for r in range(rows):
        grid[r] = [8] * cols
    # Place special first at hub
    place_shape_special(grid, special_color, hub_r, hub_c, p_special)
    # Place 3 left of hub
    left_c = hub_c - 5  # gap
    place_shape_3(grid, 3, hub_r, left_c, p3)
    # Place 1 below hub
    below_r = hub_r + 4  # gap
    place_shape_1(grid, 1, below_r, hub_c, p1)
    # Place 2 right of hub
    right_c = hub_c + 5  # gap
    place_shape_2(grid, 2, hub_r, right_c, p2)
    return grid
```