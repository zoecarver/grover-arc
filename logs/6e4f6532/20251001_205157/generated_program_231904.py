```python
from typing import List, Tuple
from collections import Counter, defaultdict

def get_background(g: List[List[int]]) -> int:
    """Rule: Background is 0 if present, else the most frequent color."""
    flat = [cell for row in g for cell in row]
    if 0 in flat:
        return 0
    count = Counter(flat)
    return count.most_common(1)[0][0] if count else 0

def find_blobs(g: List[List[int]], background: int) -> List[List[Tuple[int, int, int]]]:
    """Rule: Find connected components (4-way) of non-background cells, regardless of color, including positions and values."""
    height = len(g)
    if height == 0:
        return []
    width = len(g[0])
    visited = [[False] * width for _ in range(height)]
    blobs = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(height):
        for j in range(width):
            if not visited[i][j] and g[i][j] != background:
                blob = []
                stack = [(i, j, g[i][j])]
                visited[i][j] = True
                while stack:
                    x, y, num = stack.pop()
                    blob.append((x, y, num))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny] and g[nx][ny] != background:
                            visited[nx][ny] = True
                            stack.append((nx, ny, g[nx][ny]))
                if blob:
                    blobs.append(blob)
    return blobs

def sort_blobs(blobs: List[List[Tuple[int, int, int]]]) -> List[List[Tuple[int, int, int]]]:
    """Rule: Sort blobs bottom-to-top by maximum row index for sequential processing."""
    def get_max_row(blob: List[Tuple[int, int, int]]) -> int:
        return max(x for x, _, _ in blob)
    return sorted(blobs, key=get_max_row, reverse=True)

def compute_drop_distance(blob: List[Tuple[int, int, int]], g: List[List[int]], bg: int) -> int:
    """Rule: Compute rigid drop distance as minimum consecutive background cells below the lowest point in each column of the blob."""
    h = len(g)
    col_low = defaultdict(int)
    for x, y, _ in blob:
        col_low[y] = max(col_low[y], x)
    min_d = float('inf')
    for y, low in col_low.items():
        d = 0
        r = low + 1
        while r < h and g[r][y] == bg:
            d += 1
            r += 1
        min_d = min(min_d, d)
    return min_d

def drop_and_place(g: List[List[int]], blob: List[Tuple[int, int, int]], d: int, bg: int) -> List[List[int]]:
    """Rule: Clear original blob positions to background, then place the blob shifted down by d rows (clip if out of bounds)."""
    h = len(g)
    new_g = [row[:] for row in g]
    # Clear original
    for x, y, _ in blob:
        new_g[x][y] = bg
    # Place shifted
    for x, y, num in blob:
        new_x = x + d
        if 0 <= new_x < h:
            new_g[new_x][y] = num
    return new_g

def apply_gravity(g: List[List[int]], bg: int) -> List[List[int]]:
    """Rule: Apply downward gravity to non-background connected blobs as rigid units, processing from bottom to top with clearing for accurate spacing."""
    blobs = find_blobs(g, bg)
    if not blobs:
        return g
    sorted_blobs = sort_blobs(blobs)
    current_g = [row[:] for row in g]
    for blob in sorted_blobs:
        temp_g = [row[:] for row in current_g]
        # Temporarily clear for computation
        for x, y, _ in blob:
            temp_g[x][y] = bg
        d = compute_drop_distance(blob, temp_g, bg)
        # Place on temporary (already cleared) shifted
        temp_g = drop_and_place(temp_g, blob, d, bg)
        current_g = temp_g
    return current_g

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    return apply_gravity(g, bg)
```