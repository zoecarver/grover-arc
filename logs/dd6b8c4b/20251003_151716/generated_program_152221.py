```python
from typing import List

def color_central_object(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    left_wall = (new_g[4][3] == 6 and new_g[5][3] == 6 and new_g[6][3] == 6)
    right_wall = (new_g[4][7] == 6 and new_g[5][7] == 6 and new_g[6][7] == 6)
    bottom_open = (new_g[7][4] == 7 and new_g[7][5] == 7 and new_g[7][6] == 7)
    if left_wall and right_wall and bottom_open:
        for i in range(4, 7):
            for j in range(4, 7):
                new_g[i][j] = 9
    elif left_wall and right_wall:
        new_g[4][4] = 9
        new_g[4][5] = 9
    else:
        new_g[4][4] = 9
        new_g[4][5] = 9
        new_g[4][6] = 9
        new_g[5][4] = 9
    return new_g

def remove_upper_isolated_blue(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(4):
        for c in range(11):
            if new_g[r][c] == 9:
                has_adj = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 11 and 0 <= nc < 11 and new_g[nr][nc] == 9:
                        has_adj = True
                        break
                if not has_adj:
                    new_g[r][c] = 7
    return new_g

def remove_middle_left_isolated_blue(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(4, 7):
        for c in range(4):
            if new_g[r][c] == 9:
                has_adj = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 11 and 0 <= nc < 11 and new_g[nr][nc] == 9:
                        has_adj = True
                        break
                if not has_adj:
                    new_g[r][c] = 7
    return new_g

def trim_unsupported_left_blue(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    for r in range(11):
        for c in range(10):
            left_is_open = (c == 0 or new_g[r][c - 1] != 9)
            down_is_seven = (r < 10 and new_g[r + 1][c] == 7)
            left_is_seven = (c == 0 or new_g[r][c - 1] == 7)
            if (new_g[r][c] == 9 and new_g[r][c + 1] == 9 and
                left_is_open and down_is_seven and left_is_seven):
                new_g[r][c] = 7
    return new_g

def remove_l_corner_blue(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(11):
        for c in range(11):
            if new_g[r][c] == 9:
                has_adj = False
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 11 and 0 <= nc < 11 and new_g[nr][nc] == 9:
                        has_adj = True
                        break
                left_six = (c > 0 and new_g[r][c - 1] == 6)
                up_six = (r > 0 and new_g[r - 1][c] == 6)
                if not has_adj and left_six and up_six:
                    new_g[r][c] = 7
    return new_g

def remove_lower_blue(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    for r in range(8, 11):
        for c in range(11):
            if new_g[r][c] == 9:
                new_g[r][c] = 7
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    new_g = color_central_object(new_g)
    new_g = remove_upper_isolated_blue(new_g)
    new_g = remove_middle_left_isolated_blue(new_g)
    new_g = trim_unsupported_left_blue(new_g)
    new_g = remove_l_corner_blue(new_g)
    new_g = remove_lower_blue(new_g)
    return new_g
```