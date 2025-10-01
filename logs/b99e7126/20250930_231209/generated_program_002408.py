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
    out = [row[:] for row in g]
    b = compute_background(g)
    new_c = find_new_color(g, b)
    if new_c is None:
        return out
    best_k = -1
    best_len = -1
    for k in range(7):
        fs = get_block_filled_stripes(g, new_c, k)
        l = len(fs)
        if l > best_len or (l == best_len and k > best_k):
            best_len = l
            best_k = k
    if best_len == 0:
        return out
    filled_ss = sorted(get_block_filled_stripes(g, new_c, best_k))
    min_s = filled_ss[0]
    max_s = filled_ss[-1]
    best_cnt = -1
    best_s = -1
    for s in filled_ss:
        temp_check = extract_template(g, best_k, s)
        cnt = count_new(temp_check, new_c)
        if cnt > best_cnt or (cnt == best_cnt and s > best_s):
            best_cnt = cnt
            best_s = s
    temp = extract_template(g, best_k, best_s)
    for s in range(min_s, max_s + 1):
        overlay(out, best_k, s, temp)
    is_bottom = all(temp[2][cc] == new_c for cc in range(3))
    is_cross = (temp[0][1] == new_c)
    if is_bottom:
        num_up = min_s
        for di in range(1, num_up + 1):
            nk = best_k - di
            if nk >= 0:
                for ss in [min_s, max_s]:
                    overlay(out, nk, ss, temp)
    elif is_cross:
        nk = best_k - 1
        if nk >= 0:
            center = (min_s + max_s) // 2
            overlay(out, nk, center, temp)
        nk = best_k + 1
        if nk < 7:
            for ss in [min_s, max_s]:
                overlay(out, nk, ss, temp)
    else:
        for direction in [-1, 1]:
            nk = best_k + direction
            if 0 <= nk < 7:
                for ss in [min_s, max_s]:
                    overlay(out, nk, ss, temp)
    return out
```