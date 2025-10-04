```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def find_bars(row: List[int], bg: int, w: int) -> List[Tuple[int, int, int]]:
    res: List[Tuple[int, int, int]] = []
    i = 0
    while i < w - 10:
        if row[i] == bg:
            i += 1
            continue
        c = row[i]
        j = i + 1
        while j < w and row[j] == c:
            j += 1
        length = j - i
        if length == 11:
            res.append((i, i + 10, c))
        i = j
    return res

def is_full(row: List[int], l: int, r: int, c: int) -> bool:
    for k in range(l, r + 1):
        if row[k] != c:
            return False
    return True

def is_leg(row: List[int], l: int, r: int, c: int, bg: int, w: int) -> bool:
    if l < 0 or r >= w:
        return False
    if row[l] != c or row[r] != c:
        return False
    for k in range(l + 1, r):
        if row[k] != bg:
            return False
    return True

def get_k(c: int, l: int, s: int) -> int:
    if c == 1:
        return 4 - l
    if c == 2:
        return 1 if s == 1 else 2
    return c // 2 + 1

def draw_structure(out: List[List[int]], s: int, l: int, r: int, c: int, leg_rows: List[int], bottom_row: int, mid_row: int, h: int, w: int) -> None:
    if s + 4 >= h or bottom_row >= h:
        return
    for j in range(l, r + 1):
        if 0 <= s < h and 0 <= j < w:
            out[s][j] = c
        if 0 <= bottom_row < h and 0 <= j < w:
            out[bottom_row][j] = c
    for tr in leg_rows:
        if 0 <= tr < h:
            if 0 <= l < w:
                out[tr][l] = c
            if 0 <= r < w:
                out[tr][r] = c
    k = get_k(c, l, s)
    pos = r
    count = 0
    while count < k and pos >= l and 0 <= mid_row < h and 0 <= pos < w:
        out[mid_row][pos] = c
        pos -= 2
        count += 1

def mark_visited(visited: List[bool], start: int, end: int, h: int) -> None:
    for rr in range(start, min(end + 1, h)):
        visited[rr] = True

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    bg = get_background(g)
    out = [[bg] * w for _ in range(h)]
    visited = [False] * h
    s = 0
    while s < h:
        if visited[s]:
            s += 1
            continue
        bars = find_bars(g[s], bg, w)
        drew = False
        for bar in bars:
            l, r, c = bar
            if c == bg:
                continue
            leg_rows = []
            num_leg = 0
            current = s + 1
            while current < h and num_leg < 4 and is_leg(g[current], l, r, c, bg, w):
                leg_rows.append(current)
                num_leg += 1
                current += 1
            if num_leg < 3:
                continue
            bottom_row = current
            if bottom_row >= h or not is_full(g[bottom_row], l, r, c):
                continue
            mid_row = s + 1 + (num_leg // 2)
            draw_structure(out, s, l, r, c, leg_rows, bottom_row, mid_row, h, w)
            mark_visited(visited, s, bottom_row, h)
            drew = True
            break
        s += 1
    return out
```