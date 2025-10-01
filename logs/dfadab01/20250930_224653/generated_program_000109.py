```python
from typing import List, Dict, Tuple

def draw_type_a(grid: List[List[int]], start_r: int, start_c: int, color: int, size: int = 4) -> None:
    """Draws a full outer border frame starting at (start_r, start_c) with given color and size, clipping to grid bounds."""
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
    """Draws an inner border frame starting at (start_r, start_c) with given color and size, clipping to grid bounds."""
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
    """Draws a type C inner frame (corners on top/bottom, inner columns on middle rows) starting at (start_r, start_c) with given color and size, clipping to grid bounds."""
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
    """Draws a step/L-shaped pattern (left half on top half rows, right half on bottom half rows) starting at (start_r, start_c) with given color and size, clipping to grid bounds."""
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
    """Detects if there is a complete type C pattern starting at (r, c) in the input grid, requiring exact match including zeros in non-pattern positions."""
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
    """Checks if the seed at (start_r, start_c) with value v is isolated in its window: exactly one v, no conflicting non-zero non-target values in existing cells (clips to grid bounds)."""
    n = len(g)
    m = len(g[0])
    count = 0
    conflicting = False
    for i in range(size):
        rr = start_r + i
        if rr >= n:
            continue
        for j in range(size):
            cc = start_c + j
            if cc >= m:
                continue
            gv = g[rr][cc]
            if gv == v:
                count += 1
            if (i != 0 or j != 0) and gv != 0 and gv != target:
                conflicting = True
    return count == 1 and not conflicting

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Initializes output grid to zeros, draws complete type C patterns from input, then expands isolated seeds to their mapped shapes."""
    if not g or not g[0]:
        return []
    n = len(g)
    m = len(g[0])
    out = [[0] * m for _ in range(n)]

    # Rule: Detect and draw complete type C patterns first, using their input value as color
    for r in range(n - 3):
        for c in range(m - 3):
            if detect_type_c(g, r, c):
                draw_type_c(out, r, c, g[r][c])

    # Mapping: Seed value to (type, color, size)
    v_map: Dict[int, Tuple[str, int, int]] = {
        1: ('b', 1, 4),
        2: ('a', 4, 4),
        3: ('b', 1, 4),
        5: ('step', 6, 4),
        7: ('c', 7, 4),
        8: ('c', 7, 4)
    }
    draw_dict: Dict[str, callable] = {
        'a': draw_type_a,
        'b': draw_type_b,
        'c': draw_type_c,
        'step': draw_step
    }

    # Rule: Scan for isolated seeds and draw their corresponding patterns
    for r in range(n):
        for c in range(m):
            v = g[r][c]
            if v in v_map:
                typ, color, sz = v_map[v]
                if is_isolated_seed(g, r, c, v, color, sz):
                    draw_dict[typ](out, r, c, color, sz)

    return out
```