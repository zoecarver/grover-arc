```python
from typing import List, Tuple
from collections import deque

def find_column(g: List[List[int]], h: int, w: int) -> int:
    for r in range(h):
        for c in range(w):
            if g[r][c] == 4:
                return c
    return -1

def fill_stem(g: List[List[int]], out: List[List[int]], c: int, h: int, w: int) -> None:
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

def get_row_groups(row: List[int], w: int) -> List[Tuple[int, int]]:
    groups = []
    j = 0
    while j < w:
        if row[j] == 8:
            j += 1
            continue
        s = j
        j += 1
        while j < w and row[j] != 8:
            j += 1
        groups.append((s, j - 1))
    return groups

def fill_horizontal_gaps(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for r in range(h):
        groups = get_row_groups(g[r], w)
        for i in range(len(groups) - 1):
            s1, e1 = groups[i]
            s2, e2 = groups[i + 1]
            if e1 + 1 >= s2:
                continue
            has1_1 = any(g[r][cc] == 1 for cc in range(s1, e1 + 1))
            if not has1_1:
                continue
            has1_2 = any(g[r][cc] == 1 for cc in range(s2, e2 + 1))
            if not has1_2:
                continue
            border3 = (g[r][e1] == 3) or (g[r][s2] == 3)
            if not border3:
                continue
            for cc in range(e1 + 1, s2):
                if out[r][cc] == 8:
                    out[r][cc] = 2
                    changed = True
    return changed

def get_col_groups(g: List[List[int]], c: int, h: int) -> List[Tuple[int, int]]:
    groups = []
    i = 0
    while i < h:
        if g[i][c] == 8:
            i += 1
            continue
        s = i
        i += 1
        while i < h and g[i][c] != 8:
            i += 1
        groups.append((s, i - 1))
    return groups

def fill_vertical_gaps(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for c in range(w):
        groups = get_col_groups(g, c, h)
        for i in range(len(groups) - 1):
            s1, e1 = groups[i]
            s2, e2 = groups[i + 1]
            if e1 + 1 >= s2:
                continue
            has1_1 = any(g[rr][c] == 1 for rr in range(s1, e1 + 1))
            if not has1_1:
                continue
            has1_2 = any(g[rr][c] == 1 for rr in range(s2, e2 + 1))
            if not has1_2:
                continue
            border3 = (g[e1][c] == 3) or (g[s2][c] == 3)
            if not border3:
                continue
            for rr in range(e1 + 1, s2):
                if out[rr][c] == 8:
                    out[rr][c] = 2
                    changed = True
    return changed

def flood_fill(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        for c in range(w):
            if out[r][c] == 2 and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    changed = False
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and out[nx][ny] == 8 and g[nx][ny] in (1, 3):
                out[nx][ny] = 2
                visited[nx][ny] = True
                q.append((nx, ny))
                changed = True
    return changed

def extend_horizontal_edges(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for r in range(h):
        groups = get_row_groups(g[r], w)
        if not groups:
            continue
        # leftmost
        s, e = groups[0]
        if s > 0 and g[r][s] == 3:
            has1 = any(g[r][cc] == 1 for cc in range(s, e + 1))
            if has1:
                has2 = any(out[r][cc] == 2 for cc in range(s, e + 1))
                if has2:
                    for cc in range(s):
                        if out[r][cc] == 8:
                            out[r][cc] = 2
                            changed = True
        # rightmost
        s, e = groups[-1]
        if e < w - 1 and g[r][e] == 3:
            has1 = any(g[r][cc] == 1 for cc in range(s, e + 1))
            if has1:
                has2 = any(out[r][cc] == 2 for cc in range(s, e + 1))
                if has2:
                    for cc in range(e + 1, w):
                        if out[r][cc] == 8:
                            out[r][cc] = 2
                            changed = True
    return changed

def extend_vertical_edges(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for c in range(w):
        groups = get_col_groups(g, c, h)
        if not groups:
            continue
        # topmost
        s, e = groups[0]
        if s > 0 and g[s][c] == 3:
            has1 = any(g[rr][c] == 1 for rr in range(s, e + 1))
            if has1:
                has2 = any(out[rr][c] == 2 for rr in range(s, e + 1))
                if has2:
                    for rr in range(s):
                        if out[rr][c] == 8:
                            out[rr][c] = 2
                            changed = True
        # bottommost
        s, e = groups[-1]
        if e < h - 1 and g[e][c] == 3:
            has1 = any(g[rr][c] == 1 for rr in range(s, e + 1))
            if has1:
                has2 = any(out[rr][c] == 2 for rr in range(s, e + 1))
                if has2:
                    for rr in range(e + 1, h):
                        if out[rr][c] == 8:
                            out[rr][c] = 2
                            changed = True
    return changed

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    out = [[8] * w for _ in range(h)]
    for r in range(h):
        for c in range(w):
            if g[r][c] in (2, 4):
                out[r][c] = 2
    stem_col = find_column(g, h, w)
    if stem_col != -1:
        fill_stem(g, out, stem_col, h, w)
    while True:
        changed = False
        changed |= fill_horizontal_gaps(g, out, h, w)
        changed |= fill_vertical_gaps(g, out, h, w)
        changed |= flood_fill(g, out, h, w)
        changed |= extend_horizontal_edges(g, out, h, w)
        changed |= extend_vertical_edges(g, out, h, w)
        if not changed:
            break
    return out
```