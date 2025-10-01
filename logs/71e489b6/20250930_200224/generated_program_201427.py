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
            if new_g[i][j] == 0:
                n = 0
                if i > 0 and new_g[i - 1][j] == 1:
                    n += 1
                if i < rows - 1 and new_g[i + 1][j] == 1:
                    n += 1
                if j > 0 and new_g[i][j - 1] == 1:
                    n += 1
                if j < cols - 1 and new_g[i][j + 1] == 1:
                    n += 1
                if n == 4:
                    if i > 0 and new_g[i - 1][j] == 1:
                        new_g[i - 1][j] = 7
                    if i < rows - 1 and new_g[i + 1][j] == 1:
                        new_g[i + 1][j] = 7
                    if j > 0 and new_g[i][j - 1] == 1:
                        new_g[i][j - 1] = 7
                    if j < cols - 1 and new_g[i][j + 1] == 1:
                        new_g[i][j + 1] = 7
    return new_g

def propagate_to_adjacent_7(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1:
                has7 = False
                if i > 0 and g[i - 1][j] == 7:
                    has7 = True
                if i < rows - 1 and g[i + 1][j] == 7:
                    has7 = True
                if j > 0 and g[i][j - 1] == 7:
                    has7 = True
                if j < cols - 1 and g[i][j + 1] == 7:
                    has7 = True
                if has7:
                    new_g[i][j] = 7
    return new_g

def set_adjacent_to_open_top(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        for j in range(cols):
            if i == 0 and new_g[i][j] == 0 and j > 0 and new_g[i][j - 1] == 1 and j < cols - 1 and new_g[i][j + 1] == 1 and i < rows - 1 and new_g[i + 1][j] == 1:
                if j > 0 and new_g[i][j - 1] == 1:
                    new_g[i][j - 1] = 7
                if j < cols - 1 and new_g[i][j + 1] == 1:
                    new_g[i][j + 1] = 7
                if i < rows - 1 and new_g[i + 1][j] == 1:
                    new_g[i + 1][j] = 7
    return new_g

def set_adjacent_to_open_right(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        for j in range(cols):
            if j == cols - 1 and new_g[i][j] == 0 and i > 0 and new_g[i - 1][j] == 1 and i < rows - 1 and new_g[i + 1][j] == 1 and j > 0 and new_g[i][j - 1] == 1:
                if j > 0 and new_g[i][j - 1] == 1:
                    new_g[i][j - 1] = 7
                if i > 0 and new_g[i - 1][j] == 1:
                    new_g[i - 1][j] = 7
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    g = prune_dangling(g)
    g = set_adjacent_to_open_top(g)
    g = set_adjacent_to_open_right(g)
    g = set_adjacent_to_closed_holes(g)
    g = propagate_to_adjacent_7(g)
    return g
```