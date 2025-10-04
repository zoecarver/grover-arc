```python
import copy

def find_trunk_column(grid):
  h = len(grid)
  w = len(grid[0])
  trunk_col = -1
  for r in range(h - 1, -1, -1):
    for c in range(w):
      if grid[r][c] == 2 or grid[r][c] == 4:
        trunk_col = c
        break
    if trunk_col != -1:
      break
  return trunk_col

def treat_yellow_as_red(grid):
  h = len(grid)
  w = len(grid[0])
  for r in range(h):
    for c in range(w):
      if grid[r][c] == 4:
        grid[r][c] = 2
  return grid

def get_highest_intersect(grid, trunk_col):
  h = len(grid)
  highest = h
  for r in range(h):
    if grid[r][trunk_col] == 1 or grid[r][trunk_col] == 3:
      highest = min(highest, r)
  return highest

def fill_intersecting_components(grid, trunk_col):
  h = len(grid)
  w = len(grid[0])
  for r in range(h):
    if grid[r][trunk_col] == 1 or grid[r][trunk_col] == 3:
      left = trunk_col
      while left > 0 and grid[r][left - 1] in (1, 3):
        left -= 1
      right = trunk_col
      while right < w - 1 and grid[r][right + 1] in (1, 3):
        right += 1
      for c in range(left, right + 1):
        grid[r][c] = 2
  return grid

def fill_green_components(grid, trunk_col, original_g):
  h = len(grid)
  w = len(grid[0])
  for r in range(h):
    for c in range(w):
      if original_g[r][c] == 3:
        is_left_top = (c < trunk_col)
        left = c
        while left > 0 and original_g[r][left - 1] in (1, 3):
          left -= 1
        right = c
        while right < w - 1 and original_g[r][right + 1] in (1, 3):
          right += 1
        skip = False
        if is_left_top:
          has_above = False
          if r > 0:
            for k in range(left, right + 1):
              if original_g[r - 1][k] in (1, 3):
                has_above = True
                break
          if not has_above:
            skip = True
        if not skip:
          expanded_left = left
          if original_g[r][left] == 3 and trunk_col not in range(left, right + 1):
            expanded_left = 0
          for k in range(expanded_left, right + 1):
            grid[r][k] = 2
  return grid

def propagate_vertical(grid, original_g, trunk_col):
  h = len(grid)
  w = len(grid[0])
  for _ in range(h):
    # propagate down
    for r in range(h - 1):
      for c in range(w):
        if grid[r][c] == 2 and grid[r + 1][c] in (1, 3):
          left = c
          while left > 0 and grid[r + 1][left - 1] in (1, 3):
            left -= 1
          right = c
          while right < w - 1 and grid[r + 1][right + 1] in (1, 3):
            right += 1
          for k in range(left, right + 1):
            grid[r + 1][k] = 2
    # propagate up
    for r in range(1, h):
      for c in range(w):
        if grid[r][c] == 2 and grid[r - 1][c] in (1, 3):
          left = c
          while left > 0 and grid[r - 1][left - 1] in (1, 3):
            left -= 1
          right = c
          while right < w - 1 and grid[r - 1][right + 1] in (1, 3):
            right += 1
          for k in range(left, right + 1):
            grid[r - 1][k] = 2
  return grid

def apply_merge(grid, original_g, trunk_col):
  h = len(grid)
  w = len(grid[0])
  for r in range(h):
    spans = []
    c = 0
    while c < w:
      if grid[r][c] == 2:
        start = c
        while c < w and grid[r][c] == 2:
          c += 1
        spans.append((start, c - 1))
      else:
        c += 1
    if len(spans) > 1:
      has_bridge = False
      for start, end in spans:
        if start <= trunk_col <= end:
          for k in range(start, end + 1):
            if original_g[r][k] == 3:
              has_bridge = True
              break
          if has_bridge:
            break
      if has_bridge:
        min_start = min(start for start, end in spans)
        max_end = max(end for start, end in spans)
        for c in range(min_start, max_end + 1):
          grid[r][c] = 2
  return grid

def extend_top_green_right(grid, original_g, trunk_col):
  h = len(grid)
  w = len(grid[0])
  for r in range(h):
    for c in range(trunk_col, w):
      if original_g[r][c] == 3:
        left = c
        while left > 0 and original_g[r][left - 1] in (1, 3):
          left -= 1
        right = c
        while right < w - 1 and original_g[r][right + 1] in (1, 3):
          right += 1
        # check if top
        is_top = True
        if r > 0:
          for k in range(left, right + 1):
            if original_g[r - 1][k] in (1, 3):
              is_top = False
              break
        if is_top and grid[r][c] == 2:  # if filled
          for k in range(left, right + 1):
            for rr in range(r):
              grid[rr][k] = 2
  return grid

def fill_stem(grid, highest_intersect, trunk_col):
  h = len(grid)
  start_r = 0 if highest_intersect == len(grid) else highest_intersect
  for r in range(start_r, h):
    grid[r][trunk_col] = 2
  return grid

def program(g: List[List[int]]) -> List[List[int]]:
  grid = copy.deepcopy(g)
  trunk_col = find_trunk_column(grid)
  highest_intersect = get_highest_intersect(grid, trunk_col)
  grid = treat_yellow_as_red(grid)
  grid = fill_intersecting_components(grid, trunk_col)
  grid = fill_green_components(grid, trunk_col, g)
  grid = propagate_vertical(grid, g, trunk_col)
  grid = apply_merge(grid, g, trunk_col)
  grid = extend_top_green_right(grid, g, trunk_col)
  grid = fill_stem(grid, highest_intersect, trunk_col)
  # final remove any remaining 1,3
  h = len(grid)
  w = len(grid[0])
  for r in range(h):
    for c in range(w):
      if grid[r][c] in (1, 3):
        grid[r][c] = 8
  return grid
```