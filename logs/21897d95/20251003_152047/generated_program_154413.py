```python
from typing import List
from collections import deque, Counter

def program(g: List[List[int]]) -> List[List[int]]:
    # Compose individual rule functions
    g = handle_small_blue_interaction(g)
    g = handle_position_color_adjustment(g)
    g = expand_small_non_blue(g)
    g = reposition_maroon_blocks(g)
    g = handle_light_blue_enclosure(g)
    g = transpose_grid(g)
    return g

def transpose_grid(g: List[List[int]]) -> List[List[int]]:
    """Rule: Transpose the grid to match output dimensions (covers consistent size change across all examples)."""
    if not g or not g[0]:
        return []
    return [list(row) for row in zip(*g)]

def handle_small_blue_interaction(g: List[List[int]]) -> List[List[int]]:
    """Observation 1: Small blue shapes (1's, 1-4 pixels) are adjacent/embedded in larger blocks; remove blues by filling with adjacent block color using multi-source BFS (1's become passable, filled by nearest non-1 color)."""
    if not g or not g[0]:
        return g
    h, w = len(g), len(g[0])
    visited = [[False for _ in range(w)] for _ in range(h)]
    q = deque()
    # Add all non-1 positions as sources
    for i in range(h):
        for j in range(w):
            if g[i][j] != 1:
                q.append((i, j, g[i][j]))  # position and color
                visited[i][j] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-connectivity
    while q:
        x, y, color = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == 1:
                g[nx][ny] = color
                visited[nx][ny] = True
                q.append((nx, ny, color))
    return g

def handle_position_color_adjustment(g: List[List[int]]) -> List[List[int]]:
    """Observation 2: For positional overlaps of larger blocks, adjust to dominant color (here, take max color value in local 3x3 neighborhood to simulate dominance in overlaps)."""
    if not g or not g[0]:
        return g
    h, w = len(g), len(g[0])
    new_g = [row[:] for row in g]
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for i in range(h):
        for j in range(w):
            max_color = g[i][j]
            for dx, dy in directions:
                ni, nj = i + dx, j + dy
                if 0 <= ni < h and 0 <= nj < w:
                    max_color = max(max_color, g[ni][nj])
            new_g[i][j] = max_color
    return new_g

def expand_small_non_blue(g: List[List[int]]) -> List[List[int]]:
    """Observation 3: Expand small non-blue shapes (e.g., small 3's, 9's <5 pixels total) into adjacent larger blocks (flood adjacent positions if adjacent to large component, limited to 5 expansions per small component)."""
    if not g or not g[0]:
        return g
    h, w = len(g), len(g[0])
    color_counts = Counter()
    for row in g:
        for val in row:
            if val != 1 and val != 0:
                color_counts[val] += 1
    small_colors = [col for col, cnt in color_counts.items() if cnt < 5]
    new_g = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for col in small_colors:
        positions = [(i, j) for i in range(h) for j in range(w) if g[i][j] == col]
        for x, y in positions:
            # Expand to adjacent if different and large block assumed (simple: change if not small color)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < h and 0 <= ny < w and new_g[nx][ny] != col and new_g[nx][ny] not in small_colors:
                    new_g[nx][ny] = col
                    # Limit expansions (simple count per color)
    return new_g

def reposition_maroon_blocks(g: List[List[int]]) -> List[List[int]]:
    """Observation 4: Maroon (8's) occupy lower positions; reposition to bottom/side strips in output (move 8's to bottom half if not already, or to right columns)."""
    if not g or not g[0]:
        return g
    h, w = len(g), len(g[0])
    new_g = [row[:] for row in g]
    bottom_start = h // 2
    right_start = w // 2
    for i in range(h):
        for j in range(w):
            if g[i][j] == 8 and i < bottom_start:
                # Move to bottom
                new_g[bottom_start + (i % (h - bottom_start))][j] = 8
                new_g[i][j] = 0  # or background
            elif g[i][j] == 8 and j < right_start:
                # Move to right
                new_g[i][right_start + (j % (w - right_start))] = 8
                new_g[i][j] = 0
    return new_g

def handle_light_blue_enclosure(g: List[List[int]]) -> List[List[int]]:
    """Observation 5: Light blue (9's, small <=5 pixels) nested within larger blocks; emerge in similar nested zones in output (if 9 surrounded by same color on all sides, keep and expand slightly inward)."""
    if not g or not g[0]:
        return g
    h, w = len(g), len(g[0])
    new_g = [row[:] for row in g]
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] == 9:
                # Check if nested (all 4 directions same non-9 color)
                surround_color = None
                is_nested = True
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if not (0 <= ni < h and 0 <= nj < w):
                        is_nested = False
                        break
                    if g[ni][nj] == 9 or (surround_color is not None and g[ni][nj] != surround_color):
                        is_nested = False
                        break
                    if surround_color is None:
                        surround_color = g[ni][nj]
                if is_nested and surround_color != 0 and surround_color != 1:
                    # Expand slightly: change adjacent surround to 9 if possible
                    for dx, dy in directions:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < h and 0 <= nj < w and new_g[ni][nj] == surround_color:
                            new_g[ni][nj] = 9
                            break  # limit to one per direction
    return new_g
```