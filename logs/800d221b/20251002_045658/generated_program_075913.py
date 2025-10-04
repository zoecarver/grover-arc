```python
from typing import List
from collections import Counter
import copy

def get_background_canvas(g: List[List[int]]) -> tuple[int, int]:
    n = len(g)
    flat = [g[i][j] for i in range(n) for j in range(n)]
    counts = Counter(flat)
    sorted_colors = sorted(counts, key=counts.get, reverse=True)
    background = sorted_colors[0]
    canvas = sorted_colors[1]
    return background, canvas

def update_grid(g: List[List[int]], background: int, canvas: int) -> List[List[int]]:
    n = len(g)
    new_g = copy.deepcopy(g)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == canvas:
                adj_paints = []
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < n and g[ni][nj] not in (background, canvas):
                        adj_paints.append(g[ni][nj])
                if adj_paints:
                    paint_count = Counter(adj_paints)
                    if len(paint_count) == 1:
                        new_g[i][j] = next(iter(paint_count))
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    background, canvas = get_background_canvas(g)
    current = copy.deepcopy(g)
    max_iterations = len(g) * len(g)  # Safety limit
    for _ in range(max_iterations):
        new_g = update_grid(current, background, canvas)
        if new_g == current:
            return current
        current = new_g
    return current
```