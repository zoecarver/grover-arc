```python
from typing import List
from collections import Counter, deque, defaultdict

def get_neighbors(r: int, c: int, rows: int, cols: int) -> List[tuple[int, int]]:
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neigh = []
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neigh.append((nr, nc))
    return neigh

def has_zero_neighbor(r: int, c: int, g: List[List[int]]) -> bool:
    rows = len(g)
    cols = len(g[0])
    for nr, nc in get_neighbors(r, c, rows, cols):
        if g[nr][nc] == 0:
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    flat = [g[r][c] for r in range(rows) for c in range(cols)]
    counts = Counter(flat)
    if 0 in counts:
        del counts[0]
    if not counts:
        return []
    bg = max(counts, key=counts.get)
    visited = set()
    labels = []
    color_to_count = defaultdict(int)
    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue
            color = g[r][c]
            if color == 0 or color == bg:
                continue
            touch = False
            size = 0
            q = deque([(r, c)])
            visited.add((r, c))
            while q:
                cr, cc = q.popleft()
                size += 1
                if has_zero_neighbor(cr, cc, g):
                    touch = True
                for nr, nc in get_neighbors(cr, cc, rows, cols):
                    if g[nr][nc] == color and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        q.append((nr, nc))
            if not touch:
                color_to_count[color] += 1
            if size == 1 and touch:
                labels.append((r, c, color))
    labels.sort(key=lambda x: (x[0], x[1]))
    num_colors = len(labels)
    if num_colors == 0:
        return []
    label_col = labels[0][1]
    min_r = labels[0][0]
    left = label_col
    while left > 0 and g[min_r][left - 1] == 0:
        left -= 1
    right = label_col
    while right < cols - 1 and g[min_r][right + 1] == 0:
        right += 1
    strip_width = right - left + 1
    out_height = 2 * num_colors + 1
    out = [[0] * strip_width for _ in range(out_height)]
    for i in range(num_colors):
        pat_row = 2 * i + 1
        color = labels[i][2]
        num_d = color_to_count[color]
        for j in range(num_d):
            pos = 1 + 2 * j
            if pos < strip_width:
                out[pat_row][pos] = color
    return out
```