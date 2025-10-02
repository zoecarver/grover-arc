```python
from typing import List
from collections import deque

def get_distinct_colors(grid: List[List[int]]) -> List[int]:
    flat = [cell for row in grid for cell in row]
    return sorted({c for c in flat if c != 0})

def max_component_size(grid: List[List[int]], color: int) -> int:
    if color == 0 or not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    max_size = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == color and not visited[i][j]:
                size = 0
                q = deque([(i, j)])
                visited[i][j] = True
                while q:
                    x, y = q.popleft()
                    size += 1
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == color and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                max_size = max(max_size, size)
    return max_size

def get_extra_and_filler(grid: List[List[int]], high_colors: List[int]) -> tuple:
    if not high_colors:
        return None, 0
    blob_sizes = {c: max_component_size(grid, c) for c in high_colors}
    large_highs = [(c, blob_sizes[c]) for c in high_colors if blob_sizes[c] >= 3]
    if not large_highs:
        return None, min(high_colors)
    # Select the one with largest size, tiebreaker largest color
    extra = max(large_highs, key=lambda x: (x[1], x[0]))[0]
    remaining = [c for c in high_colors if c != extra]
    filler = min(remaining) if remaining else extra
    return extra, filler

def get_low_order(low_set: set) -> List[int]:
    if not low_set:
        return []
    low_order = []
    has_1 = 1 in low_set
    has_2 = 2 in low_set
    has_3 = 3 in low_set
    has_4 = 4 in low_set
    if has_1:
        low_order.append(1)
    if has_4:
        if has_2:
            low_order.append(2)
        low_order.append(4)
        if has_3:
            low_order.append(3)
    else:
        if has_3:
            low_order.append(3)
        if has_2:
            low_order.append(2)
    return low_order

def get_lengths(k: int) -> List[int]:
    if k == 0:
        return []
    lengths = []
    for r in range(1, k + 1):
        if r == 1:
            lengths.append(1)
        elif r == 2:
            lengths.append(2)
        elif r == k:
            lengths.append(4)
        else:
            lengths.append(3)
    return lengths

def build_bar(color: int, length: int, filler: int) -> List[int]:
    return [color] * length + [filler] * (4 - length)

def program(g: List[List[int]]) -> List[List[int]]:
    distinct = get_distinct_colors(g)
    high_colors = [c for c in distinct if c >= 5]
    low_set = {c for c in distinct if 1 <= c <= 4}
    extra, filler = get_extra_and_filler(g, high_colors)
    low_order = get_low_order(low_set)
    bar_colors = []
    if extra is not None:
        bar_colors.append(extra)
    bar_colors.extend(low_order)
    k = len(bar_colors)
    if k == 0:
        return []
    lengths = get_lengths(k)
    output = [build_bar(bar_colors[i], lengths[i], filler) for i in range(k)]
    return output
```