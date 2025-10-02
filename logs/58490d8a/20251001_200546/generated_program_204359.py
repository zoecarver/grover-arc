```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    """Extract background color from top-left cell."""
    return g[0][0] if g and g[0] else 0

def find_indicators(g: List[List[int]], bg: int, rows: int, cols: int) -> Tuple[int, List[Tuple[int, int]]]:
    """Find column with maximum isolated non-bg non-zero indicators; return column and sorted list of (row, color)."""
    max_cnt = 0
    best_c = -1
    best_inds: List[Tuple[int, int]] = []
    for c in range(cols):
        cand_rows = [r for r in range(rows) if g[r][c] != bg and g[r][c] != 0]
        if cand_rows:
            cand_rows.sort()
            is_isolated = all(cand_rows[j] >= cand_rows[j - 1] + 2 for j in range(1, len(cand_rows)))
            if is_isolated and len(cand_rows) > max_cnt:
                max_cnt = len(cand_rows)
                best_c = c
                best_inds = [(r, g[r][c]) for r in cand_rows]
    if max_cnt == 0:
        return -1, []
    best_inds.sort(key=lambda x: x[0])
    return best_c, best_inds

def can_expand(g: List[List[int]], bg: int, s: int, e: int, rows: int, cols: int, cand: int) -> bool:
    """Check if candidate column can be expanded into strip: no non-neutral, at least one 0."""
    if not (0 <= cand < cols):
        return False
    has_non_neutral = any(g[rr][cand] != bg and g[rr][cand] != 0 for rr in range(s, e + 1))
    has_zero = any(g[rr][cand] == 0 for rr in range(s, e + 1))
    return not has_non_neutral and has_zero

def is_touching(rr: int, cc: int, s: int, e: int, ls: int, rs: int, rows: int, cols: int) -> bool:
    """Check if cell (rr, cc) is inside strip or adjacent (8-dir) to strip."""
    if s <= rr <= e and ls <= cc <= rs:
        return True
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in dirs:
        nr = rr + dr
        nc = cc + dc
        if 0 <= nr < rows and 0 <= nc < cols and s <= nr <= e and ls <= nc <= rs:
            return True
    return False

def count_components(g: List[List[int]], color: int, rows: int, cols: int,
                      s: int, e: int, ls: int, rs: int) -> int:
    """Count 8-connected components of color fully outside and not touching (including diagonally) the strip."""
    if color == 0:
        return 0
    visited = [[False] * cols for _ in range(rows)]
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for start_r in range(rows):
        for start_c in range(cols):
            if g[start_r][start_c] == color and not visited[start_r][start_c]:
                if s <= start_r <= e and ls <= start_c <= rs:
                    continue  # Skip components starting inside strip
                touches = False
                stack: List[Tuple[int, int]] = [(start_r, start_c)]
                visited[start_r][start_c] = True
                if is_touching(start_r, start_c, s, e, ls, rs, rows, cols):
                    touches = True
                while stack:
                    cr, cc = stack.pop()
                    for dr, dc in dirs:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                            if is_touching(nr, nc, s, e, ls, rs, rows, cols):
                                touches = True
                if not touches:
                    count += 1
    return count

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compose rules to generate output grid from input."""
    if not g or not g[0]:
        return [[0]]
    rows = len(g)
    cols = len(g[0])
    bg = get_background(g)
    ind_c, inds = find_indicators(g, bg, rows, cols)
    if not inds:
        return [[0]]
    ind_rows = [r for r, _ in inds]
    min_r = min(ind_rows)
    max_r = max(ind_rows)
    s = max(0, min_r - 1)
    e = min(rows - 1, max_r + 1)
    l = ind_c
    while l > 0 and can_expand(g, bg, s, e, rows, cols, l - 1):
        l -= 1
    r = ind_c
    while r < cols - 1 and can_expand(g, bg, s, e, rows, cols, r + 1):
        r += 1
    width = r - l + 1
    colors = [colr for _, colr in inds]
    counts = [count_components(g, colr, rows, cols, s, e, l, r) for colr in colors]
    num = len(inds)
    height = 2 * num + 1
    out = [[0] * width for _ in range(height)]
    for i in range(num):
        pat_row = 2 * i + 1
        colr = colors[i]
        cnt = counts[i]
        pos = 1
        for _ in range(cnt):
            if pos < width:
                out[pat_row][pos] = colr
                pos += 2
            else:
                break
    return out
```