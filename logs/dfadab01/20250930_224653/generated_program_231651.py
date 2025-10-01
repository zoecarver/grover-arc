```python
from typing import List, Tuple

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

def is_isolated_seed(g: List[List[int]], start_r: int, start_c: int, v: int, target: int, size: int = 4) -> bool:
    n = len(g)
    m = len(g[0])
    count = 0
    conflicting = False
    for i in range(size):
        rr = start_r + i
        if rr >= n:
            return False
        for j in range(size):
            cc = start_c + j
            if cc >= m:
                return False
            gv = g[rr][cc]
            if gv == v:
                count += 1
            if gv != 0 and not (i == 0 and j == 0) and gv != target:
                conflicting = True
    return count == 1 and not conflicting

def draw_complete_type_c(g: List[List[int]], out: List[List[int]]):
    n = len(g)
    m = len(g[0])
    size = 4
    for start_r in range(n - size + 1):
        for start_c in range(m - size + 1):
            if detect_type_c(g, start_r, start_c):
                v = g[start_r][start_c]
                draw_type_c(out, start_r, start_c, v, size)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    m = len(g[0])
    out = [[0] * m for _ in range(n)]
    seed_map: dict[int, Tuple[str, int]] = {
        2: ("a", 4),
        3: ("b", 1),
        5: ("step", 6),
        7: ("c", 7),
        8: ("c", 7)
    }
    size = 4
    for r in range(n):
        for c in range(m):
            if r + size > n or c + size > m:
                continue
            v = g[r][c]
            if v not in seed_map:
                continue
            typ, target = seed_map[v]
            if is_isolated_seed(g, r, c, v, target, size):
                if typ == "a":
                    draw_type_a(out, r, c, target, size)
                elif typ == "b":
                    draw_type_b(out, r, c, target, size)
                elif typ == "step":
                    draw_step(out, r, c, target, size)
                elif typ == "c":
                    draw_type_c(out, r, c, target, size)
    draw_complete_type_c(g, out)
    return out
```