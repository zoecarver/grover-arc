```python
from typing import List
import collections
from collections import Counter, deque

def find_background(g: List[List[int]]) -> int:
    """Identify the background color: 1 if present, else the most frequent color."""
    if not g or not g[0]:
        return 1
    flat = [cell for row in g for cell in row]
    if 1 in set(flat):
        return 1
    count = Counter(flat)
    return count.most_common(1)[0][0]

def find_non_background_components(g: List[List[int]], bg: int) -> List[tuple]:
    """Find all connected components (4-connectivity, color-blind) of non-background cells.
    Returns list of (touches_border: bool, component: List[(r, c)])."""
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(h):
        for c in range(w):
            if g[r][c] != bg and not visited[r][c]:
                component = []
                touches = (r == 0 or r == h - 1 or c == 0 or c == w - 1)
                q = deque([(r, c)])
                visited[r][c] = True
                while q:
                    cr, cc = q.popleft()
                    component.append((cr, cc))
                    touches = touches or (cr == 0 or cr == h - 1 or cc == 0 or cc == w - 1)
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != bg and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                components.append((touches, component))
    return components

def translate_and_place_component(out: List[List[int]], comp: List[tuple], g: List[List[int]], h: int, w: int, min_r: int, start_r: int, shift_c: int) -> bool:
    """Try to place the component at shifted position without overlap. Returns True if successful."""
    new_comp = []
    for r, c in comp:
        new_r = start_r + (r - min_r)
        new_c = c + shift_c
        if new_c < 0 or new_c >= w or new_r < 0 or new_r >= h or out[new_r][new_c] != g[0][0] if g else 1:  # bg approx
            return False
        new_comp.append((new_r, new_c, g[r][c]))
    for new_r, new_c, col in new_comp:
        out[new_r][new_c] = col
    return True

def redistribute_pixels(out: List[List[int]], internal_colors: List[int], h: int, w: int):
    """Place individual pixels from internal colors in row-major order at free background positions starting from top-left."""
    pos_r = 0
    pos_c = 0
    for col in sorted(internal_colors):
        while pos_r < h:
            while pos_c < w:
                bg = find_background(out)  # Recompute if needed, but approx
                if out[pos_r][pos_c] == bg:
                    out[pos_r][pos_c] = col
                    pos_c += 1
                    break
                pos_c += 1
            if pos_c < w:
                break
            pos_c = 0
            pos_r += 1
        pos_c = 0

def close_background_holes(g: List[List[int]]) -> List[List[int]]:
    """Main function to close holes in background by moving internal non-background components to touch border."""
    bg = find_background(g)
    components = find_non_background_components(g, bg)
    h = len(g)
    if h == 0:
        return g
    w = len(g[0])
    out = [row[:] for row in g]
    internal_pixels = []
    for touches, comp in components:
        if touches:
            continue
        # Fill internal with bg
        min_r = min(r for r, c in comp) if comp else 0
        min_c = min(c for r, c in comp) if comp else 0
        height = max(r for r, c in comp) - min_r + 1 if comp else 1
        shift_c = -min_c
        placed = False
        for start_r in range(h - height + 1):
            if translate_and_place_component(out, comp, g, h, w, min_r, start_r, shift_c):
                placed = True
                break
        if not placed:
            # Collect for redistribution
            internal_pixels.extend([g[r][c] for r, c in comp])
    if internal_pixels:
        redistribute_pixels(out, internal_pixels, h, w)
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    return close_background_holes(g)
```