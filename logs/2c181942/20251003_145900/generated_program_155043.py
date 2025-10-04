```python
from typing import List
from collections import defaultdict
import math

def get_color_counts(g: List[List[int]]) -> dict:
    counts = defaultdict(int)
    for row in g:
        for cell in row:
            if cell != 8:
                counts[cell] += 1
    return dict(counts)

def remove_lower_color_four(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    half = rows // 2
    result = [row[:] for row in g]
    for r in range(half, rows):
        for c in range(len(g[0])):
            if result[r][c] == 4:
                result[r][c] = 8
    return result

def calculate_rectangle_dims(n: int) -> tuple:
    if n == 0:
        return 0, 0
    side = int(math.sqrt(n))
    height = side
    width = (n + side - 1) // side
    return height, width

def build_pattern(counts: dict, rows: int, cols: int) -> List[List[int]]:
    colors = sorted(counts.keys())
    group_info = []
    total_width = 0
    max_height = 0
    for color in colors:
        n = counts[color]
        height, width = calculate_rectangle_dims(n)
        group_info.append((color, n, height, width))
        total_width += width
        max_height = max(max_height, height)
    if total_width == 0:
        return [[8 for _ in range(cols)] for _ in range(rows)]
    start_r = (rows - max_height) // 2
    start_c = (cols - total_width) // 2
    result = [[8 for _ in range(cols)] for _ in range(rows)]
    current_c = start_c
    for color, n, height, width in group_info:
        i = 0
        for dr in range(height):
            for dc in range(width):
                if i < n:
                    r = start_r + dr
                    c = current_c + dc
                    if 0 <= r < rows and 0 <= c < cols:
                        result[r][c] = color
                    i += 1
        current_c += width
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    # Remove lower color 4 as observed in training example 1
    g_clean = remove_lower_color_four(g)
    # Get counts after cleaning
    counts = get_color_counts(g_clean)
    # Build the pattern by placing compact rectangles for each color
    return build_pattern(counts, len(g), len(g[0]))
```