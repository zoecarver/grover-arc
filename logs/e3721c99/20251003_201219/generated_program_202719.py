```python
from typing import List, Tuple
from collections import deque

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return g

    # Find best horizontal sep
    max_score_h = 0
    best_r = -1
    total_fives = sum(1 for i in range(n) for j in range(n) if g[i][j] == 5)
    k = 100
    for r in range(1, n):
        above_colors = sum(1 for i in range(r) for j in range(n) if g[i][j] != 0 and g[i][j] != 5)
        above_fives = sum(1 for i in range(r) for j in range(n) if g[i][j] == 5)
        below_fives = total_fives - above_fives
        score = above_colors * below_fives - k * above_fives
        if score > max_score_h:
            max_score_h = score
            best_r = r

    # Find best vertical sep
    max_score_v = 0
    best_c = -1
    for c in range(1, n):
        left_colors = sum(1 for i in range(n) for j in range(c) if g[i][j] != 0 and g[i][j] != 5)
        left_fives = sum(1 for i in range(n) for j in range(c) if g[i][j] == 5)
        right_fives = total_fives - left_fives
        score = left_colors * right_fives - k * left_fives
        if score > max_score_v:
            max_score_v = score
            best_c = c

    if max_score_h < 0 and max_score_v < 0:
        return [row[:] for row in g]

    use_horizontal = max_score_h >= max_score_v
    if use_horizontal:
        sep_type = 'h'
        sep_index = best_r
    else:
        sep_type = 'v'
        sep_index = best_c

    # Determine legend side
    if sep_type == 'h':
        above_colors = sum(1 for i in range(sep_index) for j in range(n) if g[i][j] != 0 and g[i][j] != 5)
        below_colors = sum(1 for i in range(sep_index + 1, n) for j in range(n) if g[i][j] != 0 and g[i][j] != 5)
        legend_above = above_colors > below_colors
    else:
        left_colors = sum(1 for i in range(n) for j in range(sep_index) if g[i][j] != 0 and g[i][j] != 5)
        right_colors = sum(1 for i in range(n) for j in range(sep_index + 1, n) if g[i][j] != 0 and g[i][j] != 5)
        legend_left = left_colors > right_colors

    # Extract legend colors
    legend_colors = []
    seen = set()
    if sep_type == 'h':
        if legend_above:
            for i in range(sep_index):
                for j in range(n):
                    col_val = g[i][j]
                    if col_val != 0 and col_val != 5 and col_val not in seen:
                        seen.add(col_val)
                        legend_colors.append(col_val)
        else:
            for i in range(sep_index + 1, n):
                for j in range(n):
                    col_val = g[i][j]
                    if col_val != 0 and col_val != 5 and col_val not in seen:
                        seen.add(col_val)
                        legend_colors.append(col_val)
    else:
        if legend_left:
            for i in range(n):
                for j in range(sep_index):
                    col_val = g[i][j]
                    if col_val != 0 and col_val != 5 and col_val not in seen:
                        seen.add(col_val)
                        legend_colors.append(col_val)
        else:
            for i in range(n):
                for j in range(sep_index + 1, n):
                    col_val = g[i][j]
                    if col_val != 0 and col_val != 5 and col_val not in seen:
                        seen.add(col_val)
                        legend_colors.append(col_val)

    if not legend_colors:
        return [row[:] for row in g]

    output = [row[:] for row in g]
    visited = [[False] * n for _ in range(n)]
    component_id = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def self_fill(sr: int, sc: int, color: int) -> None:
        stack = [(sr, sc)]
        visited[sr][sc] = True
        output[sr][sc] = color
        while stack:
            x, y = stack.pop()
            for dx, dy in directions:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 5 and not visited[nx][ny]:
                    visited[nx][ny] = True
                    output[nx][ny] = color
                    stack.append((nx, ny))

    # Fill picture side
    if sep_type == 'h':
        picture_start = 0 if not legend_above else sep_index + 1
        picture_end = sep_index if not legend_above else n
        for i in range(picture_start, picture_end):
            for j in range(n):
                if g[i][j] == 5 and not visited[i][j]:
                    color = legend_colors[component_id % len(legend_colors)]
                    self_fill(i, j, color)
                    component_id += 1
    else:
        picture_start = 0 if legend_left else sep_index + 1
        picture_end = sep_index if legend_left else n
        for i in range(n):
            for j in range(picture_start, picture_end):
                if g[i][j] == 5 and not visited[i][j]:
                    color = legend_colors[component_id % len(legend_colors)]
                    self_fill(i, j, color)
                    component_id += 1

    return output
```