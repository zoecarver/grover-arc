```python
from collections import Counter, deque
from typing import List, Tuple

def identify_background_color(grid: List[List[int]]) -> int:
    """Rule: Background is the most frequent color in the grid."""
    if not grid:
        return 0
    flat_grid = [cell for row in grid for cell in row]
    if not flat_grid:
        return 0
    return Counter(flat_grid).most_common(1)[0][0]

def is_non_background(cell: int, background_color: int) -> bool:
    """Observation: A cell is foreground if its color differs from background."""
    return cell != background_color

def get_grid_dimensions(grid: List[List[int]]) -> Tuple[int, int]:
    """Rule: Grid has rows and columns from input shape."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    return rows, cols

def initialize_visited(rows: int, cols: int) -> List[List[bool]]:
    """Rule: Track visited cells with a matrix initialized to False."""
    return [[False] * cols for _ in range(rows)]

def get_four_directions() -> List[Tuple[int, int]]:
    """Observation: Connectivity is 4-way (up, down, left, right)."""
    return [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid_position(nr: int, nc: int, rows: int, cols: int) -> bool:
    """Rule: Position is valid if within grid bounds."""
    return 0 <= nr < rows and 0 <= nc < cols

def find_single_blob(grid: List[List[int]], start_r: int, start_c: int, background_color: int, visited: List[List[bool]]) -> List[Tuple[int, int]]:
    """Rule: A blob is a 4-connected group of same-color non-background cells, found via BFS."""
    rows, cols = get_grid_dimensions(grid)
    directions = get_four_directions()
    color = grid[start_r][start_c]
    if not is_non_background(color, background_color):
        return []
    blob = []
    queue = deque([(start_r, start_c)])
    visited[start_r][start_c] = True
    while queue:
        cr, cc = queue.popleft()
        blob.append((cr, cc))
        for dr, dc in directions:
            nr, nc = cr + dr, cc + dc
            if is_valid_position(nr, nc, rows, cols) and not visited[nr][nc] and grid[nr][nc] == color:
                visited[nr][nc] = True
                queue.append((nr, nc))
    return blob

def find_all_blobs(grid: List[List[int]], background_color: int) -> List[List[Tuple[int, int]]]:
    """Composition: Discover all blobs by starting BFS from each unvisited non-background cell."""
    rows, cols = get_grid_dimensions(grid)
    visited = initialize_visited(rows, cols)
    blobs = []
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and is_non_background(grid[r][c], background_color):
                blob = find_single_blob(grid, r, c, background_color, visited)
                if blob:
                    blobs.append(blob)
    return blobs

def get_top_left_position(blob: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Rule: Spatial order key is min row, then min col in that row (top-left of bounding box top)."""
    if not blob:
        return (float('inf'), float('inf'))
    min_r = min(r for r, c in blob)
    min_c = min(c for r, c in blob if r == min_r)
    return (min_r, min_c)

def sort_blobs_spatially(blobs: List[List[Tuple[int, int]]]) -> List[List[Tuple[int, int]]]:
    """Rule: Sort blobs top-to-bottom, then left-to-right using top-left positions."""
    return sorted(blobs, key=get_top_left_position)

def sort_positions_row_major(positions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Observation: Within a blob, order cells by row then column (row-major)."""
    return sorted(positions, key=lambda p: (p[0], p[1]))

def extract_blob_sequence(grid: List[List[int]], blob: List[Tuple[int, int]]) -> List[int]:
    """Rule: Extract colors from blob positions in row-major order."""
    sorted_pos = sort_positions_row_major(blob)
    return [grid[r][c] for r, c in sorted_pos]

def concatenate_all_sequences(grid: List[List[int]], sorted_blobs: List[List[Tuple[int, int]]]) -> List[int]:
    """Composition: Concatenate row-major sequences from all sorted blobs."""
    sequence = []
    for blob in sorted_blobs:
        sequence.extend(extract_blob_sequence(grid, blob))
    return sequence

def reshape_to_vertical(sequence: List[int]) -> List[List[int]]:
    """Rule: Output is a vertical column, each color in a single-element row."""
    return [[color] for color in sequence]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main composition: Identify background, find and sort blobs, extract and reshape sequence."""
    bg = identify_background_color(g)
    blobs = find_all_blobs(g, bg)
    sorted_blobs = sort_blobs_spatially(blobs)
    flat_sequence = concatenate_all_sequences(g, sorted_blobs)
    return reshape_to_vertical(flat_sequence)
```