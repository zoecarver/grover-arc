```python
from collections import Counter
from typing import List

def flatten_grid(grid: List[List[int]]) -> List[int]:
    """Flattens the 2D grid into a 1D list in row-major order."""
    return [cell for row in grid for cell in row]

def find_background(flat_grid: List[int]) -> int:
    """Identifies the background color as the most frequent color in the flattened grid."""
    if not flat_grid:
        raise ValueError("Empty grid")
    counts = Counter(flat_grid)
    return max(counts, key=counts.get)

def collect_non_background(flat_grid: List[int], background: int) -> List[List[int]]:
    """Collects all non-background cells as singleton lists in raster order."""
    return [[cell] for cell in flat_grid if cell != background]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: composes flattening, background detection, and collection."""
    flat = flatten_grid(g)
    bg = find_background(flat)
    return collect_non_background(flat, bg)
```