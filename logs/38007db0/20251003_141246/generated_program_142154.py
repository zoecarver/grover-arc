```python
from collections import defaultdict
from typing import List, Tuple

def identify_border_color(grid: List[List[int]]) -> int:
    """Identify the border color from the top row."""
    return grid[0][0]

def identify_fill_color(grid: List[List[int]], border: int) -> int:
    """Identify the fill color from the inner part of the second row."""
    for j in range(1, len(grid[0])):
        if grid[1][j] != border:
            return grid[1][j]
    raise ValueError("Fill color not found")

def find_border_columns(grid: List[List[int]], row_idx: int, border: int) -> List[int]:
    """Find border column positions from the specified row."""
    W = len(grid[0])
    return sorted([j for j in range(W) if grid[row_idx][j] == border])

def compute_spacing(border_cols: List[int]) -> int:
    """Compute the uniform spacing between border columns."""
    if len(border_cols) < 2:
        raise ValueError("Insufficient border columns")
    return border_cols[1] - border_cols[0]

def extract_inner_for_strip(row: List[int], left: int, right: int, inner_len: int) -> List[int]:
    """Extract the inner cells for a strip."""
    return [row[left + k + 1] for k in range(inner_len)]

def group_patterns_by_strip(row: List[int], border_cols: List[int], d: int, m: int, fill: int, border: int) -> Tuple[dict, int]:
    """Group strip indices by their inner patterns and return if has special."""
    inner_len = d - 1
    pattern_to_strips = defaultdict(list)
    for i in range(m):
        left = border_cols[i]
        right = border_cols[i + 1]
        inner = extract_inner_for_strip(row, left, right, inner_len)
        pat = tuple(inner)
        has_special = any(c not in (border, fill) for c in inner)
        pattern_to_strips[pat].append((i, has_special))
    return pattern_to_strips, inner_len

def select_best_strip(pattern_to_strips: dict) -> int:
    """Select the best strip: unique with special if possible, else leftmost majority."""
    unique_with_special = [strips[0][0] for pat, strips in pattern_to_strips.items() if len(strips) == 1 and strips[0][1]]
    if unique_with_special:
        return min(unique_with_special)
    # Find majority freq
    freqs = [len(strips) for strips in pattern_to_strips.values()]
    if not freqs:
        return 0
    max_freq = max(freqs)
    majority_strips = []
    for pat, strips in pattern_to_strips.items():
        if len(strips) == max_freq:
            for strip_info in strips:
                majority_strips.append(strip_info[0])
    return min(majority_strips)

def compress_inner_to_five(inner: List[int], fill: int) -> List[int]:
    """Compress or pad inner to exactly 5 cells."""
    if len(inner) == 5:
        return inner
    elif len(inner) > 5:
        return inner[:5]
    else:
        return inner + [fill] * (5 - len(inner))

def build_output_row(border: int, inner_five: List[int]) -> List[int]:
    """Build the 7-column output row."""
    return [border] + inner_five + [border]

def is_all_border_row(row: List[int], border: int) -> bool:
    """Check if the row is entirely border color."""
    return all(c == border for c in row)

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing the puzzle solving rules."""
    if not g:
        return []
    H = len(g)
    W = len(g[0]) if W > 0 else 0
    if W < 7:
        # Degenerate case, pad with border or something, but assume W >=7
        border = g[0][0] if g else 0
        return [[border] * 7 for _ in range(H)]
    border = identify_border_color(g)
    fill = identify_fill_color(g, border)
    border_cols = find_border_columns(g, 1, border)
    d = compute_spacing(border_cols)
    m = len(border_cols) - 1
    inner_len = d - 1
    output = []
    for r in range(H):
        row = g[r]
        if is_all_border_row(row, border):
            output.append([border] * 7)
            continue
        pattern_to_strips, actual_inner_len = group_patterns_by_strip(row, border_cols, d, m, fill, border)
        selected_i = select_best_strip(pattern_to_strips)
        left = border_cols[selected_i]
        right = border_cols[selected_i + 1]
        inner_full = extract_inner_for_strip(row, left, right, actual_inner_len)
        inner_five = compress_inner_to_five(inner_full, fill)
        out_row = build_output_row(border, inner_five)
        output.append(out_row)
    return output
```