```python
from typing import List

def has_non_zero(row: List[int]) -> bool:
  for x in row:
    if x != 0:
      return True
  return False

def get_main_row_range(g: List[List[int]]) -> tuple[int, int]:
  size = len(g)
  max_len = 0
  best_start = 0
  current_len = 0
  for r in range(size + 1):
    if r < size and has_non_zero(g[r]):
      current_len += 1
    else:
      if current_len > max_len:
        max_len = current_len
        best_start = r - current_len
      current_len = 0
  return best_start, best_start + max_len - 1

def get_min_max_col(g: List[List[int]], min_r: int, max_r: int) -> tuple[int, int]:
  size = len(g[0])
  overall_min = size
  overall_max = -1
  for r in range(min_r, max_r + 1):
    row_min = size
    row_max = -1
    for c in range(size):
      if g[r][c] != 0:
        row_min = min(row_min, c)
        row_max = max(row_max, c)
    if row_max != -1:
      overall_min = min(overall_min, row_min)
      overall_max = max(overall_max, row_max)
  if overall_max == -1:
    return 0, 0
  return overall_min, overall_max

def program(g: List[List[int]]) -> List[List[int]]:
  size = len(g)
  if size == 0:
    return []
  min_r, max_r = get_main_row_range(g)
  h = max_r - min_r + 1
  min_c, max_c = get_min_max_col(g, min_r, max_r)
  w = max_c - min_c + 1 if max_c >= min_c else 0
  n = max(h, w)
  if n == 0:
    return []
  pad_top = (n - h) // 2
  pad_left = n - w if n > w else 0
  out = [[0] * n for _ in range(n)]
  for i in range(h):
    r = min_r + i
    out_i = pad_top + i
    for j in range(w):
      c = min_c + j
      out_j = pad_left + j
      out[out_i][out_j] = g[r][c]
  return out
```