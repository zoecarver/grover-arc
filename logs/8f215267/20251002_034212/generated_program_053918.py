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
        j = i
        while j < w and row[j] == c:
            j += 1
        length = j - i
        if length == 11:
            res.append((i, i + 10, c))
        i = j
    return res

def is_full(row: List[int], l: int, r: int, c: int) -> bool:
    for j in range(l, r + 1):
        if row[j] != c:
            return False
    return True

def is_thin(row: List[int], l: int, r: int, c: int, bg: int) -> bool:
    if row[l] != c or row[r] != c:
        return False
    for j in range(l + 1, r):
        if row[j] != bg:
            return False
    return True

def get_k(c: int, l: int, s: int) -> int:
    if c == 1:
        return 4 - l
    if c == 2:
        return 1 if s == 1 else 2
    return c // 2 + 1

def draw_structure(output: List[List[int]], s: int, l: int, r: int, c: int, thin_rows: List[int], bottom_rr: int) -> None:
    # Draw top
    for j in range(l, r + 1):
        output[s][j] = c
    # Draw bottom
    for j in range(l, r + 1):
        output[bottom_rr][j] = c
    # Draw legs
    for tr in thin_rows:
        output[tr][l] = c
        output[tr][r] = c
    # Draw crossbar
    num_thin = len(thin_rows)
    mid_row = s + 1 + (num_thin // 2)
    k = get_k(c, l, s)
    pos = r
    count = 0
    while count < k and pos >= l:
        output[mid_row][pos] = c
        pos -= 2
        count += 1

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    output = [[bg] * w for _ in range(h)]
    visited = [False] * h
    s = 0
    while s < h:
        if visited[s]:
            s += 1
            continue
        bars = find_bars(g[s], bg, w)
        drew = False
        for l, r, c in bars:
            num_thin = 0
            thin_rows = []
            rr = s + 1
            while rr < h:
                if not is_thin(g[rr], l, r, c, bg):
                    break
                thin_rows.append(rr)
                num_thin += 1
                rr += 1
            bottom_rr = rr
            if num_thin >= 2 and bottom_rr < h and is_full(g[bottom_rr], l, r, c):
                draw_structure(output, s, l, r, c, thin_rows, bottom_rr)
                for v in range(s, bottom_rr + 1):
                    if v < h:
                        visited[v] = True
                drew = True
                break
        s += 1
    return output
```