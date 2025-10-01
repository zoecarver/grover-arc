```python
from collections import defaultdict
from typing import List, Dict, Tuple

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

def propagate_pattern(result: List[List[int]], pat_cols: List[int], pat_colors: List[int], ri: int, downward: bool, h: int, w: int):
    r = ri
    for ii in range(3):
        cc = pat_cols[ii]
        if 0 <= cc < w and result[r][cc] == 8:
            result[r][cc] = pat_colors[ii]
    if downward:
        dr = 1
        r = ri + dr
        while r < h:
            can = True
            for ii in range(3):
                cc = pat_cols[ii]
                val = result[r][cc]
                if val != 8 and val != pat_colors[ii]:
                    can = False
                    break
            if not can:
                break
            for ii in range(3):
                cc = pat_cols[ii]
                if result[r][cc] == 8:
                    result[r][cc] = pat_colors[ii]
            r += dr
    else:
        dr = -1
        r = ri + dr
        while r >= 0:
            can = True
            for ii in range(3):
                cc = pat_cols[ii]
                val = result[r][cc]
                if val != 8 and val != pat_colors[ii]:
                    can = False
                    break
            if not can:
                break
            for ii in range(3):
                cc = pat_cols[ii]
                if result[r][cc] == 8:
                    result[r][cc] = pat_colors[ii]
            r += dr

def extend_horizontal(result: List[List[int]], r: int, c: int, color: int, h: int, w: int):
    j = c - 1
    while j >= 0 and result[r][j] == 8:
        result[r][j] = color
        j -= 1
    j = c + 1
    while j < w and result[r][j] == 8:
        result[r][j] = color
        j += 1

def process_stem_side(result: List[List[int]], r: int, c_adj: int, d: int, color: int, h: int, w: int, special_down: bool, s3: int):
    if r >= h:
        return
    j = c_adj
    run_len = 0
    while 0 <= j < w and result[r][j] == 8:
        run_len += 1
        j += d
    next_j = j
    do_down = False
    if special_down and run_len > 0 and 0 <= next_j < w and result[r][next_j] == s3:
        do_down = True
    # fill run
    jj = c_adj
    for _ in range(run_len):
        result[r][jj] = color
        jj += d
    # down
    if do_down and r + 1 < h:
        left_c = min(c_adj, next_j)
        right_c = max(c_adj, next_j)
        for jj in range(left_c, right_c + 1):
            if result[r + 1][jj] == 8:
                result[r + 1][jj] = s3

def process_isolated_stem(result: List[List[int]], sr: int, length: int, typ: int, c: int, s1: int, s2: int, s3: int, h: int, w: int):
    if typ == 1:
        offs = [o for o in (1, 3, 5) if sr + o < h]
        cols = [s1, s2, s3][:len(offs)]
    else:
        offs = [0]
        if length > 3:
            offs.append(3)
        if length >= 4:
            offs.append(length - 2)
        cols = [s3, s2, s1][:len(offs)]
    for i in range(len(offs)):
        o = offs[i]
        r = sr + o
        if r >= h:
            continue
        colr = cols[i]
        special = (typ == 2 and o == 0)
        process_stem_side(result, r, c - 1, -1, colr, h, w, special, s3)
        process_stem_side(result, r, c + 1, 1, colr, h, w, special, s3)

def process_paired_stem(result: List[List[int]], sr: int, length: int, typ: int, away_d: int, c: int, s1: int, s2: int, s3: int, h: int, w: int):
    if typ == 1:
        offs = [o for o in (1, 3, 5) if sr + o < h]
        cols = [s1, s2, s3][:len(offs)]
    else:
        offs = [0]
        if length > 3:
            offs.append(3)
        if length >= 4:
            offs.append(length - 2)
        cols = [s3, s2, s1][:len(offs)]
    for i in range(len(offs)):
        o = offs[i]
        r = sr + o
        if r >= h:
            continue
        colr = cols[i]
        special = (typ == 2 and o == 0)
        process_stem_side(result, r, c + away_d, away_d, colr, h, w, special, s3)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    counts = count_non_blanks(g)
    singles = [c for c, cnt in counts.items() if cnt == 1]
    if len(singles) != 3:
        return [row[:] for row in g]
    s1, s2, s3 = sorted(singles)
    result = [row[:] for row in g]
    stems = find_stems(g, h, w)
    for stem in stems:
        sr, er, c, typ = stem
        l = er - sr
        paired = False
        away_d = 0
        for o_stem in stems:
            osr, oer, oc, otyp = o_stem
            ol = oer - osr
            if otyp == 3 - typ and abs(oc - c) == 1 and max(sr, osr) < min(er, oer):
                paired = True
                if l >= ol:
                    away_d = 1 if oc < c else -1
                    process_paired_stem(result, sr, l, typ, away_d, c, s1, s2, s3, h, w)
                break
        if not paired:
            process_isolated_stem(result, sr, l, typ, c, s1, s2, s3, h, w)
    pos_dict = find_singleton_positions(g, [s1, s2, s3])
    for k in [s1, s2, s3]:
        if k not in pos_dict:
            continue
        ri, ci = pos_dict[k]
        if ri == 0:
            pcols, pcolr = get_top_pattern(ci, k, s1, s2, s3)
            if len(pcols) == 3 and all(0 <= pc < w for pc in pcols):
                propagate_pattern(result, pcols, pcolr, ri, True, h, w)
        elif ri == h - 1:
            pcols, pcolr = get_bottom_pattern(ci, k, s1, s2, s3)
            if len(pcols) == 3 and all(0 <= pc < w for pc in pcols):
                propagate_pattern(result, pcols, pcolr, ri, False, h, w)
        else:
            extend_horizontal(result, ri, ci, k, h, w)
    return result
```