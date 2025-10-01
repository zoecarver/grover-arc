```python
import collections
from typing import List

def identify_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = collections.Counter(flat)
    return count.most_common(1)[0][0]

def get_middle_positions(c: int, L: int) -> List[int]:
    if c in (6, 8):
        return list(range(0, 11, 2))
    if c == 4 or (c == 1 and L == 1):
        return [0, 6, 8, 10]
    if c == 3:
        return [0, 4, 6, 8, 10]
    if c == 1 and L == 2:
        return [0, 8, 10]
    if c == 2:
        return [0, 10]
    return [0, 10]

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    bg = identify_background(g)
    h = [row[:] for row in g]
    blocks: List[tuple] = []
    i = 0
    while i < n - 4:
        processed = False
        for j in range(m - 10):
            c = h[i][j]
            if c == bg:
                continue
            is_top = all(h[i][j + k] == c for k in range(11))
            if not is_top:
                continue
            sides_ok = True
            for r in range(1, 4):
                if h[i + r][j] != c or h[i + r][j + 10] != c:
                    sides_ok = False
                    break
            if not sides_ok:
                continue
            inner_ok = True
            for r in range(1, 3):
                if not all(h[i + r][j + k] == bg for k in range(1, 10)):
                    inner_ok = False
                    break
            if not inner_ok:
                continue
            is_r3_full = all(h[i + 3][j + k] == c for k in range(11))
            if is_r3_full:
                double_full = (i + 4 < n) and all(h[i + 4][j + k] == c for k in range(11))
                if double_full:
                    for r in range(1, 4):
                        for k in range(1, 10):
                            h[i + r][j + k] = bg
                    pos = get_middle_positions(c, j)
                    for p in pos:
                        if 0 <= j + p < m:
                            h[i + 2][j + p] = c
                    if c == 1 and j == 2:
                        h[i + 1][j + 8] = c
                    blocks.append((i, i + 4, j, j + 10))
                else:
                    if i - 1 < 0:
                        continue
                    for k in range(11):
                        if 0 <= j + k < m:
                            h[i - 1][j + k] = c
                    for k in range(1, 10):
                        h[i][j + k] = bg
                    pos = [0, 8, 10]
                    for p in pos:
                        if 0 <= j + p < m:
                            h[i + 1][j + p] = c
                    blocks.append((i - 1, i + 3, j, j + 10))
            else:
                for r in range(1, 4):
                    for k in range(1, 10):
                        h[i + r][j + k] = bg
                pos = get_middle_positions(c, j)
                for p in pos:
                    if 0 <= j + p < m:
                        h[i + 2][j + p] = c
                end_r = i + 3
                if i + 4 < n:
                    for k in range(11):
                        if 0 <= j + k < m:
                            h[i + 4][j + k] = c
                    end_r = i + 4
                blocks.append((i, end_r, j, j + 10))
            processed = True
            break
        if processed:
            i += 5
        else:
            i += 1
    final_h = [[bg for _ in range(m)] for _ in range(n)]
    for sr, er, l, r in blocks:
        for rr in range(max(0, sr), min(n, er + 1)):
            for cc in range(max(0, l), min(m, r + 1)):
                final_h[rr][cc] = h[rr][cc]
    return final_h
```