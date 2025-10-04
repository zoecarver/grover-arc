```python
from typing import List
from collections import Counter, deque

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = Counter(flat)
    return count.most_common(1)[0][0]

def flood_fill_for_color(g: List[List[int]], color: int, background: int) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    h = [row[:] for row in g]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if h[r][c] == color:
                q.append((r, c))
                visited[r][c] = True
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while q:
        r, c = q.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and h[nr][nc] == background:
                h[nr][nc] = color
                visited[nr][nc] = True
                q.append((nr, nc))
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    background = find_background(g)
    flat = [cell for row in g for cell in row]
    colors = sorted(set(flat) - {background})
    h = [row[:] for row in g]
    for color in colors:
        h = flood_fill_for_color(h, color, background)
    return h
```