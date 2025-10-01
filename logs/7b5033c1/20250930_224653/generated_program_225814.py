```python
from collections import Counter, deque
from typing import List, Tuple

def identify_background_color(grid: List[List[int]]) -> int:
    """Identifies the most frequent color as background."""
    flat_grid = [cell for row in grid for cell in row]
    color_counts = Counter(flat_grid)
    return color_counts.most_common(1)[0][0]

def find_all_blobs(grid: List[List[int]], background_color: int) -> List[List[Tuple[int, int]]]:
    """Finds all 4-connected same-color non-background blobs using BFS."""
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    blobs = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-connected
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
                if blob:  # Only add non-empty blobs
                    blobs.append(blob)
    return blobs

def get_min_position(blob: List[Tuple[int, int]]) -> Tuple[int, int]:
    """Gets min (row, col) for sorting blobs spatially."""
    min_r = min(r for r, c in blob)
    min_c = min(c for r, c in blob)
    return (min_r, min_c)

def sort_blobs(blobs: List[List[Tuple[int, int]]]) -> List[List[Tuple[int, int]]]:
    """Sorts blobs by min position for top-to-bottom, left-to-right order."""
    return sorted(blobs, key=get_min_position)

def extract_sequence_from_blob(grid: List[List[int]], blob: List[Tuple[int, int]]) -> List[int]:
    """Extracts colors from blob in row-major order."""
    sorted_positions = sorted(blob, key=lambda p: (p[0], p[1]))
    return [grid[r][c] for r, c in sorted_positions]

def concatenate_blob_sequences(blobs: List[List[Tuple[int, int]]], grid: List[List[int]]) -> List[int]:
    """Concatenates the extracted sequences from all sorted blobs."""
    sorted_blobs = sort_blobs(blobs)
    sequence = []
    for blob in sorted_blobs:
        sequence.extend(extract_sequence_from_blob(grid, blob))
    return sequence

def reshape_to_vertical_column(sequence: List[int]) -> List[List[int]]:
    """Reshapes the flat sequence into a vertical single-column grid."""
    return [[color] for color in sequence]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: identifies background, finds and sorts blobs, extracts and concatenates sequences, reshapes to vertical column."""
    bg = identify_background_color(g)
    blobs = find_all_blobs(g, bg)
    flat_sequence = concatenate_blob_sequences(blobs, g)
    return reshape_to_vertical_column(flat_sequence)
```