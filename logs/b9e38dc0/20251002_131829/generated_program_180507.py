```python
from typing import List
from collections import Counter

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = Counter(flat)
    if not count:
        return 0
    return count.most_common(1)[0][0]

def find_fill_color(g: List[List[int]], background: int) -> int:
    flat = [cell for row in g for cell in row]
    count = Counter(flat)
    non_bg = [c for c in count if c != background and count[c] > 0]
    if not non_bg:
        return background
    return min(non_bg, key=lambda c: count[c])

def expand_fill(g: List[List[int]], fill_color: int, background: int) -> List[List[int]]:
    if fill_color == background:
        return [row[:] for row in g]
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    result = [row[:] for row in g]
    changed = True
    max_iters = rows + cols
    it = 0
    while changed and it < max_iters:
        it += 1
        changed = False
        new_result = [row[:] for row in result]
        for r in range(rows):
            for c in range(cols):
                if result[r][c] == background:
                    is_adj = False
                    # up
                    if r > 0 and result[r - 1][c] == fill_color:
                        is_adj = True
                    # down
                    if r < rows - 1 and result[r + 1][c] == fill_color:
                        is_adj = True
                    # left
                    if c > 0 and result[r][c - 1] == fill_color:
                        is_adj = True
                    # right
                    if c < cols - 1 and result[r][c + 1] == fill_color:
                        is_adj = True
                    if is_adj:
                        new_result[r][c] = fill_color
                        changed = True
        result = new_result
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    background = find_background(g)
    fill_color = find_fill_color(g, background)
    return expand_fill(g, fill_color, background)
```