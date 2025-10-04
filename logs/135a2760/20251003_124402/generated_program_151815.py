```python
from typing import List
from collections import Counter

period_dict = {1: 2, 3: 3, 4: 2, 8: 4, 9: 2}

def detect_background(g: List[List[int]]) -> int:
    return g[0][0] if g and g[0] else 0

def find_walls(g: List[List[int]], s: int, h: int, w: int) -> List[int]:
    walls = [0, w - 1]
    for j in range(1, w - 1):
        if all(g[i][j] == s for i in range(h)):
            walls.append(j)
    return sorted(set(walls))

def get_dominant_color(row: List[int], start: int, end: int, s: int) -> int:
    vals = [row[j] for j in range(start, end + 1) if row[j] != s and row[j] != 2]
    if not vals:
        return -1
    uniq = set(vals)
    if len(uniq) != 1:
        return -1
    c = list(uniq)[0]
    if c in period_dict:
        return c
    return -1

def compute_pattern_mis_and_pres(row: List[int], inner_start: int, inner_end: int, unit: List[int], p: int, c: int, s: int) -> tuple[int, int, int]:
    L = inner_end - inner_start + 1
    best_mis = float('inf')
    best_pres = -1
    best_ph = 0
    for ph in range(p):
        mis = 0
        pres = 0
        for jj in range(inner_start, inner_end + 1):
            idx = (jj - inner_start + ph) % p
            exp = unit[idx]
            if row[jj] != 2 and row[jj] != exp:
                mis += 1
            if row[jj] == c and exp == c:
                pres += 1
        if mis < best_mis or (mis == best_mis and (pres > best_pres or (pres == best_pres and ph < best_ph))):
            best_mis = mis
            best_pres = pres
            best_ph = ph
    return best_mis, best_pres, best_ph

def compute_solid_mis_and_pres(row: List[int], inner_start: int, inner_end: int, c: int) -> tuple[int, int]:
    mis = 0
    pres = 0
    for jj in range(inner_start, inner_end + 1):
        if row[jj] != 2 and row[jj] != c:
            mis += 1
        if row[jj] == c:
            pres += 1
    return mis, pres

def apply_pattern_to_inner(new_row: List[int], inner_start: int, inner_end: int, unit: List[int], p: int, ph: int) -> None:
    for jj in range(inner_start, inner_end + 1):
        idx = (jj - inner_start + ph) % p
        new_row[jj] = unit[idx]

def apply_solid_to_inner(new_row: List[int], inner_start: int, inner_end: int, c: int) -> None:
    for jj in range(inner_start, inner_end + 1):
        new_row[jj] = c

def process_section(new_g: List[List[int]], r: int, sect_start: int, sect_end: int, s: int, period_dict: dict) -> None:
    row = new_g[r]
    side_left = row[sect_start]
    side_right = row[sect_end]
    shrink = (side_left == side_right and side_left != s)
    inner_start = sect_start + 1 if shrink else sect_start
    inner_end = sect_end - 1 if shrink else sect_end
    if inner_start > inner_end:
        return
    c = get_dominant_color(row, inner_start, inner_end, s)
    if c != -1:
        p = period_dict[c]
        unit = [c] * (p - 1) + [s]
        mis_p, pres_p, best_ph = compute_pattern_mis_and_pres(row, inner_start, inner_end, unit, p, c, s)
        mis_solid, pres_solid = compute_solid_mis_and_pres(row, inner_start, inner_end, c)
        apply_change = False
        if mis_p < mis_solid:
            apply_change = True
            apply_solid_to_inner = False
        elif mis_p == mis_solid and pres_p > pres_solid:
            apply_change = True
            apply_solid_to_inner = False
        else:
            apply_change = True
            apply_solid_to_inner = True
        if apply_change:
            if apply_solid_to_inner:
                apply_solid_to_inner(new_g[r], inner_start, inner_end, c)
            else:
                apply_pattern_to_inner(new_g[r], inner_start, inner_end, unit, p, best_ph)
        return
    # fallback
    has_twos = any(row[j] == 2 for j in range(inner_start, inner_end + 1))
    if not has_twos or not shrink:
        return
    side_c = side_left
    if side_c == s or side_c == 2 or side_c not in period_dict:
        return
    p = period_dict[side_c]
    unit = [side_c] * (p - 1) + [s]
    mis_p, pres_p, best_ph = compute_pattern_mis_and_pres(row, inner_start, inner_end, unit, p, side_c, s)
    mis_solid_s, pres_solid_s = compute_solid_mis_and_pres(row, inner_start, inner_end, side_c)
    apply_change = True
    apply_solid_to_inner = (mis_p > mis_solid_s) or (mis_p == mis_solid_s and pres_p <= pres_solid_s)
    if apply_change:
        if apply_solid_to_inner:
            apply_solid_to_inner(new_g[r], inner_start, inner_end, side_c)
        else:
            apply_pattern_to_inner(new_g[r], inner_start, inner_end, unit, p, best_ph)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    s = detect_background(g)
    walls = find_walls(g, s, h, w)
    new_g = [row[:] for row in g]
    for r in range(h):
        row = new_g[r]
        if row[0] != s or row[-1] != s:
            continue
        for sec in range(len(walls) - 1):
            left = walls[sec]
            right = walls[sec + 1]
            sect_start = left + 1
            sect_end = right - 1
            if sect_start > sect_end:
                continue
            process_section(new_g, r, sect_start, sect_end, s, period_dict)
    return new_g
```