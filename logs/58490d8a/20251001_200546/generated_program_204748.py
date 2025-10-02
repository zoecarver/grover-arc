```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def find_indicators(g: List[List[int]], bg: int, rows: int, cols: int) -> Tuple[int, List[Tuple[int, int]]]:
    max_cnt = 0
    best_c = -1
    best_inds: List[Tuple[int, int]] = []
    for c in range(cols):
        cand_rows = [r for r in range(rows) if g[r][c] != bg and g[r][c] != 0]
        if cand_rows:
            cand_rows.sort()
            if all(cand_rows[j] >= cand_rows[j - 1] + 2 for j in range(1, len(cand_rows))):
                if len(cand_rows) > max_cnt:
                    max_cnt = len(cand_rows)
                    best_c = c
                    best_inds = [(r, g[r][c]) for r in cand_rows]
    if max_cnt == 0:
        return -1, []
    best_inds.sort(key=lambda x: x[0])
    return best_c, best_inds

def get_strip_bounds(g: List[List[int]], ind_rows: List[int], bg: int, rows: int, cols: int, ind_c: int) -> Tuple[int, int, int, int]:
    if not ind_rows:
        return 0, 0, 0, 0
    min_r = min(ind_rows)
    max_r = max(ind_rows)
    s = max(0, min_r - 1)
    e = min(rows - 1, max_r + 1)
    def is_neutral(c: int) -> bool:
        has_non = any(g[rr][c] != bg and g[rr][c] != 0 for rr in range(s, e + 1))
        has_zero = any(g[rr][c] == 0 for rr in range(s, e + 1))
        return not has_non and has_zero
    l = ind_c
    while l > 0 and is_neutral(l - 1):
        l -= 1
    r = ind_c
    while r < cols - 1 and is_neutral(r + 1):
        r += 1
    return s, e, l, r

def touches_strip(rr: int, cc: int, s: int, e: int, l: int, r: int, rows: int, cols: int) -> bool:
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
    if color == 0:
        return 0
    visited = [[False] * cols for _ in range(rows)]
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for sr in range(rows):
        for sc in range(cols):
            if g[sr][sc] == color and not visited[sr][sc]:
                touches = False
                stack: List[Tuple[int, int]] = [(sr, sc)]
                visited[sr][sc] = True
                if touches_strip(sr, sc, s, e, l, r, rows, cols):
                    touches = True
                while stack:
                    cr, cc = stack.pop()
                    for dr, dc in dirs:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                            if touches_strip(nr, nc, s, e, l, r, rows, cols):
                                touches = True
                if not touches:
                    count += 1
    return count

def build_output(inds: List[Tuple[int, int]], strip_l: int, strip_r: int, counts: List[int]) -> List[List[int]]:
    num = len(inds)
    width = strip_r - strip_l + 1
    height = 2 * num + 1
    out = [[0] * width for _ in range(height)]
    for i in range(num):
        pat_row = 2 * i + 1
        color = inds[i][1]
        cnt = counts[i]
        pos = 1
        for _ in range(cnt):
            if pos < width:
                out[pat_row][pos] = color
            pos += 2
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return [[0]]
    bg = get_background(g)
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    ind_c, inds = find_indicators(g, bg, rows, cols)
    if not inds:
        return [[0]]
    ind_rows = [r for r, _ in inds]
    s, e, strip_l, strip_r = get_strip_bounds(g, ind_rows, bg, rows, cols, ind_c)
    counts = [count_isolated_components(g, color, rows, cols, s, e, strip_l, strip_r) for _, color in inds]
    return build_output(inds, strip_l, strip_r, counts)
```