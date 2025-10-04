```python
from collections import Counter
from typing import List
import math

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    f = g[0][0]
    # Get wall columns
    walls = [0, w - 1]
    for j in range(1, w - 1):
        if all(g[i][j] == f for i in range(h)):
            walls.append(j)
    walls = sorted(set(walls))
    new_g = [row[:] for row in g]
    for i in range(1, h - 1):
        for p in range(len(walls) - 1):
            j1 = walls[p]
            j2 = walls[p + 1]
            inner_start = j1 + 2
            if inner_start >= j2 - 1:
                continue
            subinner = new_g[i][inner_start:j2 - 1]
            L = len(subinner)
            if L <= 0:
                continue
            col_counts = Counter(subinner)
            non_f_counts = {col: cnt for col, cnt in col_counts.items() if col != f}
            if not non_f_counts:
                continue
            c = max(non_f_counts, key=non_f_counts.get)
            # Groups of c
            groups = []
            curr = 0
            for val in subinner:
                if val == c:
                    curr += 1
                else:
                    if curr > 0:
                        groups.append(curr)
                    curr = 0
            if curr > 0:
                groups.append(curr)
            if not groups:
                continue
            group_c = Counter(groups)
            max_f = max(group_c.values())
            candidates = [gg for gg, cc in group_c.items() if cc == max_f]
            g_val = max(candidates)
            u = g_val + 1
            best_dist = math.inf
            best_preserved = -1
            best_shift = math.inf
            best_pattern = None
            for shift in range(u):
                pattern = [0] * L
                for ii in range(L):
                    pos = (ii + shift) % u
                    pattern[ii] = c if pos < g_val else f
                dist = sum(pattern[kk] != subinner[kk] for kk in range(L))
                preserved = sum(1 for kk in range(L) if subinner[kk] == c and pattern[kk] == c)
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
            if best_pattern is not None:
                for kk in range(L):
                    new_g[i][inner_start + kk] = best_pattern[kk]
    return new_g
```