```python
from typing import List
from copy import deepcopy

def get_grid_dimensions(grid: List[List[int]]) -> tuple:
    """Get the number of rows and columns in the grid."""
    if not grid or not grid[0]:
        return 0, 0
    return len(grid), len(grid[0])

def get_center(grid: List[List[int]]) -> tuple:
    """Compute the center position of the grid, representing the static small Maroon shape bbox center."""
    r, c = get_grid_dimensions(grid)
    return r // 2, c // 2

def count_color_pixels(grid: List[List[int]], color: int) -> int:
    """Count the total number of pixels of a given color, conserving pixel count (consistent for colors 1,2,3)."""
    count = 0
    r, cc = get_grid_dimensions(grid)
    for i in range(r):
        for j in range(cc):
            if grid[i][j] == color:
                count += 1
    return count

def clear_color_from_grid(grid: List[List[int]], color: int) -> List[List[int]]:
    """Clear all pixels of a given color from the grid (set to 8), for repositioning."""
    new_grid = deepcopy(grid)
    r, cc = get_grid_dimensions(new_grid)
    for i in range(r):
        for j in range(cc):
            if new_grid[i][j] == color:
                new_grid[i][j] = 8
    return new_grid

def handle_variable_colors(grid: List[List[int]]) -> List[List[int]]:
    """Handle non-consistent colors like yellow (4): remove if pink (6) present, otherwise keep; keep others like 7,6."""
    # Check if 6 is present
    has_pink = any(6 in row for row in grid)
    new_grid = deepcopy(grid)
    if has_pink:
        new_grid = clear_color_from_grid(new_grid, 4)
    # Assume 7 and 6 always kept as per examples
    return new_grid

def place_color_near_center(grid: List[List[int]], color: int, count: int, center_r: int, center_c: int, offset: tuple) -> List[List[int]]:
    """Place a given number of color pixels adjacent to the center (small Maroon bbox), in a simple vertical stack with offset."""
    # Simple placement: vertical stack starting from center_r + offset[0], at col center_c + offset[1], width 1
    # This approximates clustering; exact shape unknown but ensures proximity
    new_grid = deepcopy(grid)
    r, cc = get_grid_dimensions(new_grid)
    placed = 0
    start_row = max(0, min(r - 1, center_r + offset[0] - count // 2))
    for i in range(count):
        row = start_row + i
        if 0 <= row < r:
            col = max(0, min(cc - 1, center_c + offset[1]))
            if new_grid[row][col] == 8:
                new_grid[row][col] = color
                placed += 1
            else:
                # If occupied, try next col
                col += 1
                if 0 <= col < cc and new_grid[row][col] == 8:
                    new_grid[row][col] = color
                    placed += 1
    # Note: If not all placed due to boundaries/occupancy, some lost; approximates but follows no-nested rule intent
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Compose rules to transform input to output based on consistent observations."""
    if not g or not g[0]:
        return g
    grid = deepcopy(g)
    center_r, center_c = get_center(grid)
    # Step 1: Handle variable colors (e.g., remove 4 if 6 present)
    grid = handle_variable_colors(grid)
    # Step 2: Conserve and reposition 1,2,3 near center (clustering reduces holes implicitly)
    count1 = count_color_pixels(g, 1)
    count2 = count_color_pixels(g, 2)
    count3 = count_color_pixels(g, 3)
    # Clear them first
    grid = clear_color_from_grid(grid, 1)
    grid = clear_color_from_grid(grid, 2)
    grid = clear_color_from_grid(grid, 3)
    # Place with offsets: blue left, green above, red right (approximates adjacency to center)
    grid = place_color_near_center(grid, 1, count1, center_r, center_c, (-count1 // 4, -3))  # Leftish
    grid = place_color_near_center(grid, 3, count3, center_r, center_c, (-3, 0))  # Aboveish
    grid = place_color_near_center(grid, 2, count2, center_r, center_c, (0, 3))  # Rightish
    # Note: Hole reduction via clustering is implicit in placement; exact mechanism unknown
    return grid
```