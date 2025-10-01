```python
from typing import List
from collections import defaultdict
import copy

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
    return sum(1 for row in temp for x in row if x == new_c)

def program(g: List[List[int]]) -> List[List[int]]:
    b = compute_background(g)
    new_c = find_new_color(g, b)
    if new_c is None:
        return g
    best_len = 0
    best_k = -1
    for k in range(7):
        filled = get_block_filled_stripes(g, new_c, k)
        length = len(filled)
        if length > best_len or (length == best_len and k > best_k):
            best_len = length
            best_k = k
    if best_len == 0:
        return g
    filled_ss = get_block_filled_stripes(g, new_c, best_k)
    min_s = min(filled_ss)
    max_s = max(filled_ss)
    best_count = -1
    best_ss = -1
    for ss in filled_ss:
        temp = extract_template(g, best_k, ss)
        cnt = count_new(temp, new_c)
        if cnt > best_count or (cnt == best_count and ss > best_ss):
            best_count = cnt
            best_ss = ss
    temp = extract_template(g, best_k, best_ss)
    out = [row[:] for row in g]
    for ss in range(min_s, max_s + 1):
        overlay(out, best_k, ss, temp)
    is_cross = (temp[0][1] == new_c)
    if is_cross:
        center = (min_s + max_s) // 2
        if best_k > 0:
            overlay(out, best_k - 1, center, temp)
        if best_k < 6:
            overlay(out, best_k + 1, min_s, temp)
            overlay(out, best_k + 1, max_s, temp)
    else:
        for step in range(1, min_s + 1):
            nk = best_k - step
            if nk < 0:
                break
            overlay(out, nk, 1, temp)
        if min_s <= 1 and best_k < 6:
            overlay(out, best_k + 1, 1, temp)
    return out
```