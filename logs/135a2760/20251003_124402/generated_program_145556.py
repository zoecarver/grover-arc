```python
from typing import List
from collections import Counter

def find_walls(g: List[List[int]], s: int, h: int, w: int) -> List[int]:
    walls = [0, w - 1]
    for j in range(1, w - 1):
        if all(g[i][j] == s for i in range(h)):
            walls.append(j)
    return sorted(walls)

def get_dominant_c(g: List[List[int]], r: int, istart: int, iend: int, s: int) -> int:
    vals = [g[r][j] for j in range(istart, iend + 1) if g[r][j] != s and g[r][j] != 2]
    if not vals:
        return -1
    cnt = Counter(vals)
    most_c, count = cnt.most_common(1)[0]
    if count / len(vals) > 0.5 and most_c in {1, 3, 4, 8, 9}:
        return most_c
    return -1

def get_periodic_pattern(c: int, p: int, s: int) -> List[int]:
    return [c] * (p - 1) + [s]

def get_best_phase(g: List[List[int]], r: int, istart: int, iend: int, pattern: List[int], p: int) -> int:
    inner_len = iend - istart + 1
    best_matches = -1
    best_phase = 0
    for phase in range(p):
        matches = sum(1 for j in range(istart, iend + 1) if g[r][j] == pattern[(j - istart + phase) % p])
        if matches > best_matches:
            best_matches = matches
            best_phase = phase
    return best_phase, best_matches

def get_solid_matches(g: List[List[int]], r: int, istart: int, iend: int, c: int) -> int:
    return sum(1 for j in range(istart, iend + 1) if g[r][j] == c)

def apply_pattern(g: List[List[int]], r: int, istart: int, iend: int, pattern: List[int], p: int, phase: int) -> None:
    for j in range(istart, iend + 1):
        idx = (j - istart + phase) % p
        g[r][j] = pattern[idx]

def apply_solid(g: List[List[int]], r: int, istart: int, iend: int, c: int) -> None:
    for j in range(istart, iend + 1):
        g[r][j] = c

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    s = g[0][0]
    new_g = [row[:] for row in g]
    walls = find_walls(new_g, s, h, w)
    period_dict = {1: 2, 3: 3, 4: 2, 8: 4, 9: 2}
    for r in range(h):
        for k in range(len(walls) - 1):
            left = walls[k]
            right = walls[k + 1]
            istart = left + 1
            iend = right - 1
            if istart > iend:
                continue
            side = None
            if new_g[r][istart] == new_g[r][iend] != s:
                side = new_g[r][istart]
                istart += 1
                iend -= 1
            if istart > iend:
                continue
            c = get_dominant_c(new_g, r, istart, iend, s)
            if c == -1:
                continue
            p = period_dict[c]
            pattern = get_periodic_pattern(c, p, s)
            best_phase, best_matches = get_best_phase(new_g, r, istart, iend, pattern, p)
            solid_matches = get_solid_matches(new_g, r, istart, iend, c)
            if solid_matches > best_matches:
                apply_solid(new_g, r, istart, iend, c)
            else:
                apply_pattern(new_g, r, istart, iend, pattern, p, best_phase)
    return new_g
```