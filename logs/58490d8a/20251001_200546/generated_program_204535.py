```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    """Extract background color from top-left cell."""
    return g[0][0] if g and g[0] else 0

def find_indicators(g: List[List[int]], bg: int, rows: int, cols: int) -> Tuple[int, List[Tuple[int, int]]]:
    """Find column with maximum isolated non-bg non-zero indicators; return column and sorted (row, color) list."""
    max_cnt = 0
    best_c = -1
    best_inds: List[Tuple[int, int]] = []
    for c in range(cols):
        cand_rows = [r for r in range(rows) if g[r][c] != bg and g[r][c] != 0]
        if cand_rows:
            cand_rows.sort()
            isolated = all(cand_rows[i] >= cand_rows[i - 1] + 2 for i in range(1, len(cand_rows)))
            if isolated and len(cand_rows) > max_cnt:
                max_cnt = len(cand_rows)
                best_c = c
                best_inds = [(r, g[r][c]) for r in cand_rows]
    if max_cnt == 0:
        return -1, []
    best_inds.sort(key=lambda x: x[0])
    return best_c, best_inds

def get_strip_bounds(g: List[List[int]], ind_rows: List[int], bg: int, rows: int, cols: int, ind_c: int) -> Tuple[int, int, int, int]:
    """Compute vertical and horizontal strip bounds around indicators, expanding to neutral columns."""
    if not ind_rows:
        return 0, 0, 0, 0
    min_r = min(ind_rows)
    max_r = max(ind_rows)
    s = max(0, min_r - 1)
    e = min(rows - 1, max_r + 1)

    def is_neutral(cand_c: int) -> bool:
        for rr in range(s, e + 1):
            val = g[rr][cand_c]
            if val != bg and val != 0:
                return False
        return True

    strip_l = ind_c
    while strip_l > 0 and is_neutral(strip_l - 1):
        strip_l -= 1
    strip_r = ind_c
    while strip_r < cols - 1 and is_neutral(strip_r + 1):
        strip_r += 1
    return s, e, strip_l, strip_r

def cell_touches_strip(rr: int, cc: int, s: int, e: int, l: int, r: int, rows: int, cols: int) -> bool:
    """Check if cell (rr, cc) is inside or adjacent (8-dir) to the strip."""
    if s <= rr <= e and l <= cc <= r:
        return True
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in dirs:
        nr = rr + dr
        nc = cc + dc
        if 0 <= nr < rows and 0 <= nc < cols and s <= nr <= e and l <= nc <= r:
            return True
    return False

def count_isolated_components(g: List[List[int]], color: int, rows: int, cols: int,
                              s: int, e: int, l: int, r: int) -> int:
    """Count 8-connected components of color that do not touch the strip (inside or adjacent)."""
    if color == 0:
        return 0
    visited = [[False] * cols for _ in range(rows)]
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0

    def explore_component(start_r: int, start_c: int) -> bool:
        touches = False
        stack: List[Tuple[int, int]] = [(start_r, start_c)]
        visited[start_r][start_c] = True
        while stack:
            cr, cc = stack.pop()
            if cell_touches_strip(cr, cc, s, e, l, r, rows, cols):
                touches = True
            for dr, dc in dirs:
                nr = cr + dr
                nc = cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                    visited[nr][nc] = True
                    stack.append((nr, nc))
        return not touches

    for rr in range(rows):
        for cc in range(cols):
            if g[rr][cc] == color and not visited[rr][cc] and not (s <= rr <= e and l <= cc <= r):
                if explore_component(rr, cc):
                    count += 1
    return count

def build_patterned_output(inds: List[Tuple[int, int]], strip_l: int, strip_r: int, counts: List[int]) -> List[List[int]]:
    """Build output grid with alternating empty and patterned rows based on indicators and counts."""
    if not inds:
        return [[0]]
    num_inds = len(inds)
    width = strip_r - strip_l + 1
    height = 2 * num_inds + 1
    output = [[0] * width for _ in range(height)]
    for i, (_, color) in enumerate(inds):
        pat_row = 2 * i + 1
        cnt = counts[i]
        pos = 1
        for _ in range(cnt):
            if pos < width:
                output[pat_row][pos] = color
            pos += 2
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compose functions to solve the puzzle."""
    if not g:
        return [[0]]
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    bg = get_background(g)
    ind_c, inds = find_indicators(g, bg, rows, cols)
    if not inds:
        return [[0]]
    ind_rows = [r for r, _ in inds]
    s, e, strip_l, strip_r = get_strip_bounds(g, ind_rows, bg, rows, cols, ind_c)
    counts = []
    for _, color in inds:
        cnt = count_isolated_components(g, color, rows, cols, s, e, strip_l, strip_r)
        counts.append(cnt)
    return build_patterned_output(inds, strip_l, strip_r, counts)
```