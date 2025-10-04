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

def is_full_span(row: List[int], l: int, r: int, c: int) -> bool:
    for k in range(l, r + 1):
        if row[k] != c:
            return False
    return True

def get_k(c: int, l: int, s: int) -> int:
    if c == 1:
        return 4 - l
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
    # legs
    for mid in range(1, 4):
        row_idx = s + mid
        if row_idx < h:
            output[row_idx][l] = c
            output[row_idx][r] = c
    # crossbar
    mid_row = s + 2
    if mid_row < h:
        output[mid_row][l] = c
        output[mid_row][r] = c
        k = get_k(c, l, s)
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
    if not g:
        return []
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    bg = get_background(g)
    output = [[bg for _ in range(w)] for _ in range(h)]
    visited = [False] * h
    for s in range(h - 4):
        if visited[s]:
            continue
        bars = find_bars(g[s], bg, w)
        for l, r, c in bars:
            if c == bg:
                continue
            is_valid = True
            for mid in range(1, 4):
                if not is_thin(g[s + mid], l, r, c, bg):
                    is_valid = False
                    break
            if is_valid and is_full_span(g[s + 4], l, r, c):
                draw_structure(output, s, l, r, c, h, w)
                mark_visited(visited, s, h)
                break
    return output
```