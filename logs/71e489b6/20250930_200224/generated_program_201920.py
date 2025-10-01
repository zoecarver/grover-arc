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
            n = 0
            if i > 0 and new_g[i - 1][j] == 1:
                n += 1
            if i < rows - 1 and new_g[i + 1][j] == 1:
                n += 1
            if j > 0 and new_g[i][j - 1] == 1:
                n += 1
            if j < cols - 1 and new_g[i][j + 1] == 1:
                n += 1
            if n < 2:
                new_g[i][j] = 0
    return new_g

def mark_single_notches(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        for j in range(1, cols - 1):
            if g[i][j] == 0 and g[i][j - 1] == 1 and g[i][j + 1] == 1:
                has_enclosure = (i == 0 or g[i - 1][j] == 1) or (i < rows - 1 and g[i + 1][j] == 1)
                if has_enclosure:
                    new_g[i][j - 1] = 7
                    new_g[i][j + 1] = 7
                    if i > 0 and g[i - 1][j] == 1:
                        if j - 1 >= 0 and g[i - 1][j - 1] == 1:
                            new_g[i - 1][j - 1] = 7
                        if g[i - 1][j] == 1:
                            new_g[i - 1][j] = 7
                        if j + 1 < cols and g[i - 1][j + 1] == 1:
                            new_g[i - 1][j + 1] = 7
                    if i < rows - 1 and g[i + 1][j] == 1:
                        if j - 1 >= 0 and g[i + 1][j - 1] == 1:
                            new_g[i + 1][j - 1] = 7
                        if g[i + 1][j] == 1:
                            new_g[i + 1][j] = 7
                        if j + 1 < cols and g[i + 1][j + 1] == 1:
                            new_g[i + 1][j + 1] = 7
                    if i < rows - 1 and g[i + 1][j] == 0:
                        below_n = count_1_neighbors(g, i + 1, j)
                        if below_n < 2:
                            if j - 1 >= 0:
                                new_g[i + 1][j - 1] = 7
                            new_g[i + 1][j] = 7
                            if j + 1 < cols:
                                new_g[i + 1][j + 1] = 7
    return new_g

def mark_double_notches(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        for jj in range(2, cols - 1):
            j = jj - 1  # center of the two 0s
            if g[i][j] == 0 and g[i][j + 1] == 0 and (j - 1 >= 0 and g[i][j - 1] == 1) and g[i][j + 2] == 1:
                start = j
                end = j + 2
                has_enclosure = (i == 0 or (g[i - 1][j] == 1 and g[i - 1][j + 1] == 1)) or (i < rows - 1 and (g[i + 1][j] == 1 and g[i + 1][j + 1] == 1))
                if has_enclosure:
                    if j - 1 >= 0:
                        new_g[i][j - 1] = 7
                    new_g[i][j + 2] = 7
                    # vertical up for sides
                    if i > 0:
                        if j - 1 >= 0 and g[i - 1][j - 1] == 1:
                            new_g[i - 1][j - 1] = 7
                        if j + 2 < cols and g[i - 1][j + 2] == 1:
                            new_g[i - 1][j + 2] = 7
                    if i > 0 and g[i - 1][j] == 1 and g[i - 1][j + 1] == 1:
                        for c in range(max(0, j - 1), min(cols, j + 3)):
                            if g[i - 1][c] == 1:
                                new_g[i - 1][c] = 7
                    if i < rows - 1 and g[i + 1][j] == 1 and g[i + 1][j + 1] == 1:
                        for c in range(max(0, j - 1), min(cols, j + 3)):
                            if g[i + 1][c] == 1:
                                new_g[i + 1][c] = 7
    return new_g

def mark_vertical_notches(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    # Right edge
    for i in range(rows):
        j = cols - 1
        if j > 0 and g[i][j] == 0 and g[i][j - 1] == 1:
            has_enclosure = (i == 0 or g[i - 1][j] == 1) or (i < rows - 1 and g[i + 1][j] == 1)
            if has_enclosure:
                new_g[i][j - 1] = 7
                if i > 0 and g[i - 1][j] == 1:
                    if j - 1 >= 0 and g[i - 1][j - 1] == 1:
                        new_g[i - 1][j - 1] = 7
                    if g[i - 1][j] == 1:
                        new_g[i - 1][j] = 7
                if i < rows - 1 and g[i + 1][j] == 1:
                    if j - 1 >= 0 and g[i + 1][j - 1] == 1:
                        new_g[i + 1][j - 1] = 7
                    if g[i + 1][j] == 1:
                        new_g[i + 1][j] = 7
    # Left edge
    for i in range(rows):
        j = 0
        if j < cols - 1 and g[i][j] == 0 and g[i][j + 1] == 1:
            has_enclosure = (i == 0 or g[i - 1][j] == 1) or (i < rows - 1 and g[i + 1][j] == 1)
            if has_enclosure:
                new_g[i][j + 1] = 7
                if i > 0 and g[i - 1][j] == 1:
                    if g[i - 1][j] == 1:
                        new_g[i - 1][j] = 7
                    if j + 1 < cols and g[i - 1][j + 1] == 1:
                        new_g[i - 1][j + 1] = 7
                if i < rows - 1 and g[i + 1][j] == 1:
                    if g[i + 1][j] == 1:
                        new_g[i + 1][j] = 7
                    if j + 1 < cols and g[i + 1][j + 1] == 1:
                        new_g[i + 1][j + 1] = 7
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    g = prune_dangling(g)
    g = mark_single_notches(g)
    g = mark_double_notches(g)
    g = mark_vertical_notches(g)
    return g
```