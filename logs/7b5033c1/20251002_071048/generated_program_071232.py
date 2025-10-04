```python
from typing import List

def get_background(grid: List[List[int]]) -> int:
    """Determine the background color from the top-left cell."""
    return grid[0][0]

def extract_non_background(grid: List[List[int]], bg: int) -> List[int]:
    """Extract all non-background cells in row-major order."""
    seq = []
    for row in grid:
        for cell in row:
            if cell != bg:
                seq.append(cell)
    return seq

def format_as_column(seq: List[int]) -> List[List[int]]:
    """Format the sequence as a list of single-element lists (column)."""
    return [[x] for x in seq]

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    seq = extract_non_background(g, bg)
    return format_as_column(seq)
```