```python
from typing import List

def detect_pink_presence(grid: List[List[int]]) -> bool:
    """Detect if pink (6) is present in the grid."""
    return any(6 in row for row in grid)

def remove_yellow_if_pink(grid: List[List[int]], has_pink: bool) -> List[List[int]]:
    """Replace yellow (4) with maroon (8) if pink is present."""
    return [[8 if has_pink and cell == 4 else cell for cell in row] for row in grid]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: remove yellow if pink is present."""
    has_pink = detect_pink_presence(g)
    return remove_yellow_if_pink(g, has_pink)
```