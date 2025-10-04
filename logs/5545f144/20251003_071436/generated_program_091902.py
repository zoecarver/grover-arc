```python
from collections import Counter
from typing import List

def find_background_color(g: List[List[int]]) -> int:
    """Find the background color as the most frequent color in the grid."""
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_separator_color(g: List[List[int]]) -> int:
    """Find the separator color: the color with identical non-empty positions across all rows, not the background."""
    num_rows = len(g)
    if num_rows == 0:
        return -1
    num_cols = len(g[0])
    all_colors = set(cell for row in g for cell in row)
    bg = find_background_color(g)
    for color in all_colors:
        if color == bg:
            continue
        pos_sets = [frozenset(j for j in range(num_cols) if g[r][j] == color) for r in range(num_rows)]
        if len(set(pos_sets)) == 1 and pos_sets[0]:
            return color
    return -1

def get_panel_size(g: List[List[int]], sep_color: int) -> int:
    """Compute the panel size based on separator positions; fall back to full width if invalid or no sep."""
    num_cols = len(g[0]) if g else 0
    if sep_color == -1 or num_cols == 0:
        return num_cols
    # Positions are the same for all rows, use row 0
    pos = sorted([j for j in range(num_cols) if g[0][j] == sep_color])
    if not pos:
        return num_cols
    s = pos[0]  # First panel size
    prev = 0
    for p in pos:
        if p - prev - 1 != s:
            return num_cols  # Invalid, fall back
        prev = p
    if num_cols - prev - 1 != s:
        return num_cols  # Invalid last panel
    return s

def extract_left_panel(g: List[List[int]], s: int) -> List[List[int]]:
    """Extract the leftmost panel of width s from the grid."""
    num_rows = len(g)
    output = []
    for r in range(num_rows):
        # Take first s columns
        row_out = g[r][:s]
        # Pad if s > current length (though shouldn't happen)
        if len(row_out) < s:
            row_out += [find_background_color(g)] * (s - len(row_out))
        output.append(row_out)
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: infer background, separator, panel size, and extract left panel."""
    if not g:
        return []
    bg = find_background_color(g)
    sep = find_separator_color(g)
    s = get_panel_size(g, sep)
    return extract_left_panel(g, s)
```