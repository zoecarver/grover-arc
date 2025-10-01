```python
from typing import List

def prune_dangling(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    while True:
        new_g = [row[:] for row in g]
        changed = False
        for i in range(rows):
            for j in range(cols):
                if new_g[i][j] != 1:
                    continue
                n = 0
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and new_g[ni][nj] == 1:
                        n += 1
                if n < 2:
                    new_g[i][j] = 0
                    changed = True
        g = new_g
        if not changed:
            break
    return g

def mark_horizontal_single(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        for j in range(1, cols - 1):
            if g[i][j] == 0 and g[i][j - 1] == 1 and g[i][j + 1] == 1:
                new_g[i][j - 1] = 7
                new_g[i][j + 1] = 7
                if i > 0:
                    center_val = g[i - 1][j]
                    if center_val == 1:
                        for dk in [-1, 0, 1]:
                            k = j + dk
                            if 0 <= k < cols and g[i - 1][k] == 1:
                                new_g[i - 1][k] = 7
                    elif center_val == 0:
                        left_0 = (j - 1 < 0 or g[i - 1][j - 1] == 0)
                        right_0 = (j + 1 >= cols or g[i - 1][j + 1] == 0)
                        if left_0 and right_0:
                            for dk in [-1, 0, 1]:
                                k = j + dk
                                if 0 <= k < cols:
                                    new_g[i - 1][k] = 7
                if i + 1 < rows:
                    center_val = g[i + 1][j]
                    if center_val == 1:
                        for dk in [-1, 0, 1]:
                            k = j + dk
                            if 0 <= k < cols and g[i + 1][k] == 1:
                                new_g[i + 1][k] = 7
                    elif center_val == 0:
                        left_0 = (j - 1 < 0 or g[i + 1][j - 1] == 0)
                        right_0 = (j + 1 >= cols or g[i + 1][j + 1] == 0)
                        if left_0 and right_0:
                            for dk in [-1, 0, 1]:
                                k = j + dk
                                if 0 <= k < cols:
                                    new_g[i + 1][k] = 7
    return new_g

def mark_horizontal_left_edge(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        j = 0
        if cols > 1 and g[i][j] == 0 and g[i][1] == 1:
            new_g[i][1] = 7
            if i > 0:
                center_val = g[i - 1][j]
                if center_val == 1:
                    for k in [0, 1]:
                        if g[i - 1][k] == 1:
                            new_g[i - 1][k] = 7
                elif center_val == 0:
                    left_0 = True
                    right_0 = g[i - 1][1] == 0
                    if left_0 and right_0:
                        for k in [0, 1]:
                            new_g[i - 1][k] = 7
            if i + 1 < rows:
                center_val = g[i + 1][j]
                if center_val == 1:
                    for k in [0, 1]:
                        if g[i + 1][k] == 1:
                            new_g[i + 1][k] = 7
                elif center_val == 0:
                    left_0 = True
                    right_0 = g[i + 1][1] == 0
                    if left_0 and right_0:
                        for k in [0, 1]:
                            new_g[i + 1][k] = 7
    return new_g

def mark_horizontal_right_edge(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        j = cols - 1
        if j > 0 and g[i][j] == 0 and g[i][j - 1] == 1:
            new_g[i][j - 1] = 7
            if i > 0:
                center_val = g[i - 1][j]
                if center_val == 1:
                    for k in [j - 1, j]:
                        if 0 <= k < cols and g[i - 1][k] == 1:
                            new_g[i - 1][k] = 7
                elif center_val == 0:
                    left_0 = g[i - 1][j - 1] == 0
                    right_0 = True
                    if left_0 and right_0:
                        for k in [j - 1, j]:
                            new_g[i - 1][k] = 7
            if i + 1 < rows:
                center_val = g[i + 1][j]
                if center_val == 1:
                    for k in [j - 1, j]:
                        if 0 <= k < cols and g[i + 1][k] == 1:
                            new_g[i + 1][k] = 7
                elif center_val == 0:
                    left_0 = g[i + 1][j - 1] == 0
                    right_0 = True
                    if left_0 and right_0:
                        for k in [j - 1, j]:
                            new_g[i + 1][k] = 7
    return new_g

def mark_double_horizontal(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for i in range(rows):
        for j in range(cols - 3):
            if g[i][j] == 1 and g[i][j + 1] == 0 and g[i][j + 2] == 0 and g[i][j + 3] == 1:
                new_g[i][j] = 7
                new_g[i][j + 3] = 7
                if i > 0:
                    c1 = g[i - 1][j + 1]
                    c2 = g[i - 1][j + 2]
                    if c1 == 1 and c2 == 1:
                        for k in range(j, j + 4):
                            if 0 <= k < cols and g[i - 1][k] == 1:
                                new_g[i - 1][k] = 7
                if i + 1 < rows:
                    c1 = g[i + 1][j + 1]
                    c2 = g[i + 1][j + 2]
                    if c1 == 1 and c2 == 1:
                        for k in range(j, j + 4):
                            if 0 <= k < cols and g[i + 1][k] == 1:
                                new_g[i + 1][k] = 7
    return new_g

def mark_vertical_single(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for j in range(cols):
        for i in range(1, rows - 1):
            if g[i][j] == 0 and g[i - 1][j] == 1 and g[i + 1][j] == 1:
                new_g[i - 1][j] = 7
                new_g[i + 1][j] = 7
                if j > 0:
                    center_val = g[i][j - 1]
                    if center_val == 1:
                        for di in [-1, 0, 1]:
                            ii = i + di
                            if 0 <= ii < rows and g[ii][j - 1] == 1:
                                new_g[ii][j - 1] = 7
                    elif center_val == 0:
                        up_0 = (i - 1 < 0 or g[i - 1][j - 1] == 0)
                        down_0 = (i + 1 >= rows or g[i + 1][j - 1] == 0)
                        if up_0 and down_0:
                            for di in [-1, 0, 1]:
                                ii = i + di
                                if 0 <= ii < rows:
                                    new_g[ii][j - 1] = 7
                if j + 1 < cols:
                    center_val = g[i][j + 1]
                    if center_val == 1:
                        for di in [-1, 0, 1]:
                            ii = i + di
                            if 0 <= ii < rows and g[ii][j + 1] == 1:
                                new_g[ii][j + 1] = 7
                    elif center_val == 0:
                        up_0 = (i - 1 < 0 or g[i - 1][j + 1] == 0)
                        down_0 = (i + 1 >= rows or g[i + 1][j + 1] == 0)
                        if up_0 and down_0:
                            for di in [-1, 0, 1]:
                                ii = i + di
                                if 0 <= ii < rows:
                                    new_g[ii][j + 1] = 7
    return new_g

def mark_vertical_top_edge(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    if rows < 2:
        return new_g
    i = 0
    for j in range(cols):
        if g[i][j] == 0 and g[i + 1][j] == 1:
            new_g[i + 1][j] = 7
            if j > 0:
                center_val = g[i][j - 1]
                if center_val == 1:
                    for ii in [i, i + 1]:
                        if g[ii][j - 1] == 1:
                            new_g[ii][j - 1] = 7
                elif center_val == 0:
                    up_0 = True
                    down_0 = g[i + 1][j - 1] == 0
                    if up_0 and down_0:
                        for ii in [i, i + 1]:
                            new_g[ii][j - 1] = 7
            if j + 1 < cols:
                center_val = g[i][j + 1]
                if center_val == 1:
                    for ii in [i, i + 1]:
                        if g[ii][j + 1] == 1:
                            new_g[ii][j + 1] = 7
                elif center_val == 0:
                    up_0 = True
                    down_0 = g[i + 1][j + 1] == 0
                    if up_0 and down_0:
                        for ii in [i, i + 1]:
                            new_g[ii][j + 1] = 7
    return new_g

def mark_vertical_bottom_edge(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    if rows < 2:
        return new_g
    i = rows - 1
    for j in range(cols):
        if g[i][j] == 0 and g[i - 1][j] == 1:
            new_g[i - 1][j] = 7
            if j > 0:
                center_val = g[i][j - 1]
                if center_val == 1:
                    for ii in [i - 1, i]:
                        if g[ii][j - 1] == 1:
                            new_g[ii][j - 1] = 7
                elif center_val == 0:
                    up_0 = g[i - 1][j - 1] == 0
                    down_0 = True
                    if up_0 and down_0:
                        for ii in [i - 1, i]:
                            new_g[ii][j - 1] = 7
            if j + 1 < cols:
                center_val = g[i][j + 1]
                if center_val == 1:
                    for ii in [i - 1, i]:
                        if g[ii][j + 1] == 1:
                            new_g[ii][j + 1] = 7
                elif center_val == 0:
                    up_0 = g[i - 1][j + 1] == 0
                    down_0 = True
                    if up_0 and down_0:
                        for ii in [i - 1, i]:
                            new_g[ii][j + 1] = 7
    return new_g

def mark_double_vertical(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for j in range(cols):
        for i in range(rows - 3):
            if g[i][j] == 1 and g[i + 1][j] == 0 and g[i + 2][j] == 0 and g[i + 3][j] == 1:
                new_g[i][j] = 7
                new_g[i + 3][j] = 7
                if j > 0:
                    c1 = g[i + 1][j - 1]
                    c2 = g[i + 2][j - 1]
                    if c1 == 1 and c2 == 1:
                        for ii in range(i, i + 4):
                            if 0 <= ii < rows and g[ii][j - 1] == 1:
                                new_g[ii][j - 1] = 7
                if j + 1 < cols:
                    c1 = g[i + 1][j + 1]
                    c2 = g[i + 2][j + 1]
                    if c1 == 1 and c2 == 1:
                        for ii in range(i, i + 4):
                            if 0 <= ii < rows and g[ii][j + 1] == 1:
                                new_g[ii][j + 1] = 7
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    g = prune_dangling(g)
    g = mark_horizontal_single(g)
    g = mark_horizontal_left_edge(g)
    g = mark_horizontal_right_edge(g)
    g = mark_double_horizontal(g)
    g = mark_vertical_single(g)
    g = mark_vertical_top_edge(g)
    g = mark_vertical_bottom_edge(g)
    g = mark_double_vertical(g)
    return g
```