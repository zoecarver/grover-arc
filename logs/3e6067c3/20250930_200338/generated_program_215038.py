```python
from typing import List, Optional, Tuple

def detect_bg(grid: List[List[int]], proto: int, n: int, m: int) -> int:
    count = {}
    for i in range(n - 2):
        for j in range(m):
            c = grid[i][j]
            if c != proto:
                count[c] = count.get(c, 0) + 1
    if not count:
        return grid[n - 1][0] if n > 0 and m > 0 else 0
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

def find_sections(grid: List[List[int]], n: int, m: int, proto: int) -> List[Tuple[int, int]]:
    sections = []
    i = 0
    while i < n - 2:
        row_has_proto = any(grid[i][j] == proto for j in range(m))
        row_all_proto = all(grid[i][j] == proto for j in range(m))
        if row_has_proto and not row_all_proto:
            sec_start = i
            i += 1
            while i < n - 2:
                row_has_proto = any(grid[i][j] == proto for j in range(m))
                row_all_proto = all(grid[i][j] == proto for j in range(m))
                if not (row_has_proto and not row_all_proto):
                    break
                i += 1
            sections.append((sec_start, i - 1))
        else:
            i += 1
    return sections

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
        left_s, left_e, a = comps[k]
        right_s, right_e, b = comps[k + 1]
        fill_c = is_adjacent_preceding(chain, a, b)
        if fill_c is not None:
            for j in range(left_e + 1, right_s):
                if row[j] == bg:
                    row[j] = fill_c

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
    walls = [-1] + [j for j in range(m) if row[j] == proto] + [m]
    regions = []
    for k in range(len(walls) - 1):
        s = walls[k] + 1
        e = walls[k + 1] - 1
        if s > e:
            continue
        seg_colors = {row[j] for j in range(s, e + 1) if row[j] != proto and row[j] != bg}
        if len(seg_colors) == 1:
            c = next(iter(seg_colors))
            regions.append((s, e, c))
    return regions

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    n = len(out)
    if n == 0:
        return out
    m = len(out[0])
    proto = 1
    if n < 3:
        return out
    bg = detect_bg(out, proto, n, m)
    chain = extract_chain(out, n, m, bg, proto)
    for i in range(n - 2):
        horizontal_fill(out, i, m, proto, bg, chain)
    sections = find_sections(out, n, m, proto)
    for start, end in sections:
        vertical_propagate_within(out, start, end, m, proto, bg)
    for k in range(len(sections) - 1):
        upper_start, upper_end = sections[k]
        lower_start, lower_end = sections[k + 1]
        if lower_start > upper_end + 1:
            inner_u = get_inner(out, upper_start, upper_end, m, proto, bg)
            if inner_u is None:
                continue
            inner_l = get_inner(out, lower_start, lower_end, m, proto, bg)
            if inner_l is None:
                continue
            regs_u = get_filled_regions(out, inner_u, m, proto, bg)
            regs_l = get_filled_regions(out, inner_l, m, proto, bg)
            for su, eu, cu in regs_u:
                for sl, el, cl in regs_l:
                    os = max(su, sl)
                    oe = min(eu, el)
                    if os <= oe:
                        fill_c = is_adjacent_preceding(chain, cu, cl)
                        if fill_c is not None:
                            for gi in range(upper_end + 1, lower_start):
                                for j in range(os, oe + 1):
                                    if out[gi][j] == bg:
                                        out[gi][j] = fill_c
    return out
```