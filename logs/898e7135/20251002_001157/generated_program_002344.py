```python
from typing import List
from collections import defaultdict
import math

def get_dominant_color(g: List[List[int]]) -> int:
    """Identify the dominant color by maximum cell count."""
    total = defaultdict(int)
    flat = [cell for row in g for cell in row]
    for cell in flat:
        total[cell] += 1
    return max(total, key=total.get) if total else 0

def get_other_colors(g: List[List[int]], dominant: int, threshold: int = 4) -> List[int]:
    """Get sorted list of other significant colors."""
    total = defaultdict(int)
    flat = [cell for row in g for cell in row]
    for cell in flat:
        total[cell] += 1
    return sorted(k for k in total if k != 0 and k != dominant and total[k] >= threshold)

def get_total_for_color(g: List[List[int]], color: int) -> int:
    """Count total cells of a specific color."""
    flat = [cell for row in g for cell in row]
    return sum(1 for cell in flat if cell == color)

def create_empty_grid(width: int, height: int, fill: int) -> List[List[int]]:
    """Create a grid filled with a value."""
    return [[fill] * width for _ in range(height)]

def fill_border(grid: List[List[int]], dominant: int):
    """Fill the border of thickness 2 with dominant color."""
    h, w = len(grid), len(grid[0]) if grid else 0
    for r in range(h):
        grid[r][0] = dominant
        grid[r][1] = dominant
        if w > 2:
            grid[r][w-1] = dominant
            grid[r][w-2] = dominant
    for c in range(w):
        grid[0][c] = dominant
        grid[1][c] = dominant
        if h > 2:
            grid[h-1][c] = dominant
            grid[h-2][c] = dominant

def place_color_block(grid: List[List[int]], color: int, start_r: int, start_c: int, num_cells: int):
    """Place exactly num_cells of color starting from (start_r, start_c), overwriting background."""
    h, w = len(grid), len(grid[0])
    filled = 0
    r = start_r
    c = start_c
    while filled < num_cells and r < h - 2:
        while filled < num_cells and c < w - 2 and grid[r][c] == grid[0][0]:  # Assume background is uniform
            grid[r][c] = color
            filled += 1
            c += 1
        r += 1
        c = start_c

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to generate the output grid."""
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    dominant = get_dominant_color(g)
    other_colors = get_other_colors(g, dominant)
    # Determine output dimensions based on input size
    out_w = max(12, int(cols * 0.8))
    out_h = max(12, int(rows * 0.8))
    grid = create_empty_grid(out_w, out_h, dominant)
    fill_border(grid, dominant)
    current_r = 2
    for color in other_colors:
        num_cells = get_total_for_color(g, color)
        place_color_block(grid, color, current_r, 2, num_cells)
        # Advance starting row for next block
        approx_h = int(math.sqrt(num_cells)) + 1
        current_r += max(2, approx_h)
        if current_r >= out_h - 4:
            current_r = 2
    return grid
```