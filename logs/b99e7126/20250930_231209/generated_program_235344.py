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

def count_new(temp: List[List[int]], new_c: int) -> int:
    return sum(1 for row in temp for x in row if x == new_c)

def find_best_block(g: List[List[int]], new_c: int) -> int:
    totals = [sum(count_new(extract_template(g, k, s), new_c) for s in range(7)) for k in range(7)]
    return max(range(7), key=lambda k: (totals[k], k))

def get_filled_stripes(g: List[List[int]], new_c: int, block_i: int) -> List[int]:
    return [s for s in range(7) if count_new(extract_template(g, block_i, s), new_c) > 0]

def select_best_stripe_and_template(g: List[List[int]], new_c: int, block_i: int, filled_ss: List[int]) -> tuple:
    best_s = max(filled_ss, key=lambda s: (count_new(extract_template(g, block_i, s), new_c), s))
    return best_s, extract_template(g, block_i, best_s)

def get_min_max_filled(filled_ss: List[int]) -> tuple:
    if not filled_ss:
        return 0, 0
    return min(filled_ss), max(filled_ss)

def is_bottom_full(temp: List[List[int]], new_c: int) -> bool:
    return all(temp[2][cc] == new_c for cc in range(3))

def is_top_center_new(temp: List[List[int]], new_c: int) -> bool:
    return temp[0][1] == new_c

def fill_range_in_block(grid: List[List[int]], block_i: int, min_s: int, max_s: int, template: List[List[int]]) -> None:
    for s in range(min_s, max_s + 1):
        overlay(grid, block_i, s, template)

def propagate_upward(grid: List[List[int]], best_k: int, min_s: int, max_s: int, template: List[List[int]], is_top_center_flag: bool) -> None:
    num_up = min_s
    for di in range(1, num_up + 1):
        nk = best_k - di
        if nk < 0:
            continue
        if is_top_center_flag:
            center_s = (min_s + max_s) // 2
            if 0 <= center_s <= 6:
                overlay(grid, nk, center_s, template)
        else:
            shift = 1 if min_s > 1 else 0
            left_s = min_s - shift
            right_s = max_s
            if 0 <= left_s <= 6:
                overlay(grid, nk, left_s, template)
            if 0 <= right_s <= 6 and right_s != left_s:
                overlay(grid, nk, right_s, template)

def propagate_downward(grid: List[List[int]], best_k: int, min_s: int, max_s: int, template: List[List[int]], is_top_center_flag: bool, is_bottom_full_flag: bool) -> None:
    if is_bottom_full_flag or best_k >= 6:
        return
    nk = best_k + 1
    if nk > 6:
        return
    if is_top_center_flag:
        left_s = min_s
        right_s = max_s + 1 if max_s < 6 else max_s
        if 0 <= left_s <= 6:
            overlay(grid, nk, left_s, template)
        if 0 <= right_s <= 6 and right_s != left_s:
            overlay(grid, nk, right_s, template)
    else:
        left_s = min_s
        right_s = max_s
        if 0 <= left_s <= 6:
            overlay(grid, nk, left_s, template)
        if 0 <= right_s <= 6 and right_s != left_s:
            overlay(grid, nk, right_s, template)

def program(g: List[List[int]]) -> List[List[int]]:
    b = compute_background(g)
    new_c = find_new_color(g, b)
    if new_c is None:
        return [row[:] for row in g]
    out = [row[:] for row in g]
    best_k = find_best_block(g, new_c)
    filled_ss = get_filled_stripes(g, new_c, best_k)
    if not filled_ss:
        return out
    min_s, max_s = get_min_max_filled(filled_ss)
    _, temp = select_best_stripe_and_template(g, new_c, best_k, filled_ss)
    fill_range_in_block(out, best_k, min_s, max_s, temp)
    is_bottom_full_flag = is_bottom_full(temp, new_c)
    is_top_center_flag = is_top_center_new(temp, new_c)
    propagate_upward(out, best_k, min_s, max_s, temp, is_top_center_flag)
    propagate_downward(out, best_k, min_s, max_s, temp, is_top_center_flag, is_bottom_full_flag)
    return out
```