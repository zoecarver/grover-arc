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
    pos_dict = {}
    for i in range(h):
        for j in range(w):
            cc = g[i][j]
            if cc in singletons:
                pos_dict[cc] = (i, j)
    return pos_dict

def get_pat_cols(k: int, c: int, s1: int, s2: int, s3: int, is_top: bool) -> Tuple[List[int], List[int]]:
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
    else:
        pat_colors = [s1, s2, s3]
        if k == s1:
            pat_cols = [c, c + 1, c + 4]
        elif k == s2:
            pat_cols = [c - 1, c, c + 3]
        elif k == s3:
            pat_cols = [c - 4, c - 3, c]
        else:
            return [], []
    if any(pc < 0 or pc >= len(g[0]) for pc in pat_cols if len(g) > 0):
        return [], []
    return pat_cols, pat_colors

def process_top_patterns(result: List[List[int]], pos: Dict[int, Tuple[int, int]], s1: int, s2: int, s3: int, h: int, w: int):
    for k in [s1, s2, s3]:
        if k in pos and pos[k][0] == 0:
            c = pos[k][1]
            pat_cols, pat_colors = get_pat_cols(k, c, s1, s2, s3, True)
            if not pat_cols:
                continue
            r = 0
            for jj in range(3):
                pc = pat_cols[jj]
                if result[r][pc] == 8:
                    result[r][pc] = pat_colors[jj]
            for r in range(1, h):
                can = all(result[r][pat_cols[jj]] == 8 or result[r][pat_cols[jj]] == pat_colors[jj] for jj in range(3))
                if not can:
                    break
                for jj in range(3):
                    pc = pat_cols[jj]
                    if result[r][pc] == 8:
                        result[r][pc] = pat_colors[jj]

def process_bottom_patterns(result: List[List[int]], pos: Dict[int, Tuple[int, int]], s1: int, s2: int, s3: int, h: int, w: int):
    for k in [s1, s2, s3]:
        if k in pos and pos[k][0] == h - 1:
            c = pos[k][1]
            pat_cols, pat_colors = get_pat_cols(k, c, s1, s2, s3, False)
            if not pat_cols:
                continue
            for r in range(h - 2, -1, -1):
                can = all(result[r][pat_cols[jj]] == 8 for jj in range(3))
                if not can:
                    break
                for jj in range(3):
                    pc = pat_cols[jj]
                    result[r][pc] = pat_colors[jj]

def process_middle(result: List[List[int]], pos: Dict[int, Tuple[int, int]], h: int, w: int):
    for k in pos:
        r, c = pos[k]
        if 0 < r < h - 1:
            j = c - 1
            while j >= 0 and result[r][j] == 8:
                result[r][j] = k
                j -= 1
            j = c + 1
            while j < w and result[r][j] == 8:
                result[r][j] = k
                j += 1

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

def process_stems(result: List[List[int]], s1: int, s2: int, s3: int, h: int, w: int):
    stems = find_stems(result, h, w)
    for stem in stems:
        sr, er, c, typ = stem
        length = er - sr
        adjacent_col = None
        for o_sr, o_er, o_c, o_typ in stems:
            if o_typ == 3 - typ and o_c in (c - 1, c + 1) and max(sr, o_sr) < min(er, o_er):
                adjacent_col = o_c
                break
        if adjacent_col is not None:
            direction = 'right' if adjacent_col < c else 'left'
            offsets = [0, 2, 4] if typ == 1 and direction == 'right' else [1, 3, 5] if typ == 1 else [0, 3, length - 2]
            colors = [s1, s2, s3] if typ == 1 else [s3, s2, s1]
            fill_dir = direction
        else:
            offsets = [1, 3, 5] if typ == 1 else [0, 3, length - 2]
            colors = [s1, s2, s3] if typ == 1 else [s3, s2, s1]
            fill_dir = None  # isolated
        for off_idx, off in enumerate(offsets):
            row = sr + off
            if row >= h:
                continue
            colr = colors[off_idx]
            # compute right_len
            right_len = 0
            j = c + 1
            while j < w and result[row][j] == 8:
                right_len += 1
                j += 1
            # left_len
            left_len = 0
            j = c - 1
            while j >= 0 and result[row][j] == 8:
                left_len += 1
                j -= 1
            if adjacent_col is not None:
                if fill_dir == 'right':
                    jj = c + 1
                    for _ in range(right_len):
                        result[row][jj] = colr
                        jj += 1
                else:
                    jj = c - 1
                    for _ in range(left_len):
                        result[row][jj] = colr
                        jj -= 1
            else:
                if right_len > 0:
                    jj = c + 1
                    for _ in range(right_len):
                        result[row][jj] = colr
                        jj += 1
                elif left_len > 0:
                    jj = c - 1
                    for _ in range(left_len):
                        result[row][jj] = colr
                        jj -= 1

def process_cap_extensions(result: List[List[int]], stems: List[Tuple[int, int, int, int]], h: int, w: int):
    for sr, er, c, typ in stems:
        if typ == 2 and sr > 0 and result[sr - 1][c] != 8:
            color_above = result[sr - 1][c]
            left_j = c - 1
            if left_j >= 0 and result[sr][left_j] == 8 and result[sr - 1][left_j] == color_above:
                result[sr][left_j] = color_above

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    counts = count_non_blanks(g)
    singletons = [c for c in counts if counts[c] == 1]
    if len(singletons) != 3:
        return [row[:] for row in g]
    s1, s2, s3 = sorted(singletons)
    pos = find_singleton_positions(g, [s1, s2, s3])
    result = [row[:] for row in g]
    h = len(result)
    w = len(result[0])
    process_top_patterns(result, pos, s1, s2, s3, h, w)
    process_bottom_patterns(result, pos, s1, s2, s3, h, w)
    process_middle(result, pos, h, w)
    process_stems(result, s1, s2, s3, h, w)
    stems = find_stems(result, h, w)
    process_cap_extensions(result, stems, h, w)
    return result
```