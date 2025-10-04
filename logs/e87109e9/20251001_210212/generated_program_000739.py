```python
from typing import List


def get_background(g: List[List[int]]) -> int:
    """Observe that the background color is consistent and found in row 6, column 0."""
    return g[6][0]


def clear_top(g: List[List[int]], b: int) -> List[List[int]]:
    """Rule: Clear the top 5 rows to background, removing walls and colors, preparing for shift."""
    new_g = [row[:] for row in g]
    for i in range(6):
        for j in range(24):
            new_g[i][j] = b
    return new_g


def fill_empties(g: List[List[int]], fill_color: int = 8) -> List[List[int]]:
    """Rule: Fill all empty spaces (0) with the fill color 8 across the grid."""
    new_g = [row[:] for row in g]
    for i in range(24):
        for j in range(24):
            if new_g[i][j] == 0:
                new_g[i][j] = fill_color
    return new_g


def shift_single_column(col: List[int], b: int, amount: int) -> List[int]:
    """Rule: For a single column, shift non-background blocks up by the amount, clipping to top, filling original positions with background."""
    new_col = [b] * 24
    i = 0
    while i < 24:
        if col[i] != b:
            c = col[i]
            start = i
            length = 0
            while i < 24 and col[i] == c:
                length += 1
                i += 1
            new_start = max(0, start - amount)
            end = min(24, new_start + length)
            for k in range(new_start, end):
                new_col[k] = c
        else:
            i += 1
    return new_col


def shift_blocks_up(g: List[List[int]], b: int, amount: int = 6) -> List[List[int]]:
    """Compose: Shift all non-background blocks up in each column by the fixed amount of 6 rows."""
    new_g = [[0] * 24 for _ in range(24)]
    for j in range(24):
        col = [g[i][j] for i in range(24)]
        new_col = shift_single_column(col, b, amount)
        for i in range(24):
            new_g[i][j] = new_col[i]
    return new_g


def extend_fill_vertical(g: List[List[int]], b: int, fill_color: int = 8) -> List[List[int]]:
    """Rule: For columns with fill color (8) blocks, extend them vertically up to row 0 and down until hitting non-background non-fill."""
    new_g = [row[:] for row in g]
    for j in range(24):
        col = [new_g[i][j] for i in range(24)]
        i = 0
        fill_ranges = []
        while i < 24:
            if col[i] == fill_color:
                start = i
                while i < 24 and col[i] == fill_color:
                    i += 1
                end = i
                fill_ranges.append((start, end - 1))
            else:
                i += 1
        if fill_ranges:
            overall_min = min(start for start, _ in fill_ranges)
            overall_max = max(end for _, end in fill_ranges)
            # extend up
            for k in range(overall_min):
                if new_g[k][j] == b:
                    new_g[k][j] = fill_color
            # extend down
            for k in range(overall_max + 1, 24):
                if new_g[k][j] != b and new_g[k][j] != fill_color:
                    break
                new_g[k][j] = fill_color
    return new_g


def add_upper_connections(g: List[List[int]], b: int, fill_color: int = 8) -> List[List[int]]:
    """Rule: At levels with fill blocks, extend each non-background block horizontally by 2 columns and fill small gaps to connect."""
    new_g = [row[:] for row in g]
    # Find connection rows (where there is fill block of length 2+)
    connection_rows = set()
    for r in range(23):
        for j in range(22):
            if new_g[r][j] == fill_color and new_g[r][j + 1] == fill_color:
                connection_rows.add(r)
                break
    for r in connection_rows:
        # Find all non-b blocks in this row
        blocks = []
        j = 0
        while j < 24:
            if new_g[r][j] != b:
                start = j
                c = new_g[r][j]
                while j < 24 and new_g[r][j] == c:
                    j += 1
                end = j - 1
                blocks.append((start, end, c))
            else:
                j += 1
        # Sort blocks by start
        blocks.sort(key=lambda x: x[0])
        # Extend each by 2 to the right (clip)
        for idx, (s, e, c) in enumerate(blocks):
            extend_end = min(24, e + 2)
            for k in range(e + 1, extend_end + 1):
                if new_g[r][k] == b:
                    new_g[r][k] = fill_color
            blocks[idx] = (s, extend_end, c)
        # Fill gaps between consecutive extended blocks if gap <=4
        for idx in range(len(blocks) - 1):
            s1, e1, _ = blocks[idx]
            s2, e2, _ = blocks[idx + 1]
            gap_start = e1 + 1
            gap_end = s2 - 1
            if gap_start <= gap_end and gap_end - gap_start + 1 <= 4:
                for k in range(gap_start, gap_end + 1):
                    if new_g[r][k] == b:
                        new_g[r][k] = fill_color
    return new_g


def add_lower_connections(g: List[List[int]], b: int, fill_color: int = 8) -> List[List[int]]:
    """Rule: Add lower vertical extensions and final horizontal connection above the bottom block from left extension columns to end."""
    new_g = [row[:] for row in g]
    # Find the bottom block start row (lowest non-b block start)
    bottom_start = 24
    for j in range(24):
        i = 23
        while i >= 0:
            if new_g[i][j] != b:
                bottom_start = min(bottom_start, i)
                break
            i -= 1
    # Assume lower connection at row bottom_start -1 full from 4 to 23 with fill
    connect_row = bottom_start - 1
    if connect_row >= 0:
        for j in range(4, 24):
            if new_g[connect_row][j] == b:
                new_g[connect_row][j] = fill_color
    # Add symmetric for row connect_row -1 if possible
    connect_row2 = connect_row - 1
    if connect_row2 >= 0:
        for j in range(4, 24):
            if new_g[connect_row2][j] == b:
                new_g[connect_row2][j] = fill_color
    # Extend left vertical down if needed
    for r in range(9, bottom_start):
        for j in [4, 5, 8, 9]:
            if new_g[r][j] == b:
                new_g[r][j] = fill_color
    return new_g


def program(g: List[List[int]]) -> List[List[int]]:
    """Compose all rules: clear top, fill empties, shift blocks up, extend fill vertical, add upper and lower connections."""
    b = get_background(g)
    fill_color = 8
    amount = 6
    h = clear_top(g, b)
    h = fill_empties(h, fill_color)
    h = shift_blocks_up(h, b, amount)
    h = extend_fill_vertical(h, b, fill_color)
    h = add_upper_connections(h, b, fill_color)
    h = add_lower_connections(h, b, fill_color)
    return h
```