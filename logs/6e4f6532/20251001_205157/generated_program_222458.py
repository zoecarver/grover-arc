```python
from collections import Counter
from typing import List

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def is_isolated(r: int, c: int, g: List[List[int]], bg: int) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(g), len(g[0])
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if g[nr][nc] != bg:
                return False
    return True

def transfer_pixels(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    out = [row[:] for row in g]
    rows, cols = len(g), len(g[0])
    for r in range(rows):
        for c in range(cols):
            if out[r][c] == 9 and not is_isolated(r, c, out, bg):
                out[r][c] = bg
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    # Compose rules: apply pixel transfer from small shapes (non-isolated 9's) to background
    # This handles the consistent pixel transfer (-3 small, +3 background) and contributes to hole reduction
    # Other rules (shape movement, static borders) are preserved in the input as base, with transfer applied
    return transfer_pixels(g)
```