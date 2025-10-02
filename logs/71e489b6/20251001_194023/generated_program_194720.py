```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return g
    cols = len(g[0])

    # Rule 1: Remove 1s with fewer than 2 adjacent 1s (4-connectivity) - cleans isolated or thin protrusions
    def remove_thin_protrusions(grid: List[List[int]]) -> List[List[int]]:
        new_grid = [row[:] for row in grid]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] != 1:
                    continue
                count = sum(1 for di, dj in directions if 0 <= i + di < rows and 0 <= j + dj < cols and grid[i + di][j + dj] == 1)
                if count < 2:
                    new_grid[i][j] = 0
        return new_grid

    # Rule 2: Color 1s to 7 if they have fewer than 3 adjacent 1s (4-connectivity) - colors boundary/thin areas dark red
    def color_boundary_areas(grid: List[List[int]]) -> List[List[int]]:
        new_grid = [row[:] for row in grid]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] != 1:
                    continue
                count = sum(1 for di, dj in directions if 0 <= i + di < rows and 0 <= j + dj < cols and grid[i + di][j + dj] == 1)
                if count < 3:
                    new_grid[i][j] = 7
        return new_grid

    # Rule 3: Fill 0s to 7 if they have at least 2 adjacent 1s or 7s (8-connectivity) - fills small gaps near structures
    def fill_small_gaps(grid: List[List[int]]) -> List[List[int]]:
        new_grid = [row[:] for row in grid]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] != 0:
                    continue
                count = sum(1 for di, dj in directions if 0 <= i + di < rows and 0 <= j + dj < cols and grid[i + di][j + dj] in (1, 7))
                if count >= 2:
                    new_grid[i][j] = 7
        return new_grid

    # Compose the rules: clean, color boundaries, fill gaps
    cleaned = remove_thin_protrusions(g)
    colored = color_boundary_areas(cleaned)
    filled = fill_small_gaps(colored)
    return filled
```