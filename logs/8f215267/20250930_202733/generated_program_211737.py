```python
import collections
from typing import List

def identify_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = collections.Counter(flat)
    return count.most_common(1)[0][0]

def get_middle_positions(c: int, i: int) -> List[int]:
    positions = [0, 10]
    mod = i % 10
    if c == 4:
        positions.extend([6, 8])
    elif c == 6:
        positions.extend([4, 6, 8])
    elif c == 8:
        positions.extend([2, 4, 6, 8])
    elif c == 3:
        positions.extend([2, 4, 6, 8])
    elif c in (1, 2):
        if mod == 3:
            if c == 1:
                positions.extend([6, 8])
            else:
                positions.extend([8])
    return positions

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    n = len(g)
    m = len(g[0])
    bg = identify_background(g)
    h = [[bg] * m for _ in range(n)]
    i = 0
    while i < n - 3:
        found = False
        for j in range(m - 10):
            c = g[i][j]
            if c == bg:
                continue
            is_top = all(g[i][j + k] == c for k in range(11))
            if not is_top:
                continue
            valid = True
            for r in range(1, 4):
                if i + r >= n or g[i + r][j] != c or g[i + r][j + 10] != c:
                    valid = False
                    break
                if r < 3:
                    for k in range(1, 10):
                        if g[i + r][j + k] != bg:
                            valid = False
                            break
            if not valid:
                continue
            row3_full = all(g[i + 3][j + k] == c for k in range(11))
            for k in range(11):
                h[i][j + k] = c
            for r in range(1, 4):
                h[i + r][j] = c
                h[i + r][j + 10] = c
                if r < 3 or not row3_full:
                    for k in range(1, 10):
                        h[i + r][j + k] = bg
                else:
                    for k in range(11):
                        h[i + 3][j + k] = c
            positions = get_middle_positions(c, i)
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