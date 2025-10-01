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

def is_isolated(stem: Tuple[int, int, int, int], all_stems: List[Tuple[int, int, int, int]]) -> bool:
    sr, er, c, typ = stem
    opp = 3 - typ
    for osr, oer, oc, otyp in all_stems:
        if otyp == opp and abs(oc - c) == 1 and max(sr, osr) < min(er, oer):
            return False
    return True

def get_top_pattern(c: int, k: int, s1: int, s2: int, s3: int) -> Tuple[List[int], List[int]]:
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
        return [], []
    return pat_cols, pat_colors

def get_bottom_pattern(c: int, k: int, s1: int, s2: int, s3: int) -> Tuple[List[int], List[int]]:
    pat_colors = [s1, s2, s3]
    if k == s1:
        pat_cols = [c, c + 1, c + 4]
    elif k == s2:
        pat_cols = [c - 1, c, c + 3]
    elif k == s3:
        pat_cols = [c - 4, c - 3, c]
    else:
        return [], []
    return pat_cols, pat_colors

def propagate_pattern(result: List[List[int]], pat_cols: List[int], pat_colors: List[int], start_r: int, downward: bool, h: int, w: int):
    if len(pat_cols) != 3:
        return
    r = start_r
    can_fill_start = all(0 <= pat_cols[i] < w and (result[r][pat_cols[i]] == 8 or result[r][pat_cols[i]] == pat_colors[i]) for i in range(3))
    if not can_fill_start:
        return
    for i in range(3):
        cc = pat_cols[i]
        if 0 <= cc < w and result[r][cc] == 8:
            result[r][cc] = pat_colors[i]
    if downward:
        r += 1
        while r < h:
            can = all(0 <= pat_cols[i] < w and (result[r][pat_cols[i]] == 8 or result[r][pat_cols[i]] == pat_colors[i]) for i in range(3))
            if not can:
                break
            for i in range(3):
                cc = pat_cols[i]
                if result[r][cc] == 8:
                    result[r][cc] = pat_colors[i]
            r += 1
    else:
        r -= 1
        while r >= 0:
            can = all(0 <= pat_cols[i] < w and (result[r][pat_cols[i]] == 8 or result[r][pat_cols[i]] == pat_colors[i]) for i in range(3))
            if not can:
                break
            for i in range(3):
                cc = pat_cols[i]
                if result[r][cc] == 8:
                    result[r][cc] = pat_colors[i]
            r -= 1

def extend_horizontal(result: List[List[int]], r: int, c: int, color: int, h: int, w: int):
    j = c - 1
    while j >= 0 and result[r][j] == 8:
        result[r][j] = color
        j -= 1
    j = c + 1
    while j < w and result[r][j] == 8:
        result[r][j] = color
        j += 1

def fill_in_direction(result: List[List[int]], row: int, start_j: int, d: int, color: int, h: int, w: int):
    j = start_j
    while 0 <= j < w and result[row][j] == 8:
        result[row][j] = color
        j += d

def process_isolated_stems(result: List[List[int]], stems: List[Tuple[int, int, int, int]], s1: int, s2: int, s3: int, h: int, w: int):
    for stem in stems:
        sr, er, c, typ = stem
        l = er - sr
        if typ == 1:
            if not is_isolated(stem, stems):
                continue
            offs = []
            if sr + 1 < h:
                offs.append((sr + 1, s1))
            if sr + 3 < h:
                offs.append((sr + 3, s2))
            if sr + 5 < h:
                offs.append((sr + 5, s3))
            for roww, colr in offs:
                for dd in [-1, 1]:
                    fill_in_direction(result, roww, c + dd, dd, colr, h, w)
        elif typ == 2:
            if not is_isolated(stem, stems):
                continue
            off_list = [0, 3, l - 2] if l - 2 >= 0 else [0, 3]
            col_list = [s3, s2, s1][:len(off_list)]
            for idx, off in enumerate(off_list):
                roww = sr + off
                if roww >= h:
                    continue
                colr = col_list[idx]
                for dd in [-1, 1]:
                    fill_in_direction(result, roww, c + dd, dd, colr, h, w)

def process_paired_type1_stems(result: List[List[int]], stems: List[Tuple[int, int, int, int]], s1: int, s2: int, s3: int, h: int, w: int):
    for stem in stems:
        sr, er, c, typ = stem
        if typ != 1 or is_isolated(stem, stems):
            continue
        l = er - sr
        for o_sr, o_er, o_c, o_typ in stems:
            if o_typ != 2 or abs(o_c - c) != 1:
                continue
            overlap_sr = max(sr, o_sr)
            overlap_er = min(er, o_er)
            if overlap_sr >= overlap_er:
                continue
            ol = overlap_er - overlap_sr
            dir_to = 1 if o_c > c else -1
            away_d = -dir_to
            off_col = [(0, s1), (1, s2), (3, s3)]
            for off, colr in off_col:
                if off >= ol:
                    continue
                roww = overlap_sr + off
                if roww >= h:
                    continue
                fill_in_direction(result, roww, c + away_d, away_d, colr, h, w)

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    result = [row[:] for row in g]
    counts = count_non_blanks(result)
    singleton_list = [col for col, cnt in counts.items() if cnt == 1]
    if len(singleton_list) != 3:
        return result
    singleton_list.sort()
    s1, s2, s3 = singleton_list
    pos = find_singleton_positions(result, singleton_list)
    for sk in [s1, s2, s3]:
        ri_ci = pos.get(sk, (None, None))
        if ri_ci[0] is None:
            continue
        ri, ci = ri_ci
        if ri == 0:
            pat_cols, pat_colors = get_top_pattern(ci, sk, s1, s2, s3)
            propagate_pattern(result, pat_cols, pat_colors, ri, True, h, w)
        elif ri == h - 1:
            pat_cols, pat_colors = get_bottom_pattern(ci, sk, s1, s2, s3)
            propagate_pattern(result, pat_cols, pat_colors, ri, False, h, w)
        else:
            extend_horizontal(result, ri, ci, sk, h, w)
    stems = find_stems(result, h, w)
    process_isolated_stems(result, stems, s1, s2, s3, h, w)
    process_paired_type1_stems(result, stems, s1, s2, s3, h, w)
    return result
```