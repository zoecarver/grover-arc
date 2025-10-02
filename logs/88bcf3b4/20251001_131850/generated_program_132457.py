```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    """Identify the background color as the most frequent value."""
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_colors(g: List[List[int]], background: int) -> set:
    """Get all non-background colors present."""
    colors = set()
    for row in g:
        for cell in row:
            if cell != background:
                colors.add(cell)
    return colors

def is_vertical_aligned(g: List[List[int]], color: int, background: int) -> bool:
    """Check if all blocks of a color are vertically aligned in one column without gaps."""
    positions = [(i, j) for i in range(len(g)) for j in range(len(g)) if g[i][j] == color]
    if not positions:
        return True
    cols = {j for _, j in positions}
    if len(cols) != 1:
        return False
    col = next(iter(cols))
    rows = sorted(set(i for i, _ in positions))
    if len(rows) != len(positions):
        return False  # Duplicates, but unlikely
    for k in range(1, len(rows)):
        if rows[k] != rows[k - 1] + 1:
            return False
    return True

def create_vertical_stack(n: int, k: int, start_row: int, col: int, color: int) -> List[List[int]]:
    """Create a vertical stack of k blocks of color starting from start_row in column col."""
    stack = [[0] * n for _ in range(n)]
    for i in range(k):
        r = start_row + i
        if r < n:
            stack[r][col] = color
    return stack

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: copy vertical aligned colors, straighten non-aligned to vertical stacks at top left available positions."""
    n = len(g)
    background = get_background(g)
    colors = get_colors(g, background)
    output = [[background] * n for _ in range(n)]  # Start with background

    current_col = 0
    for color in sorted(colors):  # Sort colors for consistent ordering
        if is_vertical_aligned(g, color, background):
            # Copy as is
            for i in range(n):
                for j in range(n):
                    if g[i][j] == color:
                        output[i][j] = color
        else:
            # Count number of blocks
            k = sum(1 for row in g for cell in row if cell == color)
            # Place vertical stack at top in next available column
            start_row = 0
            while current_col < n:
                if all(output[r][current_col] == background for r in range(start_row, start_row + k)):
                    # Available, place
                    for ii in range(k):
                        r = start_row + ii
                        if r < n:
                            output[r][current_col] = color
                    current_col += 1
                    break
                else:
                    current_col += 1
            else:
                # If no space, place from top in last column or skip, but assume space
                pass
    return output
```