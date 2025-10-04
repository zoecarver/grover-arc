```python
from typing import List
from collections import Counter

def get_background(grid: List[List[int]]) -> int:
    """Identify the background color as the most frequent value in the grid."""
    flat = [cell for row in grid for cell in row]
    return Counter(flat).most_common(1)[0][0]

def has_non_background(row: List[int], bg: int) -> bool:
    """Check if a row contains any non-background cell."""
    return any(cell != bg for cell in row)

def find_min_max_col(grid: List[List[int]], start_row: int, num_rows: int, bg: int, num_cols: int) -> tuple:
    """Find the minimum and maximum column indices with non-background cells in the specified rows."""
    min_col = num_cols
    max_col = -1
    for r in range(start_row, start_row + num_rows):
        for c in range(num_cols):
            if grid[r][c] != bg:
                min_col = min(min_col, c)
                max_col = max(max_col, c)
    return min_col, max_col

def extract_subgrid(grid: List[List[int]], start_row: int, min_col: int, max_col: int, num_rows: int) -> List[List[int]]:
    """Extract the subgrid from the specified rows and column range."""
    return [[grid[r][c] for c in range(min_col, max_col + 1)] for r in range(start_row, start_row + num_rows)]

def find_bands(grid: List[List[int]], bg: int, band_height: int = 5) -> List[tuple]:
    """Find starting rows for bands of the specified height where the first and last row have non-background cells."""
    num_rows = len(grid)
    num_cols = len(grid[0]) if grid else 0
    bands = []
    i = 0
    while i <= num_rows - band_height:
        if has_non_background(grid[i], bg) and has_non_background(grid[i + band_height - 1], bg):
            min_c, max_c = find_min_max_col(grid, i, band_height, bg, num_cols)
            if min_c <= max_c:
                bands.append((i, min_c, max_c))
            i += band_height
        else:
            i += 1
    return bands

def program(g: List[List[int]]) -> List[List[int]]:
    """Main function to process the grid and generate the output by extracting and concatenating bands from bottom to top."""
    if not g or not g[0]:
        return []
    bg = get_background(g)
    bands = find_bands(g, bg)
    # Sort bands by starting row descending (bottom to top)
    bands.sort(key=lambda x: x[0], reverse=True)
    subgrids = [extract_subgrid(g, start_r, min_c, max_c, 5) for start_r, min_c, max_c in bands]
    # Concatenate subgrids horizontally
    output_rows = []
    for row_idx in range(5):
        row = []
        for sub in subgrids:
            row += sub[row_idx]
        output_rows.append(row)
    return output_rows
```