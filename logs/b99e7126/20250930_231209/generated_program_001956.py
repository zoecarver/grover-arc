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
            b[r][28] = bg
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

def compute_template(g: List[List[int]], b: List[List[int]], block_i: int, filled_ss: List[int], new_c: int) -> List[List[int]]:
    r0 = 4 * block_i + 1
    temp = [[0] * 3 for _ in range(3)]
    for rr in range(3):
        r = r0 + rr
        for cc in range(3):
            vals = [g[r][4 * s + 1 + cc] for s in filled_ss]
            b_val = b[r][1 + cc]
            non_bg_vals = [v for v in vals if v != b_val]
            if non_bg_vals:
                temp[rr][cc] = majority(non_bg_vals)
            else:
                temp[rr][cc] = b_val
    return temp

def overlay_conditional(grid: List[List[int]], block_i: int, stripe_s: int, template: List[List[int]], b: List[List[int]]) -> None:
    r0 = 4 * block_i + 1
    for rr in range(3):
        r = r0 + rr
        for cc in range(3):
            c = 4 * stripe_s + 1 + cc
            if grid[r][c] == b[r][c]:
                grid[r][c] = template[rr][cc]

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    b = compute_background(out)
    new_c = find_new_color(out, b)
    if new_c is None:
        return out
    for block_i in range(6, -1, -1):
        filled_ss = get_block_filled_stripes(out, new_c, block_i)
        if not filled_ss:
            continue
        filled_ss = sorted(set(filled_ss))
        min_s = min(filled_ss)
        max_s = max(filled_ss)
        temp = compute_template(out, b, block_i, filled_ss, new_c)
        for s in range(min_s, max_s + 1):
            overlay_conditional(out, block_i, s, temp, b)
        is_cross = (temp[0][1] == new_c)
        is_bottom_full = all(temp[2][cc] == new_c for cc in range(3))
        if is_cross:
            center = (min_s + max_s) // 2
            if block_i > 0:
                overlay_conditional(out, block_i - 1, center, temp, b)
            if block_i < 6:
                for s in [min_s, max_s]:
                    overlay_conditional(out, block_i + 1, s, temp, b)
        else:
            num_up = 1 if not is_bottom_full else (min_s if min_s > 1 else 0)
            for di in range(1, num_up + 1):
                nk = block_i - di
                if nk < 0:
                    break
                left_s = max(1, min_s - di)
                right_s = max_s
                overlay_conditional(out, nk, left_s, temp, b)
                if left_s != right_s:
                    overlay_conditional(out, nk, right_s, temp, b)
            if not is_bottom_full and block_i < 6:
                for s in [min_s, max_s]:
                    overlay_conditional(out, block_i + 1, s, temp, b)
    return out
```