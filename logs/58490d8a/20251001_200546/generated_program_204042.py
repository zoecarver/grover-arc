```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def find_indicator_column_and_rows(g: List[List[int]], bg: int, rows: int, cols: int) -> Tuple[int, List[int]]:
    max_count = 0
    best_c = -1
    best_rows: List[int] = []
    for c in range(cols):
        ind_rs: List[int] = [r for r in range(rows) if g[r][c] != bg and g[r][c] != 0]
        if ind_rs:
            ind_rs.sort()
            isolated = all(ind_rs[i] >= ind_rs[i - 1] + 2 for i in range(1, len(ind_rs)))
            if isolated and len(ind_rs) > max_count:
                max_count = len(ind_rs)
                best_c = c
                best_rows = ind_rs[:]
    return best_c, best_rows

def get_strip_bounds(g: List[List[int]], ind_rows: List[int], bg: int, rows: int, cols: int, ind_c: int) -> Tuple[int, int, int, int]:
    if not ind_rows:
        return 0, 0, 0, 0
    min_r = min(ind_rows)
    max_r = max(ind_rows)
    s = max(0, min_r - 1)
    e = min(rows - 1, max_r + 1)

    def is_neutral(cand_c: int) -> bool:
        if cand_c < 0 or cand_c >= cols:
            return False
        has_zero = False
        for rr in range(s, e + 1):
            val = g[rr][cand_c]
            if val != bg and val != 0:
                return False
            if val == 0:
                has_zero = True
        return has_zero

    strip_l = ind_c
    while strip_l > 0 and is_neutral(strip_l - 1):
        strip_l -= 1
    strip_r = ind_c
    while strip_r < cols - 1 and is_neutral(strip_r + 1):
        strip_r += 1
    return s, e, strip_l, strip_r

def count_components_for_color(g: List[List[int]], color: int, rows: int, cols: int,
                               s: int, e: int, strip_l: int, strip_r: int) -> int:
    if color == 0:
        return 0
    visited = [[False] * cols for _ in range(rows)]
    dirs: List[Tuple[int, int]] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0

    def touches_or_inside(rr: int, cc: int) -> bool:
        if s <= rr <= e and strip_l <= cc <= strip_r:
            return True
        for dr, dc in dirs:
            nr = rr + dr
            nc = cc + dc
            if 0 <= nr < rows and 0 <= nc < cols and s <= nr <= e and strip_l <= nc <= strip_r:
                return True
        return False

    def dfs(start_r: int, start_c: int) -> bool:
        touches = False
        stack: List[Tuple[int, int]] = [(start_r, start_c)]
        visited[start_r][start_c] = True
        while stack:
            cr, cc = stack.pop()
            if touches_or_inside(cr, cc):
                touches = True
            for dr, dc in dirs:
                nr = cr + dr
                nc = cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                    visited[nr][nc] = True
                    stack.append((nr, nc))
        return not touches

    for r in range(rows):
        for c in range(cols):
            if g[r][c] == color and not visited[r][c] and not (s <= r <= e and strip_l <= c <= strip_r):
                if dfs(r, c):
                    count += 1
    return count

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
    ind_rows.sort()
    indicators = [(r, g[r][ind_c]) for r in ind_rows]
    counts = [count_components_for_color(g, color, rows, cols, s, e, strip_l, strip_r) for _, color in indicators]
    width = strip_r - strip_l + 1
    height = 2 * len(indicators) + 1
    out = [[0] * width for _ in range(height)]
    for i, (r, color) in enumerate(indicators):
        pat_row = 2 * i + 1
        pos = 1
        for j in range(counts[i]):
            if pos < width:
                out[pat_row][pos] = color
            pos += 2
    return out
```