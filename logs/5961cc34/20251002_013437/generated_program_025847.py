```python
from typing import List

def find_red_column(g: List[List[int]]) -> int:
    """Rule: The red column is the column containing the yellow (4) cell, which is stacked above the initial red bar (2s)."""
    height = len(g)
    width = len(g[0]) if height > 0 else 0
    red_col = -1
    for r in range(height):
        for c in range(width):
            if g[r][c] == 4:
                red_col = c
                break
        if red_col != -1:
            break
    # Verify with 2s if needed, but assume unique 4
    return red_col

def remove_non_maroon_and_red(g: List[List[int]], red_col: int) -> List[List[int]]:
    """Transformation: Replace all greens (3), blues (1), and yellow (4) with maroon (8); preserve initial reds (2) but will be overwritten by extension."""
    height = len(g)
    width = len(g[0]) if height > 0 else 0
    new_g = [[8 for _ in range(width)] for _ in range(height)]
    for r in range(height):
        for c in range(width):
            if g[r][c] == 2:
                new_g[r][c] = 2  # Temporarily preserve initial reds
    return new_g

def extend_red_to_full_height(new_g: List[List[int]], red_col: int) -> List[List[int]]:
    """Rule: Extend the red (2) to full vertical height in the identified column, overwriting all cells in that column. This resolves holes by filling and splits maroon into left/right components."""
    height = len(new_g)
    width = len(new_g[0]) if height > 0 else 0
    for r in range(height):
        new_g[r][red_col] = 2
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose rules: Find red column, remove non-maroon/non-red elements, extend red full height."""
    red_col = find_red_column(g)
    temp_g = remove_non_maroon_and_red(g, red_col)
    result = extend_red_to_full_height(temp_g, red_col)
    return result
```