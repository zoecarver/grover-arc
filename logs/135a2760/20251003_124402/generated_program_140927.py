```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def is_bordered_row(row: List[int], s: int) -> bool:
    return len(row) >= 2 and row[0] == s and row[-1] == s

def get_inner_range(row: List[int], s: int) -> Tuple[int, int]:
    w = len(row)
    if w < 3:
        return 1, 0
    if row[1] == 2 and row[w - 2] == 2:
        return 2, w - 3
    return 1, w - 2

def get_dominant_color(row: List[int], istart: int, iend: int, s: int) -> int:
    vals = [row[j] for j in range(istart, iend + 1) if row[j] != s and row[j] != 2]
    if not vals:
        return -1
    counter = Counter(vals)
    most, count = counter.most_common(1)[0]
    if count / len(vals) > 0.5:
        return most
    return -1

def get_period(c: int) -> int:
    period_dict = {1: 2, 3: 3, 4: 2, 8: 4, 9: 2}
    return period_dict.get(c, 2)

def get_pattern(c: int, period: int, s: int) -> List[int]:
    return [c] * (period - 1) + [s]

def find_best_phase(row: List[int], istart: int, iend: int, pattern: List[int], period: int) -> int:
    best_matches = -1
    best_phase = 0
    for phase in range(period):
        matches = 0
        for jj in range(istart, iend + 1):
            if row[jj] != 2:
                idx = (jj - istart + phase) % period
                if row[jj] == pattern[idx]:
                    matches += 1
        if matches > best_matches:
            best_matches = matches
            best_phase = phase
    return best_phase

def apply_pattern(grid_row: List[int], istart: int, iend: int, pattern: List[int], period: int, phase: int) -> None:
    for jj in range(istart, iend + 1):
        idx = (jj - istart + phase) % period
        grid_row[jj] = pattern[idx]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    new_g = [row[:] for row in g]
    s = get_background(g)
    h = len(g)
    if h == 0:
        return new_g
    w = len(g[0])
    for r in range(h):
        row = new_g[r]
        if not is_bordered_row(row, s):
            continue
        istart, iend = get_inner_range(row, s)
        if istart > iend:
            continue
        c = get_dominant_color(row, istart, iend, s)
        if c == -1:
            continue
        period = get_period(c)
        pattern = get_pattern(c, period, s)
        phase = find_best_phase(row, istart, iend, pattern, period)
        apply_pattern(new_g[r], istart, iend, pattern, period, phase)
    return new_g
```