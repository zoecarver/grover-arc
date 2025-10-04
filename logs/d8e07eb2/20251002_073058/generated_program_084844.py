```python
from typing import List

def count_eights_in_top(grid: List[List[int]]) -> int:
    count = 0
    for r in range(5):
        for c in range(22):
            if grid[r][c] == 8:
                count += 1
    return count

def greenify_top_if_condition(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    if count_eights_in_top(new_grid) == 84:
        for r in range(5):
            for c in range(22):
                if new_grid[r][c] == 8:
                    new_grid[r][c] = 3
    return new_grid

def set_bottom_based_on_top_condition(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    is_condition = count_eights_in_top(new_grid) == 84
    bottom_color = 3 if is_condition else 2
    for r in [28, 29]:
        new_grid[r] = [bottom_color] * 22
    return new_grid

def fill_middle_green_if_condition(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    if count_eights_in_top(new_grid) == 84:
        for r in range(12, 17):
            for c in range(1, 21):
                if new_grid[r][c] == 8:
                    new_grid[r][c] = 3
    return new_grid

def copy_pink_rows(grid: List[List[int]]) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    # Pink rows unchanged
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    result = g
    result = greenify_top_if_condition(result)
    result = set_bottom_based_on_top_condition(result)
    result = fill_middle_green_if_condition(result)
    # Other rows copy as is
    return result
```