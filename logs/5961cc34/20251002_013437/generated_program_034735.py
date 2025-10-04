```python
from typing import List, Tuple
from collections import deque

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    out = [[8] * w for _ in range(h)]
    stem_col = find_stem_column(g, h, w)
    copy_seeds(g, out, h, w)
    if stem_col != -1:
        fill_stem(g, out, stem_col, h, w)
    changed = True
    while changed:
        changed = False
        changed |= fill_horizontal_gaps(g, out, h, w)
        changed |= fill_vertical_gaps(g, out, h, w)
        changed |= flood_fill(g, out, h, w)
        changed |= extend_horizontal_edges(g, out, h, w)
        changed |= extend_vertical_edges(g, out, h, w)
    return out

def find_stem_column(g: List[List[int]], h: int, w: int) -> int:
    for r in range(h):
        for c in range(w):
            if g[r][c] == 4:
                return c
    return -1

def copy_seeds(g: List[List[int]], out: List[List[int]], h: int, w: int) -> None:
    for r in range(h):
        for c in range(w):
            if g[r][c] in (2, 4):
                out[r][c] = 2

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
    start_row = 0 if len(blocks) == 1 else min(blocks[0])
    for r in range(start_row, h):
        out[r][c] = 2

def get_row_groups(g: List[List[int]], r: int, w: int) -> List[Tuple[int, int]]:
    groups = []
    j = 0
    while j < w:
        if g[r][j] == 8:
            j += 1
            continue
        s = j
        while j < w and g[r][j] != 8:
            j += 1
        groups.append((s, j - 1))
    return groups

def has_one(g: List[List[int]], r: int, start: int, end: int) -> bool:
    for c in range(start, end + 1):
        if g[r][c] == 1:
            return True
    return False

def is_border(g: List[List[int]], r: int, c: int, direction: str) -> bool:
    if direction == 'right':
        return g[r][c] == 3
    if direction == 'left':
        return g[r][c] == 3
    return False

def fill_horizontal_gaps(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for r in range(h):
        groups = get_row_groups(g, r, w)
        for i in range(len(groups) - 1):
            g1_start, g1_end = groups[i]
            g2_start, g2_end = groups[i + 1]
            if g2_start > g1_end + 1:
                if has_one(g, r, g1_start, g1_end) and has_one(g, r, g2_start, g2_end):
                    if g[r][g1_end] == 3 or g[r][g2_start] == 3:
                        for c in range(g1_end + 1, g2_start):
                            if out[r][c] == 8:
                                out[r][c] = 2
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
        while i < h and g[i][c] != 8:
            i += 1
        groups.append((s, i - 1))
    return groups

def has_one_col(g: List[List[int]], c: int, start: int, end: int) -> bool:
    for r in range(start, end + 1):
        if g[r][c] == 1:
            return True
    return False

def is_border_col(g: List[List[int]], r: int, c: int, direction: str) -> bool:
    if direction == 'bottom':
        return g[r][c] == 3
    if direction == 'top':
        return g[r][c] == 3
    return False

def fill_vertical_gaps(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for c in range(w):
        groups = get_col_groups(g, c, h)
        for i in range(len(groups) - 1):
            g1_start, g1_end = groups[i]
            g2_start, g2_end = groups[i + 1]
            if g2_start > g1_end + 1:
                if has_one_col(g, c, g1_start, g1_end) and has_one_col(g, c, g2_start, g2_end):
                    if g[g1_end][c] == 3 or g[g2_start][c] == 3:
                        for r in range(g1_end + 1, g2_start):
                            if out[r][c] == 8:
                                out[r][c] = 2
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

def has_two(g: List[List[int]], out: List[List[int]], r: int, start: int, end: int) -> bool:
    for c in range(start, end + 1):
        if out[r][c] == 2:
            return True
    return False

def extend_horizontal_edges(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for r in range(h):
        groups = get_row_groups(g, r, w)
        if not groups:
            continue
        # Left edge
        left_group = groups[0]
        if left_group[0] > 0 and g[r][left_group[0]] == 3 and has_one(g, r, left_group[0], left_group[1]) and has_two(g, out, r, left_group[0], left_group[1]):
            for c in range(0, left_group[0]):
                if out[r][c] == 8:
                    out[r][c] = 2
                    changed = True
        # Right edge
        right_group = groups[-1]
        if right_group[1] < w - 1 and g[r][right_group[1]] == 3 and has_one(g, r, right_group[0], right_group[1]) and has_two(g, out, r, right_group[0], right_group[1]):
            for c in range(right_group[1] + 1, w):
                if out[r][c] == 8:
                    out[r][c] = 2
                    changed = True
    return changed

def has_two_col(g: List[List[int]], out: List[List[int]], c: int, start: int, end: int) -> bool:
    for r in range(start, end + 1):
        if out[r][c] == 2:
            return True
    return False

def extend_vertical_edges(g: List[List[int]], out: List[List[int]], h: int, w: int) -> bool:
    changed = False
    for c in range(w):
        groups = get_col_groups(g, c, h)
        if not groups:
            continue
        # Top edge
        top_group = groups[0]
        if top_group[0] > 0 and g[top_group[0]][c] == 3 and has_one_col(g, c, top_group[0], top_group[1]) and has_two_col(g, out, c, top_group[0], top_group[1]):
            for r in range(0, top_group[0]):
                if out[r][c] == 8:
                    out[r][c] = 2
                    changed = True
        # Bottom edge
        bottom_group = groups[-1]
        if bottom_group[1] < h - 1 and g[bottom_group[1]][c] == 3 and has_one_col(g, c, bottom_group[0], bottom_group[1]) and has_two_col(g, out, c, bottom_group[0], bottom_group[1]):
            for r in range(bottom_group[1] + 1, h):
                if out[r][c] == 8:
                    out[r][c] = 2
                    changed = True
    return changed
```