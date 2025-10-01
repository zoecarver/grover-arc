```python
from typing import List, Dict, Tuple

def draw_type_a(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4) -> None:
    n = len(grid)
    m = len(grid[0])
    for i in range(size):
        r = start_r + i
        if r >= n:
            break
        row = grid[r]
        if i == 0 or i == size - 1:
            for j in range(start_c, start_c + size):
                if j < m:
                    row[j] = color
        else:
            if start_c < m:
                row[start_c] = color
            end_c = start_c + size - 1
            if end_c < m:
                row[end_c] = color

def draw_type_b(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4) -> None:
    n = len(grid)
    m = len(grid[0])
    for i in range(size):
        r = start_r + i
        if r >= n:
            break
        row = grid[r]
        if i == 0 or i == size - 1:
            for j in range(start_c + 1, start_c + size - 1):
                if j < m:
                    row[j] = color
        else:
            if start_c < m:
                row[start_c] = color
            end_c = start_c + size - 1
            if end_c < m:
                row[end_c] = color

def draw_type_c(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4) -> None:
    n = len(grid)
    m = len(grid[0])
    for i in range(size):
        r = start_r + i
        if r >= n:
            break
        row = grid[r]
        if i == 0 or i == size - 1:
            if start_c < m:
                row[start_c] = color
            end_c = start_c + size - 1
            if end_c < m:
                row[end_c] = color
        else:
            for j in range(1, size - 1):
                cc = start_c + j
                if cc < m:
                    row[cc] = color

def draw_step(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4) -> None:
    n = len(grid)
    m = len(grid[0])
    half = size // 2
    for i in range(half):
        r = start_r + i
        if r >= n:
            break
        row = grid[r]
        for j in range(start_c, start_c + half):
            if j < m:
                row[j] = color
    for i in range(half, size):
        r = start_r + i
        if r >= n:
            break
        row = grid[r]
        for j in range(start_c + half, start_c + size):
            if j < m:
                row[j] = color

def detect_type_c(g: List[List[int]], r: int, c: int, size: int = 4) -> bool:
    n = len(g)
    m = len(g[0])
    if r + size > n or c + size > m:
        return False
    v = g[r][c]
    if v == 0:
        return False
    for i in range(size):
        for j in range(size):
            rr = r + i
            cc = c + j
            expected = 0
            if (i == 0 or i == size - 1) and (j == 0 or j == size - 1):
                expected = v
            elif 1 <= i < size - 1 and 1 <= j < size - 1:
                expected = v
            if g[rr][cc] != expected:
                return False
    return True

def is_isolated_seed(g: List[List[int]], r: int, c: int, v: int, target: int, size: int = 4) -> bool:
    n = len(g)
    m = len(g[0])
    if r + size > n or c + size > m:
        return False
    count = 0
    conflicting = False
    for i in range(size):
        rr = r + i
        for j in range(size):
            cc = c + j
            gv = g[rr][cc]
            if gv == v:
                count += 1
            if (i != 0 or j != 0) and gv != 0 and gv != target:
                conflicting = True
    return count == 1 and not conflicting

def initialize_output(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    m = len(g[0])
    return [[0] * m for _ in range(n)]

def draw_complete_type_c_patterns(g: List[List[int]], output: List[List[int]]) -> None:
    n = len(g)
    m = len(g[0])
    size = 4
    for r in range(n - size + 1):
        for c in range(m - size + 1):
            if detect_type_c(g, r, c, size):
                v = g[r][c]
                draw_type_c(output, r, c, v, size)

def draw_isolated_seeds(g: List[List[int]], output: List[List[int]], v_map: Dict[int, Tuple[str, int]], draw_dict: Dict[str, callable]) -> None:
    n = len(g)
    m = len(g[0])
    size = 4
    for r in range(n - size + 1):
        for c in range(m - size + 1):
            v = g[r][c]
            if v in v_map:
                typ, target = v_map[v]
                if is_isolated_seed(g, r, c, v, target, size):
                    draw_dict[typ](output, r, c, target, size)

def program(g: List[List[int]]) -> List[List[int]]:
    output = initialize_output(g)
    v_map: Dict[int, Tuple[str, int]] = {
        1: ('b', 1),
        2: ('a', 4),
        3: ('b', 1),
        5: ('step', 6),
        7: ('c', 7),
        8: ('c', 7)
    }
    draw_dict: Dict[str, callable] = {
        'a': draw_type_a,
        'b': draw_type_b,
        'c': draw_type_c,
        'step': draw_step
    }
    draw_complete_type_c_patterns(g, output)
    draw_isolated_seeds(g, output, v_map, draw_dict)
    return output
```