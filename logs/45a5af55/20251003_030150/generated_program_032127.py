```python
from typing import List, Tuple

def get_border_info(grid: List[List[int]]) -> Tuple[int, int, List[List[int]]]:
    """Extract border color, thickness, and content grid."""
    if not grid:
        return 0, 0, []
    border_color = grid[0][0]
    thickness = 0
    n = len(grid)
    while thickness < n and all(cell == border_color for cell in grid[thickness]):
        thickness += 1
    content = grid[thickness:] if thickness < n else []
    return border_color, thickness, content

def get_stripes(content: List[List[int]]) -> List[Tuple[int, int]]:
    """Extract stripes (color, height) from content grid, from outer to inner."""
    if not content:
        return []
    stripes = []
    current_c = content[0][0]
    current_t = 1
    for row in content[1:]:
        c = row[0]
        if c == current_c:
            current_t += 1
        else:
            stripes.append((current_c, current_t))
            current_c = c
            current_t = 1
    stripes.append((current_c, current_t))
    return stripes

def build_inner_grid(stripes: List[Tuple[int, int]]) -> List[List[int]]:
    """Build the inner grid by composing frames from inside out."""
    if not stripes:
        return []
    inner_stripes = list(reversed(stripes))
    # Innermost
    t_last = inner_stripes[0][1]
    c_last = inner_stripes[0][0]
    current_size = max(0, 2 * (t_last - 1))
    if current_size == 0:
        current_grid = []
    else:
        current_grid = [[c_last for _ in range(current_size)] for _ in range(current_size)]
    current_size = len(current_grid) if current_grid else 0
    # Add outer frames
    for idx in range(1, len(inner_stripes)):
        t_new = inner_stripes[idx][1]
        c_new = inner_stripes[idx][0]
        inner_size = current_size
        new_size = inner_size + 2 * t_new
        new_grid = [[0] * new_size for _ in range(new_size)]
        offset = t_new
        # Place inner grid
        for ii in range(inner_size):
            for jj in range(inner_size):
                new_grid[offset + ii][offset + jj] = current_grid[ii][jj]
        # Fill left and right
        for ii in range(new_size):
            for jj in range(t_new):
                new_grid[ii][jj] = c_new
            for jj in range(new_size - t_new, new_size):
                new_grid[ii][jj] = c_new
        # Fill top and bottom
        for jj in range(new_size):
            for ii in range(t_new):
                new_grid[ii][jj] = c_new
            for ii in range(new_size - t_new, new_size):
                new_grid[ii][jj] = c_new
        current_grid = new_grid
        current_size = new_size
    return current_grid

def compose_full_grid(border_color: int, thickness: int, inner_grid: List[List[int]]) -> List[List[int]]:
    """Compose the full output grid with borders and inner content."""
    inner_size = len(inner_grid) if inner_grid else 0
    total_size = inner_size + 2 * thickness
    full_grid = [[border_color for _ in range(total_size)] for _ in range(total_size)]
    if inner_size > 0:
        offset = thickness
        for i in range(inner_size):
            for j in range(inner_size):
                full_grid[offset + i][offset + j] = inner_grid[i][j]
    return full_grid

def program(g: List[List[int]]) -> List[List[int]]:
    border_color, thickness, content = get_border_info(g)
    num_content = len(content)
    if num_content == 0:
        total_size = 2 * thickness
        return [[border_color for _ in range(total_size)] for _ in range(total_size)]
    stripes = get_stripes(content)
    inner_grid = build_inner_grid(stripes)
    full_grid = compose_full_grid(border_color, thickness, inner_grid)
    return full_grid
```