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
    if h == 0:
        return {}
    w = len(g[0])
    pos_dict = {}
    for i in range(h):
        for j in range(w):
            cc = g[i][j]
            if cc in singletons:
                pos_dict[cc] = (i, j)
    return pos_dict

def find_stems(g: List[List[int]]) -> List[Tuple[int, int, int, int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
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
                    runs.append((start_i, i, col, cl))
            else:
                i += 1
    return runs

def get_top_pattern(sk: int, c: int, s1: int, s2: int, s3: int) -> Tuple[List[int], List[int]]:
    if sk == s1:
        pat_cols = [c, c + 2, c + 4]
        pat_colors = [s1, s2, s3]
    elif sk == s2:
        pat_cols = [c - 2, c, c + 2]
        pat_colors = [s3, s2, s1]
    elif sk == s3:
        pat_cols = [c - 4, c - 2, c]
        pat_colors = [s3, s2, s1]
    else:
        return [], []
    return pat_cols, pat_colors

def get_bottom_pattern(sk: int, c: int, s1: int, s2: int, s3: int) -> Tuple[List[int], List[int]]:
    if sk == s1:
        pat_cols = [c, c + 1, c + 3]
        pat_colors = [s1, s2, s3]
    elif sk == s2:
        pat_cols = [c - 1, c, c + 3]
        pat_colors = [s1, s2, s3]
    elif sk == s3:
        pat_cols = [c - 3, c - 1, c]
        pat_colors = [s1, s2, s3]
    else:
        return [], []
    return pat_cols, pat_colors

def propagate_pattern(result: List[List[int]], pat_cols: List[int], pat_colors: List[int], start_r: int, h: int, w: int, downward: bool):
    r = start_r
    for ii, cc in enumerate(pat_cols):
        if 0 <= cc < w and result[r][cc] == 8:
            result[r][cc] = pat_colors[ii]
    if downward:
        dr = 1
        end = h
    else:
        dr = -1
        end = -1
    r += dr
    while (dr > 0 and r < h) or (dr < 0 and r >= 0):
        can_fill = all(0 <= pat_cols[ii] < w and (result[r][pat_cols[ii]] == 8 or result[r][pat_cols[ii]] == pat_colors[ii]) for ii in range(len(pat_cols)))
        if not can_fill:
            break
        for ii, cc in enumerate(pat_cols):
            if result[r][cc] == 8:
                result[r][cc] = pat_colors[ii]
        r += dr

def extend_middle_horizontal(result: List[List[int]], r: int, c: int, color: int, w: int):
    # left
    cc = c
    while cc > 0 and result[r][cc - 1] == 8:
        cc -= 1
        result[r][cc] = color
    # right
    cc = c
    while cc < w - 1 and result[r][cc + 1] == 8:
        cc += 1
        result[r][cc] = color

def fill_stem_direction(result: List[List[int]], row: int, col: int, step: int, color: int, h: int, w: int):
    if not 0 <= row < h:
        return
    cc = col + step
    while 0 <= cc < w and result[row][cc] == 8:
        result[row][cc] = color
        cc += step

def process_type1_stem(result: List[List[int]], stem: List[Tuple[int, int, int, int]], stems: List[Tuple[int, int, int, int]], s1: int, s2: int, s3: int, h: int, w: int):
    sr, er, col, typ = stem
    length = er - sr
    left_paired = any(ot == 2 and oc == col - 1 and max(sr, os) < min(er, oe) for os, oe, oc, ot in stems)
    right_paired = any(ot == 2 and oc == col + 1 and max(sr, os) < min(er, oe) for os, oe, oc, ot in stems)
    directions = []
    if not left_paired:
        directions.append(-1)
    if not right_paired:
        directions.append(1)
    offs_colors = [(1, s1), (3, s2), (5, s3)]
    for step in directions:
        for off, color in offs_colors:
            if off >= length:
                continue
            frow = sr + off
            fill_stem_direction(result, frow, col, step, color, h, w)

def process_type2_stem(result: List[List[int]], stem: List[Tuple[int, int, int, int]], stems: List[Tuple[int, int, int, int]], s1: int, s2: int, s3: int, h: int, w: int):
    sr, er, col, typ = stem
    length = er - sr
    # check isolated
    paired = any(ot == 1 and abs(oc - col) == 1 and max(sr, os) < min(er, oe) for os, oe, oc, ot in stems)
    if paired:
        return
    # possible directions
    for step in [-1, 1]:
        offset_row = sr + 0
        if not 0 <= offset_row < h:
            continue
        start_cc = col + step
        if not 0 <= start_cc < w or result[offset_row][start_cc] != 8:
            continue
        # compute num and condition
        cc = start_cc
        num = 0
        while 0 <= cc < w and result[offset_row][cc] == 8:
            num += 1
            cc += step
        next_cc = cc
        condition = 0 <= next_cc < w and result[offset_row][next_cc] == s3
        # fill offset 0
        cc = start_cc
        for _ in range(num):
            result[offset_row][cc] = s3
            cc += step
        # determine offs
        s2_offs = [3] if not condition else [3, length - 2]
        s1_off = (length - 1) if condition else (length - 2)
        # fill s2
        for off in s2_offs:
            if off >= length:
                continue
            frow = sr + off
            fill_stem_direction(result, frow, col, step, s2, h, w)
        # fill s1
        if s1_off >= length:
            return
        frow = sr + s1_off
        fill_stem_direction(result, frow, col, step, s1, h, w)

def program(g: List[List[int]]) -> List[List[int]]:
    result = [row[:] for row in g]
    h = len(result)
    if h == 0:
        return result
    w = len(result[0])
    counts = count_non_blanks(result)
    singletons = [c for c, cnt in counts.items() if cnt == 1]
    if len(singletons) != 3:
        return result
    singletons.sort()
    s1, s2, s3 = singletons
    pos = find_singleton_positions(result, singletons)
    # process top patterns
    for sk in singletons:
        r, c = pos[sk]
        if r == 0:
            pat_cols, pat_colors = get_top_pattern(sk, c, s1, s2, s3)
            if len(pat_cols) == 3 and all(0 <= pc < w for pc in pat_cols):
                propagate_pattern(result, pat_cols, pat_colors, 0, h, w, True)
    # process bottom patterns
    for sk in singletons:
        r, c = pos[sk]
        if r == h - 1:
            pat_cols, pat_colors = get_bottom_pattern(sk, c, s1, s2, s3)
            if len(pat_cols) == 3 and all(0 <= pc < w for pc in pat_cols):
                propagate_pattern(result, pat_cols, pat_colors, h - 1, h, w, False)
    # process middle horizontals
    for sk in singletons:
        r, c = pos[sk]
        if 0 < r < h - 1:
            extend_middle_horizontal(result, r, c, sk, w)
    # process stems
    stems = find_stems(result)
    for stem in stems:
        sr, er, col, typ = stem
        length = er - sr
        if typ == 1:
            process_type1_stem(result, stem, stems, s1, s2, s3, h, w)
        elif typ == 2:
            process_type2_stem(result, stem, stems, s1, s2, s3, h, w)
    return result
```