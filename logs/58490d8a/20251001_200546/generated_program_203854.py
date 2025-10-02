```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    """Extract background color from top-left cell."""
    return g[0][0] if g and g[0] else 0

def find_indicator_column_and_singles(g: List[List[int]], bg: int, rows: int, cols: int) -> Tuple[int, List[int], List[int]]:
    """Find column with maximum number of single-cell non-bg non-zero indicators; return column, sorted rows, colors."""
    max_count = 0
    best_c = -1
    best_rows: List[int] = []
    best_colors: List[int] = []
    for c in range(cols):
        singles: List[Tuple[int, int]] = []
        for r in range(rows):
            if g[r][c] != bg and g[r][c] != 0:
                is_single = True
                if r > 0 and g[r-1][c] != bg and g[r-1][c] != 0:
                    is_single = False
                if r < rows - 1 and g[r+1][c] != bg and g[r+1][c] != 0:
                    is_single = False
                if is_single:
                    singles.append((r, g[r][c]))
        count = len(singles)
        if count > max_count:
            max_count = count
            best_c = c
            best_rows = [s[0] for s in singles]
            best_colors = [s[1] for s in singles]
    best_rows.sort()
    return best_c, best_rows, best_colors

def get_strip_bounds(g: List[List[int]], ind_rows: List[int], bg: int, rows: int, cols: int, ind_c: int) -> Tuple[int, int, int, int]:
    """Compute strip bounds: vertical around indicators +/-1, horizontal expansion to neutral (bg or 0) columns."""
    if not ind_rows:
        return 0, 0, 0, 0
    min_r = min(ind_rows)
    max_r = max(ind_rows)
    s = max(0, min_r - 1)
    e = min(rows - 1, max_r + 1)

    def is_neutral_column(candidate_c: int, start_r: int, end_r: int) -> bool:
        for rr in range(start_r, end_r + 1):
            val = g[rr][candidate_c]
            if val != bg and val != 0:
                return False
        return True

    strip_l = ind_c
    while strip_l > 0 and is_neutral_column(strip_l - 1, s, e):
        strip_l -= 1
    strip_r = ind_c
    while strip_r < cols - 1 and is_neutral_column(strip_r + 1, s, e):
        strip_r += 1
    return s, e, strip_l, strip_r

def count_components(g: List[List[int]], color: int, rows: int, cols: int,
                      s: int, e: int, strip_l: int, strip_r: int) -> int:
    """Count 8-connected components of color entirely outside and not touching the strip."""
    if color == 0:
        return 0
    visited = [[False] * cols for _ in range(rows)]
    dirs: List[Tuple[int, int]] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0

    def flood(start_r: int, start_c: int) -> bool:
        touches_strip = False
        stack: List[Tuple[int, int]] = [(start_r, start_c)]
        visited[start_r][start_c] = True
        while stack:
            cr, cc = stack.pop()
            if s <= cr <= e and strip_l <= cc <= strip_r:
                touches_strip = True
            for dr, dc in dirs:
                nr = cr + dr
                nc = cc + dc
                if (0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color):
                    visited[nr][nc] = True
                    stack.append((nr, nc))
        return not touches_strip

    for rr in range(rows):
        for cc in range(cols):
            if (g[rr][cc] == color and not visited[rr][cc] and
                not (s <= rr <= e and strip_l <= cc <= strip_r)):
                if flood(rr, cc):
                    count += 1
    return count

def build_output(num_indicators: int, colors: List[int], counts: List[int], width: int) -> List[List[int]]:
    """Build output grid with alternating empty and patterned rows using color repetitions."""
    height = 2 * num_indicators + 1
    output = [[0] * width for _ in range(height)]
    for i in range(num_indicators):
        pat_row = 2 * i + 1
        colr = colors[i]
        cnt = counts[i]
        pos = 1
        for _ in range(cnt):
            if pos < width:
                output[pat_row][pos] = colr
            pos += 2
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing all rules to solve the puzzle."""
    if not g or not g[0]:
        return [[0]]
    rows = len(g)
    cols = len(g[0])
    bg = get_background(g)
    ind_c, ind_rows, colors = find_indicator_column_and_singles(g, bg, rows, cols)
    if not ind_rows:
        return [[0]]
    s, e, strip_l, strip_r = get_strip_bounds(g, ind_rows, bg, rows, cols, ind_c)
    width = strip_r - strip_l + 1
    counts = [count_components(g, colr, rows, cols, s, e, strip_l, strip_r) for colr in colors]
    return build_output(len(ind_rows), colors, counts, width)
```