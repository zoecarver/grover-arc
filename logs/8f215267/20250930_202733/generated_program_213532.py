```python
import collections
from typing import List

def identify_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return collections.Counter(flat).most_common(1)[0][0]

def get_middle_positions(c: int, mod: int) -> List[int]:
    pos = [0, 10]
    if c == 1:
        pos.append(8)
        if mod == 3:
            pos.append(6)
    elif c == 2:
        if mod == 3:
            pos.append(8)
    elif c == 3:
        pos += [2, 4, 6, 8]
    elif c == 4:
        pos += [6, 8]
    elif c == 6:
        pos += [4, 6, 8]
    elif c == 8:
        pos += [2, 4, 6, 8]
    return sorted(set(pos))

def find_max_r(g: List[List[int]], background: int) -> int:
    n = len(g)
    if n == 0:
        return 0
    m = len(g[0])
    max_r = 0
    for i in range(n):
        for j in range(m - 10):
            c = g[i][j]
            if c == background:
                continue
            is_bar = all(g[i][j + k] == c for k in range(11))
            if is_bar:
                max_r = max(max_r, j + 10)
    return max_r

def remove_strays(g: List[List[int]], background: int, max_r: int) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return g
    m = len(g[0])
    h = [row[:] for row in g]
    for i in range(n):
        for j in range(max_r + 1, m):
            h[i][j] = background
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n = len(g)
    m = len(g[0])
    bg = identify_background(g)
    h = [[bg for _ in range(m)] for _ in range(n)]
    i = 0
    while i < n - 4:
        found = False
        for j in range(m - 10):
            c = g[i][j]
            if c == bg:
                continue
            is_bar = all(g[i][j + k] == c for k in range(11))
            if not is_bar:
                continue
            valid = True
            for r in range(1, 4):
                if i + r >= n:
                    valid = False
                    break
                if g[i + r][j] != c and g[i + r][j] != bg:
                    valid = False
                    break
                if g[i + r][j + 10] != c and g[i + r][j + 10] != bg:
                    valid = False
                    break
                for k in range(1, 10):
                    if g[i + r][j + k] != bg:
                        valid = False
                        break
                if not valid:
                    break
            if not valid:
                continue
            for k in range(11):
                h[i][j + k] = c
            for r in range(1, 4):
                h[i + r][j] = c
                h[i + r][j + 10] = c
                for k in range(1, 10):
                    h[i + r][j + k] = bg
            mod = i % 10
            positions = get_middle_positions(c, mod)
            for p in positions:
                if 0 <= p <= 10:
                    h[i + 2][j + p] = c
            if i + 4 < n:
                for k in range(11):
                    h[i + 4][j + k] = c
            found = True
            break
        if found:
            i += 5
        else:
            i += 1
    max_r = find_max_r(h, bg)
    h = remove_strays(h, bg, max_r)
    return h
```