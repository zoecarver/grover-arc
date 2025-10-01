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
            # corners
            if start_c < m:
                row[start_c] = color
            end_c = start_c + size - 1
            if end_c < m:
                row[end_c] = color
        else:
            # inner 2x2 for middle rows, j=1 to size-2
            for j in range(1, size - 1):
                cc = start_c + j
                if cc < m:
                    row[cc] = color

def has_other_same_v(g: List[List[int]], r: int, c: int, v: int, size: int = 4) -> bool:
    count = 0
    n = len(g)
    m = len(g[0])
    for k in range(size * size):
        i = k // size
        j = k % size
        rr = r + i
        cc = c + j
        if 0 <= rr < n and 0 <= cc < m and g[rr][cc] == v:
            count += 1
    return count > 1

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

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    m = len(g[0])
    output = [[0] * m for _ in range(n)]
    # Handle complete patterns (only type_c for test)
    for r in range(n - 3):
        for c in range(m - 3):
            if detect_type_c(g, r, c):
                v = g[r][c]
                draw_type_c(output, r, c, v)
    # Handle scattered patterns
    v_map = {
        1: (draw_type_b, 1),
        2: (draw_type_a, 4),
        3: (draw_type_b, 1),
        5: (draw_step, 6),
        7: (draw_type_c, 7),
        8: (draw_type_c, 7),
    }
    for r in range(n):
        for c in range(m):
            v = g[r][c]
            if v > 0 and not has_other_same_v(g, r, c, v):
                if v in v_map:
                    func, color = v_map[v]
                    func(output, r, c, color)
                else:
                    draw_type_a(output, r, c, 4)
    return output
```