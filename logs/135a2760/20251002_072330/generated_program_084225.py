```python
from typing import List, Dict
from copy import deepcopy

def flip_color(c: int) -> int:
    """Rule: Flip between colors 1 and 3 for alternating pattern (4 - c)."""
    return 4 - c

def find_inner_bounds(row: List[int], border_color: int = 2) -> tuple:
    """Observation: Inner region is between the two border 2s in training examples."""
    borders = [j for j in range(len(row)) if row[j] == border_color]
    if len(borders) >= 2:
        return borders[0] + 1, borders[-1] - 1
    return 0, len(row) - 1

def fix_alternating_regions(grid: List[List[int]]) -> List[List[int]]:
    """Rule: If no separator 4 present, enforce alternating 1 and 3 starting from left inner color."""
    new_grid = deepcopy(grid)
    for i, row in enumerate(grid):
        if 4 in row:
            continue  # Skip if separator present
        start, end = find_inner_bounds(row)
        if start > end:
            continue
        expected = row[start]
        for j in range(start, end + 1):
            if row[j] not in (1, 3):
                continue  # Skip non-alternating colors
            if row[j] != expected:
                new_grid[i][j] = expected
            expected = flip_color(expected)
    return new_grid

def get_adjacent_run_length(row: List[int], pos: int, direction: int, sep_color: int) -> tuple:
    """Helper: Compute run length and color of adjacent main run."""
    c = row[pos]
    if c == sep_color:
        return 0, None
    length = 1
    step = 1 if direction > 0 else -1
    p = pos + step
    while 0 <= p < len(row) and row[p] == c:
        length += 1
        p += step
    return length, c

def fix_separator_runs(grid: List[List[int]], sep_color: int = 4, max_runs: Dict[int, int] = None) -> List[List[int]]:
    """Rule: For separator runs >=2, change one pixel to merge with adjacent main run preferring side where new length == k."""
    if max_runs is None:
        max_runs = {}
    new_grid = deepcopy(grid)
    for i, row in enumerate(grid):
        j = 0
        n = len(row)
        while j < n:
            if row[j] != sep_color:
                j += 1
                continue
            start = j
            while j < n and row[j] == sep_color:
                j += 1
            l = j - start
            if l < 2:
                continue
            # Left adjacent
            L, left_c = get_adjacent_run_length(row, start - 1, -1, sep_color) if start > 0 else (0, None)
            # Right adjacent
            R, right_c = get_adjacent_run_length(row, j, 1, sep_color) if j < n else (0, None)
            change_pos = None
            change_to = None
            # Prefer right if it reaches k
            if right_c is not None and R + 1 == max_runs.get(right_c, 1):
                change_pos = j - 1
                change_to = right_c
            # Then left if it reaches k
            elif left_c is not None and L + 1 == max_runs.get(left_c, 1):
                change_pos = start
                change_to = left_c
            # Fallback: change second to right if possible
            elif right_c is not None:
                change_pos = start + 1
                change_to = right_c
            if change_pos is not None and change_to is not None:
                new_grid[i][change_pos] = change_to
    return new_grid

def fix_main_runs(grid: List[List[int]], max_runs: Dict[int, int], sep_color: int = 4) -> List[List[int]]:
    """Rule: For main runs > k, change the (k+1)-th pixel to separator color."""
    new_grid = deepcopy(grid)
    for i, row in enumerate(grid):
        j = 0
        n = len(row)
        while j < n:
            c = row[j]
            if c not in max_runs or c == sep_color:
                j += 1
                continue
            start = j
            k = max_runs[c]
            while j < n and row[j] == c:
                j += 1
            l = j - start
            if l > k:
                pos = start + k
                new_grid[i][pos] = sep_color
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose rules: alternating for no-sep cases, then fix separators, then fix main runs."""
    max_runs = {1: 1, 2: 2, 3: 2, 8: 3, 9: 1}
    grid = fix_alternating_regions(g)
    grid = fix_separator_runs(grid, max_runs=max_runs)
    grid = fix_main_runs(grid, max_runs, sep_color=4)
    return grid
```