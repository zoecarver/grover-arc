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
    return sum(1 for row in temp for x in row if x == new_c)

def program(g: List[List[int]]) -> List[List[int]]:
    n = 29
    grid = [[g[r][c] for c in range(n)] for r in range(n)]
    b = compute_background(g)
    new_c = find_new_color(g, b)
    if new_c is None:
        return grid
    best_len = 0
    best_k = -1
    best_filled_ss = []
    for k in range(7):
        fs = get_block_filled_stripes(g, new_c, k)
        l = len(fs)
        if l > best_len or (l == best_len and k > best_k):
            best_len = l
            best_k = k
            best_filled_ss = fs
    if best_len == 0:
        return grid
    filled_ss = sorted(best_filled_ss)
    min_s = min(filled_ss)
    max_s = max(filled_ss)
    best_count = -1
    best_s = -1
    best_template = [[0] * 3 for _ in range(3)]
    for s in filled_ss:
        temp = extract_template(g, best_k, s)
        cnt = count_new(temp, new_c)
        if cnt > best_count or (cnt == best_count and s > best_s):
            best_count = cnt
            best_s = s
            best_template = temp
    is_bottom = all(best_template[2][cc] == new_c for cc in range(3))
    is_top_center = best_template[0][1] == new_c
    original_min_s = min_s
    new_min = min_s
    new_max = max_s
    if is_bottom:
        if min_s > 1:
            new_min = min_s - 1
        num_upper = original_min_s
        num_down = 0
        prop_up_stripes = [new_min, new_max]
        prop_down_stripes = []
    else:
        if not is_top_center:
            if max_s < 6:
                new_max = max_s + 1
        num_upper = 1
        num_down = 1
        center_s = (min_s + max_s) // 2
        if is_top_center:
            prop_up_stripes = [center_s]
            prop_down_stripes = [1, 3]
        else:
            prop_up_stripes = [1, 3]
            prop_down_stripes = [1, 3]
    for s in range(new_min, new_max + 1):
        if 0 <= s <= 6:
            overlay(grid, best_k, s, best_template)
    for di in range(1, num_upper + 1):
        nk = best_k - di
        if nk < 0:
            break
        for ps in prop_up_stripes:
            if 0 <= ps <= 6:
                overlay(grid, nk, ps, best_template)
    for di in range(1, num_down + 1):
        nk = best_k + di
        if nk > 6:
            break
        for ps in prop_down_stripes:
            if 0 <= ps <= 6:
                overlay(grid, nk, ps, best_template)
    return grid
```