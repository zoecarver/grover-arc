```python
from typing import List, Tuple
from collections import Counter

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int) -> List[List[Tuple[int, int, int]]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    if h == 0 or w == 0:
        return []
    visited = set()
    components = []
    dirs: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if (i, j) not in visited and g[i][j] != bg:
                component = []
                stack = [(i, j)]
                visited.add((i, j))
                while stack:
                    x, y = stack.pop()
                    component.append((x, y, g[x][y]))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and (nx, ny) not in visited and g[nx][ny] != bg:
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

def compute_translation(sr: int, sc: int, comp_h: int, comp_w: int, h: int, w: int, bg: int, is_tall: bool) -> Tuple[int, int]:
    dy = 0
    dx = 0
    if is_tall:
        target_c = 9 - (w // 2)
        override = comp_w > 2 * comp_h
        if override:
            target_c = bg % w
        dx = target_c - sc
    else:
        target_r = 9 - (h // 2)
        override = comp_h > 2 * comp_w
        if override:
            target_r = bg % h
        dy = target_r - sr
        dx = 0
        if sr < target_r and not override:
            dx -= 1
    return dy, dx

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    bg = find_background(g)
    components = find_components(g, bg)
    new_g = [row[:] for row in g]
    is_tall = h > w
    for comp in components:
        if len(comp) <= 1:
            continue
        sr, sc, _ = get_special(comp)
        if sr == -1:
            continue
        _, max_r, _, max_c = get_bounds(comp)
        min_r, _, min_c, _ = get_bounds(comp)
        comp_h = max_r - min_r + 1
        comp_w = max_c - min_c + 1
        dy, dx = compute_translation(sr, sc, comp_h, comp_w, h, w, bg, is_tall)
        for r, c, _ in comp:
            new_g[r][c] = bg
        for r, c, col in comp:
            nr = r + dy
            nc = c + dx
            if 0 <= nr < h and 0 <= nc < w:
                new_g[nr][nc] = col
    return new_g
```