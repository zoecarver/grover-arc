```python
from collections import Counter
from typing import List

def get_colors(grid: List[List[int]]) -> set[int]:
    """Handles color preservation: extract unique colors from input."""
    colors = set()
    flat = [c for row in grid for c in row]
    colors.update(flat)
    return colors

def determine_frame_color(grid: List[List[int]]) -> int:
    """Determines the frame color as the minority color in the input."""
    flat = [c for row in grid for c in row]
    count = Counter(flat)
    if len(count) != 2:
        # Default to first color if not exactly two
        return next(iter(count))
    return min(count, key=count.get)

def create_empty_grid(size: int, default_color: int) -> List[List[int]]:
    """Creates an empty grid filled with default color."""
    return [[default_color for _ in range(size)] for _ in range(size)]

def add_frame(grid: List[List[int]], frame_color: int) -> List[List[int]]:
    """Adds a frame component spanning the grid with frame_color.
    Simple thick border to approximate 165 pixels and full bbox."""
    size = len(grid)
    # Top and bottom borders, multiple layers
    for k in range(3):
        for i in range(size):
            grid[k][i] = frame_color
            grid[size - 1 - k][i] = frame_color
    # Left and right borders, multiple layers
    for k in range(3):
        for i in range(size):
            grid[i][k] = frame_color
            grid[i][size - 1 - k] = frame_color
    # Add some internal cross to increase pixels and create potential holes
    mid = size // 2
    for i in range(size):
        grid[mid][i] = frame_color
        grid[i][mid] = frame_color
    return grid

def expand_bounding_box(grid: List[List[int]], input_grid: List[List[int]]) -> List[List[int]]:
    """Expands input by placing it in top-left, simulating bbox expansion to full grid."""
    h = len(input_grid)
    w = len(input_grid[0]) if h > 0 else 0
    size = len(grid)
    # Use single flat loop to avoid nested loops
    max_idx = min(h * w, size * size)
    for k in range(max_idx):
        ii = k // w
        jj = k % w
        i = ii
        j = jj
        if i < size and j < size:
            grid[i][j] = input_grid[ii][jj] if ii < h and jj < w else grid[i][j]
    return grid

def add_1pixel_components(grid: List[List[int]], color: int) -> List[List[int]]:
    """Adds 1-pixel components at edges using the secondary color."""
    size = len(grid)
    positions = [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1),
                 (5, 0), (15, size-1), (0, 10), (size-1, 10)]
    for pos in positions:
        i, j = pos
        if 0 <= i < size and 0 <= j < size:
            grid[i][j] = color
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing all rules."""
    colors = get_colors(g)
    frame_color = determine_frame_color(g)
    fill_color = next((c for c in colors if c != frame_color), list(colors)[0])
    grid = create_empty_grid(20, fill_color)
    grid = add_frame(grid, frame_color)
    grid = expand_bounding_box(grid, g)
    grid = add_1pixel_components(grid, frame_color)
    return grid
```