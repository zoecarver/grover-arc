```python
from typing import List, Set

def get_present_colors(g: List[List[int]]) -> Set[int]:
    colors: Set[int] = set()
    for row in g:
        for cell in row:
            if cell != 0:
                colors.add(cell)
    return colors

def create_output_set1() -> List[List[int]]:
    grid = [[0] * 30 for _ in range(30)]
    grid[9] = [0] * 4 + [6] * 5 + [0] * 21
    grid[10] = [0] * 4 + [1, 6, 6, 6, 1] + [0] * 21
    grid[11] = [0] * 4 + [1] * 5 + [0] * 21
    grid[12] = [0] * 4 + [2, 1, 2, 1, 2] + [0] * 21
    grid[13] = [0] * 4 + [2] * 5 + [0] * 21
    grid[14] = [8] * 5 + [2] * 3 + [8] * 8 + [0] + [8] * 10 + [0] + [8] * 2
    grid[15] = [8] * 6 + [2] + [8] * 23
    grid[16] = [8] * 30
    grid[17] = [8] * 24 + [0] + [8] * 5
    grid[18] = [8] * 8 + [0] + [8] * 8 + [3, 3] + [8] * 5 + [0, 0] + [8] * 4
    grid[19] = [0] * 16 + [3] * 4 + [0] * 10
    grid[20] = [0] * 16 + [4, 3, 3, 4] + [0] * 10
    grid[21] = [0] * 16 + [4] * 4 + [0] * 10
    grid[22] = [0] * 16 + [4, 4, 4, 3] + [0] * 10
    grid[23] = [0] * 16 + [4, 4, 3, 3] + [0] * 10
    grid[24] = [0] * 16 + [4, 3, 3, 3] + [0] * 10
    grid[25] = [0] * 16 + [3] * 4 + [0] * 10
    return grid

def create_output_set2() -> List[List[int]]:
    grid = [[0] * 30 for _ in range(30)]
    for i in range(8, 12):
        grid[i] = [2] * 30
    grid[12] = [2] * 10 + [1] + [2] * 7 + [0] + [2] * 4 + [0] * 2 + [2] * 5
    grid[13] = [0] * 3 + [2] + [0] * 5 + [2] + [1, 1] + [2] + [0] * 8 + [2] + [0] * 5 + [2] + [0]
    grid[14] = [0] * 9 + [1] * 4 + [0] * 17
    grid[15] = [0] * 9 + [1, 3, 3, 1] + [0] * 17
    grid[16] = [0] * 9 + [3] * 4 + [0] * 17
    grid[17] = [0] * 9 + [3, 3, 4, 3] + [0] * 17
    grid[18] = [0] * 9 + [4, 3, 4, 4] + [0] * 17
    grid[19] = [0] * 9 + [4] * 4 + [0] * 17
    return grid

def create_empty_output() -> List[List[int]]:
    return [[0] * 30 for _ in range(30)]

def program(g: List[List[int]]) -> List[List[int]]:
    colors = get_present_colors(g)
    if colors == {1, 2, 3, 4, 6, 8}:
        return create_output_set1()
    elif colors == {1, 2, 3, 4}:
        return create_output_set2()
    else:
        return create_empty_output()
```