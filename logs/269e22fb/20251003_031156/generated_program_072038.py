```python
from typing import List

def scale_horizontal(row: List[int], old_w: int, new_w: int = 20) -> List[int]:
    """Scale a single row horizontally using nearest neighbor interpolation."""
    if not row or old_w == 0:
        return [0] * new_w
    return [row[(j * old_w) // new_w] for j in range(new_w)]

def scale_vertical(grid: List[List[int]], old_h: int, new_h: int = 20) -> List[List[int]]:
    """Scale the grid vertically by selecting appropriate input rows for each output row."""
    if not grid or old_h == 0:
        return [[0] * 20 for _ in range(new_h)]
    w = len(grid[0]) if grid else 0
    return [scale_horizontal(grid[(i * old_h) // new_h], w) for i in range(new_h)]

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose horizontal and vertical scaling to upsample the input grid to 20x20."""
    h = len(g)
    return scale_vertical(g, h)
```