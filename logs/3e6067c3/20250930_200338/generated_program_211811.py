```python
from typing import List, Optional, Tuple

def detect_bg(grid: List[List[int]], proto: int) -> int:
    n = len(grid)
    if n == 0:
        return 0
    m = len(grid[0]) if n > 0 else 0
    count = {}
    for i in range(min(n - 2, n)):
        for j in range(m):
            c = grid[i][j]
            if c != proto:
                count[c] = count.get(c, 0) + 1
    if not count:
        return 0
    return max(count, key=count.get)

def extract_chain(grid: List[List[int]], n: int, m: int, bg: int, proto: int) -> List[int]:
    if n < 2:
        return []
    return [grid[n - 2][j] for j in range(m) if grid[n - 2][j] != bg and grid[n - 2][j] != proto]

def is_adjacent_preceding(chain: List[int], a: int, b: int) -> Optional[int]:
    if a == b:
        return a
    for ii in range(len(chain) - 1):
        if (chain[ii] == a and chain[ii + 1] == b) or (chain[ii] == b and chain[ii + 1] == a):
            return chain[ii]
    return None

def horizontal_fill(grid: List[List[int]], i: int, m: int, proto: int, bg: int, chain: List[int]):
    row = grid[i]
    walls = [-1] + [j for j in range(m) if row[j] == proto] + [m]
    comps: List[Tuple[int, int, int]] = []
    for k in range(len(walls) - 1):
        s = walls[k] + 1
        e = walls[k + 1] - 1
        if s > e:
            continue
        seg_colors = {row[j] for j in range(s, e + 1) if row[j] != proto and row[j] != bg}
        if len(seg_colors) == 1:
            c = next(iter(seg_colors))
            for j in range(s, e + 1):
                if row[j] == bg:
                    row[j] = c
            comps.append((s, e, c))
    for k in range(len(comps) - 1):
        left_end = comps[k][1]
        right_start = comps[k + 1][0]
        a = comps[k][2]
        b = comps[k + 1][2]
        fill_c = is_adjacent_preceding(chain, a, b)
        if fill_c is not None:
            for j in range(left_end + 1, right_start):
                if row[j] == bg:
                    row[j] = fill_c

def find_sections(grid: List[List[int]], n: int, m: int, proto: int) -> List[Tuple[int, int]]:
    sections = []
    i = 0
    while i < n - 2:
        row = grid[i]
        has_proto = any(row[j] == proto for j in range(m))
        all_proto = all(row[j] == proto for j in range(m))
        if has_proto and not all_proto:
            sec_start = i
            i += 1
            while i < n - 2:
                row = grid[i]
                has_proto = any(row[j] == proto for j in range(m))
                all_proto = all(row[j] == proto for j in range(m))
                if not (has_proto and not all_proto):
                    break
                i += 1
            sections.append((sec_start, i - 1))
        else:
            i += 1
    return sections

def vertical_propagate_within(grid: List[List[int]], sec_start: int, sec_end: int, m: int, proto: int, bg: int):
    for j in range(m):
        i = sec_start
        while i <= sec_end:
            if grid[i][j] == proto:
                i += 1
                continue
            v_start = i
            colors_set = set()
            i_temp = i
            while i_temp <= sec_end and grid[i_temp][j] != proto:
                cc = grid[i_temp][j]
                if cc != bg and cc != proto:
                    colors_set.add(cc)
                i_temp += 1
            v_end = i_temp - 1
            if len(colors_set) == 1:
                c = next(iter(colors_set))
                for k in range(v_start, v_end + 1):
                    if grid[k][j] == bg:
                        grid[k][j] = c
            i = i_temp

def get_inner(grid: List[List[int]], sec_start: int, sec_end: int, m: int, proto: int, bg: int) -> Optional[int]:
    for i in range(sec_start, sec_end + 1):
        for j in range(m):
            if grid[i][j] != proto and grid[i][j] != bg:
                return i
    return None

def get_filled_regions(grid: List[List[int]], i: int, m: int, proto: int, bg: int) -> List[Tuple[int, int, int]]:
    row = grid[i]
    walls = [j for j in range(m) if row[j] == proto]
    regions = []
    prev = -1
    for w in walls:
        s = prev + 1
        e = w - 1
        if s > e:
            prev = w
            continue
        seg_colors = {row[k] for k in range(s, e + 1) if row[k] != proto and row[k] != bg}
        if len(seg_colors) == 1:
            c = next(iter(seg_colors))
            regions.append((s, e, c))
        prev = w
    s = prev + 1
    e = m - 1
    if s <= e:
        seg_colors = {row[k] for k in range(s, e + 1) if row[k] != proto and row[k] != bg}
        if len(seg_colors) == 1:
            c = next(iter(seg_colors))
            regions.append((s, e, c))
    return regions

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n = len(g)
    m = len(g[0])
    proto = 1
    bg = detect_bg(g, proto)
    chain = extract_chain(g, n, m, bg, proto)
    out = [row[:] for row in g]
    for i in range(n - 2):
        horizontal_fill(out, i, m, proto, bg, chain)
    sections = find_sections(out, n, m, proto)
    for sec_start, sec_end in sections:
        vertical_propagate_within(out, sec_start, sec_end, m, proto, bg)
    for kk in range(len(sections) - 1):
        us, ue = sections[kk]
        ls, le = sections[kk + 1]
        gs = ue + 1
        ge = ls - 1
        if gs > ge:
            continue
        iu = get_inner(out, us, ue, m, proto, bg)
        if iu is None:
            continue
        il = get_inner(out, ls, le, m, proto, bg)
        if il is None:
            continue
        urs = get_filled_regions(out, iu, m, proto, bg)
        lrs = get_filled_regions(out, il, m, proto, bg)
        for ur in urs:
            for lr in lrs:
                os = max(ur[0], lr[0])
                oe = min(ur[1], lr[1])
                if os <= oe:
                    fc = is_adjacent_preceding(chain, ur[2], lr[2])
                    if fc is not None:
                        for gi in range(gs, ge + 1):
                            for gj in range(os, oe + 1):
                                if out[gi][gj] == bg:
                                    out[gi][gj] = fc
    return out
```