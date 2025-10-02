```python
from typing import List

directions_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def count_neighbors(grid: List[List[int]], i: int, j: int, rows: int, cols: int, directions: List[tuple], target: tuple = (1,)) -> int:
    return sum(1 for di, dj in directions
               if 0 <= i + di < rows and 0 <= j + dj < cols and grid[i + di][j + dj] in target)

def remove_isolated(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    output = [row[:] for row in g]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1:
                n = count_neighbors(g, i, j, rows, cols, directions_4)
                if n == 0:
                    output[i][j] = 0
    return output

def handle_horizontal_size1(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    output = [row[:] for row in g]
    rows, cols = len(g), len(g[0])
    for i in range(rows):
        for j in range(1, cols - 1):
            up_zero = i > 0 and g[i - 1][j] == 0
            down_zero = i < rows - 1 and g[i + 1][j] == 0
            if (g[i][j] == 0 and g[i][j - 1] == 1 and g[i][j + 1] == 1 and
                not (up_zero and down_zero)):
                start = j - 1
                end = j + 1
                output[i][start] = 7
                output[i][end] = 7
                # above
                if i > 0:
                    for k in range(start, end + 1):
                        if g[i - 1][k] == 1:
                            output[i - 1][k] = 7
                # below
                if i + 1 < rows:
                    for k in range(start, end + 1):
                        if g[i + 1][k] == 1:
                            output[i + 1][k] = 7
                    all_zero_below = all(g[i + 1][k] == 0 for k in range(start, end + 1))
                    if all_zero_below:
                        for k in range(start, end + 1):
                            output[i + 1][k] = 7
    return output

def handle_horizontal_size2(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    output = [row[:] for row in g]
    rows, cols = len(g), len(g[0])
    for i in range(rows):
        j = 1
        while j < cols - 2:
            if (g[i][j] == 0 and g[i][j + 1] == 0 and
                g[i][j - 1] == 1 and g[i][j + 2] == 1):
                start = j - 1
                end = j + 2
                output[i][start] = 7
                output[i][end] = 7
                # above
                if i > 0:
                    for k in range(start, end + 1):
                        if g[i - 1][k] == 1:
                            output[i - 1][k] = 7
                # below
                if i + 1 < rows:
                    all_zero_below = all(g[i + 1][k] == 0 for k in range(start, end + 1))
                    if all_zero_below:
                        for k in range(start, end + 1):
                            output[i + 1][k] = 7
                    else:
                        all_one_below = all(g[i + 1][k] == 1 for k in range(start, end + 1))
                        has_zero_above = i > 0 and any(g[i - 1][k] == 0 for k in range(start, end + 1))
                        if all_one_below and has_zero_above:
                            for k in range(start, end + 1):
                                output[i + 1][k] = 7
            j += 1
    return output

def handle_vertical_size1(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    output = [row[:] for row in g]
    rows, cols = len(g), len(g[0])
    for j in range(cols):
        for i in range(1, rows - 1):
            left_zero = j > 0 and g[i][j - 1] == 0
            right_zero = j < cols - 1 and g[i][j + 1] == 0
            if (g[i][j] == 0 and g[i - 1][j] == 1 and g[i + 1][j] == 1 and
                not (left_zero and right_zero)):
                start = i - 1
                end = i + 1
                output[start][j] = 7
                output[end][j] = 7
                open_left = j == 0 or g[i][j - 1] == 0
                open_right = j == cols - 1 or g[i][j + 1] == 0
                if open_left and open_right:
                    if j > 0:
                        for k in range(start, end + 1):
                            if g[k][j - 1] == 1:
                                output[k][j - 1] = 7
                    if j < cols - 1:
                        for k in range(start, end + 1):
                            if g[k][j + 1] == 1:
                                output[k][j + 1] = 7
                elif open_left:
                    if j > 0:
                        all_zero_left = all(g[k][j - 1] == 0 for k in range(start, end + 1))
                        all_one_left = all(g[k][j - 1] == 1 for k in range(start, end + 1))
                        if all_zero_left or all_one_left:
                            for k in range(start, end + 1):
                                output[k][j - 1] = 7
                elif open_right:
                    if j < cols - 1:
                        all_zero_right = all(g[k][j + 1] == 0 for k in range(start, end + 1))
                        all_one_right = all(g[k][j + 1] == 1 for k in range(start, end + 1))
                        if all_zero_right or all_one_right:
                            for k in range(start, end + 1):
                                output[k][j + 1] = 7
                    else:
                        if j > 0:
                            for k in range(start, end + 1):
                                output[k][j - 1] = 7
                else:
                    if j > 0:
                        for k in range(start, end + 1):
                            if g[k][j - 1] == 1:
                                output[k][j - 1] = 7
                    if j < cols - 1:
                        for k in range(start, end + 1):
                            if g[k][j + 1] == 1:
                                output[k][j + 1] = 7
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    output = remove_isolated(g)
    output = handle_horizontal_size1(output)
    output = handle_horizontal_size2(output)
    output = handle_vertical_size1(output)
    return output
```