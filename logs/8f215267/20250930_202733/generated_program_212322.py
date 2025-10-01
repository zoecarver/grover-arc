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

def get_middle_positions(c: int, mod: int) -> List[int]:
    pos = [0, 10]
    if c in (1, 4):
        pos.extend([6, 8])
    elif c == 2:
        if mod == 3:
            pos.append(8)
    elif c == 3:
        pos.extend([2, 4, 6, 8])
    elif c == 6:
        pos.extend([4, 6, 8])
    elif c == 8:
        pos.extend([2, 4, 6, 8])
    return pos

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    bg = identify_background(g)
    h = [row[:] for row in g]
    i = 0
    while i < n - 4:
        found = False
        for j in range(m - 10):
            c = h[i][j]
            if c == bg:
                continue
            is_top = all(h[i][j + k] == c for k in range(11))
            if not is_top:
                continue
            valid = True
            for r in range(1, 4):
                if i + r >= n:
                    valid = False
                    break
                left = h[i + r][j]
                right = h[i + r][j + 10]
                if (left != c and left != bg) or (right != c and right != bg):
                    valid = False
                    break
                for k in range(1, 10):
                    if h[i + r][j + k] != bg:
                        valid = False
                        break
                if not valid:
                    break
            if not valid:
                continue
            found = True
            for k in range(11):
                h[i][j + k] = c
            for r in range(1, 4):
                h[i + r][j] = c
                h[i + r][j + 10] = c
                for k in range(1, 10):
                    h[i + r][j + k] = bg
            mod = i % 10
            positions = get_middle_positions(c, mod)
            for rel in positions:
                h[i + 2][j + rel] = c
            if i + 4 < n:
                for k in range(11):
                    h[i + 4][j + k] = c
        if found:
            i += 5
        else:
            i += 1
    max_r = find_max_r(h, bg)
    h = remove_strays(h, bg, max_r)
    return h
```