```python
from typing import List

def replace_high_colors(cell: int) -> int:
    """Rule: Replace colors greater than 4 with color - 4 to map to 1-4 range."""
    if cell == 0 or cell <= 4:
        return cell
    else:
        return cell - 4

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose rules: Apply high color replacement to the entire grid."""
    return [[replace_high_colors(cell) for cell in row] for row in g]
```