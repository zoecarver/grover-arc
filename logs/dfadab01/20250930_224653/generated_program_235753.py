```python
from typing import List

def draw_type_a(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4):
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

def draw_type_b(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4):
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

def draw_type_c(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4):
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

def draw_step(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4):
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

def detect_type_c(g: List[List[int]], r: int, c: int) -> bool:
    size = 4
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
            if i == 0 or i == size - 1:
                if j == 0 or j == size - 1:
                    expected = v
            elif 1 <= i <= size - 2:
                if 1 <= j <= size - 2:
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

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    out = [[0] * m for _ in range(n)]
    # Detect and draw complete type C patterns
    for rr in range(n - 3):
        for cc in range(m - 3):
            if g[rr][cc] in {7, 8} and detect_type_c(g, rr, cc):
                draw_type_c(out, rr, cc, 7)
    # Process isolated seeds
    v_map = {
        1: ('b', 1, 4),
        2: ('a', 4, 4),
        3: ('b', 1, 4),
        5: ('step', 6, 4),
        7: ('c', 7, 4),
        8: ('c', 7, 4)
    }
    draw_dict = {
        'a': draw_type_a,
        'b': draw_type_b,
        'c': draw_type_c,
        'step': draw_step
    }
    seeds = set(v_map.keys())
    for rr in range(n):
        for cc in range(m):
            v = g[rr][cc]
            if v not in seeds:
                continue
            typ, target, sz = v_map[v]
            if rr + sz > n or cc + sz > m:
                continue
            if not is_isolated_seed(g, rr, cc, v, target, sz):
                continue
            draw_dict[typ](out, rr, cc, target, sz)
    return out
```