```python
from typing import List, Tuple

def identify_bg(grid: List[List[int]]) -> int:
    return grid[-1][0] if grid else 0

def extract_chain(grid: List[List[int]], n: int, bg: int) -> List[int]:
    if n < 2:
        return []
    m = len(grid[0])
    return [grid[n-2][j] for j in range(m) if grid[n-2][j] != bg]

def find_sections(grid: List[List[int]], proto: int) -> List[Tuple[int, int]]:
    n = len(grid)
    sections = []
    i = 0
    while i < n - 2:
        if any(c == proto for c in grid[i]):
            start = i
            i += 1
            while i < n - 2 and any(c == proto for c in grid[i]):
                i += 1
            sections.append((start, i - 1))
        else:
            i += 1
    return sections

def get_inner_row(start: int, end: int, grid: List[List[int]], proto: int, bg: int) -> int:
    for r in range(start, end + 1):
        if any(c != proto and c != bg for c in grid[r]):
            return r
    return -1

def get_regions(grid: List[List[int]], i: int, proto: int, bg: int) -> List[Tuple[int, int, int]]:
    if i < 0:
        return []
    row = grid[i]
    m = len(row)
    walls = [j for j in range(m) if row[j] == proto]
    regions = []
    prev = -1
    for w in walls:
        inner_s = prev + 1
        inner_e = w - 1
        if inner_s > inner_e:
            prev = w
            continue
        colors = {row[j] for j in range(inner_s, inner_e + 1) if row[j] != proto and row[j] != bg}
        if len(colors) == 1:
            c = next(iter(colors))
            js = [j for j in range(inner_s, inner_e + 1) if row[j] == c]
            if js:
                min_j = min(js)
                max_j = max(js)
                regions.append((min_j, max_j, c))
        prev = w
    # last region
    inner_s = prev + 1
    inner_e = m - 1
    if inner_s <= inner_e:
        colors = {row[j] for j in range(inner_s, inner_e + 1) if row[j] != proto and row[j] != bg}
        if len(colors) == 1:
            c = next(iter(colors))
            js = [j for j in range(inner_s, inner_e + 1) if row[j] == c]
            if js:
                min_j = min(js)
                max_j = max(js)
                regions.append((min_j, max_j, c))
    return regions

def is_adjacent_preceding(chain: List[int], a: int, b: int) -> int:
    for ii in range(len(chain) - 1):
        if chain[ii] == a and chain[ii + 1] == b:
            return a
        if chain[ii] == b and chain[ii + 1] == a:
            return b
    return None

def vertical_fill(grid: List[List[int]], sections: List[Tuple[int, int]], proto: int, bg: int, chain: List[int]) -> List[List[int]]:
    n = len(grid)
    if len(sections) < 2:
        return [row[:] for row in grid]
    new_grid = [row[:] for row in grid]
    for s in range(len(sections) - 1):
        start1, end1 = sections[s]
        start2, end2 = sections[s + 1]
        if start2 <= end1 + 1:
            continue
        inner1 = get_inner_row(start1, end1, grid, proto, bg)
        if inner1 == -1:
            continue
        inner2 = get_inner_row(start2, end2, grid, proto, bg)
        if inner2 == -1:
            continue
        reg1 = get_regions(grid, inner1, proto, bg)
        reg2 = get_regions(grid, inner2, proto, bg)
        for r1 in reg1:
            s1, e1, c1 = r1
            for r2 in reg2:
                s2, e2, c2 = r2
                ov_s = max(s1, s2)
                ov_e = min(e1, e2)
                if ov_s > ov_e:
                    continue
                fill_c = is_adjacent_preceding(chain, c1, c2)
                if fill_c is not None:
                    for ii in range(end1 + 1, start2):
                        for j in range(ov_s, ov_e + 1):
                            if new_grid[ii][j] == bg:
                                new_grid[ii][j] = fill_c
    return new_grid

def horizontal_fill(grid: List[List[int]], proto: int, bg: int, chain: List[int]) -> List[List[int]]:
    n, m = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for i in range(n - 2):
        row = new_grid[i]
        wall_pos = [j for j in range(m) if row[j] == proto]
        if len(wall_pos) < 2:
            continue
        regions = []
        prev = -1
        for k in range(len(wall_pos)):
            w = wall_pos[k]
            inner_s = prev + 1
            inner_e = w - 1
            if inner_s > inner_e:
                prev = w
                continue
            colors = {row[j] for j in range(inner_s, inner_e + 1) if row[j] != proto and row[j] != bg}
            if len(colors) == 1:
                c = next(iter(colors))
                js = [j for j in range(inner_s, inner_e + 1) if row[j] == c]
                if js:
                    regions.append((k, c))
            prev = w
        for p in range(len(regions) - 1):
            k1, c1 = regions[p]
            k2, c2 = regions[p + 1]
            fill_c = is_adjacent_preceding(chain, c1, c2)
            if fill_c is not None:
                left_wall = wall_pos[k1]
                right_wall = wall_pos[k2]
                for j in range(left_wall + 1, right_wall):
                    if new_grid[i][j] == bg:
                        new_grid[i][j] = fill_c
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n < 3:
        return [row[:] for row in g]
    m = len(g[0])
    bg = identify_bg(g)
    proto = 1
    chain = extract_chain(g, n, bg)
    sections = find_sections(g, proto)
    g = vertical_fill(g, sections, proto, bg, chain)
    g = horizontal_fill(g, proto, bg, chain)
    return g
```