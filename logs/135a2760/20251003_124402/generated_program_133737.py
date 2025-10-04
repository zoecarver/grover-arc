```python
from typing import List
from collections import Counter

def detect_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def is_eligible_row(row: List[int], s: int) -> bool:
    return len(row) > 1 and row[0] == s and row[-1] == s

def has_side_two(row: List[int], s: int) -> bool:
    return len(row) > 2 and row[1] == 2 and row[-2] == 2 and 2 != s

def get_inner_start_end(w: int, has_side_two: bool) -> tuple:
    if has_side_two:
        return 2, w - 3
    else:
        return 1, w - 2

def get_dominant_color(row: List[int], istart: int, iend: int, s: int) -> int:
    vals = [row[j] for j in range(istart, iend + 1) if row[j] != s and row[j] != 2]
    if not vals:
        return -1
    counter = Counter(vals)
    most, count = counter.most_common(1)[0]
    total = len(vals)
    if count / total > 0.5 and most in {1, 3, 4, 8, 9}:
        return most
    return -1

def get_period(row: List[int], istart: int, iend: int, s: int, c: int) -> int:
    s_pos = [j for j in range(istart, iend + 1) if row[j] == s]
    inner_len = iend - istart + 1
    if len(s_pos) < 2:
        return inner_len + 1
    diffs = [s_pos[k + 1] - s_pos[k] for k in range(len(s_pos) - 1)]
    counter = Counter(diffs)
    if not counter:
        return inner_len + 1
    max_freq = max(counter.values())
    candidates = [d for d, f in counter.items() if f == max_freq]
    return max(candidates)

def get_pattern(c: int, s: int, period: int) -> List[int]:
    return [c] * (period - 1) + [s]

def find_best_phase(row: List[int], istart: int, iend: int, pattern: List[int], period: int) -> int:
    best_matches = -1
    best_phase = 0
    for phase in range(period):
        matches = 0
        for j in range(istart, iend + 1):
            if row[j] == 2:
                continue
            idx = (j - istart + phase) % period
            if row[j] == pattern[idx]:
                matches += 1
        if matches > best_matches:
            best_matches = matches
            best_phase = phase
    return best_phase

def apply_pattern(new_row: List[int], istart: int, iend: int, pattern: List[int], period: int, phase: int) -> None:
    for j in range(istart, iend + 1):
        if new_row[j] == 2:
            continue
        idx = (j - istart + phase) % period
        new_row[j] = pattern[idx]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [row[:] for row in g]
    new_g = [row[:] for row in g]
    h = len(g)
    w = len(g[0])
    s = detect_background(g)
    for r in range(h):
        row = new_g[r]
        if not is_eligible_row(row, s):
            continue
        has_side = has_side_two(row, s)
        istart, iend = get_inner_start_end(w, has_side)
        if istart > iend:
            continue
        c = get_dominant_color(row, istart, iend, s)
        if c == -1:
            continue
        period = get_period(row, istart, iend, s, c)
        pattern = get_pattern(c, s, period)
        phase = find_best_phase(row, istart, iend, pattern, period)
        apply_pattern(new_g[r], istart, iend, pattern, period, phase)
    return new_g
```