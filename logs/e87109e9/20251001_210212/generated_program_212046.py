```python
from typing import List
from collections import Counter

def get_background(grid: List[List[int]]) -> int:
    flat = [cell for row in grid for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_bands(grid: List[List[int]]) -> List[tuple]:
    bands = []
    i = 0
    n = len(grid)
    while i < n:
        j = i
        while j < n and grid[j] == grid[i]:
            j += 1
        pattern = grid[i]
        runs = []
        k = 0
        m = len(pattern)
        while k < m:
            if pattern[k] == get_background(grid):
                k += 1
                continue
            color = pattern[k]
            start = k
            while k < m and pattern[k] == color:
                k += 1
            end = k - 1
            width = end - start + 1
            runs.append((start, end, color, width))
        bands.append((i, j - i, runs))
        i = j
    return bands

def find_line_pairs(bands: List[tuple], bg: int) -> set:
    line_pairs = set()
    for _, _, runs in bands:
        for start, end, color, width in runs:
            if color == 8 and width >= 2:
                line_pairs.add((start, start + 1))
            elif width <= 4 and color != bg:
                if start < 12:
                    new_start = end + 1
                    new_end = new_start + 1
                    line_pairs.add((new_start, new_end))
                if end > 11:
                    new_end = start - 1
                    new_start = new_end - 1
                    if new_start >= 0:
                        line_pairs.add((new_start, new_end))
    return line_pairs

def program(g: List[List[int]]) -> List[List[int]]:
    if len(g) < 6:
        return []
    main_grid = g[6:]
    if not main_grid:
        return []
    bg = get_background(main_grid)
    bands = get_bands(main_grid)
    line_pairs_list = list(find_line_pairs(bands, bg))
    if not line_pairs_list:
        return [row[:] for row in main_grid]
    out = [row[:] for row in main_grid]
    n = len(out)
    for row_idx in range(n):
        original_row = main_grid[row_idx]
        has_8 = any(original_row[c] == 8 for p in line_pairs_list for c in range(p[0], p[1] + 1))
        if has_8:
            left = min(p[0] for p in line_pairs_list)
            right = max(p[1] for p in line_pairs_list)
            for c in range(left, right + 1):
                if out[row_idx][c] == bg:
                    out[row_idx][c] = 8
    return out
```