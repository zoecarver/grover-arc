```python
from typing import List, Dict, Set, Tuple

def get_internal_max_run(g: List[List[int]]) -> Tuple[int, int]:
    max_l = 0
    main_c = 0
    ROW_SIZE = 30
    for row in g:
        i = 0
        while i < ROW_SIZE:
            start = i
            c = row[start]
            i += 1
            while i < ROW_SIZE and row[i] == c:
                i += 1
            l = i - start
            if l > max_l and l > 1 and start > 0 and i < ROW_SIZE:
                max_l = l
                main_c = c
    return max_l, main_c

def get_color_counts(g: List[List[int]], exclude: Set[int]) -> Dict[int, int]:
    counts: Dict[int, int] = {}
    for row in g:
        for cell in row:
            if cell not in exclude:
                counts[cell] = counts.get(cell, 0) + 1
    return counts

def program(g: List[List[int]]) -> List[List[int]]:
    input_bg = g[0][0]
    n, main_c = get_internal_max_run(g)
    exclude = {input_bg, main_c}
    counts = get_color_counts(g, exclude)
    if not counts:
        return [[main_c] * n for _ in range(n)]
    # Sort by descending count, then descending id for ties
    sorted_colors = sorted(counts, key=lambda c: (-counts[c], -c))
    corner_c = sorted_colors[0]
    # For connect: min count candidates, max id
    min_cnt = min(counts.values())
    min_candidates = [c for c in sorted_colors if counts[c] == min_cnt]
    connect_c = max(min_candidates)
    # For center: second in sorted
    center_c = sorted_colors[1] if len(sorted_colors) > 1 else main_c
    grid = [[main_c for _ in range(n)] for _ in range(n)]
    # Place corners 2x2
    width = 2
    offset = 1
    positions = [
        (offset, offset),
        (offset, n - offset - width),
        (n - offset - width, offset),
        (n - offset - width, n - offset - width)
    ]
    for r_start, c_start in positions:
        for dr in range(width):
            for dc in range(width):
                grid[r_start + dr][c_start + dc] = corner_c
    # Place connections
    center_r = n // 2
    # Horizontal left and right
    left_start = 1
    grid[center_r][left_start] = connect_c
    grid[center_r][left_start + 1] = connect_c
    right_start = n - 3
    grid[center_r][right_start] = connect_c
    grid[center_r][right_start + 1] = connect_c
    # Vertical top and bottom
    center_col = n // 2
    top_start = 1
    grid[top_start][center_col] = connect_c
    grid[top_start + 1][center_col] = connect_c
    bottom_start = n - 3
    grid[bottom_start][center_col] = connect_c
    grid[bottom_start + 1][center_col] = connect_c
    # Place center cross
    center_r_pos = n // 2
    center_col_pos = n // 2
    # Horizontal 3
    for dc in range(-1, 2):
        if 0 <= center_col_pos + dc < n:
            grid[center_r_pos][center_col_pos + dc] = center_c
    # Vertical above and below
    if center_r_pos - 1 >= 0:
        grid[center_r_pos - 1][center_col_pos] = center_c
    if center_r_pos + 1 < n:
        grid[center_r_pos + 1][center_col_pos] = center_c
    return grid
```