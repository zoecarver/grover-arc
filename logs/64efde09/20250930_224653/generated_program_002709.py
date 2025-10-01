```python
from typing import List, Dict, Tuple
from collections import defaultdict
import copy

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
                    runs.append((start_i, i, col, cl))
            else:
                i += 1
    return runs

def process_top_pattern(result: List[List[int]], pat_cols: List[int], pat_colors: List[int], h: int, w: int):
    if not all(0 <= pc < w for pc in pat_cols):
        return
    r = 0
    can_fill_start = all(result[r][pc] == 8 or result[r][pc] == pat_colors[i] for i, pc in enumerate(pat_cols))
    if can_fill_start:
        for i, pc in enumerate(pat_cols):
            if result[r][pc] == 8:
                result[r][pc] = pat_colors[i]
    r = 1
    while r < h:
        if all(result[r][pc] == 8 for pc in pat_cols):
            for i, pc in enumerate(pat_cols):
                result[r][pc] = pat_colors[i]
            r += 1
        else:
            break

def process_bottom_pattern(result: List[List[int]], pat_cols: List[int], pat_colors: List[int], h: int, w: int):
    if not all(0 <= pc < w for pc in pat_cols):
        return
    r = h - 2
    while r >= 0:
        if all(result[r][pc] == 8 for pc in pat_cols):
            for i, pc in enumerate(pat_cols):
                result[r][pc] = pat_colors[i]
            r -= 1
        else:
            break

def extend_middle_horizontal(result: List[List[int]], r: int, c: int, color: int, w: int):
    j = c - 1
    while j >= 0 and result[r][j] == 8:
        result[r][j] = color
        j -= 1
    j = c + 1
    while j < w and result[r][j] == 8:
        result[r][j] = color
        j += 1

def is_isolated_stem(stem: Tuple[int, int, int, int], all_stems: List[Tuple[int, int, int, int]]) -> bool:
    sr, er, c, typ = stem
    ln = er - sr
    opp_typ = 3 - typ
    for osr, oer, oc, otyp in all_stems:
        if abs(oc - c) != 1 or otyp != opp_typ:
            continue
        oln = oer - osr
        if oln >= ln and max(sr, osr) < min(er, oer):
            return False
    return True

def process_stem(result: List[List[int]], stem: Tuple[int, int, int, int], s1: int, s2: int, s3: int, h: int, w: int, all_stems: List[Tuple[int, int, int, int]]):
    sr, er, c, typ = stem
    ln = er - sr
    if not is_isolated_stem(stem, all_stems):
        return
    directions = [-1, 1]
    if typ == 1:
        offs_colors = [(1, s1), (3, s2), (5, s3)]
    else:
        offs_colors = [(0, s3), (3, s2), (ln - 2, s1)]
    for off, color in offs_colors:
        if 0 <= off < ln:
            row = sr + off
            if row >= h:
                continue
            for d in directions:
                j = c + d
                while 0 <= j < w and result[row][j] == 8:
                    result[row][j] = color
                    j += d

def program(g: List[List[int]]) -> List[List[int]]:
    counts = count_non_blanks(g)
    singletons = [c for c in sorted(counts.keys()) if counts[c] == 1]
    if len(singletons) != 3:
        return [row[:] for row in g]
    s1, s2, s3 = singletons
    result = [row[:] for row in g]
    h = len(result)
    if h == 0:
        return result
    w = len(result[0])
    pos = find_singleton_positions(result, singletons)
    # Process top patterns
    for k in singletons:
        if k not in pos or pos[k][0] != 0:
            continue
        c = pos[k][1]
        if k == s1:
            pat_cols = [c - 4, c - 2, c]
            pat_colors = [s3, s2, s1]
        elif k == s2:
            pat_cols = [c - 2, c, c + 2]
            pat_colors = [s3, s2, s1]
        elif k == s3:
            pat_cols = [c, c + 2, c + 4]
            pat_colors = [s3, s2, s1]
        else:
            continue
        process_top_pattern(result, pat_cols, pat_colors, h, w)
    # Process bottom patterns
    for k in singletons:
        if k not in pos or pos[k][0] != h - 1:
            continue
        c = pos[k][1]
        if k == s1:
            pat_cols = [c, c + 1, c + 4]
            pat_colors = [s1, s2, s3]
        elif k == s2:
            pat_cols = [c - 1, c, c + 3]
            pat_colors = [s1, s2, s3]
        elif k == s3:
            pat_cols = [c - 4, c - 3, c]
            pat_colors = [s1, s2, s3]
        else:
            continue
        process_bottom_pattern(result, pat_cols, pat_colors, h, w)
    # Process middle extensions
    for k in singletons:
        if k not in pos or not (0 < pos[k][0] < h - 1):
            continue
        r, c = pos[k]
        extend_middle_horizontal(result, r, c, k, w)
    # Process stems
    stems = find_stems(result, h, w)
    for stem in stems:
        process_stem(result, stem, s1, s2, s3, h, w, stems)
    return result
```