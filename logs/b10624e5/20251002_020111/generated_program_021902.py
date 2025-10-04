```python
from typing import List
from copy import deepcopy

def make_grid_copy(g: List[List[int]]) -> List[List[int]]:
    return deepcopy(g)

def apply_left_right_symmetry(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    for i in range(n):
        left_non4 = []
        right_non4 = []
        for j in range(13):
            left_pos = g[i][j]
            right_pos = g[i][26 - j]
            if left_pos != 4:
                left_non4.append((j, left_pos))
            if right_pos != 4:
                right_non4.append((26 - j, right_pos))
        for j, color in left_non4:
            sym_j = 26 - j
            if g[i][sym_j] == 4:
                g[i][sym_j] = color
        for j, color in right_non4:
            sym_j = 26 - j
            if g[i][sym_j] == 4:
                g[i][sym_j] = color
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(g)
    g = apply_left_right_symmetry(g)
    return g
```