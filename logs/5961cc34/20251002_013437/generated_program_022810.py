```python
from typing import List
from collections import deque

def find_column(g: List[List[int]]) -> int:
    h = len(g)
    if h == 0:
        return -1
    w = len(g[0])
    for r in range(h):
        for s in range(w):
            if g[r][s] == 4:
                return s
    return -1

def fill_stem(g: List[List[int]], out: List[List[int]], c: int) -> None:
    h = len(g)
    non8_rows = [r for r in range(h) if g[r][c] != 8]
    if not non8_rows:
        return
    blocks = []
    curr = [non8_rows[0]]
    for r in non8_rows[1:]:
        if r == curr[-1] + 1:
            curr.append(r)
        else:
            blocks.append(curr)
            curr = [r]
    blocks.append(curr)
    if len(blocks) == 1:
        start_row = 0
    else:
        start_row = min(blocks[0])
    for r in range(start_row, h):
        out[r][c] = 2

def get_groups_row(row: List[int]) -> List[tuple[int, int]]:
    groups = []
    n = len(row)
    j = 0
    while j < n:
        if row[j] == 8:
            j += 1
            continue
        s = j
        j += 1
        while j < n and row[j] != 8:
            j += 1
        groups.append((s, j - 1))
    return groups

def fill_horizontal_gaps(g: List[List[int]], out: List[List[int]], r: int, w: int) -> None:
    row = g[r]
    groups = get_groups_row(row)
    for i in range(1, len(groups)):
        left_start, left_end = groups[i - 1]
        right_start, right_end = groups[i]
        gap_start = left_end + 1
        gap_end = right_start - 1
        if gap_start > gap_end:
            continue
        left_has_1 = any(g[r][j] == 1 for j in range(left_start, left_end + 1))
        right_has_1 = any(g[r][j] == 1 for j in range(right_start, right_end + 1))
        if not (left_has_1 and right_has_1):
            continue
        left_border = g[r][left_end]
        right_border = g[r][right_start]
        if left_border == 3 or right_border == 3:
            for j in range(gap_start, gap_end + 1):
                out[r][j] = 2

def get_groups_col(g: List[List[int]], s: int) -> List[tuple[int, int]]:
    h = len(g)
    groups = []
    i = 0
    while i < h:
        if g[i][s] == 8:
            i += 1
            continue
        start = i
        i += 1
        while i < h and g[i][s] != 8:
            i += 1
        groups.append((start, i - 1))
    return groups

def fill_vertical_gaps(g: List[List[int]], out: List[List[int]], s: int, h: int) -> None:
    groups = get_groups_col(g, s)
    for i in range(1, len(groups)):
        upper_start, upper_end = groups[i - 1]
        lower_start, lower_end = groups[i]
        gap_start = upper_end + 1
        gap_end = lower_start - 1
        if gap_start > gap_end:
            continue
        upper_has_1 = any(g[j][s] == 1 for j in range(upper_start, upper_end + 1))
        lower_has_1 = any(g[j][s] == 1 for j in range(lower_start, lower_end + 1))
        if not (upper_has_1 and lower_has_1):
            continue
        upper_border = g[upper_end][s]
        lower_border = g[lower_start][s]
        if upper_border == 3 or lower_border == 3:
            for rr in range(gap_start, gap_end + 1):
                out[rr][s] = 2

def flood_fill(g: List[List[int]], out: List[List[int]], h: int, w: int) -> None:
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        for s in range(w):
            if out[r][s] == 2:
                q.append((r, s))
                visited[r][s] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] in (1, 3):
                out[nx][ny] = 2
                visited[nx][ny] = True
                q.append((nx, ny))

def extend_horizontal_edges(g: List[List[int]], out: List[List[int]], r: int, w: int) -> None:
    groups = get_groups_row(g[r])
    if not groups:
        return
    first_start, first_end = groups[0]
    has_one = any(g[r][j] == 1 for j in range(first_start, first_end + 1))
    is_filled = any(out[r][j] == 2 for j in range(first_start, first_end + 1))
    if g[r][first_start] == 3 and has_one and is_filled:
        for j in range(0, first_start):
            out[r][j] = 2
    last_start, last_end = groups[-1]
    has_one = any(g[r][j] == 1 for j in range(last_start, last_end + 1))
    is_filled = any(out[r][j] == 2 for j in range(last_start, last_end + 1))
    if g[r][last_end] == 3 and has_one and is_filled:
        for j in range(last_end + 1, w):
            out[r][j] = 2

def extend_vertical_edges(g: List[List[int]], out: List[List[int]], s: int, h: int) -> None:
    groups = get_groups_col(g, s)
    if not groups:
        return
    first_start, first_end = groups[0]
    has_one = any(g[j][s] == 1 for j in range(first_start, first_end + 1))
    is_filled = any(out[j][s] == 2 for j in range(first_start, first_end + 1))
    if g[first_start][s] == 3 and has_one and is_filled:
        for rr in range(0, first_start):
            out[rr][s] = 2
    last_start, last_end = groups[-1]
    has_one = any(g[j][s] == 1 for j in range(last_start, last_end + 1))
    is_filled = any(out[j][s] == 2 for j in range(last_start, last_end + 1))
    if g[last_end][s] == 3 and has_one and is_filled:
        for rr in range(last_end + 1, h):
            out[rr][s] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    out = [[8] * w for _ in range(h)]
    c = find_column(g)
    if c != -1:
        fill_stem(g, out, c)
    for r in range(h):
        for s in range(w):
            if g[r][s] in (2, 4):
                out[r][s] = 2
    for r in range(h):
        fill_horizontal_gaps(g, out, r, w)
    for s in range(w):
        fill_vertical_gaps(g, out, s, h)
    flood_fill(g, out, h, w)
    for r in range(h):
        extend_horizontal_edges(g, out, r, w)
    for s in range(w):
        extend_vertical_edges(g, out, s, h)
    return out
```