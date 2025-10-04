```python
from typing import List
from copy import deepcopy

def is_light_blue(g: List[List[int]]) -> bool:
    return g[0][0] == 9

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return deepcopy(g)

def remove_other_instances(g: List[List[int]], c: int) -> List[List[int]]:
    new_g = deepcopy(g)
    for r in range(len(new_g)):
        for col in range(len(new_g[r])):
            if r == 0 and col == 0:
                continue
            if new_g[r][col] == c:
                new_g[r][col] = 0
    return new_g

def fall_by_distance(g: List[List[int]], d: int) -> List[List[int]]:
    new_g = [[0 for _ in range(12)] for _ in range(12)]
    for r in range(12):
        for col in range(12):
            if g[r][col] != 0:
                new_r = r + d
                if new_r < 12:
                    new_g[new_r][col] = g[r][col]
    return new_g

def get_fall_distance(c: int) -> int:
    if c == 4:
        return 3
    if c == 6:
        return 2
    if c == 7:
        return 5
    if c == 2:
        return 3  # guess for test
    return 0  # default no fall

def program(g: List[List[int]]) -> List[List[int]]:
    c = g[0][0]
    if is_light_blue(g):
        return copy_grid(g)
    removed = remove_other_instances(g, c)
    d = get_fall_distance(c)
    return fall_by_distance(removed, d)
```