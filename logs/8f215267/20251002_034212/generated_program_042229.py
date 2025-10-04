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

def is_thin(row: List[int], l: int, r: int, c: int, bg: int) -> bool:
    if row[l] != c or row[r] != c:
        return False
    for k in range(l + 1, r):
        if row[k] != bg:
            return False
    return True

def is_full(row: List[int], l: int, r: int, c: int) -> bool:
    for k in range(l, r + 1):
        if row[k] != c:
            return False
    return True

def get_k(c: int, s: int) -> int:
    if c == 1:
        return 3
    if c == 2:
        return 1 if s == 1 else 2
    return c // 2 + 1

def draw_structure(output: List[List[int]], s: int, l: int, r: int, c: int, h: int, w: int) -> None:
    if s + 4 >= h:
        return
    # top
    for col in range(l, r + 1):
        output[s][col] = c
    # bottom
    for col in range(l, r + 1):
        output[s + 4][col] = c
    # legs in all three middle rows
    for mid in range(1, 4):
        row_idx = s + mid
        if row_idx < h:
            output[row_idx][l] = c
            output[row_idx][r] = c
    # crossbar in central middle row
    mid_row = s + 2
    if mid_row < h:
        k = get_k(c, s)
        pos = r
        count = 0
        while count < k and pos >= l:
            output[mid_row][pos] = c
            pos -= 2
            count += 1

def mark_visited(visited: List[bool], s: int, h: int) -> None:
    for rr in range(s, min(s + 5, h)):
        visited[rr] = True

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    output = [[bg for _ in range(w)] for _ in range(h)]
    visited = [False for _ in range(h)]
    for s in range(h - 4):
        if visited[s]:
            continue
        bars = find_bars(g[s], bg, w)
        for bar in bars:
            l, r, c = bar
            if c == bg:
                continue
            valid = s + 4 < h and is_full(g[s + 4], l, r, c)
            if not valid:
                continue
            for m in range(1, 4):
                mr = s + m
                if mr >= h or not is_thin(g[mr], l, r, c, bg):
                    valid = False
                    break
            if valid:
                draw_structure(output, s, l, r, c, h, w)
                mark_visited(visited, s, h)
                break
    return output
```