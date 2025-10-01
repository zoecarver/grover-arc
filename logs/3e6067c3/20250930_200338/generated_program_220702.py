```python
from typing import List, Optional, Tuple
from collections import Counter

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n = len(g)
    if n < 2:
        return [row[:] for row in g]
    m = len(g[0])
    out = [row[:] for row in g]
    proto = 1
    count = Counter()
    for i in range(n - 2):
        for j in range(m):
            c = out[i][j]
            if c != proto:
                count[c] += 1
    bg = count.most_common(1)[0][0] if count else (g[-1][0] if n > 0 and m > 0 else 0)
    chain = extract_chain(out, n, m, bg, proto)
    for i in range(n - 2):
        horizontal_fill(out, i, m, proto, bg, chain)
    sections = find_sections(out, n, m, proto)
    for k in range(len(sections) - 1):
        s_start, s_end = sections[k]
        l_start, l_end = sections[k + 1]
        g_start = s_end + 1
        g_end = l_start - 1
        if g_start > g_end:
            continue
        for j in range(m):
            cu = get_section_color(out, s_start, s_end, j, proto, bg)
            cl = get_section_color(out, l_start, l_end, j, proto, bg)
            if cu is not None and cl is not None:
                fc = is_adjacent_preceding(chain, cu, cl)
                if fc is not None:
                    for ii in range(g_start, g_end + 1):
                        if out[ii][j] == bg or out[ii][j] == proto:
                            out[ii][j] = fc
    return out

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

def get_section_color(grid: List[List[int]], start: int, end: int, j: int, proto: int, bg: int) -> Optional[int]:
    colors = set()
    for i in range(start, end + 1):
        c = grid[i][j]
        if c != bg and c != proto:
            colors.add(c)
    if len(colors) == 1:
        return next(iter(colors))
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
        left_s, left_e, a = comps[k]
        right_s, right_e, b = comps[k + 1]
        fill_c = is_adjacent_preceding(chain, a, b)
        if fill_c is not None:
            for j in range(left_e + 1, right_s):
                if row[j] == bg:
                    row[j] = fill_c
```