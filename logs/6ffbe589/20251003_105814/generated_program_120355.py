```python
from typing import List, Tuple

def get_row_sums(g: List[List[int]]) -> List[int]:
    """Compute sum of non-zero pixels per row."""
    return [sum(1 for v in row if v != 0) for row in g]

def find_main_y_range(row_sums: List[int]) -> Tuple[int, int]:
    """Find the start and end of the main consecutive rows with non-zero pixels, choosing the one with maximum total sum."""
    n = len(row_sums)
    max_total = 0
    best_start = 0
    best_end = -1
    current_start = -1
    current_total = 0
    for y in range(n):
        if row_sums[y] > 0:
            if current_start == -1:
                current_start = y
            current_total += row_sums[y]
        else:
            if current_start != -1:
                if current_total > max_total:
                    max_total = current_total
                    best_start = current_start
                    best_end = y - 1
                current_start = -1
                current_total = 0
    if current_start != -1:
        if current_total > max_total:
            max_total = current_total
            best_start = current_start
            best_end = n - 1
    return best_start, best_end

def get_row_bounds(g: List[List[int]]) -> List[Tuple[int, int]]:
    """Precompute leftmost and rightmost non-zero positions per row."""
    n = len(g)
    bounds = []
    for row in g:
        left = n
        right = -1
        for x, v in enumerate(row):
            if v != 0:
                left = min(left, x)
                right = max(right, x)
        if right == -1:
            bounds.append((n, -1))
        else:
            bounds.append((left, right))
    return bounds

def get_main_bbox(g: List[List[int]], min_y: int, max_y: int, row_bounds: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Compute the bounding box (min_x, min_y, max_x, max_y) for the main structure in the y-range."""
    n = len(g)
    min_x = n
    max_x = -1
    for y in range(min_y, max_y + 1):
        l, r = row_bounds[y]
        if r >= 0:
            min_x = min(min_x, l)
            max_x = max(max_x, r)
    return min_x, min_y, max_x, max_y

def extract_pixels_in_bbox(g: List[List[int]], bbox: Tuple[int, int, int, int]) -> List[Tuple[int, int, int]]:
    """Extract all non-zero pixels within the bbox."""
    min_x, min_y, max_x, max_y = bbox
    pixels = []
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            v = g[y][x]
            if v != 0:
                pixels.append((y, x, v))
    return pixels

def translate_pixels(pixels: List[Tuple[int, int, int]], dx: int, dy: int) -> List[Tuple[int, int, int]]:
    """Translate pixels by (dx, dy)."""
    return [(y + dy, x + dx, v) for y, x, v in pixels]

def compute_output_size(bbox: Tuple[int, int, int, int]) -> int:
    """Compute the side length of the square output grid based on bbox dimensions."""
    min_x, min_y, max_x, max_y = bbox
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    return max(w, h)

def build_output_grid(pixels: List[Tuple[int, int, int]], s: int) -> List[List[int]]:
    """Build the s x s output grid, placing translated pixels and padding with 0s."""
    grid = [[0] * s for _ in range(s)]
    for y, x, v in pixels:
        if 0 <= y < s and 0 <= x < s:
            grid[y][x] = v
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compose functions to generate the output grid."""
    if not g or not g[0]:
        return []
    n = len(g)
    row_sums = get_row_sums(g)
    min_y, max_y = find_main_y_range(row_sums)
    if max_y < min_y:
        return [[0] * n for _ in range(n)]  # empty case
    row_bounds = get_row_bounds(g)
    bbox = get_main_bbox(g, min_y, max_y, row_bounds)
    min_x, _, max_x, _ = bbox
    if max_x < min_x:
        return [[0] * n for _ in range(n)]
    pixels = extract_pixels_in_bbox(g, bbox)
    dx = -min_x
    dy = -min_y
    translated_pixels = translate_pixels(pixels, dx, dy)
    s = compute_output_size(bbox)
    output = build_output_grid(translated_pixels, s)
    return output
```