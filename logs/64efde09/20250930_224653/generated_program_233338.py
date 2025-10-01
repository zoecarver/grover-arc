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
                    runs.append((start_i, i, col, cl))
            else:
                i += 1
    return runs

def is_isolated(stem: Tuple[int, int, int, int], all_stems: List[Tuple[int, int, int, int]]) -> bool:
    sr, er, c, typ = stem
    length = er - sr
    opp = 3 - typ
    for osr, oer, oc, otyp in all_stems:
        other_length = oer - osr
        if otyp == opp and oc in (c - 1, c + 1) and other_length >= length:
            if max(sr, osr) < min(er, oer):
                return False
    return True

def get_pattern_cols_and_colors(k: int, c: int, s1: int, s2: int, s3: int, is_top: bool) -> Tuple[List[int], List[int]]:
    if is_top:
        pat_colors = [s3, s2, s1]
        if k == s1:
            pat_cols = [c - 4, c - 2, c]
        elif k == s2:
            pat_cols = [c - 2, c, c + 2]
        elif k == s3:
            pat_cols = [c, c + 2, c + 4]
        else:
            return [], []
    else:  # bottom
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

def propagate_top_pattern(result: List[List[int]], pat_cols: List[int], pat_colors: List[int], h: int, w: int, start_r: int):
    # Fill starting row
    r = start_r
    for ii, cc in enumerate(pat_cols):
        if 0 <= cc < w and result[r][cc] == 8:
            result[r][cc] = pat_colors[ii]
    # Propagate downward
    for r in range(start_r + 1, h):
        can_fill = all(0 <= pat_cols[ii] < w and (result[r][pat_cols[ii]] == 8 or result[r][pat_cols[ii]] == pat_colors[ii]) for ii in range(len(pat_cols)))
        if not can_fill:
            break
        for ii, cc in enumerate(pat_cols):
            if result[r][cc] == 8:
                result[r][cc] = pat_colors[ii]

def propagate_bottom_pattern(result: List[List[int]], pat_cols: List[int], pat_colors: List[int], h: int, w: int, start_r: int):
    # Fill starting row
    r = start_r
    for ii, cc in enumerate(pat_cols):
        if 0 <= cc < w and result[r][cc] == 8:
            result[r][cc] = pat_colors[ii]
    # Propagate upward
    for r in range(start_r - 1, -1, -1):
        can_fill = all(0 <= pat_cols[ii] < w and (result[r][pat_cols[ii]] == 8 or result[r][pat_cols[ii]] == pat_colors[ii]) for ii in range(len(pat_cols)))
        if not can_fill:
            break
        for ii, cc in enumerate(pat_cols):
            if result[r][cc] == 8:
                result[r][cc] = pat_colors[ii]

def extend_middle_horizontal(result: List[List[int]], r: int, c: int, color: int, h: int, w: int):
    # left
    j = c - 1
    while j >= 0 and result[r][j] == 8:
        result[r][j] = color
        j -= 1
    # right
    j = c + 1
    while j < w and result[r][j] == 8:
        result[r][j] = color
        j += 1

def process_stem_fills(result: List[List[int]], stems: List[Tuple[int, int, int, int]], s1: int, s2: int, s3: int, h: int, w: int, g: List[List[int]]):
    isolated_stems = [stem for stem in stems if is_isolated(stem, stems)]
    for sr, er, col, typ in isolated_stems:
        length = er - sr
        if typ == 1:
            offsets = [1, 3, 5]
            colors = [s1, s2, s3]
        else:  # typ == 2
            offsets = [0, 3, length - 2]
            colors = [s3, s2, s1]
        for idx, off in enumerate(offsets):
            r = sr + off
            if r >= h:
                continue
            # fill left
            j = col - 1
            while j >= 0 and result[r][j] == 8:
                result[r][j] = colors[idx]
                j -= 1
            # fill right
            j = col + 1
            while j < w and result[r][j] == 8:
                result[r][j] = colors[idx]
                j += 1
        # Special for type1 with left prefix
        if typ == 1:
            left_col = col - 1
            if left_col >= 0:
                p = 0
                color_left = None
                for rr in range(sr, min(er, h)):
                    val = g[rr][left_col]
                    if val == 8 or val == 1 or val == 2:
                        break
                    if color_left is None:
                        color_left = val
                    if val != color_left:
                        break
                    p += 1
                if p >= 2 and color_left is not None:
                    extra_off = 2
                    extra_r = sr + extra_off
                    if 0 <= extra_r < h:
                        # fill right with s1
                        j = col + 1
                        while j < w and result[extra_r][j] == 8:
                            result[extra_r][j] = s1
                            j += 1
                        # extend left
                        if result[extra_r][left_col] in (1, 2, 8):
                            result[extra_r][left_col] = color_left

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    result = [row[:] for row in g]
    counts = count_non_blanks(g)
    singletons = [c for c, cnt in counts.items() if cnt == 1]
    if len(singletons) != 3:
        return result
    s = sorted(singletons)
    s1, s2, s3 = s
    pos = find_singleton_positions(g, s)
    stems = find_stems(g, h, w)
    process_stem_fills(result, stems, s1, s2, s3, h, w, g)
    for k in [s1, s2, s3]:
        if k not in pos:
            continue
        r, c = pos[k]
        pat_cols, pat_colors = [], []
        if r == 0:
            pat_cols, pat_colors = get_pattern_cols_and_colors(k, c, s1, s2, s3, True)
            if len(pat_cols) == 3 and all(0 <= cc < w for cc in pat_cols):
                propagate_top_pattern(result, pat_cols, pat_colors, h, w, r)
        elif r == h - 1:
            pat_cols, pat_colors = get_pattern_cols_and_colors(k, c, s1, s2, s3, False)
            if len(pat_cols) == 3 and all(0 <= cc < w for cc in pat_cols):
                propagate_bottom_pattern(result, pat_cols, pat_colors, h, w, r)
        else:
            extend_middle_horizontal(result, r, c, k, h, w)
    return result
```