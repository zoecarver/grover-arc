```python
import collections
from typing import List

def identify_background(g: List[List[int]]) -> int:
    if not g:
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
    return pos

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    bg = identify_background(g)
    n = len(g)
    m = len(g[0])
    blocks = []
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
                if i + r >= n or g[i + r][j] != c or g[i + r][j + 10] != c:
                    valid = False
                    break
            if valid:
                blocks.append((i, j, c))
                found = True
                break
        if found:
            i += 5
        else:
            i += 1
    output = [[bg] * m for _ in range(n)]
    for start_i, start_j, c in blocks:
        for k in range(11):
            output[start_i][start_j + k] = c
        for r in range(1, 4):
            output[start_i + r][start_j] = c
            output[start_i + r][start_j + 10] = c
            for k in range(1, 10):
                output[start_i + r][start_j + k] = bg
        modd = start_i % 10
        poss = get_middle_positions(c, modd)
        for p in poss:
            if 0 <= start_j + p < m:
                output[start_i + 2][start_j + p] = c
        if start_i + 4 < n:
            for k in range(11):
                output[start_i + 4][start_j + k] = c
    return output
```