```python
from typing import List, Tuple
import sys

def get_background(g: List[List[int]]) -> int:
    """Extract background color from top-left cell."""
    return g[0][0] if g and g[0] else 0

def find_indicator_column_and_rows(g: List[List[int]], bg: int, rows: int, cols: int) -> Tuple[int, List[int]]:
    """Find column with maximum isolated (non-adjacent row) non-bg non-zero cells; return column and sorted row indices."""
    max_count = 0
    best_c = -1
    best_rows: List[int] = []
    for c in range(cols):
        ind_rs: List[int] = [r for r in range(rows) if g[r][c] != bg and g[r][c] != 0]
        if ind_rs and all(ind_rs[i] != ind_rs[i-1] + 1 for i in range(1, len(ind_rs))):
            if len(ind_rs) > max_count:
                max_count = len(ind_rs)
                best_c = c
                best_rows = ind_rs[:]
    best_rows.sort()
    return best_c, best_rows

def get_strip_bounds(g: List[List[int]], ind_rows: List[int], bg: int, rows: int, cols: int, ind_c: int) -> Tuple[int, int, int, int]:
    """Compute strip row/column bounds: vertical around indicators +/-1, horizontal expand to neutral columns (only bg or 0)."""
    if not ind_rows:
        return 0, 0, 0, 0
    min_r = min(ind_rows)
    max_r = max(ind_rows)
    s = max(0, min_r - 1)
    e = min(rows - 1, max_r + 1)

    def can_expand_to(candidate_c: int, start_r: int, end_r: int) -> bool:
        if candidate_c < 0 or candidate_c >= cols:
            return False
        segment = [g[r][candidate_c] for r in range(start_r, end_r + 1)]
        has_non_bg_non_zero = any(val != bg and val != 0 for val in segment)
        return not has_non_bg_non_zero

    strip_left = ind_c
    while strip_left > 0 and can_expand_to(strip_left - 1, s, e):
        strip_left -= 1
    strip_right = ind_c
    while strip_right < cols - 1 and can_expand_to(strip_right + 1, s, e):
        strip_right += 1
    return s, e, strip_left, strip_right

def count_components_for_color(g: List[List[int]], color: int, rows: int, cols: int,
                               strip_s: int, strip_e: int, strip_l: int, strip_r: int) -> int:
    """Count 8-connected components of color entirely outside and not touching the strip."""
    if color == 0 or color == g[0][0]:
        return 0
    visited = [[False] * cols for _ in range(rows)]
    dirs: List[Tuple[int, int]] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0

    def dfs(start_r: int, start_c: int) -> bool:
        touches = False
        stack: List[Tuple[int, int]] = [(start_r, start_c)]
        visited[start_r][start_c] = True
        while stack:
            cr, cc = stack.pop()
            if strip_s <= cr <= strip_e and strip_l <= cc <= strip_r:
                touches = True
            for dr, dc in dirs:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                    visited[nr][nc] = True
                    stack.append((nr, nc))
        return not touches

    for r in range(rows):
        for c in range(cols):
            if (g[r][c] == color and not visited[r][c] and
                not (strip_s <= r <= strip_e and strip_l <= c <= strip_r)):
                if dfs(r, c):
                    count += 1
    return count

def build_output(ind_rows: List[int], ind_c: int, g: List[List[int]], counts: List[int],
                 strip_l: int, strip_r: int) -> List[List[int]]:
    """Build output grid: alternating empty and patterned rows with color repetitions."""
    num_ind = len(ind_rows)
    if num_ind == 0:
        return [[0]]
    height = 2 * num_ind + 1
    width = strip_r - strip_l + 1
    colors = [g[r][ind_c] for r in ind_rows]
    output: List[List[int]] = []
    for h in range(height):
        if h % 2 == 0:
            output.append([0] * width)
        else:
            k = (h - 1) // 2
            colr = colors[k]
            cnt = counts[k]
            row = [0] * width
            for i in range(cnt):
                pos = 1 + 2 * i
                if pos < width:
                    row[pos] = colr
            output.append(row)
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compose functions to process grid and generate output."""
    if not g or not g[0]:
        return [[0]]
    rows = len(g)
    cols = len(g[0])
    bg = get_background(g)
    ind_c, ind_rows = find_indicator_column_and_rows(g, bg, rows, cols)
    if ind_c == -1:
        return [[0]]
    strip_s, strip_e, strip_l, strip_r = get_strip_bounds(g, ind_rows, bg, rows, cols, ind_c)
    colors = [g[r][ind_c] for r in ind_rows]
    counts = [count_components_for_color(g, colr, rows, cols, strip_s, strip_e, strip_l, strip_r) for colr in colors]
    return build_output(ind_rows, ind_c, g, counts, strip_l, strip_r)
```