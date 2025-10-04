```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = Counter(flat)
    return count.most_common(1)[0][0]

def count_same_neighbors(g: List[List[int]], r: int, c: int, color: int) -> int:
    rows = len(g)
    cols = len(g[0])
    count = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == color:
            count += 1
    return count

def remove_low_degree_pixels(g: List[List[int]], background: int) -> List[List[int]]:
    out = [row[:] for row in g]
    rows = len(out)
    cols = len(out[0])
    to_change = []
    for r in range(rows):
        for c in range(cols):
            if out[r][c] == background:
                continue
            color = out[r][c]
            same = count_same_neighbors(g, r, c, color)
            if same < 2:
                to_change.append((r, c))
    for r, c in to_change:
        out[r][c] = background
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    background = get_background(g)
    out = remove_low_degree_pixels(g, background)
    return out
```