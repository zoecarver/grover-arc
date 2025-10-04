```python
from typing import List
import copy
from math import gcd
from functools import reduce

def compute_gcd(diffs: List[int]) -> int:
    if not diffs:
        return 1
    return reduce(gcd, diffs)

def is_uniform(pos_color: List[tuple[int, int]]) -> bool:
    if not pos_color:
        return True
    c0 = pos_color[0][1]
    return all(c == c0 for _, c in pos_color)

def extend_uniform(line: List[int], pos_color: List[tuple[int, int]]) -> List[int]:
    poss = sorted(p for p, _ in pos_color)
    diffs = [poss[i + 1] - poss[i] for i in range(len(poss) - 1)]
    d = compute_gcd(diffs)
    r = poss[0] % d
    c = pos_color[0][1]
    n = len(line)
    out = line[:]
    for p in range(1, n + 1):
        if p % d == r:
            out[p - 1] = c
    return out

def extend_mixed_horizontal(line: List[int], pos_color: List[tuple[int, int]]) -> List[int]:
    poss = sorted(p for p, _ in pos_color)
    diffs = [poss[i + 1] - poss[i] for i in range(len(poss) - 1)]
    d = compute_gcd(diffs)
    min_p = poss[0]
    max_p = poss[-1]
    sorted_pos_color = sorted(pos_color)
    c = sorted_pos_color[-1][1]
    out = line[:]
    current = min_p
    while current <= max_p:
        out[current - 1] = c
        current += d
    return out

def process_row(line: List[int]) -> List[int]:
    n = len(line)
    pos_color = [(j + 1, line[j]) for j in range(n) if line[j] != 0]
    k = len(pos_color)
    if k < 2:
        return line[:]
    if is_uniform(pos_color):
        return extend_uniform(line, pos_color)
    else:
        return extend_mixed_horizontal(line, pos_color)

def per_color_extension(line: List[int], n: int) -> List[int]:
    out = line[:]
    pos_by_color: dict[int, List[int]] = {}
    for i in range(n):
        c = line[i]
        if c != 0:
            if c not in pos_by_color:
                pos_by_color[c] = []
            pos_by_color[c].append(i + 1)
    for c, group_poss in pos_by_color.items():
        group_k = len(group_poss)
        if group_k < 2:
            continue
        group_poss = sorted(group_poss)
        group_diffs = [group_poss[m + 1] - group_poss[m] for m in range(group_k - 1)]
        group_d = compute_gcd(group_diffs)
        group_r = group_poss[0] % group_d
        for p in range(1, n + 1):
            if p % group_d == group_r:
                if out[p - 1] == 0 or out[p - 1] == c:
                    out[p - 1] = c
    return out

def mixed_override(line: List[int], n: int) -> List[int]:
    pos_color = [(i + 1, line[i]) for i in range(n) if line[i] != 0]
    k = len(pos_color)
    if k < 2:
        return line[:]
    poss = sorted(p for p, _ in pos_color)
    colors_set = set(c for _, c in pos_color)
    if len(colors_set) <= 1:
        return line[:]
    diffs = [poss[m + 1] - poss[m] for m in range(k - 1)]
    d = compute_gcd(diffs)
    min_p = poss[0]
    max_p = poss[-1]
    num_exp = (max_p - min_p) // d + 1
    if num_exp == k:
        c = next(c for p, c in pos_color if p == min_p)
        out = line[:]
        current = min_p
        while current <= max_p:
            out[current - 1] = c
            current += d
        return out
    return line[:]

def process_column(line: List[int]) -> List[int]:
    n = len(line)
    extended = per_color_extension(line, n)
    overridden = mixed_override(extended, n)
    return overridden

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    grid = copy.deepcopy(g)
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    if num_rows > num_cols:
        for i in range(num_rows):
            grid[i] = process_row(grid[i])
    else:
        for j in range(num_cols):
            col = [grid[i][j] for i in range(num_rows)]
            processed_col = process_column(col)
            for i in range(num_rows):
                grid[i][j] = processed_col[i]
    return grid
```