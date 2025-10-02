```python
from typing import List, Tuple, Set
from copy import deepcopy
from collections import deque

directions_4: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
directions_8: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def count_neighbors(grid: List[List[int]], i: int, j: int, rows: int, cols: int, directions: List[Tuple[int, int]], target: Tuple[int, ...]) -> int:
    count = 0
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] in target:
            count += 1
    return count

def is_on_border(i: int, j: int, rows: int, cols: int) -> bool:
    return i == 0 or i == rows - 1 or j == 0 or j == cols - 1

def remove_thin_protrusions(grid: List[List[int]]) -> List[List[int]]:
    rows, cols = len(grid), len(grid[0])
    fixed = [row[:] for row in grid]
    output = [row[:] for row in fixed]
    for i in range(rows):
        for j in range(cols):
            if fixed[i][j] == 1 and count_neighbors(fixed, i, j, rows, cols, directions_4, (1,)) < 2:
                output[i][j] = 0
    return output

def identify_background(grid: List[List[int]]) -> Set[Tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    background: Set[Tuple[int, int]] = set()
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    for i in range(rows):
        if grid[i][0] == 0 and not visited[i][0]:
            q.append((i, 0))
            visited[i][0] = True
            background.add((i, 0))
        if grid[i][cols - 1] == 0 and not visited[i][cols - 1]:
            q.append((i, cols - 1))
            visited[i][cols - 1] = True
            background.add((i, cols - 1))
    for j in range(cols):
        if grid[0][j] == 0 and not visited[0][j]:
            q.append((0, j))
            visited[0][j] = True
            background.add((0, j))
        if grid[rows - 1][j] == 0 and not visited[rows - 1][j]:
            q.append((rows - 1, j))
            visited[rows - 1][j] = True
            background.add((rows - 1, j))
    while q:
        x, y = q.popleft()
        for di, dj in directions_4:
            nx, ny = x + di, y + dj
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                background.add((nx, ny))
                q.append((nx, ny))
    return background

def mark_internal_boundaries(grid: List[List[int]], background: Set[Tuple[int, int]]) -> List[List[int]]:
    rows, cols = len(grid), len(grid[0])
    output = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                adjacent_internal_0 = any(
                    0 <= i + di < rows and 0 <= j + dj < cols and grid[i + di][j + dj] == 0 and (i + di, j + dj) not in background
                    for di, dj in directions_8
                )
                if adjacent_internal_0:
                    output[i][j] = 7
    return output

def handle_shallow_holes(grid: List[List[int]], background: Set[Tuple[int, int]]) -> List[List[int]]:
    rows, cols = len(grid), len(grid[0])
    output = [row[:] for row in grid]
    fixed = [row[:] for row in grid]
    dir_list = directions_4
    opposites = {(-1, 0): (1, 0), (1, 0): (-1, 0), (0, -1): (0, 1), (0, 1): (0, -1)}
    for i in range(rows):
        for j in range(cols):
            if fixed[i][j] == 0 and (i, j) not in background and count_neighbors(fixed, i, j, rows, cols, directions_4, (1,)) == 4:
                for di, dj in dir_list:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and fixed[ni][nj] == 1:
                        oi = ni + di
                        oj = nj + dj
                        is_shallow = not (0 <= oi < rows and 0 <= oj < cols) or fixed[oi][oj] == 0
                        if is_shallow:
                            # fill hole
                            output[i][j] = 7
                            # set thin to 0
                            output[ni][nj] = 0
                            # fill outer patch
                            if 0 <= oi < rows and 0 <= oj < cols and output[oi][oj] == 0:
                                output[oi][oj] = 7
                                if dj == 0:  # vertical open
                                    for s in [-1, 1]:
                                        po = oj + s
                                        if 0 <= po < cols:
                                            output[oi][po] = 7
                                else:  # horizontal open
                                    for s in [-1, 1]:
                                        po = oi + s
                                        if 0 <= po < rows:
                                            output[po][oj] = 7
                            # mark perp sides at hole level
                            if dj == 0:  # vertical, mark horizontal
                                for s in [-1, 1]:
                                    pj = j + s
                                    if 0 <= pj < cols and output[i][pj] == 1:
                                        output[i][pj] = 7
                            else:  # horizontal, mark vertical
                                for s in [-1, 1]:
                                    pi = i + s
                                    if 0 <= pi < rows and output[pi][j] == 1:
                                        output[pi][j] = 7
                            break
    return output

def handle_external_dents(grid: List[List[int]], background: Set[Tuple[int, int]]) -> List[List[int]]:
    rows, cols = len(grid), len(grid[0])
    output = [row[:] for row in grid]
    fixed = [row[:] for row in grid]
    dir_list = directions_4
    for i in range(rows):
        for j in range(cols):
            num_adj = count_neighbors(fixed, i, j, rows, cols, directions_4, (1,))
            if (i, j) in background and fixed[i][j] == 0 and num_adj >= 2:
                # mark adjacent 1s
                for dii, djj in directions_8:
                    ni = i + dii
                    nj = j + djj
                    if 0 <= ni < rows and 0 <= nj < cols and output[ni][nj] == 1:
                        output[ni][nj] = 7
            if num_adj == 3:
                # find open dir
                open_di, open_dj = None, None
                for di, dj in dir_list:
                    ni = i + di
                    nj = j + dj
                    if not (0 <= ni < rows and 0 <= nj < cols) or fixed[ni][nj] != 1:
                        open_di, open_dj = di, dj
                        break
                if open_di is not None and open_dj is not None:
                    oi = i + open_di
                    oj = j + open_dj
                    if 0 <= oi < rows and 0 <= oj < cols and output[oi][oj] == 0:
                        output[oi][oj] = 7
                        if open_dj == 0:  # vertical
                            for s in [-1, 1]:
                                po = oj + s
                                if 0 <= po < cols:
                                    output[oi][po] = 7
                        else:  # horizontal
                            for s in [-1, 1]:
                                po = oi + s
                                if 0 <= po < rows:
                                    output[po][oj] = 7
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    cleaned = remove_thin_protrusions(g)
    bg = identify_background(cleaned)
    shallow_filled = handle_shallow_holes(cleaned, bg)
    marked_internal = mark_internal_boundaries(shallow_filled, bg)
    final = handle_external_dents(marked_internal, bg)
    return final
```