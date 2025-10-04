```python
from collections import Counter
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_key_cols(g: List[List[int]], B: int, n: int) -> List[int]:
    key_cols = []
    for c in range(1, min(10, n), 2):
        if any(g[r][c] != B for r in range(min(8, n))):
            key_cols.append(c)
    return key_cols

def get_key_rows(g: List[List[int]], B: int, key_cols: List[int]) -> List[int]:
    rows = set()
    for r in range(min(8, len(g))):
        if any(g[r][c] != B for c in key_cols):
            rows.add(r)
    return sorted(rows)

def get_key_colors(g: List[List[int]], key_rows: List[int], key_cols: List[int], B: int) -> List[List[int]]:
    m = len(key_rows)
    k = len(key_cols)
    kc = [[B] * k for _ in range(m)]
    for i in range(m):
        r = key_rows[i]
        for j in range(k):
            kc[i][j] = g[r][key_cols[j]]
    return kc

def get_scale(g: List[List[int]], B: int, n: int) -> int:
    max_s = 1
    for row in g:
        i = 0
        while i < n:
            if row[i] == B:
                i += 1
                continue
            start_color = row[i]
            j = i + 1
            while j < n and row[j] == start_color:
                j += 1
            length = j - i
            if length > max_s:
                max_s = length
            i = j
    return max_s

def get_main_start_cols(g: List[List[int]], B: int, s: int, n: int) -> List[int]:
    starts = set()
    for r in range(n):
        i = 0
        while i <= n - s:
            if all(g[r][c] == g[r][i] != B for c in range(i, i + s)):
                starts.add(i)
            j = i
            while j < n and g[r][j] == g[r][i]:
                j += 1
            i = j
    return sorted(list(starts))

def get_block_info(g: List[List[int]], B: int, s: int, start_c: int, n: int) -> Tuple[int, int, int]:
    present_rows = []
    for r in range(n):
        if all(g[r][c] == g[r][start_c] != B for c in range(start_c, start_c + s)):
            present_rows.append(r)
    if not present_rows:
        return None
    min_r = min(present_rows)
    max_r = max(present_rows)
    color = g[min_r][start_c]
    for r in range(min_r, max_r + 1):
        if not all(g[r][c] == color for c in range(start_c, start_c + s)):
            return None
    h = max_r - min_r + 1
    return (min_r, h, color)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    B = get_background(g)
    key_cols = get_key_cols(g, B, n)
    k = len(key_cols)
    key_rows = get_key_rows(g, B, key_cols)
    m = len(key_rows)
    key_colors = get_key_colors(g, key_rows, key_cols, B)
    s = get_scale(g, B, n)
    starts = get_main_start_cols(g, B, s, n)
    if len(starts) < 1:
        return out
    if len(starts) >= 2:
        diff = starts[1] - starts[0]
        empty = diff - s
    else:
        empty = 1  # default
    logo_start = starts[0]
    # determine i_filled
    possible_is = set()
    for ej in range(len(starts)):
        sc = starts[ej]
        info = get_block_info(g, B, s, sc, n)
        if info is None:
            continue
        _, _, color = info
        for ii in range(m):
            if key_colors[ii][ej] == color:
                possible_is.add(ii)
    if possible_is:
        i_filled = max(possible_is)
    else:
        i_filled = 0
    # get h and r_start_filled
    info = get_block_info(g, B, s, starts[0], n)
    if info is not None:
        h = info[1]
        r_start_filled = info[0]
    else:
        h = s
        r_start_filled = n // 2
    spacing = s + empty
    r_starts = [r_start_filled + (ii - i_filled) * spacing for ii in range(m)]
    # block starts
    block_starts = []
    for jj in range(k):
        bs = logo_start + jj * (s + empty)
        if bs + s <= n:
            block_starts.append(bs)
        else:
            block_starts.append(-1)
    # protection
    protect = (s == 2 and B == 8)
    protect_top = 8
    protect_bottom_start = n - 9 if protect else n
    for jj in range(k):
        bs = block_starts[jj]
        if bs == -1:
            continue
        for ii in range(m):
            colr = key_colors[ii][jj]
            if colr == B:
                continue
            sr = r_starts[ii]
            if sr < 0 or sr + h > n:
                continue
            for rr in range(sr, sr + h):
                if protect and (rr < protect_top or rr >= protect_bottom_start):
                    continue
                for cc in range(bs, bs + s):
                    if out[rr][cc] == B:
                        out[rr][cc] = colr
    return out
```