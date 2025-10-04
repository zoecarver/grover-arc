```python
from typing import List
from collections import Counter

def fill_stray_twos(g: List[List[int]], B: int) -> List[List[int]]:
    if not g:
        return []
    new_g = [row[:] for row in g]
    h = len(new_g)
    w = len(new_g[0])
    for r in range(h):
        if new_g[r][1] != 2:
            for j in range(w):
                if new_g[r][j] == 2:
                    new_g[r][j] = B
    return new_g

def find_walls(g: List[List[int]], B: int, h: int, w: int) -> List[int]:
    if h == 0 or w == 0:
        return []
    walls = [0, w - 1]
    for j in range(1, w - 1):
        if all(g[i][j] == B for i in range(h)):
            walls.append(j)
    return sorted(set(walls))

def get_mode_k(row: List[int], istart: int, iend: int, c: int) -> int:
    blocks = []
    j = istart
    while j <= iend:
        if row[j] == c:
            size = 1
            j += 1
            while j <= iend and row[j] == c:
                size += 1
                j += 1
            blocks.append(size)
        else:
            j += 1
    if not blocks:
        return 0
    k_count = Counter(blocks)
    max_freq = max(k_count.values())
    cand_k = [k for k, f in k_count.items() if f == max_freq]
    return max(cand_k)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [row[:] for row in g]
    B = g[0][0]
    h = len(g)
    w = len(g[0])
    temp_g = fill_stray_twos(g, B)
    walls = find_walls(g, B, h, w)
    for r in range(h):
        row = temp_g[r]
        for idx in range(len(walls) - 1):
            j1 = walls[idx]
            j2 = walls[idx + 1]
            sub_start = j1 + 1
            sub_end = j2 - 1
            if sub_start > sub_end:
                continue
            side_l = row[sub_start]
            side_r = row[sub_end]
            side_c = side_l if side_l == side_r and side_l != B else None
            istart = sub_start + 1 if side_c is not None else sub_start
            iend = sub_end - 1 if side_c is not None else sub_end
            if istart > iend:
                continue
            inner_len = iend - istart + 1
            vals = [row[j] for j in range(istart, iend + 1) if row[j] != B and row[j] != side_c]
            if not vals:
                continue
            counter = Counter(vals)
            c = counter.most_common(1)[0][0]
            K = get_mode_k(row, istart, iend, c)
            if K == 0:
                continue
            p = K + 1
            num_c = sum(1 for j in range(istart, iend + 1) if row[j] == c)
            solid_mis = inner_len - num_c
            best_mis = float('inf')
            best_phase = 0
            for phase in range(p):
                this_mis = 0
                for ii in range(inner_len):
                    jj = istart + ii
                    pos = (ii + phase) % p
                    exp = c if pos < K else B
                    if row[jj] != exp:
                        this_mis += 1
                if this_mis < best_mis:
                    best_mis = this_mis
                    best_phase = phase
            if best_mis < solid_mis:
                for ii in range(inner_len):
                    jj = istart + ii
                    pos = (ii + best_phase) % p
                    row[jj] = c if pos < K else B
            else:
                for jj in range(istart, iend + 1):
                    row[jj] = c
    return temp_g
```