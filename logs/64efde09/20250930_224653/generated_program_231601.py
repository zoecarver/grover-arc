```python
from typing import List, Dict, Tuple
from collections import defaultdict

def count_non_blanks(g: List[List[int]]) -> Dict[int, int]:
    h = len(g)
    if h == 0:
        return {}
    w = len(g[0])
    counts = defaultdict(int)
    for i in range(h):
        for j in range(w):
            c = g[i][j]
            if c != 8:
                counts[c] += 1
    return counts

def find_singleton_positions(g: List[List[int]], singletons: List[int]) -> Dict[int, Tuple[int, int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    pos_dict: Dict[int, Tuple[int, int]] = {}
    for i in range(h):
        for j in range(w):
            cc = g[i][j]
            if cc in singletons:
                pos_dict[cc] = (i, j)
    return pos_dict

def find_stems(g: List[List[int]], h: int, w: int) -> List[Tuple[int, int, int, int]]:
    runs = []
    for col in range(w):
        i = 0
        while i < h:
            val = g[i][col]
            if val == 1 or val == 2:
                cl = val
                start_i = i
                i += 1
                while i < h and g[i][col] == cl:
                    i += 1
                length = i - start_i
                if length >= 4:
                    runs.append((start_i, i - 1, col, cl))
            else:
                i += 1
    return runs

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    counts = count_non_blanks(grid)
    singleton_list = [c for c in sorted(counts) if counts[c] == 1]
    if len(singleton_list) != 3:
        return grid
    s1, s2, s3 = singleton_list
    pos_dict = find_singleton_positions(grid, singleton_list)
    # Top pattern parameters
    pat_offsets_top = [0, 2, 3]
    colors_top = [s3, s2, s1]
    off_top = {s1: 3, s2: 2, s3: 0}
    # Bottom pattern parameters
    pat_offsets_bottom = [0, 1, 4]
    colors_bottom = [s1, s2, s3]
    off_bottom = {s1: 0, s2: 1, s3: 4}
    # Process singletons using initial positions
    for sc in singleton_list:
        if sc not in pos_dict:
            continue
        r, c = pos_dict[sc]
        if r == 0:  # top
            if sc not in off_top:
                continue
            off = off_top[sc]
            start_c = c - off
            if start_c < 0:
                continue
            pat_cs = [start_c + o for o in pat_offsets_top]
            if any(pc < 0 or pc >= w for pc in pat_cs):
                continue
            pat_col = pat_cs
            pat_color = colors_top
            # propagate downward
            curr_r = 0
            while curr_r < h:
                if all(grid[curr_r][pc] == 8 for pc in pat_col):
                    for idx, pc in enumerate(pat_col):
                        grid[curr_r][pc] = pat_color[idx]
                    curr_r += 1
                else:
                    break
        elif r == h - 1:  # bottom
            if sc not in off_bottom:
                continue
            off = off_bottom[sc]
            start_c = c - off
            if start_c < 0:
                continue
            pat_cs = [start_c + o for o in pat_offsets_bottom]
            if any(pc < 0 or pc >= w for pc in pat_cs):
                continue
            pat_col = pat_cs
            pat_color = colors_bottom
            # propagate upward
            curr_r = h - 1
            while curr_r >= 0:
                if all(grid[curr_r][pc] == 8 for pc in pat_col):
                    for idx, pc in enumerate(pat_col):
                        grid[curr_r][pc] = pat_color[idx]
                    curr_r -= 1
                else:
                    break
        else:  # middle
            # horizontal extension
            j = c - 1
            while j >= 0 and grid[r][j] == 8:
                grid[r][j] = sc
                j -= 1
            j = c + 1
            while j < w and grid[r][j] == 8:
                grid[r][j] = sc
                j += 1
    # Now process stems on updated grid
    stems = find_stems(grid, h, w)
    for start_r, end_r, col, typ in stems:
        l = end_r - start_r + 1
        if typ == 1:
            offs = [1, 3, 5]
            fill_cs = [s1, s2, s3]
        else:  # typ == 2
            offs = [0, 3, l - 2]
            fill_cs = [s3, s2, s1]
        for idx, off in enumerate(offs):
            if off > l - 1:
                continue
            fr = start_r + off
            if fr >= h:
                continue
            fc = col
            fill_c = fill_cs[idx]
            # fill left
            le = fc - 1
            while le >= 0 and grid[fr][le] == 8:
                grid[fr][le] = fill_c
                le -= 1
            # fill right
            ri = fc + 1
            while ri < w and grid[fr][ri] == 8:
                grid[fr][ri] = fill_c
                ri += 1
    return grid
```