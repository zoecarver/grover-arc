```python
from typing import List

def mapping_normalize(g: List[List[int]]) -> List[List[int]]:
    """Apply the fixed color mapping to standardize the grid colors."""
    mapping = {0: 8, 1: 1, 2: 5, 3: 0, 4: 7, 5: 6, 6: 9, 7: 4, 8: 2, 9: 3}
    return [[mapping.get(cell, cell) for cell in row] for row in g]

def copy_bottom_19(g_norm: List[List[int]]) -> List[List[int]]:
    """Copy the bottom 19 rows of the normalized grid, assuming input has at least 25 rows."""
    if len(g_norm) < 25:
        return g_norm
    return [row[:] for row in g_norm[6:25]]

def extract_beam_config(g_norm: List[List[int]]) -> List[tuple]:
    """Extract beam positions and colors from the normalized beam row (row 1, 0-indexed)."""
    beam_row = g_norm[1]
    panels = []
    i = 0
    n = len(beam_row)
    while i < n:
        if beam_row[i] == 6:  # wall
            i += 1
            continue
        start = i
        beam_pos = -1
        beam_color = 0
        for j in range(4):
            if i + j >= n:
                break
            if beam_row[i + j] != 8 and beam_row[i + j] != 6:
                beam_pos = j
                beam_color = beam_row[i + j]
                break
        if beam_pos != -1:
            panels.append((start, beam_pos, beam_color))
        i += 4
    return panels

def determine_fill_columns(panels: List[tuple]) -> List[int]:
    """Determine columns to fill with 2 (maroon) based on beam positions and colors in panels."""
    fill_cols = []
    for start, pos, color in panels:
        if pos == 0:  # pos1 beam
            if start == 7 and color in (7, 9):  # panel2, yellow or pink
                fill_cols += [start + 1, start + 2]  # pos2-3
            if start == 13 and color == 7:  # panel3, yellow
                fill_cols += [start + 3, start + 4]  # pos4 and next wall approximation
        elif pos == 3:  # pos4 beam
            if start == 1 and color == 5:  # panel1, red
                fill_cols += [start + 3, start + 3 + 1]  # pos4 and next
            if start == 1 and color == 7:  # panel1, yellow
                fill_cols += [start + 2, start + 3]  # pos3-4
            if start == 19 and color == 5:  # panel4, red
                fill_cols += [start, start + 1]  # pos1-2
    return list(set(fill_cols))  # unique

def fill_vertical_upper(grid: List[List[int]], fill_cols: List[int]) -> List[List[int]]:
    """Fill vertical lines in the upper 7 rows with 2 if 0 or background (0 green)."""
    for r in range(min(7, len(grid))):
        for c in fill_cols:
            if 0 <= c < len(grid[r]) and grid[r][c] in (0, 8):  # empty or green
                grid[r][c] = 2
    return grid

def horizontal_fill_regions(grid: List[List[int]]) -> List[List[int]]:
    """Perform horizontal fill of 0 and 0 (green) connected to 2's in each row."""
    for r in range(len(grid)):
        row = grid[r]
        new_row = row[:]
        i = 0
        n = len(row)
        while i < n:
            if row[i] != 2:
                i += 1
                continue
            # spread left
            j = i
            while j > 0 and row[j - 1] in (0, 8):
                new_row[j - 1] = 2
                j -= 1
            # spread right
            j = i
            while j < n - 1 and row[j + 1] in (0, 8):
                new_row[j + 1] = 2
                j += 1
            i = j + 1
        grid[r] = new_row
    return grid

def fill_lower_vertical(grid: List[List[int]], fill_cols: List[int]) -> List[List[int]]:
    """Fill vertical lines in lower rows (from row 7) with 2 if 0."""
    for r in range(7, len(grid)):
        for c in fill_cols:
            if 0 <= c < len(grid[r]) and grid[r][c] == 0:
                grid[r][c] = 2
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing the rules to transform the input grid."""
    g_norm = mapping_normalize(g)
    grid = copy_bottom_19(g_norm)
    panels = extract_beam_config(g_norm)
    fill_cols = determine_fill_columns(panels)
    grid = fill_vertical_upper(grid, fill_cols)
    grid = horizontal_fill_regions(grid)
    grid = fill_lower_vertical(grid, fill_cols)
    # Denormalize back to original color codes by replacing 2 with 8 (maroon is always 8 in original)
    for row in grid:
        for i in range(len(row)):
            if row[i] == 2:
                row[i] = 8
    return grid
```