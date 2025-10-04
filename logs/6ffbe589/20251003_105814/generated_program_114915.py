```python
from typing import List, Tuple

def count_nonzeros(row: List[int]) -> int:
    return sum(1 for x in row if x != 0)

def get_row_counts(g: List[List[int]]) -> List[int]:
    return [count_nonzeros(row) for row in g]

def find_largest_contiguous_block(counts: List[int]) -> Tuple[int, int]:
    n = len(counts)
    max_length = 0
    best_start = 0
    current_start = 0
    for i in range(n + 1):
        if i == n or counts[i] == 0:
            length = i - current_start
            if length > max_length:
                max_length = length
                best_start = current_start
            current_start = i + 1
    best_end = best_start + max_length - 1
    return best_start, best_end

def get_row_first_last(g: List[List[int]]) -> List[Tuple[int, int]]:
    bounds = []
    for row in g:
        n = len(row)
        first = n
        last = -1
        for j in range(n):
            if row[j] != 0:
                first = min(first, j)
                last = max(last, j)
        bounds.append((first, last))
    return bounds

def compute_global_bounds(bounds: List[Tuple[int, int]], start: int, end: int) -> Tuple[int, int]:
    min_c = len(bounds[0][0]) if bounds else 0
    max_c = -1
    for i in range(start, end + 1):
        f, l = bounds[i]
        if l != -1:
            min_c = min(min_c, f)
            max_c = max(max_c, l)
    return min_c, max_c

def crop_grid(g: List[List[int]], start_r: int, end_r: int, min_c: int, max_c: int) -> List[List[int]]:
    cropped = []
    for i in range(start_r, end_r + 1):
        row = g[i][min_c : max_c + 1]
        cropped.append(row)
    return cropped

def pad_to_square(grid: List[List[int]]) -> List[List[int]]:
    if not grid:
        return [[0]]
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    size = max(h, w)
    # Pad columns first if needed
    if w < size:
        pad_left = (size - w) // 2
        pad_right = size - w - pad_left
        for i in range(h):
            grid[i] = [0] * pad_left + grid[i] + [0] * pad_right
        w = size
    # Pad rows if needed
    if h < size:
        pad_top = (size - h) // 2
        pad_bottom = size - h - pad_top
        empty = [0] * size
        for _ in range(pad_top):
            grid.insert(0, empty[:])
        for _ in range(pad_bottom):
            grid.append(empty[:])
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    counts = get_row_counts(g)
    start, end = find_largest_contiguous_block(counts)
    bounds = get_row_first_last(g)
    min_c, max_c = compute_global_bounds(bounds, start, end)
    cropped = crop_grid(g, start, end, min_c, max_c)
    return pad_to_square(cropped)
```