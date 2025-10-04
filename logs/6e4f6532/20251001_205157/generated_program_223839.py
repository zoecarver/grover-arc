```python
from typing import List
from collections import Counter

def find_dominant_color(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_bounding_box(g: List[List[int]], color: int) -> tuple:
    rows = len(g)
    if rows == 0:
        return 0, -1, 0, -1
    cols = len(g[0])
    min_r = rows
    max_r = -1
    min_c = cols
    max_c = -1
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == color:
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    return min_r, max_r, min_c, max_c

def fill_small_components(g: List[List[int]], dominant: int, bbox: tuple, threshold: int = 10) -> List[List[int]]:
    out = [row[:] for row in g]
    min_r, max_r, min_c, max_c = bbox
    if max_r < min_r:
        return out
    rows = len(g)
    cols = len(g[0])
    visited = set()
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) not in visited and g[r][c] != dominant:
                component = []
                stack = [(r, c)]
                visited.add((r, c))
                while stack:
                    cr, cc = stack.pop()
                    component.append((cr, cc))
                    for dr, dc in directions:
                        nr = cr + dr
                        nc = cc + dc
                        if min_r <= nr <= max_r and min_c <= nc <= max_c and 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and g[nr][nc] != dominant:
                            visited.add((nr, nc))
                            stack.append((nr, nc))
                size = len(component)
                if size < threshold:
                    for pr, pc in component:
                        out[pr][pc] = dominant
    return out

def move_maroon_toward_center(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    # Simple shift for maroon (8) toward center: move right by 5 columns if possible, for new approach
    rows = len(g)
    if rows == 0:
        return out
    cols = len(g[0])
    shift = 5
    for r in range(rows):
        for c in range(cols - shift):
            if g[r][c] == 8:
                out[r][c + shift] = 8
                out[r][c] = 0  # Clear original, assuming 0 is neutral; adjust if needed
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    dominant = find_dominant_color(g)
    bbox = get_bounding_box(g, dominant)
    out = fill_small_components(g, dominant, bbox)
    out = move_maroon_toward_center(out)
    return out
```