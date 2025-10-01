```python
from typing import List, Optional, Tuple

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

def find_sections(grid: List[List[int]], proto: int) -> List[Tuple[int, int]]:
    n = len(grid)
    sections = []
    i = 0
    while i < n - 2:
        row_has_proto = any(grid[i][j] == proto for j in range(len(grid[0])))
        row_all_proto = all(grid[i][j] == proto for j in range(len(grid[0])))
        if row_has_proto and not row_all_proto:
            sec_start = i
            i += 1
            while i < n - 2:
                row_has_proto = any(grid[i][j] == proto for j in range(len(grid[0])))
                row_all_proto = all(grid[i][j] == proto for j in range(len(grid[0])))
                if not (row_has_proto and not row_all_proto):
                    break
                i += 1
            sections.append((sec_start, i - 1))
        else:
            i += 1
    return sections

def horizontal_fill(grid: List[List[int]], i: int, m: int, proto: int, bg: int, chain: List[int]):
    row = grid[i]
    walls = [j for j in range(m) if row[j] == proto]
    comps: List[Tuple[int, int, int]] = []
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
            for k in range(s, e + 1):
                if row[k] == bg:
                    row[k] = c
            comps.append((s, e, c))
        prev = w
    s = prev + 1
    e = m - 1
    if s <= e:
        seg_colors = {row[k] for k in range(s, e + 1) if row[k] != proto and row[k] != bg}
        if len(seg_colors) == 1:
            c = next(iter(seg_colors))
            for k in range(s, e + 1):
                if row[k] == bg:
                    row[k] = c
            comps.append((s, e, c))
    for k in range(len(comps) - 1):
        left_start, left_end, a = comps[k]
        right_start, right_end, b = comps[k + 1]
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
                c = list(colors_set)[0]
                min_k = v_end + 1
                max_k = v_start - 1
                for k in range(v_start, v_end + 1):
                    cc = grid[k][j]
                    if cc != bg and cc != proto:
                        min_k = min(min_k, k)
                        max_k = max(max_k, k)
                if min_k <= max_k:
                    for k in range(min_k, max_k + 1):
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
    regions = []
    walls = [j for j in range(m) if row[j] == proto]
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
    grid = [row[:] for row in g]
    n = len(grid)
    if n < 2:
        return grid
    m = len(grid[0])
    proto = 1
    bg = grid[-1][0]
    chain = extract_chain(grid, n, m, bg, proto)
    for i in range(n - 2):
        horizontal_fill(grid, i, m, proto, bg, chain)
    sections = find_sections(grid, proto)
    for sec_start, sec_end in sections:
        vertical_propagate_within(grid, sec_start, sec_end, m, proto, bg)
    for k in range(len(sections) - 1):
        u_start, u_end = sections[k]
        l_start, l_end = sections[k + 1]
        g_start = u_end + 1
        g_end = l_start - 1
        if g_start > g_end:
            continue
        iu = get_inner(grid, u_start, u_end, m, proto, bg)
        if iu is None:
            continue
        il = get_inner(grid, l_start, l_end, m, proto, bg)
        if il is None:
            continue
        ru_list = get_filled_regions(grid, iu, m, proto, bg)
        rl_list = get_filled_regions(grid, il, m, proto, bg)
        for ru in ru_list:
            for rl in rl_list:
                ol_s = max(ru[0], rl[0])
                ol_e = min(ru[1], rl[1])
                if ol_s > ol_e:
                    continue
                a = ru[2]
                b = rl[2]
                fill_c = is_adjacent_preceding(chain, a, b)
                if fill_c is not None:
                    for ii in range(g_start, g_end + 1):
                        for jj in range(ol_s, ol_e + 1):
                            if grid[ii][jj] == bg:
                                grid[ii][jj] = fill_c
    return grid
```