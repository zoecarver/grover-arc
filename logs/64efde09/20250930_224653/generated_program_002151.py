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

def get_top_pattern(c: int, sk: int, s1: int, s2: int, s3: int, w: int) -> Tuple[List[int], List[int]]:
    if sk == s1:
        pat_cols = [c - 4, c - 2, c]
        pat_colors = [s3, s2, s1]
    elif sk == s2:
        pat_cols = [c - 2, c, c + 2]
        pat_colors = [s3, s2, s1]
    elif sk == s3:
        pat_cols = [c, c + 2, c + 4]
        pat_colors = [s3, s2, s1]
    else:
        return [], []
    if all(0 <= cc < w for cc in pat_cols):
        return pat_cols, pat_colors
    return [], []

def get_bottom_pattern(c: int, sk: int, s1: int, s2: int, s3: int, w: int) -> Tuple[List[int], List[int]]:
    if sk == s1:
        pat_cols = [c, c + 1, c + 4]
        pat_colors = [s1, s2, s3]
    elif sk == s2:
        pat_cols = [c - 1, c, c + 3]
        pat_colors = [s1, s2, s3]
    elif sk == s3:
        pat_cols = [c - 4, c - 3, c]
        pat_colors = [s1, s2, s3]
    else:
        return [], []
    if all(0 <= cc < w for cc in pat_cols):
        return pat_cols, pat_colors
    return [], []

def propagate_down(result: List[List[int]], pat_cols: List[int], pat_colors: List[int], start_r: int, h: int, w: int):
    r = start_r
    while r < h:
        can = all(0 <= pat_cols[i] < w and (result[r][pat_cols[i]] == 8 or result[r][pat_cols[i]] == pat_colors[i]) for i in range(3))
        if not can:
            break
        for i in range(3):
            cc = pat_cols[i]
            if result[r][cc] == 8:
                result[r][cc] = pat_colors[i]
        r += 1

def propagate_up(result: List[List[int]], pat_cols: List[int], pat_colors: List[int], start_r: int, h: int, w: int):
    r = start_r
    while r >= 0:
        can = all(0 <= pat_cols[i] < w and (result[r][pat_cols[i]] == 8 or result[r][pat_cols[i]] == pat_colors[i]) for i in range(3))
        if not can:
            break
        for i in range(3):
            cc = pat_cols[i]
            if result[r][cc] == 8:
                result[r][cc] = pat_colors[i]
        r -= 1

def extend_middle_horizontal(result: List[List[int]], r: int, c: int, color: int, h: int, w: int):
    j = c - 1
    while j >= 0 and result[r][j] == 8:
        result[r][j] = color
        j -= 1
    j = c + 1
    while j < w and result[r][j] == 8:
        result[r][j] = color
        j += 1

def get_partners(stem: Tuple[int, int, int, int], stems: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int]]:
    sr, er, c, typ = stem
    opp = 3 - typ
    partners = []
    for osr, oer, oc, otyp in stems:
        if (oc == c - 1 or oc == c + 1) and otyp == opp and max(sr, osr) < min(er, oer):
            partners.append((oc, osr, oer))
    return partners

def do_stem_fills(stem: Tuple[int, int, int, int], directions: List[int], s1: int, s2: int, s3: int, result: List[List[int]], h: int, w: int):
    sr, er, c, typ = stem
    ln = er - sr
    if typ == 1:
        for off, color in [(1, s1), (3, s2), (5, s3)]:
            if off < ln and sr + off < h:
                row = sr + off
                for d in directions:
                    j = c + d
                    while 0 <= j < w and result[row][j] == 8:
                        result[row][j] = color
                        j += d
    else:  # typ == 2
        # off 0 s3
        row = sr
        if row < h:
            color = s3
            for d in directions:
                j = c + d
                while 0 <= j < w and result[row][j] == 8:
                    result[row][j] = color
                    j += d
        # off 3 s2
        off = 3
        if off < ln and sr + off < h:
            row = sr + off
            color = s2
            for d in directions:
                j = c + d
                while 0 <= j < w and result[row][j] == 8:
                    result[row][j] = color
                    j += d
        # off ln-2 s1
        off = ln - 2
        if ln >= 6 and off < ln and sr + off < h:
            row = sr + off
            color = s1
            for d in directions:
                j = c + d
                while 0 <= j < w and result[row][j] == 8:
                    result[row][j] = color
                    j += d

def program(g: List[List[int]]) -> List[List[int]]:
    result = [row[:] for row in g]
    h = len(g)
    if h == 0:
        return result
    w = len(g[0])
    counts = count_non_blanks(g)
    singletons = [c for c, cnt in counts.items() if cnt == 1]
    if len(singletons) != 3:
        return result
    singletons.sort()
    s1, s2, s3 = singletons
    pos = find_singleton_positions(g, singletons)
    # Process top patterns
    for sk in [s1, s2, s3]:
        if sk in pos:
            r, c = pos[sk]
            if r == 0:
                pat_cols, pat_colors = get_top_pattern(c, sk, s1, s2, s3, w)
                if pat_cols:
                    # Fill anchor
                    for i in range(3):
                        cc = pat_cols[i]
                        if result[0][cc] == 8:
                            result[0][cc] = pat_colors[i]
                    # Propagate down
                    propagate_down(result, pat_cols, pat_colors, 1, h, w)
    # Process bottom patterns
    for sk in [s1, s2, s3]:
        if sk in pos:
            r, c = pos[sk]
            if r == h - 1:
                pat_cols, pat_colors = get_bottom_pattern(c, sk, s1, s2, s3, w)
                if pat_cols:
                    # Fill anchor
                    for i in range(3):
                        cc = pat_cols[i]
                        if result[r][cc] == 8:
                            result[r][cc] = pat_colors[i]
                    # Propagate up
                    propagate_up(result, pat_cols, pat_colors, r - 1, h, w)
    # Process middle extensions
    for sk in [s1, s2, s3]:
        if sk in pos:
            r, c = pos[sk]
            if 0 < r < h - 1:
                extend_middle_horizontal(result, r, c, sk, h, w)
    # Process stems
    stems = find_stems(result, h, w)
    for stem in stems:
        partners = get_partners(stem, stems)
        if not partners:
            directions = [-1, 1]
            do_stem_fills(stem, directions, s1, s2, s3, result, h, w)
        else:
            away = set()
            max_pln = 0
            for pc, posr, poer in partners:
                away.add(1 if pc < c else -1)
                max_pln = max(max_pln, poer - posr)
            sr, er, c, typ = stem
            ln = er - sr
            if ln > max_pln and away:
                directions = list(away)
                do_stem_fills(stem, directions, s1, s2, s3, result, h, w)
    return result
```