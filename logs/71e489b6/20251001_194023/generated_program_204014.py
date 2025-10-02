```python
from typing import List, Tuple

directions_4: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def count_neighbors(grid: List[List[int]], i: int, j: int, rows: int, cols: int, directions: List[Tuple[int, int]], target_values: Tuple[int, ...] = (1,)) -> int:
    """Count adjacent cells matching target_values in given directions. Handles observation of isolated cells."""
    count = 0
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] in target_values:
            count += 1
    return count

def remove_isolated(grid: List[List[int]]) -> List[List[int]]:
    """Remove 1s with zero 4-connected 1-neighbors (isolated pixels). Based on observation that single-pixel Blues disappear."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            if new_grid[i][j] == 1 and count_neighbors(new_grid, i, j, rows, cols, directions_4, (1,)) == 0:
                new_grid[i][j] = 0
    return new_grid

def handle_horizontal_size1_gaps(grid: List[List[int]]) -> List[List[int]]:
    """Handle horizontal gaps of size 1 by marking flanking 1s to 7 and propagating to uniform adjacent rows. Part of gap-bridging rule."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(1, cols - 1):
            if new_grid[i][j] == 0 and new_grid[i][j - 1] == 1 and new_grid[i][j + 1] == 1:
                new_grid[i][j - 1] = 7
                new_grid[i][j + 1] = 7
                # Propagate up
                if i > 0:
                    vals = [new_grid[i - 1][k] for k in (j - 1, j, j + 1)]
                    if all(v == 1 for v in vals) or all(v == 0 for v in vals):
                        for k in (j - 1, j, j + 1):
                            new_grid[i - 1][k] = 7
                # Propagate down
                if i < rows - 1:
                    vals = [new_grid[i + 1][k] for k in (j - 1, j, j + 1)]
                    if all(v == 1 for v in vals) or all(v == 0 for v in vals):
                        for k in (j - 1, j, j + 1):
                            new_grid[i + 1][k] = 7
    return new_grid

def handle_horizontal_size2_gaps(grid: List[List[int]]) -> List[List[int]]:
    """Handle horizontal gaps of size 2 by marking flanking 1s to 7 and propagating to uniform adjacent rows. Part of gap-bridging rule."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        for j in range(1, cols - 2):
            if new_grid[i][j - 1] == 1 and new_grid[i][j] == 0 and new_grid[i][j + 1] == 0 and new_grid[i][j + 2] == 1:
                new_grid[i][j - 1] = 7
                new_grid[i][j + 2] = 7
                # Propagate up
                if i > 0:
                    vals = [new_grid[i - 1][k] for k in range(j - 1, j + 3)]
                    if all(v == 1 for v in vals) or all(v == 0 for v in vals):
                        for k in range(j - 1, j + 3):
                            new_grid[i - 1][k] = 7
                # Propagate down
                if i < rows - 1:
                    vals = [new_grid[i + 1][k] for k in range(j - 1, j + 3)]
                    if all(v == 1 for v in vals) or all(v == 0 for v in vals):
                        for k in range(j - 1, j + 3):
                            new_grid[i + 1][k] = 7
    return new_grid

def handle_horizontal_edge_gaps(grid: List[List[int]]) -> List[List[int]]:
    """Handle size-1 horizontal gaps at left/right edges by marking adjacent 1s to 7 and propagating. Addresses edge cases in gap rule."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for i in range(rows):
        # Left edge
        if cols >= 2 and new_grid[i][0] == 0 and new_grid[i][1] == 1:
            new_grid[i][1] = 7
            # Prop up
            if i > 0:
                vals = [new_grid[i - 1][k] for k in range(2)]
                if len(set(vals)) == 1:
                    for k in range(2):
                        new_grid[i - 1][k] = 7
            # Prop down
            if i < rows - 1:
                vals = [new_grid[i + 1][k] for k in range(2)]
                if len(set(vals)) == 1:
                    for k in range(2):
                        new_grid[i + 1][k] = 7
        # Right edge
        if cols >= 2 and new_grid[i][cols - 2] == 1 and new_grid[i][cols - 1] == 0:
            new_grid[i][cols - 2] = 7
            # Prop up
            if i > 0:
                vals = [new_grid[i - 1][k] for k in (cols - 2, cols - 1)]
                if len(set(vals)) == 1:
                    for k in (cols - 2, cols - 1):
                        new_grid[i - 1][k] = 7
            # Prop down
            if i < rows - 1:
                vals = [new_grid[i + 1][k] for k in (cols - 2, cols - 1)]
                if len(set(vals)) == 1:
                    for k in (cols - 2, cols - 1):
                        new_grid[i + 1][k] = 7
    return new_grid

def handle_horizontal_gaps(grid: List[List[int]]) -> List[List[int]]:
    """Compose horizontal gap handling: edges, size1, size2. Implements horizontal gap-bridging observation."""
    grid1 = handle_horizontal_edge_gaps(grid)
    grid2 = handle_horizontal_size1_gaps(grid1)
    return handle_horizontal_size2_gaps(grid2)

def handle_vertical_size1_gaps(grid: List[List[int]]) -> List[List[int]]:
    """Handle vertical gaps of size 1 by marking flanking 1s to 7 and propagating to uniform adjacent columns. Part of gap-bridging rule."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for j in range(cols):
        for i in range(1, rows - 1):
            if new_grid[i][j] == 0 and new_grid[i - 1][j] == 1 and new_grid[i + 1][j] == 1:
                new_grid[i - 1][j] = 7
                new_grid[i + 1][j] = 7
                # Prop left
                if j > 0:
                    vals = [new_grid[k][j - 1] for k in (i - 1, i, i + 1)]
                    if all(v == 1 for v in vals) or all(v == 0 for v in vals):
                        for k in (i - 1, i, i + 1):
                            new_grid[k][j - 1] = 7
                # Prop right
                if j < cols - 1:
                    vals = [new_grid[k][j + 1] for k in (i - 1, i, i + 1)]
                    if all(v == 1 for v in vals) or all(v == 0 for v in vals):
                        for k in (i - 1, i, i + 1):
                            new_grid[k][j + 1] = 7
    return new_grid

def handle_vertical_size2_gaps(grid: List[List[int]]) -> List[List[int]]:
    """Handle vertical gaps of size 2 by marking flanking 1s to 7 and propagating to uniform adjacent columns. Part of gap-bridging rule."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for j in range(cols):
        for i in range(1, rows - 2):
            if new_grid[i - 1][j] == 1 and new_grid[i][j] == 0 and new_grid[i + 1][j] == 0 and new_grid[i + 2][j] == 1:
                new_grid[i - 1][j] = 7
                new_grid[i + 2][j] = 7
                # Prop left
                if j > 0:
                    vals = [new_grid[k][j - 1] for k in range(i - 1, i + 3)]
                    if all(v == 1 for v in vals) or all(v == 0 for v in vals):
                        for k in range(i - 1, i + 3):
                            new_grid[k][j - 1] = 7
                # Prop right
                if j < cols - 1:
                    vals = [new_grid[k][j + 1] for k in range(i - 1, i + 3)]
                    if all(v == 1 for v in vals) or all(v == 0 for v in vals):
                        for k in range(i - 1, i + 3):
                            new_grid[k][j + 1] = 7
    return new_grid

def handle_vertical_edge_gaps(grid: List[List[int]]) -> List[List[int]]:
    """Handle size-1 vertical gaps at top/bottom edges by marking adjacent 1s to 7 and propagating. Addresses edge cases in gap rule."""
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    new_grid = [row[:] for row in grid]
    for j in range(cols):
        # Top edge
        if rows >= 2 and new_grid[0][j] == 0 and new_grid[1][j] == 1:
            new_grid[1][j] = 7
            # Prop left
            if j > 0:
                vals = [new_grid[k][j - 1] for k in (0, 1)]
                if len(set(vals)) == 1:
                    for k in (0, 1):
                        new_grid[k][j - 1] = 7
            # Prop right
            if j < cols - 1:
                vals = [new_grid[k][j + 1] for k in (0, 1)]
                if len(set(vals)) == 1:
                    for k in (0, 1):
                        new_grid[k][j + 1] = 7
        # Bottom edge
        if rows >= 2 and new_grid[rows - 2][j] == 1 and new_grid[rows - 1][j] == 0:
            new_grid[rows - 2][j] = 7
            # Prop left
            if j > 0:
                vals = [new_grid[k][j - 1] for k in (rows - 2, rows - 1)]
                if len(set(vals)) == 1:
                    for k in (rows - 2, rows - 1):
                        new_grid[k][j - 1] = 7
            # Prop right
            if j < cols - 1:
                vals = [new_grid[k][j + 1] for k in (rows - 2, rows - 1)]
                if len(set(vals)) == 1:
                    for k in (rows - 2, rows - 1):
                        new_grid[k][j + 1] = 7
    return new_grid

def handle_vertical_gaps(grid: List[List[int]]) -> List[List[int]]:
    """Compose vertical gap handling: edges, size1, size2. Implements vertical gap-bridging observation."""
    grid1 = handle_vertical_edge_gaps(grid)
    grid2 = handle_vertical_size1_gaps(grid1)
    return handle_vertical_size2_gaps(grid2)

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: remove isolated, handle horizontal and vertical gaps in passes to propagate markings. Matches gap-filling and boundary marking patterns."""
    grid = remove_isolated(g)
    grid = handle_horizontal_gaps(grid)
    grid = handle_vertical_gaps(grid)
    grid = handle_horizontal_gaps(grid)
    grid = handle_vertical_gaps(grid)
    return grid
```