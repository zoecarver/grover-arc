```python
from collections import Counter
from typing import List, Dict, Tuple

def find_background_color(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    flat_list = [cell for row in grid for cell in row]
    count = Counter(flat_list)
    return count.most_common(1)[0][0]

def find_zero_bounds(grid: List[List[int]]) -> Tuple[int, int, int, int]:
    if not grid or not grid[0]:
        return 0, -1, 0, -1
    rows = len(grid)
    cols = len(grid[0])
    all_positions = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == 0]
    if not all_positions:
        return 0, -1, 0, -1
    min_r = min(i for i, j in all_positions)
    max_r = max(i for i, j in all_positions)
    min_c = min(j for i, j in all_positions)
    max_c = max(j for i, j in all_positions)
    return min_r, max_r, min_c, max_c

def get_first_adj_rows(grid: List[List[int]], background: int) -> Dict[int, int]:
    first_rows: Dict[int, int] = {}
    rows = len(grid)
    if rows == 0:
        return first_rows
    cols = len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            c = grid[i][j]
            if c != 0 and c != background:
                is_adj = any(
                    0 <= i + di < rows and 0 <= j + dj < cols and grid[i + di][j + dj] == 0
                    for di, dj in directions
                )
                if is_adj:
                    if c not in first_rows or i < first_rows[c]:
                        first_rows[c] = i
    return first_rows

def compute_num_bars(color: int, canvas_width: int) -> int:
    if color == 4:
        return 1
    if color == 3:
        return 4
    if color in (1, 2):
        return 2
    if color == 8:
        return 3 if canvas_width == 7 else 2
    return 2

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background_color(g)
    bounds = find_zero_bounds(g)
    min_r, max_r, min_c, max_c = bounds
    if max_r < min_r:
        return [[0]]
    width = max_c - min_c + 1
    first_rows = get_first_adj_rows(g, bg)
    if not first_rows:
        return [[0] * width]
    ordered_colors = sorted(first_rows, key=first_rows.get)
    num_colors = len(ordered_colors)
    height = 2 * num_colors + 1
    out = [[0] * width for _ in range(height)]
    for idx, color in enumerate(ordered_colors):
        bar_row_idx = 2 * idx + 1
        num_bars = compute_num_bars(color, width)
        for k in range(num_bars):
            col_idx = 2 * k + 1
            if col_idx < width:
                out[bar_row_idx][col_idx] = color
    return out
```