```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], background: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != background:
                color = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def touches_left(component: List[Tuple[int, int]]) -> bool:
    return any(c == 0 for _, c in component)

def has_anchored(g: List[List[int]], bg: int) -> bool:
    for row in g:
        if row[0] != bg:
            return True
    return False

def get_main_color(g: List[List[int]], bg: int) -> int:
    for row in g:
        if row[0] != bg:
            return row[0]
    return None

def get_subcomponents(g: List[List[int]], bg: int, main_color: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    all_comp = find_components(g, bg)
    subs = [comp for comp in all_comp if comp[0] == main_color and touches_left(comp[1])]
    return sorted(subs, key=lambda x: min(r for r, c in x[1]))

def get_noise_colors(g: List[List[int]], bg: int, main_color: int) -> List[int]:
    all_comp = find_components(g, bg)
    colors = {comp[0] for comp in all_comp if comp[0] != bg and comp[0] != main_color and not touches_left(comp[1])}
    return sorted(list(colors))

def get_inner_extension(size_u: int, size_l: int, c1: int, c2: int) -> Tuple[int, int]:
    if size_u > size_l:
        return c2, c1
    return c1, c2

def apply_anchored_reconstruction(g: List[List[int]], bg: int, main_color: int) -> List[List[int]]:
    subcomps = get_subcomponents(g, bg, main_color)
    if len(subcomps) != 2:
        return [row[:] for row in g]
    upper, lower = subcomps
    size_u = len(upper[1])
    size_l = len(lower[1])
    noise_colors = get_noise_colors(g, bg, main_color)
    if len(noise_colors) != 2:
        return [row[:] for row in g]
    c1, c2 = noise_colors
    inner, extension = get_inner_extension(size_u, size_l, c1, c2)
    out = [[bg] * len(g[0]) for _ in range(len(g))]
    for _, pos in subcomps:
        for r, c in pos:
            out[r][c] = main_color
    min_r = min(min(r for r, c in pos) for _, pos in subcomps)
    max_r = max(max(r for r, c in pos) for _, pos in subcomps)
    for r in range(min_r, max_r + 1):
        for c in range(4):
            if out[r][c] == bg:
                out[r][c] = inner
    partial_rows = set()
    for _, pos in subcomps:
        row_count = Counter(r for r, c in pos if c < 4)
        for r, count in row_count.items():
            if 0 < count < 4:
                partial_rows.add(r)
    for r in partial_rows:
        for c in range(4, 9):
            out[r][c] = extension
    max_u = max(r for r, c in upper[1])
    min_l = min(r for r, c in lower[1])
    for r in range(max_u + 1, min_l):
        if 8 < len(g[0]):
            out[r][8] = extension
    for _, pos in subcomps:
        rows = set(r for r, c in pos)
        if len(rows) == 1:
            r = next(iter(rows))
            if 8 < len(g[0]):
                out[r][8] = extension
            if 9 < len(g[0]):
                out[r][9] = extension
    return out

def apply_rigid_gravity(g: List[List[int]], bg: int) -> List[List[int]]:
    components = find_components(g, bg)
    comp_list = sorted(components, key=lambda x: -max(r for r, c in x[1]))
    out = [[bg] * len(g[0]) for _ in range(len(g))]
    placed = set()
    rows_n = len(g)
    for color, pos in comp_list:
        max_r = max(r for r, c in pos)
        max_k = rows_n - 1 - max_r
        placed_pos = False
        for k in range(max_k, -1, -1):
            new_pos = [(r + k, c) for r, c in pos]
            if all(0 <= nr < rows_n and 0 <= nc < len(g[0]) and (nr, nc) not in placed for nr, nc in new_pos):
                for nr, nc in new_pos:
                    out[nr][nc] = color
                    placed.add((nr, nc))
                placed_pos = True
                break
        if not placed_pos:
            for r, c in pos:
                out[r][c] = color
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    if not has_anchored(g, bg):
        return apply_rigid_gravity(g, bg)
    main_color = get_main_color(g, bg)
    if main_color is None:
        return [row[:] for row in g]
    return apply_anchored_reconstruction(g, bg, main_color)
```