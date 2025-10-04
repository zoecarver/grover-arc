```python
from typing import List, Optional
from collections import Counter

def find_walls(g: List[List[int]], f: int, h: int, w: int) -> List[int]:
    walls = [0, w - 1]
    for j in range(1, w - 1):
        is_wall = True
        for i in range(h):
            if g[i][j] != f:
                is_wall = False
                break
        if is_wall:
            walls.append(j)
    return sorted(walls)

def get_group_lengths(subinner: List[int], c: int) -> List[int]:
    groups = []
    i = 0
    n = len(subinner)
    while i < n:
        if subinner[i] == c:
            length = 0
            while i < n and subinner[i] == c:
                length += 1
                i += 1
            groups.append(length)
        else:
            i += 1
    return groups

def fit_pattern(subinner: List[int], c: int, f: int, g_val: int) -> Optional[List[int]]:
    n = len(subinner)
    if n == 0:
        return None
    u = g_val + 1
    best_dist = float('inf')
    best_preserved = -1
    best_shift = float('inf')
    best_pattern = None
    for shift in range(u):
        pattern = [0] * n
        for ii in range(n):
            pos = (ii + shift) % u
            pattern[ii] = c if pos < g_val else f
        dist = sum(pattern[kk] != subinner[kk] for kk in range(n))
        preserved = sum(1 for kk in range(n) if subinner[kk] == c and pattern[kk] == c)
        update = False
        if dist < best_dist:
            update = True
        elif dist == best_dist:
            if preserved > best_preserved:
                update = True
            elif preserved == best_preserved and shift < best_shift:
                update = True
        if update:
            best_dist = dist
            best_preserved = preserved
            best_shift = shift
            best_pattern = pattern[:]
    return best_pattern

def program(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if not g or not g[0]:
        return new_g
    h = len(g)
    w = len(g[0])
    f = g[0][0]
    walls = find_walls(g, f, h, w)
    allowed = {1, 2, 3, 4, 8, 9}
    for r in range(1, h - 1):
        row = new_g[r]
        for sec in range(len(walls) - 1):
            j1 = walls[sec]
            j2 = walls[sec + 1]
            sub_start = j1 + 2
            sub_end = j2 - 2
            if sub_start > sub_end:
                continue
            subinner = row[sub_start:sub_end + 1]
            n_sub = len(subinner)
            if n_sub < 1:
                continue
            counter = Counter(v for v in subinner if v != f)
            if not counter:
                continue
            c = counter.most_common(1)[0][0]
            if c not in allowed:
                continue
            groups = get_group_lengths(subinner, c)
            if not groups:
                continue
            counter_g = Counter(groups)
            max_f_g = max(counter_g.values())
            candidates_g = [gl for gl, fr in counter_g.items() if fr == max_f_g]
            g_val = max(candidates_g)
            best_p = fit_pattern(subinner, c, f, g_val)
            if best_p is not None:
                for kk in range(n_sub):
                    row[sub_start + kk] = best_p[kk]
    return new_g
```