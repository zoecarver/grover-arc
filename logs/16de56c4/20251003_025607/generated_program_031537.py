```python
from typing import List
import copy
from math import gcd
from functools import reduce

def compute_gcd(diffs: List[int]) -> int:
    if not diffs:
        return 1
    return reduce(gcd, diffs)

def horizontal_completion(grid: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(grid)
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    for i in range(num_rows):
        row = grid[i]
        pos_color = [(j + 1, row[j]) for j in range(num_cols) if row[j] != 0]
        k = len(pos_color)
        if k < 2:
            continue
        poss = sorted(p for p, _ in pos_color)
        colors = [c for _, c in pos_color]
        all_same = all(c == colors[0] for c in colors)
        if all_same:
            diffs = [poss[m + 1] - poss[m] for m in range(k - 1)]
            d = compute_gcd(diffs)
            r = poss[0] % d
            c = colors[0]
            for jj in range(1, num_cols + 1):
                if jj % d == r:
                    row[jj - 1] = c
        else:
            diffs = [poss[m + 1] - poss[m] for m in range(k - 1)]
            d = compute_gcd(diffs)
            min_p = poss[0]
            max_p = poss[-1]
            color_max = next(c for p, c in pos_color if p == max_p)
            current = min_p
            while current <= max_p:
                row[current - 1] = color_max
                current += d
    return grid

def vertical_per_color_same(grid: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(grid)
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    for j in range(num_cols):
        col_pos_color = [(i + 1, grid[i][j]) for i in range(num_rows) if grid[i][j] != 0]
        k = len(col_pos_color)
        if k < 2:
            continue
        col_colors = set(c for _, c in col_pos_color)
        for cc in col_colors:
            group_pos = sorted(p for p, c in col_pos_color if c == cc)
            group_k = len(group_pos)
            if group_k < 2:
                continue
            group_diffs = [group_pos[m + 1] - group_pos[m] for m in range(group_k - 1)]
            group_d = compute_gcd(group_diffs)
            group_r = group_pos[0] % group_d
            for ii in range(1, num_rows + 1):
                if ii % group_d == group_r:
                    if grid[ii - 1][j] == 0 or grid[ii - 1][j] == cc:
                        grid[ii - 1][j] = cc
    return grid

def vertical_mixed_override(grid: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(grid)
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    for j in range(num_cols):
        pos_color = [(i + 1, grid[i][j]) for i in range(num_rows) if grid[i][j] != 0]
        k = len(pos_color)
        if k < 2:
            continue
        poss = sorted(p for p, _ in pos_color)
        colors = [c for _, c in pos_color]
        colors_set = set(colors)
        if len(colors_set) <= 1:
            continue
        diffs = [poss[m + 1] - poss[m] for m in range(k - 1)]
        d = compute_gcd(diffs)
        min_p = poss[0]
        max_p = poss[-1]
        num_exp = (max_p - min_p) // d + 1
        if num_exp == k:
            color_min = next(c for p, c in pos_color if p == min_p)
            current = min_p
            while current <= max_p:
                grid[current - 1][j] = color_min
                current += d
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    num_rows = len(g)
    num_cols = len(g[0]) if num_rows > 0 else 0
    if num_rows > num_cols:
        return horizontal_completion(g)
    else:
        temp = vertical_per_color_same(g)
        return vertical_mixed_override(temp)
```