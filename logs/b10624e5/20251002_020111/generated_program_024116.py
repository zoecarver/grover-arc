```python
from typing import List
import copy

def reflect_upper_right(grid: List[List[int]]):
  for r in range(13):
    for c in range(13):
      if grid[r][c] != 4:
        c2 = 26 - c
        if grid[r][c2] == 4:
          grid[r][c2] = grid[r][c]

def reflect_bottom_left(grid: List[List[int]]):
  for c in range(13):
    for r in range(13):
      if grid[r][c] != 4:
        r2 = 26 - r
        if grid[r2][c] == 4:
          grid[r2][c] = grid[r][c]

def reflect_bottom_right(grid: List[List[int]]):
  for r in range(13):
    for c in range(13):
      if grid[r][c] != 4:
        r2 = 26 - r
        c2 = 26 - c
        if grid[r2][c2] == 4:
          grid[r2][c2] = grid[r][c]

def program(g: List[List[int]]) -> List[List[int]]:
  grid = copy.deepcopy(g)
  reflect_upper_right(grid)
  reflect_bottom_left(grid)
  reflect_bottom_right(grid)
  return grid
```