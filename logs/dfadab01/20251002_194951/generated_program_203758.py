```python
from typing import List, Set, Tuple, Optional

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

def get_pattern_set(typ: str) -> Set[Tuple[int, int]]:
    if typ == 'rectangle':
        s: Set[Tuple[int, int]] = set()
        for k in range(4):
            s.add((0, k))
            s.add((3, k))
        s.add((1, 0))
        s.add((1, 3))
        s.add((2, 0))
        s.add((2, 3))
        return s
    elif typ == 'diamond':
        return {
            (0, 1), (0, 2), (3, 1), (3, 2),
            (1, 0), (1, 3), (2, 0), (2, 3)
        }
    elif typ == 'z':
        return {
            (0, 0), (0, 1), (1, 0), (1, 1),
            (2, 2), (2, 3), (3, 2), (3, 3)
        }
    elif typ == 'anti_diamond':
        return {
            (0, 0), (0, 3), (3, 0), (3, 3),
            (1, 1), (1, 2), (2, 1), (2, 2)
        }
    return set()

def is_valid(g: List[List[int]], i: int, j: int, pattern_set: Set[Tuple[int, int]]) -> bool:
    for di in range(4):
        for dj in range(4):
            if g[i + di][j + dj] != 0:
                rel = (di, dj)
                if rel != (0, 0) and rel not in pattern_set:
                    return False
    return True

def fill_pattern(out: List[List[int]], i: int, j: int, pattern_set: Set[Tuple[int, int]], color: int) -> None:
    for di, dj in pattern_set:
        out[i + di][j + dj] = color

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [[0] * n for _ in range(n)]
    for i in range(n - 3):
        for j in range(n - 3):
            v = g[i][j]
            typ, color = get_type_color(v)
            if typ is not None:
                pat = get_pattern_set(typ)
                if is_valid(g, i, j, pat):
                    fill_pattern(out, i, j, pat, color)
    return out
```