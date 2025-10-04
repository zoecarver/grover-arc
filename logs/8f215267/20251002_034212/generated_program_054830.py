```python
from typing import List

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def is_uniform(row: List[int], start: int, length: int, color: int) -> bool:
    return all(row[j] == color for j in range(start, start + length))

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    bg = get_background(g)
    out = [[bg for _ in range(w)] for _ in range(h)]
    frames = []
    for s in range(h - 4):
        row = g[s]
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
                L = i
                R = i + 10
                if is_uniform(g[s + 4], L, 11, c):
                    good = True
                    for dr in range(1, 4):
                        rr = s + dr
                        if g[rr][L] != c or g[rr][R] != c:
                            good = False
                            break
                        for jj in range(L + 1, R):
                            if g[rr][jj] != bg:
                                good = False
                                break
                        if not good:
                            break
                    if good:
                        frames.append((s, L, R, c))
            i = j
    for s, L, R, c in frames:
        for j in range(L, R + 1):
            out[s][j] = c
        for j in range(L, R + 1):
            out[s + 4][j] = c
        for dr in range(1, 4):
            rr = s + dr
            out[rr][L] = c
            out[rr][R] = c
        center = s + 2
        out[center][L] = c
        if c == 1:
            p = 1
            kk = 2
        elif c == 2:
            kk = 0
        else:
            p = L % 2
            kk = c // 2
        if kk > 0:
            inner_pos = [j for j in range(L + 1, R) if (j % 2) == p]
            inner_pos.sort(reverse=True)
            pattern_pos = inner_pos[:kk]
            for j in pattern_pos:
                out[center][j] = c
        set_right = True
        if kk > 0 and pattern_pos and pattern_pos[0] == R - 1:
            set_right = False
        if set_right:
            out[center][R] = c
    return out
```