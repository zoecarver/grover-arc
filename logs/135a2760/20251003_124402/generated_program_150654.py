```python
from typing import List
from collections import Counter
import copy

def find_walls(g: List[List[int]], bg: int, h: int, w: int) -> List[int]:
    walls = [0, w - 1]
    for j in range(1, w - 1):
        if all(g[i][j] == bg for i in range(h)):
            walls.append(j)
    return sorted(walls)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [row[:] for row in g]
    h = len(g)
    w = len(g[0])
    bg = g[0][0]
    out = [row[:] for row in g]
    walls = find_walls(g, bg, h, w)
    for r in range(h):
        row = out[r]
        for s in range(len(walls) - 1):
            j1 = walls[s]
            j2 = walls[s + 1]
            start = j1 + 1
            end = j2 - 1
            if start > end:
                continue
            sub_len = end - start + 1
            if sub_len < 3:
                continue
            sub = row[start : end + 1]
            if sub[0] != sub[-1] or sub[0] == bg:
                continue
            side_c = sub[0]
            inner_start_rel = 1
            inner_end_rel = sub_len - 2
            inner_len = inner_end_rel - inner_start_rel + 1
            if inner_len <= 0:
                continue
            inner = sub[inner_start_rel : inner_end_rel + 1]
            count_non = Counter(val for val in inner if val != bg and val != side_c)
            if not count_non:
                for ii in range(inner_start_rel, inner_end_rel + 1):
                    sub[ii] = side_c
                row[start : end + 1] = sub
                continue
            c = count_non.most_common(1)[0][0]
            runs = []
            i = 0
            while i < inner_len:
                if inner[i] == c:
                    leng = 1
                    i += 1
                    while i < inner_len and inner[i] == c:
                        leng += 1
                        i += 1
                    runs.append(leng)
                else:
                    i += 1
            if not runs:
                for ii in range(inner_start_rel, inner_end_rel + 1):
                    sub[ii] = side_c
                row[start : end + 1] = sub
                continue
            run_count = Counter(runs)
            max_freq = max(run_count.values())
            candidates = [leng for leng, cnt in run_count.items() if cnt == max_freq]
            k = max(candidates)
            period = k + 1
            unit = [c] * k + [bg]
            min_changes = float('inf')
            best_phase = 0
            for phase in range(period):
                changes = 0
                for ii in range(inner_len):
                    pat_idx = (ii + phase) % period
                    pat_val = unit[pat_idx]
                    if inner[ii] != pat_val:
                        changes += 1
                if changes < min_changes:
                    min_changes = changes
                    best_phase = phase
            for ii in range(inner_len):
                pat_idx = (ii + best_phase) % period
                sub[inner_start_rel + ii] = unit[pat_idx]
            row[start : end + 1] = sub
    return out
```