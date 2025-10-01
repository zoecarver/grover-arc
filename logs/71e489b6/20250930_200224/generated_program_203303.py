```python
from typing import List

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

def set_adjacent_to_closed_holes(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 0:
                n = 0
                if i > 0 and g[i - 1][j] == 1:
                    n += 1
                if i < rows - 1 and g[i + 1][j] == 1:
                    n += 1
                if j > 0 and g[i][j - 1] == 1:
                    n += 1
                if j < cols - 1 and g[i][j + 1] == 1:
                    n += 1
                if n == 4:
                    if i > 0 and g[i - 1][j] == 1:
                        new_g[i - 1][j] = 7
                    if i < rows - 1 and g[i + 1][j] == 1:
                        new_g[i + 1][j] = 7
                    if j > 0 and g[i][j - 1] == 1:
                        new_g[i][j - 1] = 7
                    if j < cols - 1 and g[i][j + 1] == 1:
                        new_g[i][j + 1] = 7
    return new_g

def mark_open_top(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    if rows < 2:
        return new_g
    for j in range(1, cols - 1):
        if g[0][j] == 0 and g[0][j - 1] == 1 and g[0][j + 1] == 1:
            new_g[0][j - 1] = 7
            new_g[0][j + 1] = 7
            new_g[1][j - 1] = 7
            new_g[1][j] = 7
            new_g[1][j + 1] = 7
    return new_g

def mark_open_right(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(1, rows - 1):
        j = cols - 1
        if g[i][j] == 0 and g[i - 1][j] == 1 and g[i + 1][j] == 1:
            new_g[i - 1][j] = 7
            new_g[i + 1][j] = 7
            if cols > 1:
                new_g[i - 1][j - 1] = 7
                new_g[i + 1][j - 1] = 7
    return new_g

def mark_open_bottom(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows - 2, -1, -1):
        for j in range(1, cols - 1):
            if g[i][j] == 0 and g[i][j - 1] == 1 and g[i][j + 1] == 1:
                new_g[i][j - 1] = 7
                new_g[i][j + 1] = 7
                if i + 1 < rows:
                    new_g[i + 1][j - 1] = 7
                    new_g[i + 1][j] = 7
                    new_g[i + 1][j + 1] = 7
    return new_g

def propagate_horizontal_one_step(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        for j in range(1, cols - 1):
            if g[i][j] == 1 and (g[i][j - 1] == 7 or g[i][j + 1] == 7):
                new_g[i][j] = 7
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    g = prune_dangling(g)
    g = mark_open_top(g)
    g = mark_open_right(g)
    g = mark_open_bottom(g)
    g = set_adjacent_to_closed_holes(g)
    g = propagate_horizontal_one_step(g)
    g = propagate_horizontal_one_step(g)
    return g
```