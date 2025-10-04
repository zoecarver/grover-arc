```python
from typing import List, Set

def get_non_zero_colors(g: List[List[int]]) -> Set[int]:
    """Extract all unique non-zero colors from the grid."""
    colors: Set[int] = set()
    for row in g:
        for cell in row:
            if cell != 0:
                colors.add(cell)
    return colors

def get_filler(colors: Set[int]) -> int:
    """Identify the filler as the color not in the standard set {1,2,3,4,8}."""
    standard: Set[int] = {1, 2, 3, 4, 8}
    for c in colors:
        if c not in standard:
            return c
    return 0  # Fallback if no filler found

def get_bar_order(colors: Set[int]) -> List[int]:
    """Determine the ordered list of main colors based on presence rules."""
    order: List[int] = []
    if 8 in colors:
        order.append(8)
    if 1 in colors:
        order.append(1)
    if 4 in colors:
        if 2 in colors:
            order.append(2)
        order.append(4)
        if 3 in colors:
            order.append(3)
    else:
        if 3 in colors:
            order.append(3)
        if 2 in colors:
            order.append(2)
    return order

def get_lengths(order: List[int], colors: Set[int]) -> List[int]:
    """Compute lengths for each color in the order based on presence rules."""
    has_8: bool = 8 in colors
    has_3: bool = 3 in colors
    has_4: bool = 4 in colors
    lengths: List[int] = []
    for c in order:
        if c == 8:
            lengths.append(1)
        elif c == 1:
            lengths.append(2 if has_8 else 1)
        elif c == 2:
            lengths.append(3 if has_8 else 4)
        elif c == 4:
            lengths.append(4 if not has_3 else 3)
        elif c == 3:
            lengths.append(4 if has_4 else 2)
        else:
            lengths.append(1)  # Fallback for unexpected colors
    return lengths

def build_row(c: int, length: int, filler: int) -> List[int]:
    """Build a single output row: repeat color 'length' times, pad with filler to 4."""
    effective_length: int = min(length, 4)
    return [c] * effective_length + [filler] * (4 - effective_length)

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: compose functions to generate the output grid."""
    if not g or not any(any(cell != 0 for cell in row) for row in g):
        return []
    colors: Set[int] = get_non_zero_colors(g)
    filler: int = get_filler(colors)
    order: List[int] = get_bar_order(colors)
    if not order:
        return []
    lengths: List[int] = get_lengths(order, colors)
    output: List[List[int]] = []
    for i, c in enumerate(order):
        row: List[int] = build_row(c, lengths[i], filler)
        output.append(row)
    return output
```