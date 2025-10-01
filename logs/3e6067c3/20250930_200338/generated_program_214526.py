```python
from typing import List, Optional, Tuple
from collections import defaultdict

def detect_bg(grid: List[List[int]], proto: int, n: int, m: int) -> int:
    count = defaultdict(int)
    for i in range(n - 2):
        for j in range(m):
            c = grid[i][j]
            if c != proto:
                count[c] += 1
    if count:
        return max(count, key=count.get)
    return grid[n - 1][0] if n > 0 and m > 0 else 0

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

def get_inner(grid: List[List[int]], sec_start: int, sec_end: int, m: int, proto: int, bg: int) -> Optional[int]:
    for i in range(sec_start, sec_end + 1):
        for j in range(m):
            if grid[i][j] != proto and grid[i][j] != bg:
                return i
    return None

def get_filled_regions(grid: List[List[int]], i: int, m: int, proto: int, bg: int) -> List[Tuple[int, int, int]]:
    if i < 0 or i >= len(grid):
        return []
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

def horizontal_fill(grid: List[List[int]], i: int, m: int, proto: int, bg: int, chain: List[int]):
    if i >= len(grid):
        return
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
    for kk in range(len(comps) - 1):
        left_start, left_end, a = comps[kk]
        right_start, right_end, b = comps[kk + 1]
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

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n = len(g)
    if n < 2:
        return [row[:] for row in g]
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
    for k in range(len(sections) - 1):
        s1, e1 = sections[k]
        s2, e2 = sections[k + 1]
        gap_start = e1 + 1
        gap_end = s2 - 1
        if gap_start > gap_end:
            continue
        inner1 = get_inner(grid_out, s1, e1, m, proto, bg)
        if inner1 is None:
            continue
        inner2 = get_inner(grid_out, s2, e2, m, proto, bg)
        if inner2 is None:
            continue
        regions1 = get_filled_regions(grid_out, inner1, m, proto, bg)
        regions2 = get_filled_regions(grid_out, inner2, m, proto, bg)
        for start1, end1, a in regions1:
            for start2, end2, b in regions2:
                ol_s = max(start1, start2)
                ol_e = min(end1, end2)
                if ol_s > ol_e:
                    continue
                fill_c = is_adjacent_preceding(chain, a, b)
                if fill_c is not None:
                    for gi in range(gap_start, gap_end + 1):
                        for gj in range(ol_s, ol_e + 1):
                            if grid_out[gi][gj] == bg or grid_out[gi][gj] == proto:
                                grid_out[gi][gj] = fill_c
    return grid_out
```