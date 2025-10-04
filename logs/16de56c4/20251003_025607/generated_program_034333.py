```python
from typing import List
from math import gcd
from functools import reduce
import copy

def compute_gcd(diffs: List[int]) -> int:
    if not diffs:
        return 1
    return reduce(gcd, diffs)

def process_horizontal(line: List[int], length: int) -> List[int]:
    out = line[:]
    pos_color = [(i + 1, line[i]) for i in range(length) if line[i] != 0]
    k = len(pos_color)
    if k < 2:
        return out
    poss = [p for p, _ in pos_color]
    colors = [c for _, c in pos_color]
    all_same = all(c == colors[0] for c in colors)
    diffs = [poss[m + 1] - poss[m] for m in range(k - 1)]
    d = compute_gcd(diffs)
    if all_same:
        r = poss[0] % d
        c = colors[0]
        for p in range(1, length + 1):
            if p % d == r:
                out[p - 1] = c
    else:
        min_p = poss[0]
        max_p = poss[-1]
        c = next(c for p, c in pos_color if p == max_p)
        current = min_p
        while current <= max_p:
            out[current - 1] = c
            current += d
    return out

def per_color_extension(line: List[int], length: int) -> List[int]:
    out = line[:]
    pos_by_color = {}
    for i in range(length):
        c = line[i]
        if c != 0:
            if c not in pos_by_color:
                pos_by_color[c] = []
            pos_by_color[c].append(i + 1)
    for cc, group_poss in pos_by_color.items():
        group_k = len(group_poss)
        if group_k < 2:
            continue
        group_poss = sorted(group_poss)
        group_diffs = [group_poss[m + 1] - group_poss[m] for m in range(group_k - 1)]
        group_d = compute_gcd(group_diffs)
        group_r = group_poss[0] % group_d
        for p in range(1, length + 1):
            if p % group_d == group_r:
                if out[p - 1] == 0 or out[p - 1] == cc:
                    out[p - 1] = cc
    return out

def mixed_override_line(line: List[int], length: int) -> List[int]:
    out = line[:]
    pos_color = [(i + 1, line[i]) for i in range(length) if line[i] != 0]
    k = len(pos_color)
    if k < 2:
        return out
    poss = sorted(p for p, _ in pos_color)
    colors = [c for _, c in pos_color]
    colors_set = set(colors)
    if len(colors_set) <= 1:
        return out
    diffs = [poss[m + 1] - poss[m] for m in range(k - 1)]
    d = compute_gcd(diffs)
    min_p = poss[0]
    max_p = poss[-1]
    num_exp = (max_p - min_p) // d + 1
    if num_exp == k:
        c = next(c for p, c in pos_color if p == min_p)
        current = min_p
        while current <= max_p:
            out[current - 1] = c
            current += d
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    num_rows = len(g)
    num_cols = len(g[0])
    out_grid = [row[:] for row in g]
    if num_rows > num_cols:
        # Horizontal processing
        for i in range(num_rows):
            out_grid[i] = process_horizontal(g[i], num_cols)
    else:
        # Vertical processing: per-color first
        for j in range(num_cols):
            col = [out_grid[i][j] for i in range(num_rows)]
            processed = per_color_extension(col, num_rows)
            for i in range(num_rows):
                out_grid[i][j] = processed[i]
        # Then mixed override
        for j in range(num_cols):
            col = [out_grid[i][j] for i in range(num_rows)]
            processed = mixed_override_line(col, num_rows)
            for i in range(num_rows):
                out_grid[i][j] = processed[i]
    return out_grid
```