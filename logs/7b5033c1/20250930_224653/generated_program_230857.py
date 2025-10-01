```python
from collections import Counter, deque
from typing import List, Tuple

def identify_background_color(grid: List[List[int]]) -> int:
    """Identifies the background color as the most frequent color in the grid."""
    if not grid or not grid[0]:
        return 0
    flat_grid = [cell for row in grid for cell in row]
    color_counts = Counter(flat_grid)
    return color_counts.most_common(1)[0][0]

def find_all_blobs(grid: List[List[int]], background_color: int) -> List[List[Tuple[int, int]]]:
    """Finds all 4-connected components of same-color non-background cells using BFS."""
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    blobs = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != background_color and not visited[r][c]:
                blob = []
                queue = deque([(r, c)])
                visited[r][c] = True
                color = grid[r][c]
                while queue:
                    cr, cc = queue.popleft()
                    blob.append((cr, cc))
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == color:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                if blob:
                    blobs.append(blob)
    return blobs

def get_top_left_position(blob: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Computes the top-left position (min row, then min col in that row) for sorting blobs."""
    if not blob:
        return (float('inf'), float('inf'))
    min_r = min(r for r, c in blob)
    min_c = min(c for r, c in blob if r == min_r)
    return (min_r, min_c)

def sort_blobs_by_top_left(blobs: List[List[Tuple[int, int]]]) -> List[List[Tuple[int, int]]]:
    """Sorts blobs by top-left position to enforce reading order."""
    return sorted(blobs, key=get_top_left_position)

def extract_row_major_sequence_from_blob(grid: List[List[int]], blob: List[Tuple[int, int]]) -> List[int]:
    """Extracts colors from a blob in row-major order."""
    if not blob:
        return []
    sorted_positions = sorted(blob, key=lambda p: (p[0], p[1]))
    return [grid[r][c] for r, c in sorted_positions]

def concatenate_sequences_from_sorted_blobs(grid: List[List[int]], blobs: List[List[Tuple[int, int]]]) -> List[int]:
    """Concatenates row-major sequences from all sorted blobs."""
    sorted_blobs = sort_blobs_by_top_left(blobs)
    sequence = []
    for blob in sorted_blobs:
        sequence.extend(extract_row_major_sequence_from_blob(grid, blob))
    return sequence

def reshape_to_vertical_column(sequence: List[int]) -> List[List[int]]:
    """Reshapes a flat sequence into a vertical single-column grid."""
    return [[color] for color in sequence]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: identifies background, finds and sorts blobs, extracts and concatenates sequences, and reshapes to vertical column."""
    bg = identify_background_color(g)
    blobs = find_all_blobs(g, bg)
    flat_sequence = concatenate_sequences_from_sorted_blobs(g, blobs)
    return reshape_to_vertical_column(flat_sequence)
```