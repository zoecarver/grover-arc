```python
from typing import List
from collections import Counter

def find_walls(g: List[List[int]], s: int, h: int, w: int) -> List[int]:
    walls = [0, w - 1]
    for j in range(1, w - 1):
        if all(g[i][j] == s for i in range(h)):
            walls.append(j)
    return sorted(set(walls))

def get_colors(row: List[int], istart: int, iend: int, s: int, side_c: int or None) -> set:
    colors = set()
    for j in range(istart, iend + 1):
        val = row[j]
        if val != s and (side_c is None or val != side_c):
            colors.add(val)
    return colors

def find_best_phase(row: List[int], istart: int, iend: int, unit: List[int], p: int, c: int) -> int:
    best_matches = -1
    best_preserved = -1
    best_phase = -1
    for phase in range(p):
        matches = 0
        preserved = 0
        for jj in range(istart, iend + 1):
            idx = (jj - istart + phase) % p
            exp = unit[idx]
            if row[jj] == exp:
                matches += 1
            if row[jj] == c and exp == c:
                preserved += 1
        update = False
        if matches > best_matches:
            update = True
        elif matches == best_matches:
            if preserved > best_preserved:
                update = True
            elif preserved == best_preserved and phase < best_phase:
                update = True
        if update:
            best_matches = matches
            best_preserved = preserved
            best_phase = phase
    return best_phase

def apply_pattern(new_row: List[int], istart: int, iend: int, unit: List[int], p: int, phase: int) -> None:
    for jj in range(istart, iend + 1):
        idx = (jj - istart + phase) % p
        new_row[jj] = unit[idx]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [row[:] for row in g]
    h = len(g)
    w = len(g[0])
    s = g[0][0]
    period_dict = {1: 2, 3: 3, 4: 2, 8: 4, 9: 2}
    walls = find_walls(g, s, h, w)
    new_g = [row[:] for row in g]
    for r in range(h):
        row = g[r]
        for k in range(len(walls) - 1):
            j1 = walls[k]
            j2 = walls[k + 1]
            left = j1 + 1
            right = j2 - 1
            if right < left:
                continue
            side_c = None
            if left < right and row[left] == row[right] and row[left] != s:
                side_c = row[left]
                istart = left + 1
                iend = right - 1
            else:
                istart = left
                iend = right
            if istart > iend:
                continue
            colors = get_colors(row, istart, iend, s, side_c)
            if len(colors) != 1:
                continue
            c = next(iter(colors))
            if c == 2:
                continue
            p = period_dict.get(c, 2)
            unit = [c] * (p - 1) + [s]
            phase = find_best_phase(row, istart, iend, unit, p, c)
            apply_pattern(new_g[r], istart, iend, unit, p, phase)
    return new_g
```