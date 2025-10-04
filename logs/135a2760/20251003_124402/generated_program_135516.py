```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def is_eligible_row(row: List[int], s: int) -> bool:
    return len(row) > 2 and row[0] == s and row[-1] == s

def get_inner_range(row: List[int], s: int, w: int) -> tuple:
    if w < 3:
        return 1, 0
    if row[1] == 2 and row[w - 2] == 2 and 2 != s:
        return 2, w - 3
    return 1, w - 2

def get_dominant_color(row: List[int], istart: int, iend: int, s: int) -> int:
    vals = [row[j] for j in range(istart, iend + 1) if row[j] != s and row[j] != 2]
    if not vals:
        return -1
    counter = Counter(vals)
    most, count = counter.most_common(1)[0]
    if count / len(vals) > 0.5 and most in {1, 3, 4, 8, 9}:
        return most
    return -1

def get_period(row: List[int], istart: int, iend: int, s: int) -> int:
    s_pos = [j for j in range(istart, iend + 1) if row[j] == s]
    n = iend - istart + 1 if istart <= iend else 0
    if len(s_pos) < 2:
        return n + 1 if n > 0 else 1
    diffs = [s_pos[k + 1] - s_pos[k] for k in range(len(s_pos) - 1)]
    if not diffs:
        return n + 1
    counter = Counter(diffs)
    max_freq = max(counter.values())
    candidates = [d for d, f in counter.items() if f == max_freq]
    return max(candidates)

def get_pattern(c: int, period: int, s: int) -> List[int]:
    return [c] * (period - 1) + [s]

def compute_matches(row: List[int], istart: int, iend: int, phase: int, pattern: List[int], period: int) -> int:
    matches = 0
    for j in range(istart, iend + 1):
        if row[j] != 2:
            idx = (j - istart + phase) % period
            if row[j] == pattern[idx]:
                matches += 1
    return matches

def find_best_phase(row: List[int], istart: int, iend: int, pattern: List[int], period: int) -> tuple:
    best_matches = -1
    best_phase = 0
    for phase in range(period):
        m = compute_matches(row, istart, iend, phase, pattern, period)
        if m > best_matches:
            best_matches = m
            best_phase = phase
    return best_phase, best_matches

def program(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if not g:
        return new_g
    h = len(g)
    w = len(g[0])
    s = get_background(g)
    for ri in range(h):
        row = new_g[ri]
        if not is_eligible_row(row, s):
            continue
        istart, iend = get_inner_range(row, s, w)
        if istart > iend:
            continue
        c = get_dominant_color(row, istart, iend, s)
        if c == -1:
            continue
        period = get_period(row, istart, iend, s)
        pattern = get_pattern(c, period, s)
        best_phase, best_matches = find_best_phase(row, istart, iend, pattern, period)
        num_non2 = sum(1 for j in range(istart, iend + 1) if row[j] != 2)
        do_full = num_non2 > 0 and best_matches / num_non2 >= 0.6
        for j in range(istart, iend + 1):
            if do_full or (row[j] == 2 or (row[j] != s and row[j] != c)):
                idx = (j - istart + best_phase) % period
                new_g[ri][j] = pattern[idx]
    return new_g
```