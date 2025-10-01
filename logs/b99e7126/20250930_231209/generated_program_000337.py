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

def extract_template(g: List[List[int]], block_i: int, stripe_s: int) -> List[List[int]]:
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
    return sum(1 for row in temp for x in row if x == new_c)

def program(g: List[List[int]]) -> List[List[int]]:
    b = compute_background(g)
    new_c = find_new_color(g, b)
    if new_c is None:
        return [row[:] for row in g]

    def get_filled(k: int) -> List[int]:
        return get_block_filled_stripes(g, new_c, k)

    best_k = max(range(7), key=lambda k: (len(get_filled(k)), k))
    filled_ss = get_filled(best_k)
    if not filled_ss:
        return [row[:] for row in g]

    def cnt(s: int) -> int:
        return count_new(extract_template(g, best_k, s), new_c)

    best_s = max(filled_ss, key=lambda s: (cnt(s), -s))
    temp = extract_template(g, best_k, best_s)

    out = [row[:] for row in g]
    min_s_val = min(filled_ss)
    max_s_val = max(filled_ss)
    for s in range(min_s_val, max_s_val + 1):
        if 0 <= s <= 6:
            overlay(out, best_k, s, temp)

    is_bottom = all(temp[2][cc] == new_c for cc in range(3))
    if is_bottom:
        left = max(1, min_s_val - 1)
        right = max_s_val
        num_up = min_s_val
        for di in range(1, num_up + 1):
            nk = best_k - di
            if nk < 0:
                break
            for ts in {left, right}:
                if 0 <= ts <= 6:
                    overlay(out, nk, ts, temp)
    else:
        # up
        nk_up = best_k - 1
        if nk_up >= 0:
            ts_up = min_s_val
            if 0 <= ts_up <= 6:
                overlay(out, nk_up, ts_up, temp)
        # down
        nk_down = best_k + 1
        if nk_down <= 6:
            for ts_down in {min_s_val, max_s_val}:
                if 0 <= ts_down <= 6:
                    overlay(out, nk_down, ts_down, temp)

    return out
```