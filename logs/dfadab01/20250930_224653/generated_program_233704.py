```python
from typing import List

def draw_type_a(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4):
    # Draws a full outer border frame based on seed value 2 or similar, using yellow (4).
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
    # Draws an inner border frame based on seed value 1 or 3, using blue (1).
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
    # Draws an inner frame with corners and middle inners based on seed value 7/8 or complete detection, using dark red (7).
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
            # inner for middle rows, j=1 to size-2
            for j in range(1, size - 1):
                cc = start_c + j
                if cc < m:
                    row[cc] = color

def draw_step(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4):
    # Draws an L-shaped step based on seed value 5, using pink (6).
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
    # Detects complete type C inner frame pattern in input for preservation/redraw with original value.
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
    # Main program: Initializes zero output grid, draws complete type C patterns first, then processes isolated seeds with mappings.
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    output = [[0] * m for _ in range(n)]

    # Step 1: Detect and draw complete type C patterns from input (preserves/redraws inner frames with original value).
    for r in range(n - 3):
        for c in range(m - 3):
            if detect_type_c(g, r, c):
                v = g[r][c]
                draw_type_c(output, r, c, v)

    # Step 2: Process scattered isolated seeds, drawing mapped patterns if unique same-value and no conflicting non-target non-zeros in window.
    draw_dict = {
        'a': draw_type_a,
        'b': draw_type_b,
        'c': draw_type_c,
        'step': draw_step
    }
    v_map = {
        1: ('b', 1),
        2: ('a', 4),
        3: ('b', 1),
        5: ('step', 6),
        7: ('c', 7),
        8: ('c', 7)
    }
    for r in range(n):
        for c in range(m):
            v = g[r][c]
            if v == 0 or v not in v_map:
                continue
            if r > n - 4 or c > m - 4:
                continue
            typ, target = v_map[v]
            count_same = 0
            conflict = False
            for i in range(4):
                for j in range(4):
                    rr = r + i
                    cc = c + j
                    gv = g[rr][cc]
                    if gv == v:
                        count_same += 1
                    if (i != 0 or j != 0) and gv != 0 and gv != target:
                        conflict = True
            if count_same == 1 and not conflict:
                draw_dict[typ](output, r, c, target)

    return output
```