```python
from collections import Counter
from typing import List, Tuple

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int) -> List[List[Tuple[int, int, int]]]:
    if not g or not g[0]:
        return []
    rows_n = len(g)
    cols_n = len(g[0])
    visited = set()
    components = []
    dirs: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows_n):
        for j in range(cols_n):
            if (i, j) not in visited and g[i][j] != bg:
                component = []
                stack = [(i, j)]
                visited.add((i, j))
                while stack:
                    x, y = stack.pop()
                    component.append((x, y, g[x][y]))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows_n and 0 <= ny < cols_n and (nx, ny) not in visited and g[nx][ny] != bg:
                            visited.add((nx, ny))
                            stack.append((nx, ny))
                components.append(component)
    return components

def get_special(component: List[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    if not component:
        return -1, -1, -1
    color_count = Counter(col for _, _, col in component)
    singleton_colors = [col for col, cnt in color_count.items() if cnt == 1]
    if len(singleton_colors) != 1:
        return -1, -1, -1
    s = singleton_colors[0]
    for r, c, col in component:
        if col == s:
            return r, c, s
    return -1, -1, -1

def get_bounds(component: List[Tuple[int, int, int]]) -> Tuple[int, int, int, int]:
    if not component:
        return 0, 0, 0, 0
    rs = [r for r, _, _ in component]
    cs = [c for _, c, _ in component]
    return min(rs), max(rs), min(cs), max(cs)

def get_translation(rows_n: int, cols_n: int, bg: int, size: int, r: int, c: int, height: int, width: int, tall: bool) -> Tuple[int, int]:
    if size == 1:
        return 0, 0
    if tall:
        target = 9 - cols_n // 2
        dy = 0
        dx = target - c
        return dy, dx
    else:
        target = 9 - rows_n // 2
        dy = target - r
        dx = 0
        special_case = height > 2 * width
        if special_case:
            target = bg % rows_n
            dy = target - r
        if r < target and not special_case:
            dx -= 1
        return dy, dx

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows_n = len(g)
    cols_n = len(g[0])
    bg = find_background(g)
    components = find_components(g, bg)
    new_grid = [row[:] for row in g]
    tall = rows_n > cols_n
    for comp in components:
        size = len(comp)
        special_r, special_c, _ = get_special(comp)
        if special_r == -1:
            continue
        min_r, max_r, min_c, max_c = get_bounds(comp)
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        dy, dx = get_translation(rows_n, cols_n, bg, size, special_r, special_c, height, width, tall)
        # Clear originals
        for rr, cc, _ in comp:
            new_grid[rr][cc] = bg
        # Place new
        for rr, cc, col in comp:
            nr = rr + dy
            nc = cc + dx
            if 0 <= nr < rows_n and 0 <= nc < cols_n:
                new_grid[nr][nc] = col
    return new_grid
```