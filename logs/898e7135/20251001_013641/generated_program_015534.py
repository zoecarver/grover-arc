```python
from typing import List, Tuple
from collections import deque, Counter

def identify_background(g: List[List[int]]) -> int:
    counts = Counter()
    for row in g:
        for cell in row:
            if cell != 0:
                counts[cell] += 1
    return max(counts, key=counts.get) if counts else 0

def flood_fill(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]], color: int) -> List[Tuple[int, int]]:
    rows, cols = len(g), len(g[0])
    queue = deque([(sr, sc)])
    visited[sr][sc] = True
    component = [(sr, sc)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                visited[nr][nc] = True
                queue.append((nr, nc))
                component.append((nr, nc))
    return component

def get_h_w(positions: List[Tuple[int, int]]) -> Tuple[int, int]:
    if not positions:
        return 0, 0
    max_r = max(r for r, c in positions)
    max_c = max(c for r, c in positions)
    return max_r + 1, max_c + 1

def normalize_shape(color: int, positions: List[Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    if not positions:
        return color, []
    min_r = min(r for r, c in positions)
    min_c = min(c for r, c in positions)
    positions = [(r - min_r, c - min_c) for r, c in positions]
    h, w = get_h_w(positions)
    if h > w:
        positions = [(c, h - 1 - r) for r, c in positions]
        h, w = w, h
    positions = [(h - 1 - r, c) for r, c in positions]
    half = h // 2
    bottom_left = sum(1 for r, c in positions if r >= half and c < w // 2)
    bottom_right = sum(1 for r, c in positions if r >= half and c >= w // 2)
    if bottom_right > bottom_left:
        positions = [(r, w - 1 - c) for r, c in positions]
    min_r = min(r for r, c in positions)
    min_c = min(c for r, c in positions)
    positions = [(r - min_r, c - min_c) for r, c in positions]
    return color, positions

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    bg = identify_background(g)
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    shapes = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != 0 and g[r][c] != bg and not visited[r][c]:
                color = g[r][c]
                component = flood_fill(g, r, c, visited, color)
                if len(component) >= 4:
                    shapes.append((color, component))
    shapes.sort(key=lambda x: min(r for r, c in x[1]))
    normalized_shapes = [normalize_shape(color, pos) for color, pos in shapes]
    if not normalized_shapes:
        return [[bg]]
    max_h = max(get_h_w(pos)[0] for _, pos in normalized_shapes)
    total_w = sum(get_h_w(pos)[1] for _, pos in normalized_shapes)
    inner = [[bg for _ in range(total_w)] for _ in range(max_h)]
    current_x = 0
    for color, pos in normalized_shapes:
        _, w_s = get_h_w(pos)
        for r, c in pos:
            inner[r][current_x + c] = color
        current_x += w_s
    out_h = max_h + 2
    out_w = total_w + 2
    out = [[bg for _ in range(out_w)] for _ in range(out_h)]
    for i in range(max_h):
        for j in range(total_w):
            out[i + 1][j + 1] = inner[i][j]
    if out_h < out_w:
        extra = out_w - out_h
        half = extra // 2
        new_out = [[bg for _ in range(out_w)] for _ in range(out_w)]
        for i in range(out_h):
            for j in range(out_w):
                new_out[i + half][j] = out[i][j]
        out = new_out
    elif out_w < out_h:
        extra = out_h - out_w
        half = extra // 2
        new_out = [[bg for _ in range(out_h)] for _ in range(out_h)]
        for i in range(out_h):
            for j in range(out_w):
                new_out[i][j + half] = out[i][j]
        out = new_out
    return out
```