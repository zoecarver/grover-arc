```python
from typing import List, Tuple
from collections import Counter, defaultdict

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [g[i][j] for i in range(len(g)) for j in range(len(g[0]))]
    count = Counter(flat)
    return count.most_common(1)[0][0] if count else 0

def find_blobs(g: List[List[int]], background: int) -> List[List[Tuple[int, int, int]]]:
    height = len(g)
    width = len(g[0]) if height > 0 else 0
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
    def get_max_row(blob: List[Tuple[int, int, int]]) -> int:
        return max(i for i, _, _ in blob)
    return sorted(blobs, key=get_max_row, reverse=True)

def compute_drop_distance(blob: List[Tuple[int, int, int]], g: List[List[int]], background: int, height: int) -> int:
    cols = set(j for _, j, _ in blob)
    if not cols:
        return 0
    ds = []
    for j in cols:
        max_i_for_col = max(i for i, jj, _ in blob if jj == j)
        d = 0
        r = max_i_for_col + 1
        while r < height and g[r][j] == background:
            d += 1
            r += 1
        ds.append(d)
    return min(ds) if ds else 0

def place_blob(g: List[List[int]], blob: List[Tuple[int, int, int]], d: int, background: int, height: int) -> None:
    to_place = []
    for i, j, num in blob:
        new_i = i + d
        if new_i < height:
            to_place.append((new_i, j, num))
    for i, j, num in to_place:
        g[i][j] = num

def apply_gravity(g: List[List[int]], sorted_blobs: List[List[Tuple[int, int, int]]], background: int) -> List[List[int]]:
    height = len(g)
    width = len(g[0]) if height > 0 else 0
    new_g = [row[:] for row in g]
    for blob in sorted_blobs:
        # Clear the blob
        for i, j, _ in blob:
            new_g[i][j] = background
        # Compute drop distance
        drop_d = compute_drop_distance(blob, new_g, background, height)
        # Place the blob
        place_blob(new_g, blob, drop_d, background, height)
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    background = get_background(g)
    blobs = find_blobs(g, background)
    sorted_blobs = sort_blobs(blobs)
    return apply_gravity(g, sorted_blobs, background)
```