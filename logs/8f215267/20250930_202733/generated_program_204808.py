```python
import collections
from typing import List

def identify_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = collections.Counter(flat)
    return count.most_common(1)[0][0]

def find_max_r(g: List[List[int]], background: int) -> int:
    n = len(g)
    m = len(g[0])
    max_r = 0
    for i in range(n):
        for j in range(m - 10):
            c = g[i][j]
            if c == background:
                continue
            is_bar = True
            for k in range(1, 11):
                if g[i][j + k] != c:
                    is_bar = False
                    break
            if is_bar:
                max_r = max(max_r, j + 10)
    return max_r

def remove_strays(g: List[List[int]], background: int, max_r: int) -> List[List[int]]:
    n = len(g)
    m = len(g[0])
    h = [row[:] for row in g]
    for i in range(n):
        for j in range(max_r + 1, m):
            h[i][j] = background
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    h = [row[:] for row in g]
    n = len(h)
    if n == 0:
        return h
    m = len(h[0])
    bg = identify_background(h)
    max_r = find_max_r(h, bg)
    h = remove_strays(h, bg, max_r)
    patterns = {
        1: [6, 8, 10],
        2: [8, 10],
        3: [6, 8, 10],
        4: [6, 8],
        6: [0, 2, 4, 6, 8, 10],
        8: [0, 2, 4, 6, 8, 10],
    }
    for i in range(n - 4):
        for j in range(m - 10):
            c = h[i][j]
            if c == bg:
                continue
            top_full = all(h[i][j + k] == c for k in range(11))
            if not top_full:
                continue
            sides_ok = True
            for mid in range(1, 4):
                if i + mid >= n or h[i + mid][j] != c or h[i + mid][j + 10] != c:
                    sides_ok = False
                    break
            if not sides_ok:
                continue
            for mid in range(1, 4):
                for k in range(1, 10):
                    h[i + mid][j + k] = bg
                h[i + mid][j] = c
                h[i + mid][j + 10] = c
            middle_r = i + 2
            for rel in patterns.get(c, []):
                col = j + rel
                if 0 <= col < m:
                    h[middle_r][col] = c
            if i + 4 < n:
                for k in range(11):
                    h[i + 4][j + k] = c
    return h
```