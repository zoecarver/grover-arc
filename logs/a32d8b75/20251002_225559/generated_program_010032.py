```python
from typing import List

def extract_base_canvas(grid: List[List[int]]) -> List[List[int]]:
    """Extract the right 24 columns as the base canvas, preserving large components in non-affected rows."""
    height = len(grid)
    width_out = 24
    return [row[6:6 + width_out] for row in grid]

def identify_affected_rows(grid: List[List[int]]) -> List[bool]:
    """Identify rows affected by small left-side blobs (non-zero in columns 0-4)."""
    height = len(grid)
    affected = [False] * height
    for i in range(height):
        left_row = grid[i][0:5]
        if any(cell != 0 for cell in left_row):
            affected[i] = True
    return affected

def propagate_small_colors(canvas: List[List[int]], grid: List[List[int]], affected: List[bool]) -> List[List[int]]:
    """Propagate colors from small left blobs to small/medium blobs in affected rows (simple replication to left of canvas)."""
    height = len(canvas)
    for i in range(height):
        if affected[i]:
            left_colors = [cell for cell in grid[i][0:5] if cell != 0]
            if left_colors:
                # Replicate the first non-zero color to first 3 positions if present
                color = left_colors[0]
                if len(canvas[i]) >= 3:
                    canvas[i][0:3] = [color, color, color]
    return canvas

def modify_holes_in_large(canvas: List[List[int]], affected: List[bool]) -> List[List[int]]:
    """Modify holes in large components in affected rows (simple fill with base color if 0 present)."""
    height = len(canvas)
    for i in range(height):
        if affected[i]:
            # Find large blocks and fill 0's with the dominant color in the row
            row = canvas[i]
            dominant = max(set(row), key=row.count)
            canvas[i] = [dominant if cell == 0 else cell for cell in row]
    return canvas

def apply_y_range_transformations(canvas: List[List[int]], affected: List[bool]) -> List[List[int]]:
    """Apply row transformations based on y-ranges of affected rows (interleave with a secondary color if possible)."""
    height = len(canvas)
    for i in range(height):
        if affected[i]:
            row = canvas[i]
            # Simple interleave: if dominant is known, interleave every 3rd with secondary (e.g., 4 if present)
            dominant = max(set(row), key=row.count)
            secondary = 4 if 4 in row else (7 if 7 in row else 8)
            new_row = []
            for j in range(len(row)):
                if j % 3 == 0 and j + 2 < len(row):
                    new_row.extend([secondary, secondary, dominant])
                    j += 2  # Skip ahead
                else:
                    new_row.append(row[j])
            if len(new_row) > len(row):
                new_row = new_row[:len(row)]
            elif len(new_row) < len(row):
                new_row.extend(row[len(new_row):])
            canvas[i] = new_row
    return canvas

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing the rules for transformation."""
    base = extract_base_canvas(g)
    affected = identify_affected_rows(g)
    canvas = propagate_small_colors(base, g, affected)
    canvas = modify_holes_in_large(canvas, affected)
    canvas = apply_y_range_transformations(canvas, affected)
    return canvas
```