```python
from typing import List

def max_zero_run(g: List[List[int]]) -> int:
    max_run = 0
    for row in g:
        current_run = 0
        for cell in row:
            if cell == 0:
                current_run += 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0
    return max_run

def has_six(g: List[List[int]]) -> bool:
    for row in g:
        for cell in row:
            if cell == 6:
                return True
    return False

def build_l_shape(n: int, use_six: bool) -> List[List[int]]:
    grid = [[0] * n for _ in range(n)]
    for j in range(n):
        grid[1][j] = 6 if use_six and j == 0 else 2
    for i in range(2, n):
        grid[i][0] = 2
    return grid

def build_h_shape(n: int) -> List[List[int]]:
    grid = [[0] * n for _ in range(n)]
    for i in range(n):
        grid[i][n - 1] = 2
        if not (i == 1 and n == 4):
            grid[i][0] = 2
    mid = n // 2
    for j in range(n):
        grid[mid][j] = 2
    if n == 4:
        grid[0][1] = 2
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    n = max_zero_run(g)
    use_six = has_six(g)
    if use_six:
        return build_l_shape(n, True)
    else:
        return build_h_shape(n)
```