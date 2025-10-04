```python
from typing import List, Tuple, Set

def get_patterns() -> dict:
    h_pattern = [(0,1),(0,2),(1,0),(1,3),(2,0),(2,3),(3,1),(3,2)]
    u_pattern = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,3),(2,0),(2,3),(3,0),(3,1),(3,2),(3,3)]
    z_pattern = [(0,0),(0,1),(1,0),(1,1),(2,2),(2,3),(3,2),(3,3)]
    o_pattern = [(0,0),(0,3),(1,1),(1,2),(2,1),(2,2),(3,0),(3,3)]
    return {
        1: (1, h_pattern),
        2: (4, u_pattern),
        3: (1, h_pattern),
        5: (6, z_pattern),
        7: (7, o_pattern),
        8: (7, o_pattern)
    }

def is_isolated(g: List[List[int]], r: int, c: int, size: int) -> bool:
    for dr in range(4):
        for dc in range(4):
            if dr == 0 and dc == 0:
                continue
            if r + dr >= size or c + dc >= size:
                return False
            if g[r + dr][c + dc] != 0:
                return False
    return True

def matches_pattern(g: List[List[int]], r: int, c: int, pattern: List[Tuple[int, int]], target_color: int, size: int) -> bool:
    pat_set: Set[Tuple[int, int]] = set(pattern)
    # Check all pattern positions have target_color
    for dr, dc in pattern:
        if r + dr >= size or c + dc >= size:
            return False
        if g[r + dr][c + dc] != target_color:
            return False
    # Check non-pattern positions except seed are 0
    for dr in range(4):
        for dc in range(4):
            if r + dr >= size or c + dc >= size:
                return False
            pos = (dr, dc)
            if pos not in pat_set and not (dr == 0 and dc == 0):
                if g[r + dr][c + dc] != 0:
                    return False
    return True

def draw_shape(out: List[List[int]], r: int, c: int, pattern: List[Tuple[int, int]], color: int, size: int) -> None:
    pat_set: Set[Tuple[int, int]] = set(pattern)
    for dr in range(4):
        for dc in range(4):
            if r + dr >= size or c + dc >= size:
                continue
            if (dr, dc) in pat_set:
                out[r + dr][c + dc] = color
            else:
                out[r + dr][c + dc] = 0

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    size = len(g)
    out = [[0] * size for _ in range(size)]
    mapping = get_patterns()
    for i in range(size):
        for j in range(size):
            k = g[i][j]
            if k == 0:
                continue
            if i + 3 >= size or j + 3 >= size:
                continue
            if k not in mapping:
                continue
            color, pattern = mapping[k]
            if is_isolated(g, i, j, size) or matches_pattern(g, i, j, pattern, color, size):
                draw_shape(out, i, j, pattern, color, size)
    return out
```