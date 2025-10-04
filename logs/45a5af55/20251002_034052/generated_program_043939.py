```python
from typing import List

def extract_sequence(g: List[List[int]]) -> List[int]:
    """Extracts the color sequence from the first column of the input grid."""
    return [row[0] for row in g]

def create_grid(s: int) -> List[List[int]]:
    """Creates an empty square grid of size s x s initialized to 0."""
    return [[0 for _ in range(s)] for _ in range(s)]

def fill_row_segment(grid: List[List[int]], r: int, start_j: int, end_j: int, col: int) -> None:
    """Fills a horizontal segment of a row with the given color."""
    s = len(grid)
    for j in range(max(0, start_j), min(s, end_j + 1)):
        grid[r][j] = col

def fill_column_segment(grid: List[List[int]], j: int, start_r: int, end_r: int, col: int) -> None:
    """Fills a vertical segment of a column with the given color."""
    s = len(grid)
    for r in range(max(0, start_r), min(s, end_r + 1)):
        grid[r][j] = col

def fill_top_perimeter(grid: List[List[int]], current_start: int, t: int, current_size: int, col: int) -> None:
    """Fills the top thickness t of the current layer with the color."""
    end = current_start + current_size - 1
    for rr in range(t):
        r = current_start + rr
        fill_row_segment(grid, r, current_start, end, col)

def fill_bottom_perimeter(grid: List[List[int]], current_start: int, t: int, current_size: int, col: int) -> None:
    """Fills the bottom thickness t of the current layer with the color."""
    end = current_start + current_size - 1
    for rr in range(t):
        r = end - rr
        fill_row_segment(grid, r, current_start, end, col)

def fill_left_perimeter(grid: List[List[int]], current_start: int, t: int, current_size: int, col: int) -> None:
    """Fills the left thickness t of the current layer with the color."""
    end = current_start + current_size - 1
    for jj in range(t):
        j = current_start + jj
        fill_column_segment(grid, j, current_start, end, col)

def fill_right_perimeter(grid: List[List[int]], current_start: int, t: int, current_size: int, col: int) -> None:
    """Fills the right thickness t of the current layer with the color."""
    end = current_start + current_size - 1
    for jj in range(t):
        j = end - jj
        fill_column_segment(grid, j, current_start, end, col)

def fill_layer_perimeter(grid: List[List[int]], current_start: int, t: int, current_size: int, col: int) -> None:
    """Fills the full perimeter of thickness t for the current layer with the color."""
    if current_size <= 0 or t <= 0:
        return
    fill_top_perimeter(grid, current_start, t, current_size, col)
    fill_bottom_perimeter(grid, current_start, t, current_size, col)
    fill_left_perimeter(grid, current_start, t, current_size, col)
    fill_right_perimeter(grid, current_start, t, current_size, col)

def compute_grid_size(n: int) -> int:
    """Computes the output grid size as 2*n - 2."""
    return 2 * n - 2

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: transforms input grid to output grid using perimeter filling based on first column runs."""
    seq = extract_sequence(g)
    n = len(seq)
    if n == 0:
        return []
    s = compute_grid_size(n)
    grid = create_grid(s)
    i = 0
    current_start = 0
    current_size = s
    while i < n:
        c = seq[i]
        j = i + 1
        while j < n and seq[j] == c:
            j += 1
        t = j - i
        fill_layer_perimeter(grid, current_start, t, current_size, c)
        current_start += t
        current_size -= 2 * t
        i = j
    return grid
```