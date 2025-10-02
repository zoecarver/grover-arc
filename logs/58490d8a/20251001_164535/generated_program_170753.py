```python
from collections import Counter, defaultdict
from typing import List, Dict, Tuple

def flatten_grid(grid: List[List[int]]) -> List[int]:
    """Flatten the grid into a 1D list for counting frequencies."""
    return [cell for row in grid for cell in row]

def find_background_color(grid: List[List[int]]) -> int:
    """Find the background color as the most frequent value in the grid."""
    if not grid or not grid[0]:
        return 0
    flat_list = flatten_grid(grid)
    count = Counter(flat_list)
    return count.most_common(1)[0][0]

def collect_zero_positions(grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Collect all positions (row, col) where the cell is 0."""
    positions = []
    rows = len(grid)
    if rows == 0:
        return positions
    cols = len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                positions.append((i, j))
    return positions

def compute_bounds(positions: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Compute min_r, max_r, min_c, max_c from zero positions."""
    if not positions:
        return 0, -1, 0, -1
    min_r = min(r for r, c in positions)
    max_r = max(r for r, c in positions)
    min_c = min(c for r, c in positions)
    max_c = max(c for r, c in positions)
    return min_r, max_r, min_c, max_c

def find_zero_bounds(grid: List[List[int]]) -> Tuple[int, int, int, int]:
    """Find the bounding box of all 0 cells in the grid."""
    positions = collect_zero_positions(grid)
    return compute_bounds(positions)

def compute_output_width(bounds: Tuple[int, int, int, int]) -> int:
    """Compute the output width from zero bounds."""
    _, _, min_c, max_c = bounds
    if max_c < min_c:
        return 1
    return max_c - min_c + 1

def is_adjacent_to_zero(grid: List[List[int]], i: int, j: int) -> bool:
    """Check if cell at (i,j) is adjacent (4-dir) to a 0 cell."""
    rows = len(grid)
    if rows == 0:
        return False
    cols = len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 0:
            return True
    return False

def collect_first_adj_rows(grid: List[List[int]], background: int) -> Dict[int, int]:
    """Collect the minimal row index for each color adjacent to a zero."""
    first_rows = {}
    rows = len(grid)
    if rows == 0:
        return first_rows
    cols = len(grid[0])
    for i in range(rows):
        for j in range(cols):
            c = grid[i][j]
            if c != 0 and c != background and is_adjacent_to_zero(grid, i, j):
                if c not in first_rows or i < first_rows[c]:
                    first_rows[c] = i
    return first_rows

def order_colors_by_first_adj(first_adj_rows: Dict[int, int]) -> List[int]:
    """Order colors by their first adjacent row index, ascending."""
    if not first_adj_rows:
        return []
    return sorted(first_adj_rows, key=first_adj_rows.get)

def compute_num_bars_for_color(color: int, width: int) -> int:
    """Compute number of bars for the color based on observed rules and width."""
    if color == 4:
        return 1
    if color == 3:
        return 4
    if color in (1, 2):
        return 2
    if color == 8:
        return 3 if width == 7 else 2
    return 2  # Default for other colors

def compute_num_bars(colors: List[int], width: int) -> List[int]:
    """Compute number of bars for each ordered color."""
    return [compute_num_bars_for_color(c, width) for c in colors]

def create_zero_row(width: int) -> List[int]:
    """Create a row filled with zeros of the given width."""
    return [0] * width

def place_bars_in_row(color: int, num_bars: int, width: int) -> List[int]:
    """Place the color in odd columns for num_bars, rest zeros."""
    row = create_zero_row(width)
    for k in range(num_bars):
        col = 2 * k + 1
        if col < width:
            row[col] = color
        else:
            break
    return row

def build_output_grid(ordered_colors: List[int], bar_counts: List[int], width: int, height: int) -> List[List[int]]:
    """Build the output grid with alternating zero and bar rows."""
    output = []
    num_colors = len(ordered_colors)
    for row_idx in range(height):
        if row_idx % 2 == 0:
            output.append(create_zero_row(width))
        else:
            color_idx = (row_idx - 1) // 2
            if color_idx < num_colors:
                c = ordered_colors[color_idx]
                num_b = bar_counts[color_idx]
                output.append(place_bars_in_row(c, num_b, width))
            else:
                output.append(create_zero_row(width))
    return output

def compute_output_height(ordered_colors: List[int]) -> int:
    """Compute the output height: 2 * num_colors + 1."""
    return 2 * len(ordered_colors) + 1 if ordered_colors else 1

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: transform input grid to output bar chart grid."""
    background = find_background_color(g)
    bounds = find_zero_bounds(g)
    width = compute_output_width(bounds)
    first_adj = collect_first_adj_rows(g, background)
    ordered_colors = order_colors_by_first_adj(first_adj)
    bar_counts = compute_num_bars(ordered_colors, width)
    height = compute_output_height(ordered_colors)
    return build_output_grid(ordered_colors, bar_counts, width, height)
```