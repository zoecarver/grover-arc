```python
from typing import List, Tuple, Optional, Set

def get_type_color(v: int) -> Tuple[Optional[str], int]:
    if v == 2:
        return 'rectangle', 4
    if v == 3:
        return 'diamond', 1
    if v == 5:
        return 'z', 6
    if v == 7 or v == 8:
        return 'anti_diamond', 7
    return None, 0

def get_rectangle_pattern() -> Set[Tuple[int, int]]:
    s: Set[Tuple[int, int]] = set()
    for k in range(4):
        s.add((0, k))
        s.add((3, k))
    s.add((1, 0))
    s.add((1, 3))
    s.add((2, 0))
    s.add((2, 3))
    return s

def get_diamond_pattern() -> Set[Tuple[int, int]]:
    return {
        (0, 1), (0, 2), (3, 1), (3, 2),
        (1, 0), (1, 3), (2, 0), (2, 3)
    }

def get_z_pattern() -> Set[Tuple[int, int]]:
    return {
        (0, 0), (0, 1), (1, 0), (1, 1),
        (2, 2), (2, 3), (3, 2), (3, 3)
    }

def get_anti_diamond_pattern() -> Set[Tuple[int, int]]:
    return {
        (0, 0), (0, 3), (3, 0), (3, 3),
        (1, 1), (1, 2), (2, 1), (2, 2)
    }

def get_pattern_set(typ: str) -> Set[Tuple[int, int]]:
    if typ == 'rectangle':
        return get_rectangle_pattern()
    if typ == 'diamond':
        return get_diamond_pattern()
    if typ == 'z':
        return get_z_pattern()
    if typ == 'anti_diamond':
        return get_anti_diamond_pattern()
    return set()

def is_valid_block(g: List[List[int]], i: int, j: int, pattern_set: Set[Tuple[int, int]]) -> bool:
    for di in range(4):
        for dj in range(4):
            val = g[i + di][j + dj]
            if val != 0:
                rel = (di, dj)
                if rel != (0, 0) and rel not in pattern_set:
                    return False
    return True

def fill_pattern(out: List[List[int]], i: int, j: int, pattern_set: Set[Tuple[int, int]], color: int) -> None:
    for di, dj in pattern_set:
        out[i + di][j + dj] = color

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out: List[List[int]] = [[0] * n for _ in range(n)]
    for i in range(n - 3):
        for j in range(n - 3):
            typ, color = get_type_color(g[i][j])
            if typ is not None:
                pattern_set = get_pattern_set(typ)
                if is_valid_block(g, i, j, pattern_set):
                    fill_pattern(out, i, j, pattern_set, color)
    return out
```