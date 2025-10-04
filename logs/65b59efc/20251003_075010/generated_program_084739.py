```python
from typing import List

def find_centers(bottom: List[int], n_cols: int) -> List[int]:
    centers = []
    i = 0
    while i < n_cols:
        if bottom[i] == 0:
            i += 1
            continue
        start = i
        while i < n_cols and bottom[i] != 0:
            i += 1
        avg = (start + i - 1) / 2
        centers.append(round(avg))
    return centers[:3]

def find_first_section_height(g: List[List[int]], n_cols: int) -> int:
    n_rows = len(g)
    seps = []
    for r in range(n_rows):
        num_fives = sum(1 for v in g[r] if v == 5)
        if num_fives > n_cols // 2:
            seps.append(r)
    return seps[0] if seps else n_rows

def extract_pattern(g: List[List[int]], center: int, w: int, first_h: int, n_cols: int, n_rows: int) -> List[List[int]]:
    pat = []
    win_start = max(0, center - w // 2)
    win_end = min(n_cols, center + w // 2 + 1)
    for r in range(min(first_h, n_rows)):
        row_slice = g[r][win_start:win_end]
        bin_row = [1 if cell not in (0, 5) else 0 for cell in row_slice]
        if len(bin_row) < w:
            bin_row += [0] * (w - len(bin_row))
        else:
            bin_row = bin_row[:w]
        pat.append(bin_row)
    while len(pat) < w:
        pat.append([0] * w)
    return pat

def is_block(pat: List[List[int]], w: int) -> bool:
    return all(sum(row) == w for row in pat)

def place_pattern(out: List[List[int]], r0: int, c0: int, pat: List[List[int]], colr: int, w: int):
    for rr in range(w):
        for cc in range(w):
            if pat[rr][cc] == 1:
                out[r0 + rr][c0 + cc] = colr

def program(g: List[List[int]]) -> List[List[int]]:
    n_rows = len(g)
    if n_rows == 0:
        return []
    n_cols = len(g[0])
    bottom = g[-1]
    centers = find_centers(bottom, n_cols)
    num_c = len(centers)
    if num_c == 0:
        return [[0]]
    if num_c == 1:
        w = 1
    else:
        diffs = [centers[k + 1] - centers[k] for k in range(num_c - 1)]
        w = min(diffs) - 1
    colors = [bottom[centers[k]] if k < num_c else 0 for k in range(3)]
    first_h = find_first_section_height(g, n_cols)
    pats = []
    for k in range(3):
        cen = centers[k] if k < num_c else centers[-1] + (centers[-1] - centers[-2] if num_c >= 2 else 0)
        pat = extract_pattern(g, cen, w, first_h, n_cols, n_rows)
        pats.append(pat)
    if is_block(pats[0], w):
        mode = 'block'
        A_pat, A_col = pats[1], colors[1]
        B_pat, B_col = pats[2], colors[2]
        C_pat, C_col = pats[0], colors[0]
        simple = False
    else:
        mode = 'pointy'
        A_pat, A_col = pats[2], colors[2]
        B_pat, B_col = pats[1], colors[1]
        C_pat, C_col = pats[0], colors[0]
        top_row = pats[0][0]
        simple = (w > 0 and top_row[0] == 0 and top_row[w - 1] == 0)
    s = w * w
    out = [[0] * s for _ in range(s)]
    if mode == 'block' or not simple:
        for i in range(w):
            r0 = i * w
            c0 = i * w
            place_pattern(out, r0, c0, A_pat, A_col, w)
            for j in range(i + 1, w):
                c0 = j * w
                place_pattern(out, r0, c0, B_pat, B_col, w)
        r0 = (w - 1) * w
        c0 = 0
        place_pattern(out, r0, c0, C_pat, C_col, w)
    else:
        right_pat, right_col = pats[0], colors[0]
        bottom_pat, bottom_col = pats[1], colors[1]
        for i in range(w - 1):
            r0 = i * w
            place_pattern(out, r0, 0, A_pat, A_col, w)
            c0 = (w - 1) * w
            place_pattern(out, r0, c0, right_pat, right_col, w)
        r0 = (w - 1) * w
        for j in range(w - 1):
            c0 = j * w
            place_pattern(out, r0, c0, bottom_pat, bottom_col, w)
    if mode == 'pointy' and not simple:
        half = w // 2
        for i in range(half):
            r0 = i * w
            place_pattern(out, r0, 0, A_pat, A_col, w)
            num_b = (w - 1) - 2 * i
            c = w
            for _ in range(num_b):
                place_pattern(out, r0, c, B_pat, B_col, w)
                c += w
        for i in range(half, w):
            r0 = i * w
            if i == half:
                num_c = 0
                num_a = half
                a_start = 0
            else:
                num_c = i - half
                num_a = w - i
                a_start = num_c * w
            c = 0
            for _ in range(num_c):
                place_pattern(out, r0, c, C_pat, C_col, w)
                c += w
            c = a_start
            for _ in range(num_a):
                place_pattern(out, r0, c, A_pat, A_col, w)
                c += w
    return out
```