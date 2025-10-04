```python
from collections import Counter, deque
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = Counter(flat)
    return count.most_common(1)[0][0]

def get_structure(g: List[List[int]], background: int) -> int:
    flat = [cell for row in g for cell in row if cell != background]
    count = Counter(flat)
    if not count:
        return None
    return count.most_common(1)[0][0]

def get_selected(g: List[List[int]], background: int, structure: int) -> int:
    h = len(g)
    w = len(g[0])
    adj_colors = set()
    for i in range(h):
        for j in range(w):
            if g[i][j] == structure:
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < h and 0 <= nj < w and g[ni][nj] != background and g[ni][nj] != structure:
                        adj_colors.add(g[ni][nj])
    if adj_colors:
        # Select the first adjacent color (arbitrary order, but consistent with examples)
        return min(adj_colors)
    # Fallback: smallest non-background, non-structure color
    flat = [cell for row in g for cell in row if cell != background and cell != structure]
    if not flat:
        return None
    count = Counter(flat)
    return count.most_common()[-1][0]  # least common

def get_bbox(g: List[List[int]], color: int) -> Tuple[int, int, int, int]:
    h = len(g)
    w = len(g[0])
    min_i = h
    max_i = -1
    min_j = w
    max_j = -1
    for i in range(h):
        for j in range(w):
            if g[i][j] == color:
                min_i = min(min_i, i)
                max_i = max(max_i, i)
                min_j = min(min_j, j)
                max_j = max(max_j, j)
    if min_i == h:
        return None
    return min_i, max_i, min_j, max_j

def flood_fill_in_bbox(out: List[List[int]], selected: int, background: int, bbox: Tuple[int, int, int, int]):
    if not bbox:
        return
    min_i, max_i, min_j, max_j = bbox
    h = len(out)
    w = len(out[0])
    visited = [[False] * w for _ in range(h)]
    q = deque()
    # Enqueue all selected cells in bbox
    for i in range(min_i, max_i + 1):
        for j in range(min_j, max_j + 1):
            if out[i][j] == selected and not visited[i][j]:
                q.append((i, j))
                visited[i][j] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        i, j = q.popleft()
        for di, dj in directions:
            ni = i + di
            nj = j + dj
            if (min_i <= ni <= max_i and min_j <= nj <= max_j and
                0 <= ni < h and 0 <= nj < w and not visited[ni][nj] and
                out[ni][nj] == background):
                out[ni][nj] = selected
                visited[ni][nj] = True
                q.append((ni, nj))

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h = len(g)
    w = len(g[0])
    background = get_background(out)
    structure = get_structure(out, background)
    if structure is None:
        return out
    selected = get_selected(out, background, structure)
    if selected is None:
        return out
    # Get bbox for structure
    bbox_s = get_bbox(out, structure)
    # Get bbox for selected
    bbox_sel = get_bbox(out, selected)
    # Combine bboxes
    min_i = h
    max_i = -1
    min_j = w
    max_j = -1
    if bbox_s:
        min_i = min(min_i, bbox_s[0])
        max_i = max(max_i, bbox_s[1])
        min_j = min(min_j, bbox_s[2])
        max_j = max(max_j, bbox_s[3])
    if bbox_sel:
        min_i = min(min_i, bbox_sel[0])
        max_i = max(max_i, bbox_sel[1])
        min_j = min(min_j, bbox_sel[2])
        max_j = max(max_j, bbox_sel[3])
    if min_i > max_i or min_j > max_j:
        return out
    # Slightly expand bbox for boundary cases
    min_i = max(0, min_i - 1)
    max_i = min(h - 1, max_i + 1)
    min_j = max(0, min_j - 1)
    max_j = min(w - 1, max_j + 1)
    bbox = (min_i, max_i, min_j, max_j)
    flood_fill_in_bbox(out, selected, background, bbox)
    return out
```