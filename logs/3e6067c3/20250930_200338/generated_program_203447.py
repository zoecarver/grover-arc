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
        return 0
    return max(count, key=count.get)

def extract_chain(grid: List[List[int]], n: int, m: int, bg: int, proto: int) -> List[int]:
    if n < 2:
        return []
    return [grid[n - 2][j] for j in range(m) if grid[n - 2][j] != bg and grid[n - 2][j] != proto]

def is_adjacent_preceding(chain: List[int], a: int, b: int) -> Optional[int]:
    for ii in range(len(chain) - 1):
        if (chain[ii] == a and chain[ii + 1] == b) or (chain[ii] == b and chain[ii + 1] == a):
            return chain[ii]
    return None

def horizontal_fill(grid: List[List[int]], i: int, m: int, proto: int, bg: int, chain: List[int]):
    walls = [j for j in range(m) if grid[i][j] == proto]
    comps: List[Tuple[int, int, int]] = []
    prev = -1
    for w in walls:
        s = prev + 1
        e = w - 1
        if s > e:
            prev = w
            continue
        seg_colors = {grid[i][k] for k in range(s, e + 1) if grid[i][k] != proto and grid[i][k] != bg}
        if len(seg_colors) == 1:
            c = next(iter(seg_colors))
            for k in range(s, e + 1):
                if grid[i][k] == bg:
                    grid[i][k] = c
            comps.append((s, e, c))
        prev = w
    s = prev + 1
    e = m - 1
    if s <= e:
        seg_colors = {grid[i][k] for k in range(s, e + 1) if grid[i][k] != proto and grid[i][k] != bg}
        if len(seg_colors) == 1:
            c = next(iter(seg_colors))
            for k in range(s, e + 1):
                if grid[i][k] == bg:
                    grid[i][k] = c
            comps.append((s, e, c))
    for k in range(len(comps) - 1):
        left_start, left_end, a = comps[k]
        right_start, right_end, b = comps[k + 1]
        fill_c = is_adjacent_preceding(chain, a, b)
        if fill_c is not None:
            for j in range(left_end + 1, right_start):
                if grid[i][j] == bg:
                    grid[i][j] = fill_c

def get_filled_regions(grid: List[List[int]], i: int, m: int, proto: int, bg: int) -> List[Tuple[int, int, int]]:
    regions = []
    walls = [j for j in range(m) if grid[i][j] == proto]
    prev = -1
    for w in walls:
        s = prev + 1
        e = w - 1
        if s > e:
            prev = w
            continue
        seg_colors = {grid[i][k] for k in range(s, e + 1) if grid[i][k] != proto and grid[i][k] != bg}
        if len(seg_colors) == 1:
            c = next(iter(seg_colors))
            regions.append((s, e, c))
        prev = w
    s = prev + 1
    e = m - 1
    if s <= e:
        seg_colors = {grid[i][k] for k in range(s, e + 1) if grid[i][k] != proto and grid[i][k] != bg}
        if len(seg_colors) == 1:
            c = next(iter(seg_colors))
            regions.append((s, e, c))
    return regions

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

def perform_gap_fills(sections: List[Tuple[int, int]], grid: List[List[int]], n: int, m: int, proto: int, bg: int, chain: List[int]):
    if len(sections) < 2:
        return
    for k in range(len(sections) - 1):
        upper_start, upper_end = sections[k]
        lower_start, lower_end = sections[k + 1]
        upper_inner = get_inner(grid, upper_start, upper_end, m, proto, bg)
        if upper_inner is None:
            continue
        lower_inner = get_inner(grid, lower_start, lower_end, m, proto, bg)
        if lower_inner is None:
            continue
        gap_start = upper_end + 1
        gap_end = lower_start - 1
        if gap_start > gap_end:
            continue
        upper_regs = get_filled_regions(grid, upper_inner, m, proto, bg)
        lower_regs = get_filled_regions(grid, lower_inner, m, proto, bg)
        for u_s, u_e, a in upper_regs:
            for l_s, l_e, b in lower_regs:
                o_l = max(u_s, l_s)
                o_r = min(u_e, l_e)
                if o_l > o_r:
                    continue
                fill_c = is_adjacent_preceding(chain, a, b)
                if fill_c is not None:
                    for ii in range(gap_start, gap_end + 1):
                        for jj in range(o_l, o_r + 1):
                            if grid[ii][jj] == bg or grid[ii][jj] == proto:
                                grid[ii][jj] = fill_c

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    proto = 1
    bg = detect_bg(g, proto, n, m)
    chain = extract_chain(g, n, m, bg, proto)
    grid_out = [row[:] for row in g]
    for i in range(n - 2):
        horizontal_fill(grid_out, i, m, proto, bg, chain)
    sections = find_sections(grid_out, n, m, proto)
    for sec_start, sec_end in sections:
        vertical_propagate_within(grid_out, sec_start, sec_end, m, proto, bg)
    perform_gap_fills(sections, grid_out, n, m, proto, bg, chain)
    return grid_out
```