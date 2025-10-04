```python
from typing import List, Tuple
from collections import Counter

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

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    bg = find_background(g)
    h = len(g)
    w = len(g[0])
    components = find_components(g, bg)
    new_g = [row[:] for row in g]
    for comp in components:
        if len(comp) <= 1:
            continue
        sr, sc, _ = get_special(comp)
        if sr == -1:
            continue
        _, max_r, _, max_c = get_bounds(comp)
        min_r = min(r for r, _, _ in comp)
        min_c = min(c for _, c, _ in comp)
        comp_h = max_r - min_r + 1
        comp_w = max_c - min_c + 1
        is_tall = h > w
        dy = 0
        dx = 0
        if is_tall:
            target_c = 9 - (w // 2)
            dx = target_c - sc
            if comp_w > 2 * comp_h:
                target_c = bg % w
                dx = target_c - sc
        else:
            target_r = 9 - (h // 2)
            dy = target_r - sr
            is_special_case = comp_h > 2 * comp_w
            if is_special_case:
                target_r = bg % h
                dy = target_r - sr
            if not is_special_case and sr < target_r:
                dx -= 1
        # clear originals
        for r, c, _ in comp:
            new_g[r][c] = bg
        # place shifted
        for r, c, col in comp:
            nr = r + dy
            nc = c + dx
            if 0 <= nr < h and 0 <= nc < w:
                new_g[nr][nc] = col
    return new_g
```