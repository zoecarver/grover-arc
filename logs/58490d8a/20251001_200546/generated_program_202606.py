```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def find_indicator_column_and_rows(g: List[List[int]], bg: int, rows: int, cols: int) -> Tuple[int, List[int]]:
    max_count = 0
    best_c = -1
    best_rows: List[int] = []
    for c in range(cols):
        ind_rs: List[int] = [r for r in range(rows) if g[r][c] != bg and g[r][c] != 0]
        if ind_rs:
            isolated = all(ind_rs[i] != ind_rs[i - 1] + 1 for i in range(1, len(ind_rs)))
            if isolated and len(ind_rs) > max_count:
                max_count = len(ind_rs)
                best_c = c
                best_rows = ind_rs
    return best_c, best_rows

def get_strip_bounds(g: List[List[int]], ind_rows: List[int], bg: int, rows: int, cols: int, ind_c: int) -> Tuple[int, int, int, int]:
    if not ind_rows:
        return 0, 0, 0, 0
    min_r = min(ind_rows)
    max_r = max(ind_rows)
    s = max(0, min_r - 1)
    e = min(rows - 1, max_r + 1)

    def can_expand_to(candidate_c: int) -> bool:
        if candidate_c < 0 or candidate_c >= cols:
            return False
        has_non_bg_non_zero = False
        has_zero = False
        for rr in range(s, e + 1):
            val = g[rr][candidate_c]
            if val != bg and val != 0:
                has_non_bg_non_zero = True
            if val == 0:
                has_zero = True
        return not has_non_bg_non_zero and has_zero

    strip_left = ind_c
    while strip_left > 0 and can_expand_to(strip_left - 1):
        strip_left -= 1

    strip_right = ind_c
    while strip_right < cols - 1 and can_expand_to(strip_right + 1):
        strip_right += 1

    return s, e, strip_left, strip_right

def count_components_for_color(g: List[List[int]], color: int, rows: int, cols: int, 
                               strip_start_r: int, strip_end_r: int, strip_start_c: int, strip_end_c: int) -> int:
    if color == 0:
        return 0
    visited = [[False] * cols for _ in range(rows)]
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    component_count = 0

    def dfs(start_r: int, start_c: int) -> bool:
        touches_strip = False
        stack: List[Tuple[int, int]] = [(start_r, start_c)]
        visited[start_r][start_c] = True
        while stack:
            cr, cc = stack.pop()
            if strip_start_r <= cr <= strip_end_r and strip_start_c <= cc <= strip_end_c:
                touches_strip = True
            for dr, dc in dirs:
                nr = cr + dr
                nc = cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                    visited[nr][nc] = True
                    stack.append((nr, nc))
        return not touches_strip

    for start_r in range(rows):
        for start_c in range(cols):
            if g[start_r][start_c] == color and not visited[start_r][start_c]:
                if not (strip_start_r <= start_r <= strip_end_r and strip_start_c <= start_c <= strip_end_c):
                    if dfs(start_r, start_c):
                        component_count += 1
    return component_count

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return [[0]]
    rows = len(g)
    cols = len(g[0])
    bg = get_background(g)
    ind_c, ind_rows = find_indicator_column_and_rows(g, bg, rows, cols)
    if not ind_rows:
        return [[0]]
    s, e, strip_l, strip_r = get_strip_bounds(g, ind_rows, bg, rows, cols, ind_c)
    width = strip_r - strip_l + 1
    num_ind = len(ind_rows)
    height = 2 * num_ind + 1
    out = [[0] * width for _ in range(height)]
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for k, r_ind in enumerate(ind_rows):
        color = g[r_ind][ind_c]
        count = count_components_for_color(g, color, rows, cols, s, e, strip_l, strip_r)
        out_row = 2 * k + 1
        for i in range(count):
            col_pos = 2 * i + 1
            if col_pos < width:
                out[out_row][col_pos] = color
    return out
```