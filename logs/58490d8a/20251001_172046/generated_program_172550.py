```python
from typing import List

def most_common(g: List[List[int]]) -> int:
    count = {}
    for row in g:
        for val in row:
            count[val] = count.get(val, 0) + 1
    return max(count, key=count.get)

def find_canvas_bounds(g: List[List[int]]) -> tuple:
    n = len(g)
    m = len(g[0])
    min_r = n
    max_r = -1
    min_c = m
    max_c = -1
    for i in range(n):
        for j in range(m):
            if g[i][j] == 0:
                min_r = min(min_r, i)
                max_r = max(max_r, i)
                min_c = min(min_c, j)
                max_c = max(max_c, j)
    return min_r, max_r, min_c, max_c

def count_components(g: List[List[int]], color: int, min_r: int, max_r: int, min_c: int, max_c: int) -> int:
    n = len(g)
    m = len(g[0])
    visited = [[False] * m for _ in range(n)]
    count = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] == color and not visited[i][j] and not (min_r <= i <= max_r and min_c <= j <= max_c):
                count += 1
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx = x + dx
                            ny = y + dy
                            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and g[nx][ny] == color and not (min_r <= nx <= max_r and min_c <= ny <= max_c):
                                visited[nx][ny] = True
                                stack.append((nx, ny))
    return count

def program(g: List[List[int]]) -> List[List[int]]:
    bg = most_common(g)
    min_r, max_r, min_c, max_c = find_canvas_bounds(g)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    out = [[0] * w for _ in range(h)]
    for sub_r in range(h):
        row_colors = set()
        gr = min_r + sub_r
        for sub_c in range(w):
            gc = min_c + sub_c
            val = g[gr][gc]
            if val != 0 and val != bg:
                row_colors.add(val)
        if row_colors:
            color = next(iter(row_colors))
            num = count_components(g, color, min_r, max_r, min_c, max_c)
            for k in range(num):
                pos = 2 * k + 1
                if pos < w:
                    out[sub_r][pos] = color
    return out
```