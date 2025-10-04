```python
from typing import List
from collections import Counter

def find_walls(g: List[List[int]], s: int, h: int, w: int) -> List[int]:
    walls = [0, w - 1]
    for j in range(1, w - 1):
        if all(g[i][j] == s for i in range(h)):
            walls.append(j)
    return sorted(set(walls))

def get_group_lengths(subrow: List[int], c: int, i_start: int, i_end: int) -> List[int]:
    groups = []
    i = i_start
    while i <= i_end:
        if subrow[i] == c:
            length = 1
            i += 1
            while i <= i_end and subrow[i] == c:
                length += 1
                i += 1
            groups.append(length)
        else:
            i += 1
    return groups

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [row[:] for row in g]
    h = len(g)
    w = len(g[0])
    new_g = [row[:] for row in g]
    s = g[0][0]
    walls = find_walls(new_g, s, h, w)
    for r in range(h):
        row = new_g[r]
        for k in range(len(walls) - 1):
            j1 = walls[k]
            j2 = walls[k + 1]
            start = j1 + 1
            end = j2 - 1
            if start > end:
                continue
            subrow = row[start:end + 1]
            l = len(subrow)
            if l < 2:
                continue
            if subrow[0] == subrow[-1] and subrow[0] != s:
                side = subrow[0]
                i_start = 1
                i_end = l - 2
            else:
                side = None
                i_start = 0
                i_end = l - 1
            if i_start > i_end:
                continue
            colors = set()
            for j in range(i_start, i_end + 1):
                val = subrow[j]
                if val != s and (side is None or val != side):
                    colors.add(val)
            if len(colors) != 1:
                continue
            c = next(iter(colors))
            groups = get_group_lengths(subrow, c, i_start, i_end)
            if not groups:
                continue
            counter_g = Counter(groups)
            max_freq = max(counter_g.values())
            candidates = [d for d, f in counter_g.items() if f == max_freq]
            g_val = max(candidates)
            u = g_val + 1
            inner_len = i_end - i_start + 1
            best_dist = float('inf')
            best_preserved = -1
            best_phase = float('inf')
            for phase in range(u):
                dist = 0
                preserved = 0
                for ii in range(i_start, i_end + 1):
                    rel_ii = ii - i_start
                    pos = (rel_ii + phase) % u
                    val = c if pos < g_val else s
                    grid_val = subrow[ii]
                    if val != grid_val:
                        dist += 1
                    if grid_val == c and val == c:
                        preserved += 1
                update = False
                if dist < best_dist:
                    update = True
                elif dist == best_dist:
                    if preserved > best_preserved:
                        update = True
                    elif preserved == best_preserved and phase < best_phase:
                        update = True
                if update:
                    best_dist = dist
                    best_preserved = preserved
                    best_phase = phase
            # apply
            for ii in range(i_start, i_end + 1):
                rel_ii = ii - i_start
                pos = (rel_ii + best_phase) % u
                val = c if pos < g_val else s
                grid_col = start + ii
                new_g[r][grid_col] = val
    return new_g
```