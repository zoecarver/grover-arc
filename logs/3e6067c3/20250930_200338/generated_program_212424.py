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
    grid = [row[:] for row in g]
    n = len(grid)
    if n < 2:
        return grid
    m = len(grid[0])
    proto = 1
    bg = detect_bg(grid, proto)
    chain = extract_chain(grid, n, m, bg, proto)
    for i in range(n - 2):
        horizontal_fill(grid, i, m, proto, bg, chain)
    sections = find_sections(grid, n, m, proto)
    for sec_start, sec_end in sections:
        vertical_propagate_within(grid, sec_start, sec_end, m, proto, bg)
    for k in range(len(sections) - 1):
        u_start, u_end = sections[k]
        l_start, l_end = sections[k + 1]
        g_start = u_end + 1
        g_end = l_start - 1
        if g_start > g_end:
            continue
        u_inner = get_inner(grid, u_start, u_end, m, proto, bg)
        if u_inner is None:
            continue
        l_inner = get_inner(grid, l_start, l_end, m, proto, bg)
        if l_inner is None:
            continue
        u_regions = get_filled_regions(grid, u_inner, m, proto, bg)
        l_regions = get_filled_regions(grid, l_inner, m, proto, bg)
        for us, ue, uc in u_regions:
            for ls, le, lc in l_regions:
                o_s = max(us, ls)
                o_e = min(ue, le)
                if o_s > o_e:
                    continue
                fill_c = is_adjacent_preceding(chain, uc, lc)
                if fill_c is None:
                    continue
                for ii in range(g_start, g_end + 1):
                    for jj in range(o_s, o_e + 1):
                        if grid[ii][jj] == bg or grid[ii][jj] == proto:
                            grid[ii][jj] = fill_c
    return grid
```