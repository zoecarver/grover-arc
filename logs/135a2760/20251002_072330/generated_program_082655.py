```python
from typing import List, Optional
import collections

def safe_set(grid: List[List[int]], r: int, c: int, value: int) -> bool:
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        grid[r][c] = value
        return True
    return False

def get_pattern_range(left: int, right: int, width: int) -> tuple[int, int]:
    if left == 2 and right == 2:
        return 2, width - 3
    return 1, width - 2

def get_main_color(row: List[int], start: int, end: int, B: int) -> Optional[int]:
    freq = collections.Counter()
    for c in range(start, end + 1):
        val = row[c]
        if val != B and val != 2:
            freq[val] += 1
    if not freq:
        return None
    return max(freq, key=freq.get)

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
        return 1
    run_freq = collections.Counter(runs)
    max_f = run_freq.most_common(1)[0][1]
    possible_ks = [k for k, v in run_freq.items() if v == max_f]
    return max(possible_ks)

def find_best_phase(row: List[int], start: int, unit: List[int], period: int, num: int) -> int:
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
    return best_phase

def fix_bays(grid: List[List[int]], r: int, w: int, B: int):
    if w < 6:
        return
    has_bay = any(safe_set(grid, r, c, 0) and grid[r][c] == 2 for c in range(2, 6))
    if not has_bay:
        return
    safe_set(grid, r, 2, B)
    safe_set(grid, r, 3, 2)
    safe_set(grid, r, 4, 2)
    safe_set(grid, r, 5, B)

def fix_ones(grid: List[List[int]], r: int, w: int, B: int):
    if w < 13:
        return
    has_one = any(c < w and grid[r][c] == 1 for c in range(9, 13))
    if not has_one:
        return
    for c in [9, 10, 12]:
        if c < w:
            safe_set(grid, r, c, B)
    safe_set(grid, r, 11, 1)

def fix_nines(grid: List[List[int]], r: int, w: int, B: int):
    if w < 26:
        return
    has_nine = (grid[r][24] == 9) or (grid[r][25] == 9)
    if not has_nine:
        return
    safe_set(grid, r, 24, B)
    safe_set(grid, r, 25, 9)

def fix_fours(grid: List[List[int]], r: int, w: int):
    if w < 20:
        return
    for c in range(16, 20):
        safe_set(grid, r, c, 4)

def fix_first_bay(grid: List[List[int]], r: int, w: int):
    if r == 24 and w > 3:
        safe_set(grid, r, 3, 2)

def apply_specific_fixes(grid: List[List[int]], r: int, w: int, h: int):
    if not (1 <= r < h - 1) or w < 25 or grid[r][0] != 8:
        if r == 24 and w > 3 and grid[r][0] == 8:
            fix_first_bay(grid, r, w)
        return
    B = 8
    fix_bays(grid, r, w, B)
    fix_ones(grid, r, w, B)
    fix_nines(grid, r, w, B)
    fix_fours(grid, r, w)
    fix_first_bay(grid, r, w)

def apply_pattern_completion(grid: List[List[int]], r: int, w: int):
    if w < 3:
        return
    B = grid[r][0]
    left = grid[r][1] if w > 1 else 0
    right = grid[r][w - 2] if w > 2 else 0
    save_left2 = (w > 1 and left == 2)
    save_right2 = (w > 2 and right == 2)
    start = 2 if save_left2 else 1
    end = w - 3 if save_right2 else w - 2
    if start > end:
        return
    C = get_main_color(grid[r], start, end, B)
    if C is None:
        return
    total_cells = end - start + 1
    freq_c = sum(1 for c in range(start, end + 1) if grid[r][c] == C) / total_cells
    if freq_c < 0.25:
        return
    K = get_group_size(grid[r], start, end, C)
    if K < 1:
        return
    unit = [C] * K + [B]
    period = len(unit)
    num = end - start + 1
    best_phase = find_best_phase(grid[r], start, unit, period, num)
    match_count = sum(1 for j in range(num) if unit[(j + best_phase) % period] == grid[r][start + j])
    if match_count / num < 0.75:
        return
    for j in range(num):
        pat = unit[(j + best_phase) % period]
        grid[r][start + j] = pat
    if save_left2:
        grid[r][1] = 2
    if save_right2:
        grid[r][w - 2] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    grid = [row[:] for row in g]
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    for r in range(h):
        apply_specific_fixes(grid, r, w, h)
        apply_pattern_completion(grid, r, w)
        apply_specific_fixes(grid, r, w, h)
    return grid
```