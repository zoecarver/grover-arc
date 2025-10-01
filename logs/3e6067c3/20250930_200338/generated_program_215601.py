```python
from typing import List, Optional, Tuple

def detect_bg(grid: List[List[int]], proto: int) -> int:
    n = len(grid)
    if n == 0:
        return 0
    m = len(grid[0]) if n > 0 else 0
    count = {}
    for i in range(n - 2):
        for j in range(m):
            c = grid[i][j]
            if c != proto:
                count[c] = count.get(c, 0) + 1
    if not count:
        return grid[-1][0] if n > 0 and m > 0 else 0
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
    walls = [-1] + [j for j in range(m) if grid[i][j] == proto] + [m]
    comps: List[Tuple[int, int, int]] = []
    for k in range(len(walls) - 1):
        s = walls[k] + 1
        e = walls[k + 1] - 1
        if s > e:
            continue
        seg_colors = {grid[i][j] for j in range(s, e + 1) if grid[i][j] != proto and grid[i][j] != bg}
        if len(seg_colors) == 1:
            c = next(iter(seg_colors))
            for j in range(s, e + 1):
                if grid[i][j] == bg:
                    grid[i][j] = c
            comps.append((s, e, c))
    for k in range(len(comps) - 1):
        left_e = comps[k][1]
        right_s = comps[k + 1][0]
        a = comps[k][2]
        b = comps[k + 1][2]
        fill_c = is_adjacent_preceding(chain, a, b)
        if fill_c is not None:
            for j in range(left_e + 1, right_s):
                if grid[i][j] == bg:
                    grid[i][j] = fill_c

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
    regions = []
    walls = [-1] + [j for j in range(m) if grid[i][j] == proto] + [m]
    for k in range(len(walls) - 1):
        s = walls[k] + 1
        e = walls[k + 1] - 1
        if s > e:
            continue
        seg_colors = {grid[i][j] for j in range(s, e + 1) if grid[i][j] != proto and grid[i][j] != bg}
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
    sections = find_sections(g, n, m, proto)
    out = [row[:] for row in g]
    for i in range(n - 2):
        horizontal_fill(out, i, m, proto, bg, chain)
    for start, end in sections:
        vertical_propagate_within(out, start, end, m, proto, bg)
    for k in range(len(sections) - 1):
        u_start, u_end = sections[k]
        l_start, l_end = sections[k + 1]
        gap_start = u_end + 1
        gap_end = l_start - 1
        if gap_start > gap_end:
            continue
        inner_u = get_inner(out, u_start, u_end, m, proto, bg)
        if inner_u is None:
            continue
        inner_l = get_inner(out, l_start, l_end, m, proto, bg)
        if inner_l is None:
            continue
        regs_u = get_filled_regions(out, inner_u, m, proto, bg)
        regs_l = get_filled_regions(out, inner_l, m, proto, bg)
        for ru in regs_u:
            su, eu, au = ru
            for rl in regs_l:
                sl, el, al = rl
                c = is_adjacent_preceding(chain, au, al)
                if c is None:
                    continue
                os_ = max(su, sl)
                oe = min(eu, el)
                if os_ > oe:
                    continue
                for gi in range(gap_start, gap_end + 1):
                    for j in range(os_, oe + 1):
                        if out[gi][j] == bg:
                            out[gi][j] = c
    return out
```