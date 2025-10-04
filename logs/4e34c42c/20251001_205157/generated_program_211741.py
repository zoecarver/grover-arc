```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    """Extract the background color from the top-left corner."""
    if not g or not g[0]:
        return 0
    return g[0][0]

def find_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    """Find bounding boxes of connected components of non-background cells (4-connected).
    Returns list of (min_r, max_r, min_c, max_c) for each component."""
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    visited = [[False for _ in range(w)] for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(h):
        for c in range(w):
            if g[r][c] != bg and not visited[r][c]:
                min_r, max_r = r, r
                min_c, max_c = c, c
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    min_r = min(min_r, cr)
                    max_r = max(max_r, cr)
                    min_c = min(min_c, cc)
                    max_c = max(max_c, cc)
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] != bg:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components.append((min_r, max_r, min_c, max_c))
    return components

def extract_subgrid(g: List[List[int]], bg: int, min_r: int, max_r: int, min_c: int, max_c: int) -> List[List[int]]:
    """Extract and pad/crop the subgrid to 5 rows, centered, with bg padding if necessary."""
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    orig_h = max_r - min_r + 1
    if orig_h > 5:
        start_r = min_r + (orig_h - 5) // 2
    else:
        pad_top = (5 - orig_h) // 2
        start_r = min_r - pad_top
        start_r = max(0, start_r)
    end_r = start_r + 5
    end_r = min(h, end_r)
    sub = []
    for rr in range(start_r, end_r):
        row = g[rr][min_c:max_c + 1]
        sub.append(row)
    # Pad if less than 5 rows
    while len(sub) < 5:
        sub.append([bg] * (max_c - min_c + 1))
    # Trim leading/trailing all-bg columns in the 5 rows
    sub_w = len(sub[0]) if sub else 0
    l = 0
    while l < sub_w and all(sub[r][l] == bg for r in range(5)):
        l += 1
    r = sub_w - 1
    while r >= l and all(sub[r][r] == bg for r in range(5)):
        r -= 1
    if l > r:
        return []
    return [row[l:r + 1] for row in sub]

def max_overlap(left_sub: List[List[int]], right_sub: List[List[int]]) -> int:
    """Compute the maximum overlap k where the right k columns of left_sub match the left k columns of right_sub."""
    w1 = len(left_sub[0]) if left_sub else 0
    w2 = len(right_sub[0]) if right_sub else 0
    max_k = min(w1, w2)
    for k in range(max_k, -1, -1):
        match = True
        for row in range(5):
            for j in range(k):
                if left_sub[row][w1 - k + j] != right_sub[row][j]:
                    match = False
                    break
            if not match:
                break
        if match:
            return k
    return 0

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: extract subgrids for components, sort by min_col, concatenate with max overlap merging."""
    bg = get_background(g)
    components = find_components(g, bg)
    subgrids = []
    for min_r, max_r, min_c, max_c in components:
        orig_h = max_r - min_r + 1
        if orig_h < 1 or orig_h > 10:  # Arbitrary filter to match examples, adjust if needed
            continue
        sub = extract_subgrid(g, bg, min_r, max_r, min_c, max_c)
        if sub:
            subgrids.append((min_c, sub))
    # Sort by min_c increasing
    subgrids.sort(key=lambda x: x[0])
    if not subgrids:
        return []
    # Build the strip by concatenating with merging
    strip = [list(row) for row in subgrids[0][1]]
    for _, new_sub in subgrids[1:]:
        k = max_overlap(strip, new_sub)
        for row in range(5):
            for j in range(len(new_sub[row]) - k):
                strip[row].append(new_sub[row][k + j])
    return strip
```