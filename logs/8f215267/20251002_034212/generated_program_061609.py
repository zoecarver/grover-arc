```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    """Identify the background color from the top-left corner."""
    return g[0][0]

def find_long_run(row: List[int], bg: int, min_len: int = 10) -> Tuple[int, int, int]:
    """Find the first long run of non-background color in the row."""
    c = None
    L = -1
    R = -1
    for j in range(len(row)):
        if row[j] != bg:
            if c is None:
                c = row[j]
                L = j
            R = j
        else:
            if c is not None and R - L + 1 >= min_len:
                return c, L, R
            c = None
            L = -1
            R = -1
    if c is not None and R - L + 1 >= min_len:
        return c, L, R
    return None, None, None

def is_solid_run(row: List[int], bg: int, L: int, R: int, c: int) -> bool:
    """Check if the segment from L to R in row is solidly color c."""
    for j in range(L, R + 1):
        if row[j] != c:
            return False
    return True

def has_side_walls(g: List[List[int]], start_r: int, end_r: int, L: int, R: int, c: int) -> bool:
    """Check if all inner rows have color c at columns L and R."""
    for r in range(start_r + 1, end_r):
        if g[r][L] != c or g[r][R] != c:
            return False
    return True

def find_blocks(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int, int]]:
    """Find all 5-row block structures based on solid top/bottom and side walls."""
    n = len(g)
    blocks = []
    for i in range(n - 4):
        c, L, R = find_long_run(g[i], bg)
        if c is None:
            continue
        cb, Lb, Rb = find_long_run(g[i + 4], bg)
        if cb != c or not is_solid_run(g[i + 4], bg, Lb, Rb, c):
            continue
        if not has_side_walls(g, i, i + 4, L, R, c):
            continue
        left = min(L, Lb)
        right = max(R, Rb)
        blocks.append((i, i + 4, left, right, c))
    return blocks

def complete_block(out: List[List[int]], bg: int, block: Tuple[int, int, int, int, int]):
    """Complete a detected block: fill top/bottom solid, sides in inner rows, and middle pattern."""
    start_r, end_r, left, right, c = block
    # Fill top and bottom solid
    for col in range(left, right + 1):
        out[start_r][col] = c
        out[end_r][col] = c
    # Fill sides and background inner columns in inner rows
    for r in range(start_r + 1, end_r):
        out[r][left] = c
        out[r][right] = c
        for col in range(left + 1, right):
            out[r][col] = bg
    # Add pattern in middle row (2nd inner row)
    middle_r = start_r + 2
    k = c // 2
    k = min(4, k)
    for ii in range(1, k + 1):
        col = right - 2 * ii
        if left <= col <= right:
            out[middle_r][col] = c

def clean_small_components(g: List[List[int]], out: List[List[int]], bg: int, min_size: int = 10):
    """Flood fill and remove small connected components of non-background colors."""
    n = len(g)
    m = len(g[0])
    visited = [[False] * m for _ in range(n)]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(n):
        for col in range(m):
            if out[r][col] != bg and not visited[r][col]:
                current_c = out[r][col]
                to_clean = []
                stack = [(r, col)]
                visited[r][col] = True
                size = 0
                while stack:
                    cr, cc = stack.pop()
                    to_clean.append((cr, cc))
                    size += 1
                    for dr, dc in dirs:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc] and out[nr][nc] == current_c:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                if size < min_size:
                    for pr, pc in to_clean:
                        out[pr][pc] = bg

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: find and complete blocks, then clean small components."""
    bg = get_background(g)
    out = [row[:] for row in g]
    blocks = find_blocks(g, bg)
    for block in blocks:
        complete_block(out, bg, block)
    clean_small_components(g, out, bg)
    return out
```