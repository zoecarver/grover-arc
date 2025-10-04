```python
from typing import List, Tuple
from collections import deque

def find_stem_column(g: List[List[int]], h: int, w: int) -> int:
    for r in range(h):
        for c in range(w):
            if g[r][c] == 4:
                return c
    return -1

def fill_stem_column(g: List[List[int]], out: List[List[int]], c: int, h: int) -> None:
    non8_rows: List[int] = [r for r in range(h) if g[r][c] != 8]
    if not non8_rows:
        return
    blocks: List[List[int]] = []
    curr: List[int] = [non8_rows[0]]
    for r in non8_rows[1:]:
        if r == curr[-1] + 1:
            curr.append(r)
        else:
            blocks.append(curr)
            curr = [r]
    blocks.append(curr)
    start_r: int = 0 if len(blocks) == 1 else blocks[0][0]
    for r in range(start_r, h):
        out[r][c] = 2

def get_row_groups(row: List[int], w: int) -> List[Tuple[int, int]]:
    groups: List[Tuple[int, int]] = []
    j: int = 0
    while j < w:
        if row[j] == 8:
            j += 1
            continue
        s: int = j
        j += 1
        while j < w and row[j] != 8:
            j += 1
        groups.append((s, j - 1))
    return groups

def fill_horizontal_gaps(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed: bool = False
    for r in range(h):
        groups: List[Tuple[int, int]] = get_row_groups(g[r], w)
        for i in range(len(groups) - 1):
            left_start: int
            left_end: int
            right_start: int
            right_end: int
            left_start, left_end = groups[i]
            right_start, right_end = groups[i + 1]
            if left_end + 1 >= right_start:
                continue
            has1_left: bool = any(g[r][cc] == 1 for cc in range(left_start, left_end + 1))
            has1_right: bool = any(g[r][cc] == 1 for cc in range(right_start, right_end + 1))
            border_left: bool = g[r][left_end] == 3
            border_right: bool = g[r][right_start] == 3
            if has1_left and has1_right and (border_left or border_right):
                for cc in range(left_end + 1, right_start):
                    if out[r][cc] == 8:
                        out[r][cc] = 2
                        changed = True
    return changed

def get_col_groups(g: List[List[int]], c: int, h: int) -> List[Tuple[int, int]]:
    groups: List[Tuple[int, int]] = []
    i: int = 0
    while i < h:
        if g[i][c] == 8:
            i += 1
            continue
        s: int = i
        i += 1
        while i < h and g[i][c] != 8:
            i += 1
        groups.append((s, i - 1))
    return groups

def fill_vertical_gaps(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed: bool = False
    for c in range(w):
        groups: List[Tuple[int, int]] = get_col_groups(g, c, h)
        for i in range(len(groups) - 1):
            upper_start: int
            upper_end: int
            lower_start: int
            lower_end: int
            upper_start, upper_end = groups[i]
            lower_start, lower_end = groups[i + 1]
            if upper_end + 1 >= lower_start:
                continue
            has1_upper: bool = any(g[rr][c] == 1 for rr in range(upper_start, upper_end + 1))
            has1_lower: bool = any(g[rr][c] == 1 for rr in range(lower_start, lower_end + 1))
            border_upper: bool = g[upper_end][c] == 3
            border_lower: bool = g[lower_start][c] == 3
            if has1_upper and has1_lower and (border_upper or border_lower):
                for rr in range(upper_end + 1, lower_start):
                    if out[rr][c] == 8:
                        out[rr][c] = 2
                        changed = True
    return changed

def flood_fill(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    visited: List[List[bool]] = [[False] * w for _ in range(h)]
    q: deque = deque()
    for r in range(h):
        for c in range(w):
            if out[r][c] == 2:
                q.append((r, c))
                visited[r][c] = True
    dirs: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    changed: bool = False
    while q:
        r: int
        c: int
        r, c = q.popleft()
        for dr, dc in dirs:
            nr: int = r + dr
            nc: int = c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] in (1, 3) and out[nr][nc] == 8:
                out[nr][nc] = 2
                visited[nr][nc] = True
                q.append((nr, nc))
                changed = True
    return changed

def extend_vertical_edges(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed: bool = False
    for c in range(w):
        groups: List[Tuple[int, int]] = get_col_groups(g, c, h)
        if not groups:
            continue
        # upward
        start_r: int
        end_r: int
        start_r, end_r = groups[0]
        if start_r > 0:
            top_cell: int = g[start_r][c]
            has1: bool = any(g[rr][c] == 1 for rr in range(start_r, end_r + 1))
            has2: bool = any(out[rr][c] == 2 for rr in range(start_r, end_r + 1))
            if top_cell == 3 and has1 and has2:
                for rr in range(start_r):
                    if out[rr][c] == 8:
                        out[rr][c] = 2
                        changed = True
        # downward
        start_r, end_r = groups[-1]
        if end_r < h - 1:
            bottom_cell: int = g[end_r][c]
            has1 = any(g[rr][c] == 1 for rr in range(start_r, end_r + 1))
            has2 = any(out[rr][c] == 2 for rr in range(start_r, end_r + 1))
            if bottom_cell == 3 and has1 and has2:
                for rr in range(end_r + 1, h):
                    if out[rr][c] == 8:
                        out[rr][c] = 2
                        changed = True
    return changed

def extend_horizontal_edges(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed: bool = False
    for r in range(h):
        groups: List[Tuple[int, int]] = get_row_groups(g[r], w)
        if not groups:
            continue
        # leftward
        start_c: int
        end_c: int
        start_c, end_c = groups[0]
        if start_c > 0:
            left_cell: int = g[r][start_c]
            has1: bool = any(g[r][cc] == 1 for cc in range(start_c, end_c + 1))
            has2: bool = any(out[r][cc] == 2 for cc in range(start_c, end_c + 1))
            if left_cell == 3 and has1 and has2:
                for cc in range(start_c):
                    if out[r][cc] == 8:
                        out[r][cc] = 2
                        changed = True
        # rightward
        start_c, end_c = groups[-1]
        if end_c < w - 1:
            right_cell: int = g[r][end_c]
            has1 = any(g[r][cc] == 1 for cc in range(start_c, end_c + 1))
            has2 = any(out[r][cc] == 2 for cc in range(start_c, end_c + 1))
            if right_cell == 3 and has1 and has2:
                for cc in range(end_c + 1, w):
                    if out[r][cc] == 8:
                        out[r][cc] = 2
                        changed = True
    return changed

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h: int = len(g)
    w: int = len(g[0])
    out: List[List[int]] = [[8] * w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c] in (2, 4):
                out[r][c] = 2
    stem_col: int = find_stem_column(g, h, w)
    if stem_col != -1:
        fill_stem_column(g, out, stem_col, h)
    changed: bool = True
    while changed:
        changed = False
        if fill_horizontal_gaps(g, out, h, w):
            changed = True
        if fill_vertical_gaps(g, out, h, w):
            changed = True
        if flood_fill(g, out, h, w):
            changed = True
        if extend_horizontal_edges(g, out, h, w):
            changed = True
        if extend_vertical_edges(g, out, h, w):
            changed = True
    return out
```