```python
import collections
from typing import List

def identify_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = collections.Counter(flat)
    return count.most_common(1)[0][0]

def get_middle_positions(c: int) -> List[int]:
    if c == 1 or c == 2:
        return [0, 8, 10]
    elif c == 3 or c == 8:
        return [0, 2, 4, 6, 8, 10]
    elif c == 4:
        return [0, 6, 8, 10]
    elif c == 6:
        return [0, 4, 6, 8, 10]
    else:
        return [0, 10]

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    bg = identify_background(g)
    h = [[bg] * m for _ in range(n)]
    i = 0
    while i < n - 4:
        found = False
        for j in range(m - 10):
            c = g[i][j]
            if c == bg:
                continue
            if not all(g[i][j + k] == c for k in range(11)):
                continue
            valid = True
            for r in range(1, 4):
                if i + r >= n:
                    valid = False
                    break
                if g[i + r][j] not in (c, bg) or g[i + r][j + 10] not in (c, bg):
                    valid = False
                    break
                for k in range(1, 10):
                    if g[i + r][j + k] != bg:
                        valid = False
                        break
            if not valid:
                continue
            for k in range(11):
                h[i][j + k] = c
            for r in range(1, 4):
                if i + r < n:
                    h[i + r][j] = c
                    h[i + r][j + 10] = c
                    for k in range(1, 10):
                        h[i + r][j + k] = bg
            positions = get_middle_positions(c)
            if i + 2 < n:
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
    return h
```