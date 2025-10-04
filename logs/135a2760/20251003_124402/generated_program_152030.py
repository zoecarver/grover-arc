```python
from typing import List
from collections import Counter

period_dict = {1: 2, 3: 3, 4: 2, 8: 4, 9: 2}

def detect_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def find_walls(g: List[List[int]], B: int, h: int, w: int) -> List[int]:
    if h == 0 or w == 0:
        return []
    walls = [0, w - 1]
    for j in range(1, w - 1):
        if all(g[i][j] == B for i in range(h)):
            walls.append(j)
    return sorted(set(walls))

def get_dominant_color(row: List[int], inner_start: int, inner_end: int, B: int, side: int or None) -> int:
    ignored = {B}
    if side is not None:
        ignored.add(side)
    vals = [row[j] for j in range(inner_start, inner_end + 1) if row[j] not in ignored]
    if not vals:
        return -1
    cnt = Counter(vals)
    if not cnt:
        return -1
    most_c, most_count = cnt.most_common(1)[0]
    total = len(vals)
    if most_count / total <= 0.5 or most_c == 2 or most_c not in period_dict:
        return -1
    return most_c

def get_best_phase_and_matches(row: List[int], inner_start: int, inner_end: int, unit: List[int], p: int) -> tuple[int, int]:
    best_matches = -1
    best_phase = 0
    for phase in range(p):
        matches = sum(1 for jj in range(inner_start, inner_end + 1) if row[jj] == unit[(jj - inner_start + phase) % p])
        if matches > best_matches:
            best_matches = matches
            best_phase = phase
    return best_phase, best_matches

def get_pattern_scores(row: List[int], inner_start: int, inner_end: int, unit: List[int], p: int, C: int, best_phase: int) -> tuple[int, int]:
    num_known = sum(1 for jj in range(inner_start, inner_end + 1) if row[jj] != 2)
    pattern_mis = num_known - get_best_phase_and_matches(row, inner_start, inner_end, unit, p)[1]  # but use the passed best
    matches = sum(1 for jj in range(inner_start, inner_end + 1) if row[jj] == unit[(jj - inner_start + best_phase) % p])
    pattern_mis = num_known - matches
    pattern_pres = sum(1 for jj in range(inner_start, inner_end + 1) if row[jj] == C and unit[(jj - inner_start + best_phase) % p] == C)
    return pattern_mis, pattern_pres

def get_solid_scores(row: List[int], inner_start: int, inner_end: int, C: int) -> tuple[int, int]:
    num_known = sum(1 for jj in range(inner_start, inner_end + 1) if row[jj] != 2)
    solid_mis = sum(1 for jj in range(inner_start, inner_end + 1) if row[jj] != 2 and row[jj] != C)
    solid_pres = sum(1 for jj in range(inner_start, inner_end + 1) if row[jj] == C)
    return solid_mis, solid_pres

def apply_pattern(new_row: List[int], inner_start: int, inner_end: int, unit: List[int], p: int, phase: int):
    for jj in range(inner_start, inner_end + 1):
        idx = (jj - inner_start + phase) % p
        new_row[jj] = unit[idx]

def apply_solid(new_row: List[int], inner_start: int, inner_end: int, C: int):
    for jj in range(inner_start, inner_end + 1):
        new_row[jj] = C

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    B = detect_background(g)
    walls = find_walls(g, B, h, w)
    new_g = [row[:] for row in g]
    for r in range(h):
        row = new_g[r]
        if row[0] != B or row[-1] != B:
            continue
        for k in range(len(walls) - 1):
            j1 = walls[k]
            j2 = walls[k + 1]
            sub_start = j1 + 1
            sub_end = j2 - 1
            if sub_start > sub_end:
                continue
            side = None
            inner_start = sub_start
            inner_end = sub_end
            if row[sub_start] == row[sub_end] and row[sub_start] != B:
                side = row[sub_start]
                inner_start += 1
                inner_end -= 1
            if inner_start > inner_end:
                continue
            C = get_dominant_color(row, inner_start, inner_end, B, side)
            if C == -1:
                continue
            p = period_dict[C]
            unit = [C] * (p - 1) + [B]
            best_phase, best_matches = get_best_phase_and_matches(row, inner_start, inner_end, unit, p)
            pattern_mis, pattern_pres = get_pattern_scores(row, inner_start, inner_end, unit, p, C, best_phase)
            solid_mis, solid_pres = get_solid_scores(row, inner_start, inner_end, C)
            if pattern_mis < solid_mis or (pattern_mis == solid_mis and pattern_pres > solid_pres):
                apply_pattern(new_g[r], inner_start, inner_end, unit, p, best_phase)
            else:
                apply_solid(new_g[r], inner_start, inner_end, C)
    return new_g
```