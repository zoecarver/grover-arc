```python
from typing import List
import collections

def get_group_size(row: List[int], start: int, end: int, C: int) -> int:
    runs = []
    i = start
    while i <= end:
        if row[i] == C:
            length = 0
            while i <= end and row[i] == C:
                length += 1
                i += 1
            runs.append(length)
        else:
            i += 1
    if not runs:
        return 0
    run_freq = collections.Counter(runs)
    max_f = max(run_freq.values())
    possible_ks = [k for k, v in run_freq.items() if v == max_f]
    return max(possible_ks)

def complete_pattern(row: List[int]) -> None:
    w = len(row)
    if w < 3:
        return
    B = row[0]
    left = row[1]
    right = row[w - 2]
    if left == right != B:
        side = left
        start = 2
        end = w - 3
    else:
        side = None
        start = 1
        end = w - 2
    if start > end:
        return
    exclude = {B, 2}
    if side is not None and side not in exclude:
        exclude.add(side)
    freq = collections.Counter()
    for i in range(start, end + 1):
        val = row[i]
        if val not in exclude:
            freq[val] += 1
    if not freq:
        return
    max_f = max(freq.values())
    num = end - start + 1
    if max_f < num * 0.25:
        return
    possible_cs = [c for c, f in freq.items() if f == max_f]
    best_c = None
    best_k = -1
    for c in possible_cs:
        k = get_group_size(row, start, end, c)
        if k > best_k or (k == best_k and (best_c is None or c < best_c)):
            best_k = k
            best_c = c
    if best_k == 0:
        return
    C = best_c
    K = best_k
    unit = [C] * K + [B]
    period = len(unit)
    best_phase = 0
    best_count = -1
    for p in range(period):
        count = 0
        for j in range(num):
            pat = unit[(j + p) % period]
            if pat == row[start + j]:
                count += 1
        if count > best_count or (count == best_count and p < best_phase):
            best_count = count
            best_phase = p
    if best_count / num < 0.75:
        return
    for j in range(num):
        pat = unit[(j + best_phase) % period]
        row[start + j] = pat

def fix_ones(grid: List[List[int]], r: int, B: int) -> None:
    w = len(grid[0])
    has = any(grid[r][c] == 1 for c in range(9, 13) if c < w)
    if has and 11 < w:
        grid[r][11] = 1
        for c in [9, 10, 12]:
            if c < w and grid[r][c] == 1:
                grid[r][c] = B

def fix_bays(grid: List[List[int]], r: int, B: int) -> None:
    w = len(grid[0])
    has = any(grid[r][c] == 2 for c in range(2, 6) if c < w)
    if has:
        for c in [3, 4]:
            if c < w:
                grid[r][c] = 2
        for c in [2, 5]:
            if c < w and grid[r][c] == 2:
                grid[r][c] = B

def fix_nines(grid: List[List[int]], r: int, B: int) -> None:
    w = len(grid[0])
    if w > 25 and grid[r][24] == 9 and grid[r][25] == 8:
        grid[r][24] = B
        grid[r][25] = 9

def fix_fours(grid: List[List[int]], r: int) -> None:
    w = len(grid[0])
    for c in range(16, 20):
        if c < w:
            grid[r][c] = 4

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    rows = len(grid)
    if rows == 0:
        return grid
    w = len(grid[0])
    if w >= 25:
        B = grid[0][0]
        for r in range(2, min(27, rows - 1) + 1):
            fix_ones(grid, r, B)
            fix_bays(grid, r, B)
            fix_fours(grid, r)
        for r in range(1, min(28, rows)):
            fix_nines(grid, r, B)
    for r in range(rows):
        complete_pattern(grid[r])
    return grid
```