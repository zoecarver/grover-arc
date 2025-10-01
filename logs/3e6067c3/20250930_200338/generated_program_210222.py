```python
from typing import List, Optional, Tuple

def detect_bg(grid: List[List[int]], proto: int) -> int:
    n = len(grid)
    if n == 0:
        return 0
    m = len(grid[0])
    count = {}
    for i in range(n - 2):
        for j in range(m):
            c = grid[i][j]
            if c != proto:
                count[c] = count.get(c, 0) + 1
    if not count:
        return 0
    return max(count, key=count.get)

def extract_chain(grid: List[List[int]], bg: int, proto: int) -> List[int]:
    n = len(grid)
    if n < 2:
        return []
    m = len(grid[0])
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
    if n < 2:
        return []
    m = len(grid[0])
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

def horizontal_fill(grid: List[List[int]], i: int, proto: int, bg: int, chain: List[int]):
    n = len(grid)
    if i >= n:
        return
    m = len(grid[0])
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

def vertical_propagate_within(grid: List[List[int]], sec_start: int, sec_end: int, proto: int, bg: int):
    n = len(grid)
    if sec_start > sec_end or sec_start >= n:
        return
    m = len(grid[0])
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

def get_inner(grid: List[List[int]], sec_start: int, sec_end: int, proto: int, bg: int) -> Optional[int]:
    n = len(grid)
    if sec_start > sec_end or sec_start >= n:
        return None
    m = len(grid[0])
    for i in range(sec_start, sec_end + 1):
        for j in range(m):
            if grid[i][j] != proto and grid[i][j] != bg:
                return i
    return None

def get_filled_regions(grid: List[List[int]], i: int, proto: int, bg: int) -> List[Tuple[int, int, int]]:
    n = len(grid)
    if i >= n:
        return []
    m = len(grid[0])
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

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    grid = [row[:] for row in g]
    n = len(grid)
    m = len(grid[0])
    proto = 1
    bg = detect_bg(grid, proto)
    chain = extract_chain(grid, bg, proto)
    for i in range(n - 2):
        horizontal_fill(grid, i, proto, bg, chain)
    sections = find_sections(grid, proto)
    for start, end in sections:
        vertical_propagate_within(grid, start, end, proto, bg)
    for k in range(len(sections) - 1):
        s1, e1 = sections[k]
        s2, e2 = sections[k + 1]
        gap_start = e1 + 1
        gap_end = s2 - 1
        if gap_start > gap_end:
            continue
        inner1 = get_inner(grid, s1, e1, proto, bg)
        if inner1 is None:
            continue
        inner2 = get_inner(grid, s2, e2, proto, bg)
        if inner2 is None:
            continue
        regs1 = get_filled_regions(grid, inner1, proto, bg)
        regs2 = get_filled_regions(grid, inner2, proto, bg)
        for st1, en1, a in regs1:
            for st2, en2, b in regs2:
                fill_c = is_adjacent_preceding(chain, a, b)
                if fill_c is not None and max(st1, st2) <= min(en1, en2) + 1:
                    for ii in range(gap_start, gap_end + 1):
                        for jj in range(st1, en1 + 1):
                            if grid[ii][jj] == bg:
                                grid[ii][jj] = fill_c
                    break
    return grid
```