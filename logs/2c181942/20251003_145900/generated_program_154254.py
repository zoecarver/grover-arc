```python
from typing import List, Dict, Tuple
from collections import defaultdict

def has_color(g: List[List[int]], c: int) -> bool:
    """Check if color c is present in the grid."""
    for row in g:
        if any(cell == c for cell in row):
            return True
    return False

def count_colors(g: List[List[int]]) -> Dict[int, int]:
    """Count occurrences of each non-8 color in the grid."""
    counts: Dict[int, int] = defaultdict(int)
    for row in g:
        for cell in row:
            if cell != 8:
                counts[cell] += 1
    return dict(counts)

def compute_avg_col(g: List[List[int]], c: int) -> float:
    """Compute the average column index of cells with color c."""
    total_col = 0.0
    count = 0
    cols = len(g[0]) if g else 0
    for i in range(len(g)):
        for j in range(cols):
            if g[i][j] == c:
                total_col += j
                count += 1
    return total_col / count if count > 0 else 0.0

def remove_yellow_if_pink(g: List[List[int]]) -> List[List[int]]:
    """Remove all yellow (4) cells if pink (6) is present."""
    new_g = [row[:] for row in g]
    if has_color(new_g, 6):
        rows = len(new_g)
        cols = len(new_g[0]) if rows > 0 else 0
        for i in range(rows):
            for j in range(cols):
                if new_g[i][j] == 4:
                    new_g[i][j] = 8
    return new_g

def get_widths(n: int, is_even: bool, has_pink: bool) -> List[int]:
    """Compute symmetric row widths for a shape of n cells."""
    if n <= 2:
        if is_even:
            return [n, 0, 0, 0]
        else:
            return [0, 0, 0, n]
    base = n // 4
    remaining = n % 4
    widths = [base, base, base, base]
    extra_per = remaining // 2
    extra_rem = remaining % 2
    widths[1] += extra_per
    widths[2] += extra_per + extra_rem
    if n % 4 == 0 and widths[0] > 0:
        widths[0] -= 1
        widths[1] += 1
        widths[3] -= 1
        widths[2] += 1
    if is_even and not has_pink:
        b = n // 2
        return [0, b, n - b, 0]
    return widths

def place_shape(g: List[List[int]], c: int, widths: List[int], box_start: int, start_row: int, is_odd: bool, has_pink: bool) -> None:
    """Place a shape for color c using given widths in the grid."""
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    max_w = max(widths) if widths else 0
    box_w = max_w + 1 if has_pink and is_odd else max_w
    for ri in range(4):
        row = start_row + ri
        if 0 <= row < rows:
            num = widths[ri]
            if num > 0:
                if not is_odd:  # even: always right align
                    fill_start = box_start + box_w - num
                elif has_pink and 1 <= ri <= 2:  # odd, pink, middle: right align
                    fill_start = box_start + box_w - num
                else:  # left align
                    fill_start = box_start
                for k in range(num):
                    col = fill_start + k
                    if 0 <= col < cols:
                        g[row][col] = c

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to transform the input grid according to puzzle rules."""
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    new_g = remove_yellow_if_pink(g)
    counts = count_colors(new_g)
    has_pink = has_color(new_g, 6)
    # Compute avgs before clearing
    avgs = {}
    for c in list(counts.keys()):
        if counts[c] > 0:
            avgs[c] = compute_avg_col(new_g, c)
    # Identify and clear large components (>2)
    large_colors = [c for c in counts if counts[c] > 2]
    for c in large_colors:
        for i in range(rows):
            for j in range(cols):
                if new_g[i][j] == c:
                    new_g[i][j] = 8
    # Sort large colors by avg col
    large_list = sorted(large_colors, key=lambda cc: avgs.get(cc, 0))
    # Prepare shapes
    shapes: List[Tuple[int, List[int], int]] = []
    for c in large_list:
        n = counts[c]
        is_even = (c % 2 == 0)
        widths = get_widths(n, has_pink, is_even)
        max_w = max(widths) if widths else 0
        shapes.append((c, widths, max_w))
    # Place shapes
    start_row = (rows - 4) // 2
    left = 2
    sep = 2
    current_col = left
    for c, widths, max_w in shapes:
        if max_w == 0:
            continue
        is_odd = not (c % 2 == 0)
        place_shape(new_g, c, widths, current_col, start_row, is_odd, has_pink)
        box_w = max_w + 1 if has_pink and is_odd else max_w
        current_col += box_w + sep
    return new_g
```