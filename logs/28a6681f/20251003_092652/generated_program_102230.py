```python
from typing import List, Tuple, Set
from copy import deepcopy

def find_horizontal_fills(g: List[List[int]]) -> List[Tuple[int, int]]:
    fills: List[Tuple[int, int]] = []
    for r in range(10):
        comps = []
        i = 0
        while i < 10:
            if g[r][i] == 0:
                i += 1
                continue
            start = i
            colors: Set[int] = set()
            has_fixed = False
            while i < 10 and g[r][i] != 0:
                if g[r][i] != 1:
                    colors.add(g[r][i])
                    has_fixed = True
                i += 1
            end = i - 1
            comps.append((start, end, colors.copy(), has_fixed))
        for idx in range(len(comps) - 1):
            l_start, l_end, l_colors, l_fixed = comps[idx]
            r_start, r_end, r_colors, r_fixed = comps[idx + 1]
            gap_start = l_end + 1
            gap_end = r_start - 1
            gap_size = gap_end - gap_start + 1
            if gap_size > 3 or gap_size < 1:
                continue
            has_nine_l = 9 in l_colors
            has_nine_r = 9 in r_colors
            if has_nine_l or has_nine_r:
                continue
            common = bool(l_colors & r_colors)
            do_fill = False
            if l_fixed and r_fixed:
                if common and gap_size <= 2:
                    do_fill = True
            if not (l_fixed and r_fixed) and gap_size <= 3:
                do_fill = True
            if do_fill:
                for cc in range(gap_start, gap_end + 1):
                    fills.append((r, cc))
    return fills

def find_vertical_fills(g: List[List[int]]) -> List[Tuple[int, int]]:
    fills: List[Tuple[int, int]] = []
    for c in range(10):
        comps = []
        i = 0
        while i < 10:
            if g[i][c] == 0 or g[i][c] == 1:
                i += 1
                continue
            start = i
            color = g[i][c]
            while i < 10 and g[i][c] != 0 and g[i][c] != 1:
                i += 1
            end = i - 1
            comps.append((start, end, color))
        for idx in range(len(comps) - 1):
            u_start, u_end, color1 = comps[idx]
            l_start, l_end, color2 = comps[idx + 1]
            gap_start = u_end + 1
            gap_end = l_start - 1
            gap_size = gap_end - gap_start + 1
            if gap_size == 1 and color1 == color2:
                fills.append((gap_start, c))
    return fills

def find_clears(g: List[List[int]]) -> List[Tuple[int, int]]:
    clears: List[Tuple[int, int]] = []
    for r in range(10):
        i = 0
        while i < 10:
            if g[r][i] == 0:
                i += 1
                continue
            start = i
            colors: Set[int] = set()
            all_one = True
            while i < 10 and g[r][i] != 0:
                if g[r][i] != 1:
                    all_one = False
                    colors.add(g[r][i])
                i += 1
            end = i - 1
            if all_one:
                # blue-only
                j = start - 1
                prev_end = -1
                while j >= 0 and g[r][j] == 0:
                    j -= 1
                if j >= 0:
                    prev_end = j
                    gap = start - (j + 1)
                if prev_end == -1 or gap > 3:
                    for p in range(start, end + 1):
                        clears.append((r, p))
            else:
                # mixed
                if 9 in colors:
                    for p in range(start, end + 1):
                        if g[r][p] == 1:
                            clears.append((r, p))
    return clears

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h_fills = find_horizontal_fills(g)
    v_fills = find_vertical_fills(g)
    all_fills = h_fills + v_fills
    clears = find_clears(g)
    for rr, cc in all_fills:
        out[rr][cc] = 1
    for rr, cc in clears:
        out[rr][cc] = 0
    return out
```