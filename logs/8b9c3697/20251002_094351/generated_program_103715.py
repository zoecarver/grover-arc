```python
from typing import List, Tuple

def is_structure(val: int, bg: int) -> bool:
    return val != bg and val != 0 and val != 2

def find_components(grid: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    height = len(grid)
    if height == 0:
        return []
    width = len(grid[0])
    visited = [[False] * width for _ in range(height)]
    comps = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(height):
        for c in range(width):
            if grid[r][c] == 2 and not visited[r][c]:
                minr, maxr, minc, maxc = r, r, c, c
                stack = [(r, c)]
                visited[r][c] = True
                size = 1
                while stack:
                    x, y = stack.pop()
                    minr = min(minr, x)
                    maxr = max(maxr, x)
                    minc = min(minc, y)
                    maxc = max(maxc, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width and grid[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            size += 1
                bb_h = maxr - minr + 1
                bb_w = maxc - minc + 1
                if size == bb_h * bb_w:
                    comps.append((minr, maxr, minc, maxc))
    return comps

def try_vertical_move(grid: List[List[int]], height: int, width: int, bg: int,
                      min_r: int, max_r: int, min_c: int, max_c: int) -> bool:
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    best_gap = float('inf')
    best_new_min_r = None
    best_new_max_r = None
    # Try up moves
    min_t = max(0, min_r - 9)
    for t in range(min_r - 1, min_t - 1, -1):
        gap = min_r - t - 1
        if gap > 8:
            continue
        valid = True
        for j in range(min_c, max_c + 1):
            if not is_structure(grid[t][j], bg):
                valid = False
                break
            for rr in range(t + 1, min_r):
                if grid[rr][j] != bg:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            continue
        new_min_r = t + 1
        new_max_r = new_min_r + h - 1
        if new_max_r >= height:
            continue
        valid = True
        for j in range(min_c, max_c + 1):
            for rr in range(new_min_r, new_max_r + 1):
                if grid[rr][j] != bg:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            continue
        span_min_r = min(new_min_r, min_r)
        span_max_r = max(new_max_r, max_r)
        valid = True
        for j in range(min_c, max_c + 1):
            for rr in range(span_min_r, span_max_r + 1):
                if min_r <= rr <= max_r:
                    continue
                if grid[rr][j] != bg:
                    valid = False
                    break
            if not valid:
                break
        if valid and gap < best_gap:
            best_gap = gap
            best_new_min_r = new_min_r
            best_new_max_r = new_max_r
    # Try down moves
    max_t = min(height - 1, max_r + 9)
    for t in range(max_r + 1, max_t + 1):
        gap = t - max_r - 1
        if gap > 8:
            continue
        valid = True
        for j in range(min_c, max_c + 1):
            if not is_structure(grid[t][j], bg):
                valid = False
                break
            for rr in range(max_r + 1, t):
                if grid[rr][j] != bg:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            continue
        new_max_r = t - 1
        new_min_r = new_max_r - h + 1
        if new_min_r < 0:
            continue
        valid = True
        for j in range(min_c, max_c + 1):
            for rr in range(new_min_r, new_max_r + 1):
                if grid[rr][j] != bg:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            continue
        span_min_r = min(new_min_r, min_r)
        span_max_r = max(new_max_r, max_r)
        valid = True
        for j in range(min_c, max_c + 1):
            for rr in range(span_min_r, span_max_r + 1):
                if min_r <= rr <= max_r:
                    continue
                if grid[rr][j] != bg:
                    valid = False
                    break
            if not valid:
                break
        if valid and gap < best_gap:
            best_gap = gap
            best_new_min_r = new_min_r
            best_new_max_r = new_max_r
    if best_gap < float('inf'):
        span_min_r = min(best_new_min_r, min_r)
        span_max_r = max(best_new_max_r, max_r)
        for r in range(span_min_r, span_max_r + 1):
            for c in range(min_c, max_c + 1):
                grid[r][c] = 0
        for r in range(best_new_min_r, best_new_max_r + 1):
            for c in range(min_c, max_c + 1):
                grid[r][c] = 2
        return True
    return False

def try_horizontal_move(grid: List[List[int]], height: int, width: int, bg: int,
                        min_r: int, max_r: int, min_c: int, max_c: int) -> bool:
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    best_gap = float('inf')
    best_new_min_c = None
    best_new_max_c = None
    # Try left moves
    min_t = max(0, min_c - 9)
    for t in range(min_c - 1, min_t - 1, -1):
        gap = min_c - t - 1
        if gap > 8:
            continue
        valid = True
        for i in range(min_r, max_r + 1):
            if not is_structure(grid[i][t], bg):
                valid = False
                break
            for cc in range(t + 1, min_c):
                if grid[i][cc] != bg:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            continue
        new_min_c = t + 1
        new_max_c = new_min_c + w - 1
        if new_max_c >= width:
            continue
        valid = True
        for i in range(min_r, max_r + 1):
            for cc in range(new_min_c, new_max_c + 1):
                if grid[i][cc] != bg:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            continue
        span_min_c = min(new_min_c, min_c)
        span_max_c = max(new_max_c, max_c)
        valid = True
        for i in range(min_r, max_r + 1):
            for cc in range(span_min_c, span_max_c + 1):
                if min_c <= cc <= max_c:
                    continue
                if grid[i][cc] != bg:
                    valid = False
                    break
            if not valid:
                break
        if valid and gap < best_gap:
            best_gap = gap
            best_new_min_c = new_min_c
            best_new_max_c = new_max_c
    # Try right moves
    max_t = min(width - 1, max_c + 9)
    for t in range(max_c + 1, max_t + 1):
        gap = t - max_c - 1
        if gap > 8:
            continue
        valid = True
        for i in range(min_r, max_r + 1):
            if not is_structure(grid[i][t], bg):
                valid = False
                break
            for cc in range(max_c + 1, t):
                if grid[i][cc] != bg:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            continue
        new_max_c = t - 1
        new_min_c = new_max_c - w + 1
        if new_min_c < 0:
            continue
        valid = True
        for i in range(min_r, max_r + 1):
            for cc in range(new_min_c, new_max_c + 1):
                if grid[i][cc] != bg:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            continue
        span_min_c = min(new_min_c, min_c)
        span_max_c = max(new_max_c, max_c)
        valid = True
        for i in range(min_r, max_r + 1):
            for cc in range(span_min_c, span_max_c + 1):
                if min_c <= cc <= max_c:
                    continue
                if grid[i][cc] != bg:
                    valid = False
                    break
            if not valid:
                break
        if valid and gap < best_gap:
            best_gap = gap
            best_new_min_c = new_min_c
            best_new_max_c = new_max_c
    if best_gap < float('inf'):
        span_min_c = min(best_new_min_c, min_c)
        span_max_c = max(best_new_max_c, max_c)
        for r in range(min_r, max_r + 1):
            for c in range(span_min_c, span_max_c + 1):
                grid[r][c] = 0
        for r in range(min_r, max_r + 1):
            for c in range(best_new_min_c, best_new_max_c + 1):
                grid[r][c] = 2
        return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    height = len(g)
    width = len(g[0])
    bg = g[0][0]
    out = [row[:] for row in g]
    components = find_components(out, bg)
    components.sort(key=lambda x: (x[0], x[2]))
    for min_r, max_r, min_c, max_c in components:
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        # Verify solid (redundant but safe)
        solid = all(out[r][c] == 2 for r in range(min_r, max_r + 1) for c in range(min_c, max_c + 1))
        if not solid:
            continue
        moved = False
        if h == 1:
            if try_horizontal_move(out, height, width, bg, min_r, max_r, min_c, max_c):
                moved = True
            elif w == 1:
                if try_vertical_move(out, height, width, bg, min_r, max_r, min_c, max_c):
                    moved = True
        else:
            if w == 1:
                if try_vertical_move(out, height, width, bg, min_r, max_r, min_c, max_c):
                    moved = True
            else:
                if try_vertical_move(out, height, width, bg, min_r, max_r, min_c, max_c):
                    moved = True
                elif try_horizontal_move(out, height, width, bg, min_r, max_r, min_c, max_c):
                    moved = True
        if not moved:
            for r in range(min_r, max_r + 1):
                for c in range(min_c, max_c + 1):
                    out[r][c] = bg
    return out
```