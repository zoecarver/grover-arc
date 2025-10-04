```python
from typing import List

def get(g: List[List[int]], r: int, c: int) -> int:
    rows = len(g)
    cols = len(g[0])
    if 0 <= r < rows and 0 <= c < cols:
        return g[r][c]
    return 0

def remove_isolated(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    result = [row[:] for row in g]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1:
                n_up = get(g, i - 1, j)
                n_down = get(g, i + 1, j)
                n_left = get(g, i, j - 1)
                n_right = get(g, i, j + 1)
                n1 = (1 if n_up == 1 else 0) + (1 if n_down == 1 else 0) + (1 if n_left == 1 else 0) + (1 if n_right == 1 else 0)
                if n1 == 0:
                    result[i][j] = 0
    return result

def color_enclosed_boundaries(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    result = [row[:] for row in g]
    dirs8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 0:
                n_up = get(g, i - 1, j)
                n_down = get(g, i + 1, j)
                n_left = get(g, i, j - 1)
                n_right = get(g, i, j + 1)
                n1 = (1 if n_up == 1 else 0) + (1 if n_down == 1 else 0) + (1 if n_left == 1 else 0) + (1 if n_right == 1 else 0)
                if n1 == 4:
                    for dr, dc in dirs8:
                        ni = i + dr
                        nj = j + dc
                        if 0 <= ni < rows and 0 <= nj < cols and g[ni][nj] == 1:
                            result[ni][nj] = 7
    return result

def handle_open_up_dents(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    result = [row[:] for row in g]
    for i in range(rows):
        for j in range(1, cols - 1):
            if g[i][j] == 0:
                has_up = (i > 0 and get(g, i - 1, j) == 1)
                has_down = get(g, i + 1, j) == 1 if i + 1 < rows else False
                has_left = get(g, i, j - 1) == 1
                has_right = get(g, i, j + 1) == 1
                if (not has_up) and has_down and has_left and has_right:
                    result[i][j - 1] = 7
                    result[i][j + 1] = 7
                    for dj in [-1, 0, 1]:
                        nj = j + dj
                        if 0 <= nj < cols and i + 1 < rows:
                            result[i + 1][nj] = 7
    return result

def handle_open_down_dents(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    result = [row[:] for row in g]
    for i in range(rows - 1):
        for j in range(1, cols - 1):
            if g[i][j] == 0:
                has_up = get(g, i - 1, j) == 1 if i > 0 else False
                has_down = get(g, i + 1, j) == 0
                has_left = get(g, i, j - 1) == 1
                has_right = get(g, i, j + 1) == 1
                if has_up and has_down and has_left and has_right:
                    # compute left_len
                    left_len = 0
                    k = j - 1
                    while k >= 0 and g[i][k] == 1:
                        left_len += 1
                        k -= 1
                    # compute right_len
                    right_len = 0
                    k = j + 1
                    while k < cols and g[i][k] == 1:
                        right_len += 1
                        k += 1
                    min_len = min(left_len, right_len)
                    # set horizontal
                    result[i][j - 1] = 7
                    result[i][j + 1] = 7
                    # set below 3-wide
                    for dj in [-1, 0, 1]:
                        nj = j + dj
                        if 0 <= nj < cols:
                            result[i + 1][nj] = 7
                    # set center if min_len <= 3
                    if min_len <= 3:
                        result[i][j] = 7
                    # set above 3-wide if min_len > 3
                    if min_len > 3 and i > 0:
                        for dj in [-1, 0, 1]:
                            nj = j + dj
                            if 0 <= nj < cols:
                                result[i - 1][nj] = 7
    return result

def handle_open_left_dents(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    result = [row[:] for row in g]
    dirs8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 0:
                has_left = j > 0 and get(g, i, j - 1) == 1
                has_right = get(g, i, j + 1) == 1
                has_up = i > 0 and get(g, i - 1, j) == 1
                has_down = get(g, i + 1, j) == 1
                n1 = (1 if has_up else 0) + (1 if has_down else 0) + (1 if has_left else 0) + (1 if has_right else 0)
                if n1 == 3 and not has_left:
                    for dr, dc in dirs8:
                        ni = i + dr
                        nj = j + dc
                        if 0 <= ni < rows and 0 <= nj < cols and g[ni][nj] == 1:
                            result[ni][nj] = 7
    return result

def handle_open_right_dents(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    result = [row[:] for row in g]
    dirs8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 0:
                has_left = get(g, i, j - 1) == 1
                has_right = j + 1 < cols and get(g, i, j + 1) == 1
                has_up = i > 0 and get(g, i - 1, j) == 1
                has_down = get(g, i + 1, j) == 1
                n1 = (1 if has_up else 0) + (1 if has_down else 0) + (1 if has_left else 0) + (1 if has_right else 0)
                if n1 == 3 and not has_right:
                    for dr, dc in dirs8:
                        ni = i + dr
                        nj = j + dc
                        if 0 <= ni < rows and 0 <= nj < cols and g[ni][nj] == 1:
                            result[ni][nj] = 7
    return result

def handle_bottom_horizontal_dents(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    result = [row[:] for row in g]
    for i in range(rows - 1):
        for j in range(1, cols - 1):
            if g[i][j] == 0:
                has_up = i > 0 and get(g, i - 1, j) == 0
                has_down = get(g, i + 1, j) == 1
                has_left = get(g, i, j - 1) == 0
                has_right = get(g, i, j + 1) == 0
                if has_down and has_left and has_right and (i == 0 or has_up):
                    # set above left right if possible
                    if i > 0:
                        result[i - 1][j - 1] = 7
                        result[i - 1][j + 1] = 7
                    # set horizontal left right
                    result[i][j - 1] = 7
                    result[i][j + 1] = 7
                    # set below 3-wide
                    for dj in [-1, 0, 1]:
                        nj = j + dj
                        if 0 <= nj < cols:
                            result[i + 1][nj] = 7
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    g = remove_isolated(g)
    g = color_enclosed_boundaries(g)
    g = handle_open_up_dents(g)
    g = handle_open_down_dents(g)
    g = handle_open_left_dents(g)
    g = handle_open_right_dents(g)
    g = handle_bottom_horizontal_dents(g)
    return g
```