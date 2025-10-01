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

def is_uniform_even1(g: List[List[int]]) -> bool:
    r = 1
    offs = [1, 2, 3]
    ps = []
    for off in offs:
        poss = list(range(off, 29, 4))
        cols = [g[r][c] for c in poss]
        p = majority(cols)
        ps.append(p)
    return ps[0] == ps[1] == ps[2]

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    b = compute_background(g)
    new_c = find_new_color(g, b)
    if new_c is None:
        return out
    filled = [get_block_filled_stripes(g, new_c, i) for i in range(7)]
    max_len = max((len(fs) for fs in filled), default=0)
    if max_len == 0:
        return out
    k = max(range(7), key=lambda i: (len(filled[i]), -i))  # max len, then largest i if tie
    S = filled[k]
    if not S:
        return out
    min_s = min(S)
    max_s = max(S)
    ss_temp = S[0]
    template = extract_template(g, k, ss_temp)
    # fill crossbar gaps
    for ss in range(min_s, max_s + 1):
        if 0 <= ss <= 6:
            overlay(out, k, ss, template)
    # determine type
    uniform = is_uniform_even1(g)
    leftish = min_s <= 1
    if uniform:
        if leftish:
            L = 1
            R = 3
            added_ss = [L, R]
            added_blocks = []
            if k - 1 >= 0:
                added_blocks.append(k - 1)
            if k + 1 <= 6:
                added_blocks.append(k + 1)
        else:
            L = min_s - 1
            R = max_s - 1
            added_ss = [L, R]
            added_blocks = []
            if k - 1 >= 0:
                added_blocks.append(k - 1)
            if k - 2 >= 0:
                added_blocks.append(k - 2)
        for ib in added_blocks:
            for ss in added_ss:
                if 0 <= ss <= 6:
                    overlay(out, ib, ss, template)
    else:
        # alternating, assume leftish as in training
        added_blocks_upper = [k - 1] if k - 1 >= 0 else []
        added_blocks_lower = [k + 1] if k + 1 <= 6 else []
        for ib in added_blocks_upper:
            ss = 2
            if 0 <= ss <= 6:
                overlay(out, ib, ss, template)
        for ib in added_blocks_lower:
            for ss in [1, 3]:
                if 0 <= ss <= 6:
                    overlay(out, ib, ss, template)
    return out
```