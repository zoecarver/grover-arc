```python
from typing import List, Tuple
from collections import deque

def get_groups_row(row: List[int]) -> List[Tuple[int, int]]:
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

def get_groups_col(g: List[List[int]], c: int) -> List[Tuple[int, int]]:
    h = len(g)
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

def fill_horizontal_gaps(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for r in range(h):
        row = g[r]
        groups = get_groups_row(row)
        for i in range(len(groups) - 1):
            ls, le = groups[i]
            rs, re = groups[i + 1]
            gap_s = le + 1
            gap_e = rs - 1
            if gap_s > gap_e:
                continue
            has1_l = any(g[r][j] == 1 for j in range(ls, le + 1))
            has1_r = any(g[r][j] == 1 for j in range(rs, re + 1))
            if not (has1_l and has1_r):
                continue
            border3 = (g[r][le] == 3) or (g[r][rs] == 3)
            if border3:
                for j in range(gap_s, gap_e + 1):
                    if out[r][j] == 8:
                        out[r][j] = 2
                        changed = True
    return changed

def fill_vertical_gaps(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for c in range(w):
        groups = get_groups_col(g, c)
        for i in range(len(groups) - 1):
            us, ue = groups[i]
            ls, le = groups[i + 1]
            gap_s = ue + 1
            gap_e = ls - 1
            if gap_s > gap_e:
                continue
            has1_u = any(g[k][c] == 1 for k in range(us, ue + 1))
            has1_l = any(g[k][c] == 1 for k in range(ls, le + 1))
            if not (has1_u and has1_l):
                continue
            border3 = (g[ue][c] == 3) or (g[ls][c] == 3)
            if border3:
                for k in range(gap_s, gap_e + 1):
                    if out[k][c] == 8:
                        out[k][c] = 2
                        changed = True
    return changed

def flood_fill(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        for cc in range(w):
            if out[r][cc] == 2 and not visited[r][cc]:
                q.append((r, cc))
                visited[r][cc] = True
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

def extend_horizontal(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for r in range(h):
        groups = get_groups_row(g[r])
        if not groups:
            continue
        # leftmost group
        ls, le = groups[0]
        if g[r][ls] == 3:
            has1 = any(g[r][j] == 1 for j in range(ls, le + 1))
            has2 = any(out[r][j] == 2 for j in range(ls, le + 1))
            if has1 and has2:
                for j in range(ls):
                    if out[r][j] == 8:
                        out[r][j] = 2
                        changed = True
        # rightmost group
        rs, re = groups[-1]
        if g[r][re] == 3:
            has1 = any(g[r][j] == 1 for j in range(rs, re + 1))
            has2 = any(out[r][j] == 2 for j in range(rs, re + 1))
            if has1 and has2:
                for j in range(re + 1, w):
                    if out[r][j] == 8:
                        out[r][j] = 2
                        changed = True
    return changed

def extend_vertical(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for c in range(w):
        groups = get_groups_col(g, c)
        if not groups:
            continue
        # top group
        us, ue = groups[0]
        if g[us][c] == 3:
            has1 = any(g[k][c] == 1 for k in range(us, ue + 1))
            has2 = any(out[k][c] == 2 for k in range(us, ue + 1))
            if has1 and has2:
                for k in range(us):
                    if out[k][c] == 8:
                        out[k][c] = 2
                        changed = True
        # bottom group
        ls, le = groups[-1]
        if g[le][c] == 3:
            has1 = any(g[k][c] == 1 for k in range(ls, le + 1))
            has2 = any(out[k][c] == 2 for k in range(ls, le + 1))
            if has1 and has2:
                for k in range(le + 1, h):
                    if out[k][c] == 8:
                        out[k][c] = 2
                        changed = True
    return changed

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    out = [[8] * w for _ in range(h)]
    # Copy pre-filled 2s and 4s
    for r in range(h):
        for c in range(w):
            if g[r][c] in (2, 4):
                out[r][c] = 2
    # Find stem column
    stem_col = -1
    for r in range(h):
        for c in range(w):
            if g[r][c] == 4:
                stem_col = c
                break
        if stem_col != -1:
            break
    if stem_col != -1:
        # Fill stem
        non8_rows = [r for r in range(h) if g[r][stem_col] != 8]
        if non8_rows:
            blocks = []
            curr = [non8_rows[0]]
            for rr in non8_rows[1:]:
                if rr == curr[-1] + 1:
                    curr.append(rr)
                else:
                    blocks.append(curr)
                    curr = [rr]
            blocks.append(curr)
            if len(blocks) == 1:
                start_r = 0
            else:
                start_r = min(blocks[0])
            for r in range(start_r, h):
                out[r][stem_col] = 2
    # Iterative filling
    changed = True
    while changed:
        changed = False
        changed |= fill_horizontal_gaps(g, out, h, w)
        changed |= fill_vertical_gaps(g, out, h, w)
        changed |= flood_fill(g, out, h, w)
        changed |= extend_horizontal(g, out, h, w)
        changed |= extend_vertical(g, out, h, w)
    return out
```