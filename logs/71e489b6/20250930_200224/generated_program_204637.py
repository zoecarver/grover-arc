```python
from typing import List

def count_1_neighbors(g: List[List[int]], i: int, j: int) -> int:
    rows = len(g)
    cols = len(g[0])
    n = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in directions:
        ni = i + di
        nj = j + dj
        if 0 <= ni < rows and 0 <= nj < cols and g[ni][nj] == 1:
            n += 1
    return n

def prune_dangling(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        for j in range(cols):
            if new_g[i][j] == 0:
                continue
            n = count_1_neighbors(new_g, i, j)
            if n < 2:
                new_g[i][j] = 0
    return new_g

def mark_single_notches(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    rows = len(g)
    cols = len(g[0])
    for i in range(rows):
        for j in range(1, cols - 1):
            if g[i][j - 1] == 1 and g[i][j] == 0 and g[i][j + 1] == 1:
                has_vertical = False
                if i > 0 and g[i - 1][j] == 1:
                    has_vertical = True
                    new_g[i - 1][j] = 7
                if i < rows - 1 and g[i + 1][j] == 1:
                    has_vertical = True
                    new_g[i + 1][j] = 7
                if i == 0 or i == rows - 1:
                    has_vertical = True
                if not has_vertical:
                    continue
                new_g[i][j - 1] = 7
                new_g[i][j + 1] = 7
                # open below propagation
                if i < rows - 1 and g[i + 1][j] == 0:
                    ni = i + 1
                    n = count_1_neighbors(g, ni, j)
                    if n < 2:
                        new_g[ni][j] = 7
                        for djj in [-1, 1]:
                            njj = j + djj
                            if 0 <= njj < cols and g[ni][njj] == 0:
                                new_g[ni][njj] = 7
                # symmetric for open above
                if i > 0 and g[i - 1][j] == 0:
                    ni = i - 1
                    n = count_1_neighbors(g, ni, j)
                    if n < 2:
                        new_g[ni][j] = 7
                        for djj in [-1, 1]:
                            njj = j + djj
                            if 0 <= njj < cols and g[ni][njj] == 0:
                                new_g[ni][njj] = 7
    return new_g

def mark_double_notches(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    rows = len(g)
    cols = len(g[0])
    for i in range(rows):
        for j in range(2, cols - 1):
            if g[i][j - 1] == 1 and g[i][j] == 0 and g[i][j + 1] == 0 and g[i][j + 2] == 1:
                new_g[i][j - 1] = 7
                new_g[i][j + 2] = 7
                has_vertical = False
                for k in [0, 1]:
                    jj = j + k
                    if i > 0 and g[i - 1][jj] == 1:
                        has_vertical = True
                        new_g[i - 1][jj] = 7
                    if i < rows - 1 and g[i + 1][jj] == 1:
                        has_vertical = True
                        new_g[i + 1][jj] = 7
                    if i == 0 or i == rows - 1:
                        has_vertical = True
                if not has_vertical:
                    continue
                # extend horizontally in vertical rows
                if i > 0:
                    for jj in range(max(0, j - 1), min(cols, j + 3)):
                        if g[i - 1][jj] == 1:
                            new_g[i - 1][jj] = 7
                if i < rows - 1:
                    for jj in range(max(0, j - 1), min(cols, j + 3)):
                        if g[i + 1][jj] == 1:
                            new_g[i + 1][jj] = 7
                # open below for double
                open_below = i < rows - 1 and g[i + 1][j] == 0 and g[i + 1][j + 1] == 0
                if open_below:
                    for jj in range(j - 1, j + 3):
                        if 0 <= jj < cols and g[i + 1][jj] == 0:
                            new_g[i + 1][jj] = 7
    return new_g

def mark_vertical_notches(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    rows = len(g)
    cols = len(g[0])
    # left edge
    for i in range(1, rows - 1):
        if g[i][0] == 0 and g[i - 1][0] == 1 and g[i + 1][0] == 1:
            new_g[i - 1][0] = 7
            new_g[i + 1][0] = 7
            # adjacent right
            for di in [-1, 0, 1]:
                ii = i + di
                if 0 <= ii < rows and 1 < cols and g[ii][1] == 1:
                    new_g[ii][1] = 7
    # right edge
    for i in range(1, rows - 1):
        if g[i][cols - 1] == 0 and g[i - 1][cols - 1] == 1 and g[i + 1][cols - 1] == 1:
            new_g[i - 1][cols - 1] = 7
            new_g[i + 1][cols - 1] = 7
            # adjacent left
            for di in [-1, 0, 1]:
                ii = i + di
                if 0 <= ii < rows and cols - 2 >= 0 and g[ii][cols - 2] == 1:
                    new_g[ii][cols - 2] = 7
    # bottom edge horizontal notches already in single/double
    # top similar
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    g = prune_dangling(g)
    g = mark_single_notches(g)
    g = mark_double_notches(g)
    g = mark_vertical_notches(g)
    return g
```