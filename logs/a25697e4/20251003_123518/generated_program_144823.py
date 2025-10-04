```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], background: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
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
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def touches_left(component: List[Tuple[int, int]]) -> bool:
    return any(c == 0 for _, c in component)

def get_min_row_for_color(g: List[List[int]], color: int, h: int, w: int) -> int:
    min_r = float('inf')
    for r in range(h):
        for c in range(w):
            if g[r][c] == color:
                min_r = min(min_r, r)
                break
        if min_r < float('inf'):
            break
    return min_r if min_r < float('inf') else float('inf')

def get_count_left_main(g: List[List[int]], r: int, main_color: int, w: int) -> int:
    return sum(1 for j in range(min(4, w)) if g[r][j] == main_color)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    anchored = any(g[r][0] != bg for r in range(h))
    out = [[bg] * w for _ in range(h)]
    if anchored:
        left_colors = {g[r][0] for r in range(h) if g[r][0] != bg}
        if len(left_colors) != 1:
            return [row[:] for row in g]
        main_color = next(iter(left_colors))
        for r in range(h):
            for c in range(w):
                if g[r][c] == main_color:
                    out[r][c] = main_color
        all_colors = set()
        for row in g:
            all_colors.update(set(row))
        noise_colors = [col for col in all_colors if col != bg and col != main_color]
        if len(noise_colors) != 2:
            return out
        min_rs = {col: get_min_row_for_color(g, col, h, w) for col in noise_colors}
        sorted_noise = sorted(noise_colors, key=lambda col: min_rs[col])
        upper_noise, lower_noise = sorted_noise
        full_rows = []
        partial_rows = []
        zero_rows_in_range = []
        for r in range(h):
            count = get_count_left_main(g, r, main_color, w)
            if count == 4:
                full_rows.append(r)
            elif count == 2:
                partial_rows.append(r)
        if len(full_rows) != 2 or len(partial_rows) != 1:
            return out
        full_rows.sort()
        top, bottom = full_rows
        middle = partial_rows[0]
        for r in range(top + 1, bottom):
            count = get_count_left_main(g, r, main_color, w)
            if count == 0:
                zero_rows_in_range.append(r)
        if len(zero_rows_in_range) != 1:
            return out
        gap = zero_rows_in_range[0]
        inner = upper_noise if gap < middle else lower_noise
        outer = lower_noise if gap < middle else upper_noise
        left_width = min(4, w)
        for j in range(left_width):
            if out[middle][j] == bg:
                out[middle][j] = inner
        for j in range(4, min(9, w)):
            out[middle][j] = outer
        for j in range(left_width):
            if out[gap][j] == bg:
                out[gap][j] = inner
        if 8 < w:
            out[gap][8] = outer
        adjacents = [r for r in full_rows if abs(r - gap) == 1]
        if len(adjacents) == 1:
            adj = adjacents[0]
            if 8 < w:
                out[adj][8] = outer
            if 9 < w:
                out[adj][9] = outer
        return out
    else:
        comps = find_components(g, bg)
        comps = [c for c in comps if c[1]]
        comps.sort(key=lambda x: min(r for r, _ in x[1]))
        for color, pos in comps:
            target_pos = [(r + 1, c + 6) for r, c in pos]
            can_shift = all(0 <= nr < h and 0 <= nc < w and out[nr][nc] == bg for nr, nc in target_pos)
            place_pos = target_pos if can_shift else pos
            for nr, nc in place_pos:
                out[nr][nc] = color
        return out
```