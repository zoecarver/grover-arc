```python
from collections import Counter

def overwrite_single_gap(g: List[List[int]]) -> List[List[int]]:
  g = [row[:] for row in g]
  colors = [1, 3, 6, 7]
  changed = True
  while changed:
    changed = False
    # horizontal overwrite single gap
    for i in range(12):
      for j in range(1, 11):
        c = g[i][j - 1]
        if c in colors and g[i][j + 1] == c and g[i][j] != c:
          g[i][j] = c
          changed = True
    # vertical overwrite single gap
    for j in range(12):
      for i in range(1, 11):
        c = g[i - 1][j]
        if c in colors and g[i + 1][j] == c and g[i][j] != c:
          g[i][j] = c
          changed = True
  return g

def fill_span(g: List[List[int]]) -> List[List[int]]:
  g = [row[:] for row in g]
  colors = [1, 3, 6, 7]
  changed = True
  while changed:
    changed = False
    # horizontal span fill for 0,2,4
    for i in range(12):
      for c in colors:
        positions = [j for j in range(12) if g[i][j] == c]
        if len(positions) >= 2:
          minj = min(positions)
          maxj = max(positions)
          for j in range(minj, maxj + 1):
            if g[i][j] in [0, 2, 4]:
              g[i][j] = c
              changed = True
    # vertical span fill for 0,2,4
    for j in range(12):
      for c in colors:
        positions = [i for i in range(12) if g[i][j] == c]
        if len(positions) >= 2:
          mini = min(positions)
          maxi = max(positions)
          for i in range(mini, maxi + 1):
            if g[i][j] in [0, 2, 4]:
              g[i][j] = c
              changed = True
  return g

def fill_adjacent(g: List[List[int]]) -> List[List[int]]:
  g = [row[:] for row in g]
  colors = [1, 3, 6, 7]
  changed = True
  while changed:
    changed = False
    for i in range(12):
      for j in range(12):
        if g[i][j] in [0, 2, 4]:
          neighbor_colors = []
          if i > 0:
            neighbor_colors.append(g[i - 1][j])
          if i < 11:
            neighbor_colors.append(g[i + 1][j])
          if j > 0:
            neighbor_colors.append(g[i][j - 1])
          if j < 11:
            neighbor_colors.append(g[i][j + 1])
          valid_neighbors = [c for c in neighbor_colors if c in colors]
          if valid_neighbors:
            counts = Counter(valid_neighbors)
            max_count = max(counts.values())
            candidates = [c for c, cnt in counts.items() if cnt == max_count]
            c = candidates[0]
            if len(candidates) > 1:
              v_counts = {}
              for cc in candidates:
                v = 0
                if i > 0 and g[i - 1][j] == cc:
                  v += 1
                if i < 11 and g[i + 1][j] == cc:
                  v += 1
                v_counts[cc] = v
              if max(v_counts.values()) > 0:
                c = max(v_counts, key=v_counts.get)
            g[i][j] = c
            changed = True
  return g

def erase_under_solid(g: List[List[int]]) -> List[List[int]]:
  g = [row[:] for row in g]
  for i in range(1, 12):
    for j in range(12):
      if g[i][j] != 0 and g[i - 1][j] != 0 and g[i][j] != g[i - 1][j]:
        c = g[i - 1][j]
        left = j
        while left > 0 and g[i - 1][left - 1] == c:
          left -= 1
        right = j
        while right < 11 and g[i - 1][right + 1] == c:
          right += 1
        length = right - left + 1
        if length >= 3:
          g[i][j] = 0
  return g

def program(g: List[List[int]]) -> List[List[int]]:
  g = overwrite_single_gap(g)
  g = erase_under_solid(g)
  g = fill_span(g)
  g = fill_adjacent(g)
  g = erase_under_solid(g)
  return g
```