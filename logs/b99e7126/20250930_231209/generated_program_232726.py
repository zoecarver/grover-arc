```python
from typing import List
from collections import defaultdict

def majority(lst: List[int]) -> int:
    if not lst:
        return 0
    counts = defaultdict(int)
    for item in lst:
        counts[item] += 1
    return max(counts, key=counts.get)

def compute_background(g: List[List[int]]) -> List[List[int]]:
    n = 29
    b = [[0] * n for _ in range(n)]
    bg = g[0][0]
    for r in range(n):
        if r % 4 == 0:
            for c in range(n):
                b[r][c] = bg
        else:
            ps = [0] * 3
            for off in range(3):
                poss = list(range(off + 1, n, 4))
                cols = [g[r][c] for c in poss]
                ps[off] = majority(cols)
            pat = [bg] + ps
            for j in range(7):
                for kk in range(4):
                    c = 4 * j + kk
                    b[r][c] = pat[kk]
    return b

def find_new_color(g: List[List[int]], b: List[List[int]]) -> int:
    n = 29
    anomaly_set = set()
    for r in range(n):
        for c in range(n):
            if g[r][c] != b[r][c]:
                anomaly_set.add(g[r][c])
    bg_set = set()
    for r in range(n):
        for c in range(n):
            bg_set.add(b[r][c])
    diff = anomaly_set - bg_set
    if not diff:
        return None
    return next(iter(diff))

def extract_template(g: List[List[int]], block_i: int, stripe_s: int) -> List[List[int]]:
    n = 29
    r0 = 4 * block_i + 1
    temp = [[0] * 3 for _ in range(3)]
    for rr in range(3):
        r = r0 + rr
        for cc in range(3):
            c = 4 * stripe_s + 1 + cc
            temp[rr][cc] = g[r][c]
    return temp

def overlay(grid: List[List[int]], block_i: int, stripe_s: int, template: List[List[int]]) -> None:
    r0 = 4 * block_i + 1
    for rr in range(3):
        r = r0 + rr
        for cc in range(3):
            c = 4 * stripe_s + 1 + cc
            grid[r][c] = template[rr][cc]

def get_block_filled_stripes(g: List[List[int]], new_c: int, block_i: int) -> List[int]:
    if new_c is None:
        return []
    r0 = 4 * block_i + 1
    filled_ss = []
    for ss in range(7):
        has = False
        for rr in range(3):
            r = r0 + rr
            for cc in range(3):
                c = 4 * ss + 1 + cc
                if g[r][c] == new_c:
                    has = True
                    break
            if has:
                break
        if has:
            filled_ss.append(ss)
    return filled_ss

def count_new(temp: List[List[int]], new_c: int) -> int:
    return sum(1 for row in temp for c in row if c == new_c)

def program(g: List[List[int]]) -> List[List[int]]:
    n = 29
    b = compute_background(g)
    new_c = find_new_color(g, b)
    if new_c is None:
        return [row[:] for row in g]
    g_out = [row[:] for row in g]
    best_k = 0
    max_filled = -1
    for i in range(7):
        filled = get_block_filled_stripes(g, new_c, i)
        len_f = len(filled)
        if len_f > max_filled or (len_f == max_filled and i > best_k):
            max_filled = len_f
            best_k = i
    if max_filled == 0:
        return g_out
    filled_ss = get_block_filled_stripes(g, new_c, best_k)
    original_len = len(filled_ss)
    min_s = min(filled_ss)
    max_s = max(filled_ss)
    def key_ss(ss):
        temp = extract_template(g, best_k, ss)
        return (count_new(temp, new_c), ss)
    best_ss = max(filled_ss, key=key_ss)
    raw_temp = extract_template(g, best_k, best_ss)
    cnt = count_new(raw_temp, new_c)
    is_middle = raw_temp[0][1] == new_c
    type_ = 'middle' if is_middle else 'side'
    r0 = 4 * best_k + 1
    bg_row0 = b[r0][4 * best_ss + 1:4 * best_ss + 4]
    bg_row1 = b[r0 + 1][4 * best_ss + 1:4 * best_ss + 4]
    bg_row2 = b[r0 + 2][4 * best_ss + 1:4 * best_ss + 4]
    temp = [[0] * 3 for _ in range(3)]
    if type_ == 'middle':
        temp[0][0] = bg_row0[0]
        temp[0][1] = new_c
        temp[0][2] = bg_row0[2]
        temp[1][0] = new_c
        temp[1][1] = new_c
        temp[1][2] = new_c
        temp[2][0] = new_c
        temp[2][2] = new_c
        if bg_row2[0] == bg_row2[1] == bg_row2[2]:
            temp[2][1] = new_c
        else:
            temp[2][1] = bg_row0[0]
    else:
        for rr in range(3):
            for cc in range(3):
                temp[rr][cc] = raw_temp[rr][cc]
    expand = original_len < 3
    if expand:
        center = best_ss
        min_s = max(0, center - 1)
        max_s = min(6, center + 1)
        effective_ss = list(range(min_s, max_s + 1))
    else:
        if type_ == 'side' and original_len % 2 == 0:
            effective_ss = list(range(min_s, max_s + 1, 2))
        else:
            effective_ss = list(range(min_s, max_s + 1))
    for ss in effective_ss:
        overlay(g_out, best_k, ss, temp)
    if type_ == 'side':
        if original_len % 2 == 0:
            prop_stripes = effective_ss
            for di in [-1, 1]:
                ni = best_k + di
                if 0 <= ni < 7:
                    for ss in prop_stripes:
                        overlay(g_out, ni, ss, temp)
        else:
            left = min_s - 1
            right = max_s
            if left >= 0:
                num_levels = min_s
                for level in range(1, num_levels + 1):
                    ni = best_k - level
                    if 0 <= ni < 7:
                        prop_stripes = [s for s in [left, right] if 0 <= s < 7]
                        for ss in prop_stripes:
                            overlay(g_out, ni, ss, temp)
    else:
        min_s_eff = min(effective_ss)
        max_s_eff = max(effective_ss)
        middle_s = (min_s_eff + max_s_eff) // 2
        uniform_row2 = bg_row2[0] == bg_row2[1] == bg_row2[2]
        if expand and uniform_row2:
            for di in [1, 2]:
                ni = best_k + di
                if 0 <= ni < 7:
                    for ss in effective_ss:
                        overlay(g_out, ni, ss, temp)
        else:
            ni = best_k - 1
            if 0 <= ni < 7:
                overlay(g_out, ni, middle_s, temp)
            sides = [min_s_eff, max_s_eff]
            ni = best_k + 1
            if 0 <= ni < 7:
                for ss in sides:
                    overlay(g_out, ni, ss, temp)
    return g_out
```