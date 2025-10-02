```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_colors(g: List[List[int]], background: int) -> List[int]:
    colors = set()
    for row in g:
        for cell in row:
            if cell != background:
                colors.add(cell)
    return sorted(colors)

def get_positions(g: List[List[int]], color: int) -> List[int]:
    n = len(g)
    count = 0
    for i in range(n):
        for j in range(n):
            if g[i][j] == color:
                count += 1
    return count

def is_vertical_aligned(g: List[List[int]], color: int, background: int) -> bool:
    n = len(g)
    positions = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == color:
                positions.append((i, j))
    if not positions:
        return True
    cols = {j for i, j in positions}
    if len(cols) != 1:
        return False
    col = next(iter(cols))
    rows = sorted(i for i, _ in positions)
    if len(set(rows)) != len(rows):
        return False
    for k in range(1, len(rows)):
        if rows[k] != rows[k - 1] + 1:
            return False
    return True

def preserve_color(out: List[List[int]], g: List[List[int]], color: int) -> None:
    n = len(g)
    for i in range(n):
        for j in range(n):
            if g[i][j] == color:
                out[i][j] = color

def find_available_column(n: int, k: int, out: List[List[int]], background: int, target: int) -> int:
    best_col = -1
    min_dist = float('inf')
    for col in range(n):
        free = True
        for r in range(k):
            if r >= n or out[r][col] != background:
                free = False
                break
        if free:
            dist = abs(col - target)
            if dist < min_dist or (dist == min_dist and col > best_col):
                min_dist = dist
                best_col = col
    if best_col == -1:
        best_col = max(0, min(n - 1, target))
    return best_col

def place_vertical(out: List[List[int]], color: int, col: int, k: int, n: int) -> None:
    for r in range(k):
        if r < n:
            out[r][col] = color

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    out = [[background for _ in range(n)] for _ in range(n)]
    colors = get_colors(g, background)
    for color in colors:
        k = get_positions(g, color)
        if k == 0:
            continue
        if is_vertical_aligned(g, color, background):
            preserve_color(out, g, color)
        else:
            positions = [(i, j) for i in range(n) for j in range(n) if g[i][j] == color]
            avg_col = sum(j for _, j in positions) / k if k > 0 else 0
            target = round(avg_col)
            col = find_available_column(n, k, out, background, target)
            place_vertical(out, color, col, k, n)
    return out
```