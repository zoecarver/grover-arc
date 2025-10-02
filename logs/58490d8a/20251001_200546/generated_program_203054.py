```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def find_indicators(g: List[List[int]], bg: int) -> Tuple[int, List[Tuple[int, int]]]:
    rows = len(g)
    cols = len(g[0]) if rows else 0
    max_count = 0
    best_c = -1
    best_inds: List[Tuple[int, int]] = []
    for c in range(cols):
        indicators: List[Tuple[int, int]] = []
        r = 0
        while r < rows:
            if g[r][c] != bg and g[r][c] != 0:
                run_start = r
                run_color = g[r][c]
                r += 1
                while r < rows and g[r][c] != bg and g[r][c] != 0:
                    r += 1
                run_len = r - run_start
                if run_len == 1:
                    indicators.append((run_start, run_color))
            else:
                r += 1
        num = len(indicators)
        if num > max_count:
            max_count = num
            best_c = c
            best_inds = indicators
    best_inds.sort(key=lambda x: x[0])
    return best_c, best_inds

def get_strip_bounds(g: List[List[int]], ind_c: int, ind_rows: List[int], bg: int, rows: int, cols: int) -> Tuple[int, int, int, int]:
    if not ind_rows:
        return 0, 0, 0, 0
    min_r = min(ind_rows)
    max_r = max(ind_rows)
    s = max(0, min_r - 1)
    e = min(rows - 1, max_r + 1)
    def can_expand_to(cand_c: int) -> bool:
        if cand_c < 0 or cand_c >= cols:
            return False
        has_non_bg_non_zero = False
        has_zero = False
        for rr in range(s, e + 1):
            val = g[rr][cand_c]
            if val != bg and val != 0:
                has_non_bg_non_zero = True
            if val == 0:
                has_zero = True
        return not has_non_bg_non_zero and has_zero
    strip_l = ind_c
    while strip_l > 0 and can_expand_to(strip_l - 1):
        strip_l -= 1
    strip_r = ind_c
    while strip_r < cols - 1 and can_expand_to(strip_r + 1):
        strip_r += 1
    return s, e, strip_l, strip_r

def count_components_for_color(g: List[List[int]], color: int, s: int, e: int, l: int, r: int, rows: int, cols: int) -> int:
    if color == 0:
        return 0
    visited = [[False] * cols for _ in range(rows)]
    dirs: List[Tuple[int, int]] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    def does_touch(start_r: int, start_c: int) -> bool:
        stack: List[Tuple[int, int]] = [(start_r, start_c)]
        visited[start_r][start_c] = True
        touches = False
        while stack:
            cr, cc = stack.pop()
            if s <= cr <= e and l <= cc <= r:
                touches = True
            for dr, dc in dirs:
                nr = cr + dr
                nc = cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                    visited[nr][nc] = True
                    stack.append((nr, nc))
        return touches
    count = 0
    for sr in range(rows):
        for sc in range(cols):
            if g[sr][sc] == color and not visited[sr][sc] and not (s <= sr <= e and l <= sc <= r):
                if not does_touch(sr, sc):
                    count += 1
    return count

def build_output(indicators: List[Tuple[int, int]], counts: List[int], strip_width: int) -> List[List[int]]:
    num = len(indicators)
    if num == 0:
        return [[0]]
    height = 2 * num + 1
    out = [[0] * strip_width for _ in range(height)]
    for k in range(num):
        row_out = 2 * k + 1
        color = indicators[k][1]
        cnt = counts[k]
        pos = 1
        for _ in range(cnt):
            if pos < strip_width:
                out[row_out][pos] = color
                pos += 2
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    rows = len(g)
    cols = len(g[0])
    bg = get_background(g)
    ind_c, ind_list = find_indicators(g, bg)
    if not ind_list:
        return [[0]]
    ind_rows = [ind[0] for ind in ind_list]
    s, e, strip_l, strip_r = get_strip_bounds(g, ind_c, ind_rows, bg, rows, cols)
    strip_w = strip_r - strip_l + 1
    component_counts = []
    for _, color in ind_list:
        cnt = count_components_for_color(g, color, s, e, strip_l, strip_r, rows, cols)
        component_counts.append(cnt)
    return build_output(ind_list, component_counts, strip_w)
```