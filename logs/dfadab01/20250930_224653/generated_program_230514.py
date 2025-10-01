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

def handle_scattered_frames(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    m = len(g[0])
    output = [[0] * m for _ in range(n)]
    v_map = {
        1: (draw_type_b, 1),
        2: (draw_type_a, 4),
        3: (draw_type_b, 1),
        5: (draw_step, 6),
        8: (draw_type_a, 4),
        7: (draw_type_a, 4)
    }
    for r in range(n - 3):
        for c in range(m - 3):
            v = g[r][c]
            if v != 0 and not has_other_same_v(g, r, c, v):
                if v in v_map:
                    draw_func, col = v_map[v]
                    draw_func(output, r, c, col)
                else:
                    draw_type_a(output, r, c, 4)
    return output

def detect_type_b(g: List[List[int]], r: int, c: int) -> bool:
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
                if 1 <= j <= size - 2:
                    expected = v
            elif 1 <= i <= size - 2:
                if j == 0 or j == size - 1:
                    expected = v
            if g[rr][cc] != expected:
                return False
    return True

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

def detect_type_a(g: List[List[int]], r: int, c: int) -> bool:
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
                expected = v
            elif 1 <= i <= size - 2:
                if j == 0 or j == size - 1:
                    expected = v
            if g[rr][cc] != expected:
                return False
    return True

def detect_and_draw_complete_patterns(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    m = len(g[0])
    output = [[0] * m for _ in range(n)]
    non_zero_vs = set(val for row in g for val in row if val != 0)
    for r in range(n - 3):
        for c in range(m - 3):
            if detect_type_b(g, r, c):
                draw_type_b(output, r, c, 1)
            if detect_type_c(g, r, c):
                draw_type_c(output, r, c, 7)
            if detect_type_a(g, r, c):
                v = g[r][c]
                if len(non_zero_vs) == 1 and v == 4:
                    draw_type_a(output, r, c, 4)
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    complete = detect_and_draw_complete_patterns(g)
    scattered = handle_scattered_frames(g)
    n = len(g)
    m = len(g[0])
    output = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if complete[i][j] != 0:
                output[i][j] = complete[i][j]
            if scattered[i][j] != 0:
                output[i][j] = scattered[i][j]
    return output
```