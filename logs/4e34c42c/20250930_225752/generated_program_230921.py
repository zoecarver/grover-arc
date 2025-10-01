```python
from typing import List

def get_bg(g: List[List[int]]) -> int:
  return g[0][0]

def get_connected_components(g: List[List[int]], bg: int) -> List[tuple]:
  rows = len(g)
  cols = len(g[0])
  visited = [[False] * cols for _ in range(rows)]
  components = []
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  for i in range(rows):
    for j in range(cols):
      if not visited[i][j] and g[i][j] != bg:
        min_r, max_r = i, i
        min_c, max_c = j, j
        stack = [(i, j)]
        visited[i][j] = True
        while stack:
          x, y = stack.pop()
          min_r = min(min_r, x)
          max_r = max(max_r, x)
          min_c = min(min_c, y)
          max_c = max(max_c, y)
          for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] != bg:
              visited[nx][ny] = True
              stack.append((nx, ny))
        components.append((min_r, max_r, min_c, max_c))
  return components

def sort_components(components: List[tuple]) -> List[tuple]:
  return sorted(components, key=lambda x: (x[2], x[0]))

def extract_sub(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> List[List[int]]:
  height = max_r - min_r + 1
  width = max_c - min_c + 1
  sub = [[g[min_r + k][min_c + l] for l in range(width)] for k in range(height)]
  if height == 5:
    frame_col = -1
    border_c = -1
    for j in range(width):
      if sub[0][j] == sub[4][j] and sub[0][j] != bg:
        frame_col = j
        border_c = sub[0][j]
        break
    if frame_col != -1:
      if border_c == 9:
        for k in range(5):
          sub[k] = sub[k][frame_col + 1:]
        width -= 1
        sub[0] = [bg] * width
        sub[4] = [bg] * width
      else:
        shift = width
        for j in range(width):
          if sub[0][j] == border_c:
            shift = j
            break
        if shift > 0:
          sub[0] = sub[0][shift:] + [bg] * shift
          sub[4] = sub[4][shift:] + [bg] * shift
  pad_top = (5 - height) // 2
  pad_bottom = 5 - height - pad_top
  padded = [[bg] * width for _ in range(pad_top)]
  for k in range(height):
    padded.append(sub[k])
  for _ in range(pad_bottom):
    padded.append([bg] * width)
  return padded

def program(g: List[List[int]]) -> List[List[int]]:
  bg = get_bg(g)
  components = get_connected_components(g, bg)
  sorted_comp = sort_components(components)
  sub_grids = []
  for comp in sorted_comp:
    min_r, max_r, min_c, max_c = comp
    height = max_r - min_r + 1
    if height > 5:
      continue
    sub = extract_sub(g, min_r, max_r, min_c, max_c, bg)
    sub_grids.append(sub)
  out_cols = sum(len(s[0]) for s in sub_grids)
  out = [[bg for _ in range(out_cols)] for _ in range(5)]
  current = 0
  for sub in sub_grids:
    w = len(sub[0])
    for r in range(5):
      for c in range(w):
        out[r][current + c] = sub[r][c]
    current += w
  return out
```