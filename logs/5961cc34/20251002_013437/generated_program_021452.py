```python
from collections import deque
from typing import List

def find_column(g: List[List[int]]) -> int:
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j] == 4:
                return j
    return -1

def fill_stem(g: List[List[int]], out: List[List[int]], c: int):
    height = len(g)
    non8_rows = [i for i in range(height) if g[i][c] != 8]
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
    for i in range(start_row, height):
        out[i][c] = 2

def get_groups_row(row: List[int]) -> List[tuple]:
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

def fill_horizontal_gaps(g: List[List[int]], out: List[List[int]]):
    for i in range(len(g)):
        groups = get_groups_row(g[i])
        for p in range(len(groups) - 1):
            ls, le = groups[p]
            rs, re = groups[p + 1]
            has1_l = any(g[i][m] == 1 for m in range(ls, le + 1))
            if g[i][le] == 3 and has1_l:
                for m in range(le + 1, rs):
                    out[i][m] = 2
            has1_r = any(g[i][m] == 1 for m in range(rs, re + 1))
            if g[i][rs] == 3 and has1_r:
                for m in range(le + 1, rs):
                    out[i][m] = 2

def get_col_groups(g: List[List[int]], j: int) -> List[tuple]:
    height = len(g)
    groups = []
    i = 0
    while i < height:
        if g[i][j] == 8:
            i += 1
            continue
        s = i
        i += 1
        while i < height and g[i][j] != 8:
            i += 1
        groups.append((s, i - 1))
    return groups

def fill_vertical_gaps(g: List[List[int]], out: List[List[int]]):
    height = len(g)
    width = len(g[0])
    for j in range(width):
        groups = get_col_groups(g, j)
        for p in range(len(groups) - 1):
            ls, le = groups[p]
            rs, re = groups[p + 1]
            has1_u = any(g[m][j] == 1 for m in range(ls, le + 1))
            if g[le][j] == 3 and has1_u:
                for m in range(le + 1, rs):
                    out[m][j] = 2
            has1_l = any(g[m][j] == 1 for m in range(rs, re + 1))
            if g[rs][j] == 3 and has1_l:
                for m in range(le + 1, rs):
                    out[m][j] = 2

def flood_fill(g: List[List[int]], out: List[List[int]]):
    height = len(g)
    width = len(g[0])
    visited = [[False] * width for _ in range(height)]
    q = deque()
    for i in range(height):
        for j in range(width):
            if out[i][j] == 2:
                q.append((i, j))
                visited[i][j] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny] and g[nx][ny] in (1, 3):
                out[nx][ny] = 2
                visited[nx][ny] = True
                q.append((nx, ny))

def extend_edges(g: List[List[int]], out: List[List[int]]):
    height = len(g)
    width = len(g[0])
    # horizontal extensions
    for i in range(height):
        groups = get_groups_row(g[i])
        if not groups:
            continue
        # leftmost group
        s, e = groups[0]
        filled = any(out[i][m] == 2 for m in range(s, e + 1))
        if filled and s > 0 and g[i][s] == 3:
            has1 = any(g[i][m] == 1 for m in range(s, e + 1))
            if has1:
                for m in range(s):
                    out[i][m] = 2
        # rightmost group
        s, e = groups[-1]
        filled = any(out[i][m] == 2 for m in range(s, e + 1))
        if filled and e < width - 1 and g[i][e] == 3:
            has1 = any(g[i][m] == 1 for m in range(s, e + 1))
            if has1:
                for m in range(e + 1, width):
                    out[i][m] = 2
    # vertical extensions
    for j in range(width):
        groups = get_col_groups(g, j)
        if not groups:
            continue
        # highest group
        s, e = groups[0]
        filled = any(out[m][j] == 2 for m in range(s, e + 1))
        if filled and s > 0 and g[s][j] == 3:
            has1 = any(g[m][j] == 1 for m in range(s, e + 1))
            if has1:
                for m in range(s):
                    out[m][j] = 2
        # lowest group
        s, e = groups[-1]
        filled = any(out[m][j] == 2 for m in range(s, e + 1))
        if filled and e < height - 1 and g[e][j] == 3:
            has1 = any(g[m][j] == 1 for m in range(s, e + 1))
            if has1:
                for m in range(e + 1, height):
                    out[m][j] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    height = len(g)
    width = len(g[0])
    out = [[8] * width for _ in range(height)]
    c = find_column(g)
    if c != -1:
        fill_stem(g, out, c)
    # set original 2 and 4
    for i in range(height):
        for j in range(width):
            if g[i][j] in (2, 4):
                out[i][j] = 2
    fill_horizontal_gaps(g, out)
    fill_vertical_gaps(g, out)
    flood_fill(g, out)
    extend_edges(g, out)
    return out
```