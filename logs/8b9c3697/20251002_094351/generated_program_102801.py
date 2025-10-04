```python
from typing import List, Tuple
import sys

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def get_nonbg_segments_row(grid: List[List[int]], row: int, bg: int, width: int) -> List[Tuple[int, int, int]]:
    line = grid[row]
    segments = []
    i = 0
    while i < width:
        if line[i] != bg and line[i] != 2:
            start = i
            while i < width and line[i] != bg and line[i] != 2:
                i += 1
            end = i - 1
            length = end - start + 1
            segments.append((start, end, length))
        else:
            i += 1
    return segments

def get_nonbg_segments_col(grid: List[List[int]], col: int, bg: int, height: int) -> List[Tuple[int, int, int]]:
    segments = []
    i = 0
    while i < height:
        if grid[i][col] != bg and grid[i][col] != 2:
            start = i
            while i < height and grid[i][col] != bg and grid[i][col] != 2:
                i += 1
            end = i - 1
            length = end - start + 1
            segments.append((start, end, length))
        else:
            i += 1
    return segments

def find_components(grid: List[List[int]], bg: int) -> List[Tuple[List[Tuple[int, int]], int, int, int, int, int]]:
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    visited = [[False] * width for _ in range(height)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(height):
        for c in range(width):
            if grid[r][c] == 2 and not visited[r][c]:
                component = []
                min_r = max_r = r
                min_c = max_c = c
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < height and 0 <= ny < width and grid[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((component, min_r, max_r, min_c, max_c, len(component)))
    return components

def process_horizontal(grid: List[List[int]], row: int, min_c: int, max_c: int, bg: int, w: int, width: int, height: int) -> bool:
    segs = get_nonbg_segments_row(grid, row, bg, width)
    best_seg = None
    min_gap = float('inf')
    for start, end, leng in segs:
        if end >= min_c:
            continue
        gap = min_c - end - 1
        if gap <= 8 and gap < min_gap and leng >= w:
            min_gap = gap
            best_seg = (start, end, leng)
    if best_seg is None:
        return False
    new_min_c = best_seg[1] + 1
    new_max_c = new_min_c + w - 1
    if new_max_c >= width:
        return False
    ok = True
    for c in range(new_min_c, new_max_c + 1):
        if grid[row][c] != bg:
            ok = False
            break
    if not ok:
        return False
    swept_min_c = min(min_c, new_min_c)
    swept_max_c = max(max_c, new_max_c)
    for c in range(swept_min_c, swept_max_c + 1):
        grid[row][c] = 0
    for c in range(new_min_c, new_max_c + 1):
        grid[row][c] = 2
    return True

def process_vertical(grid: List[List[int]], min_r: int, max_r: int, col: int, bg: int, h: int, height: int, width: int) -> bool:
    segs = get_nonbg_segments_col(grid, col, bg, height)
    best_target = None
    best_gap = float('inf')
    best_dir = None
    for start, end, leng in segs:
        if leng < 2:
            continue
        if end < min_r:
            gap = min_r - end - 1
            if gap <= 8 and gap < best_gap:
                best_gap = gap
                best_target = (start, end, leng)
                best_dir = 'down'
        elif start > max_r:
            gap = start - max_r - 1
            if gap <= 8 and gap < best_gap:
                best_gap = gap
                best_target = (start, end, leng)
                best_dir = 'up'
    if best_target is None:
        return False
    start_t, end_t, leng_t = best_target
    if best_dir == 'down':
        new_min_r = end_t + 1
        new_max_r = new_min_r + h - 1
        if new_max_r >= height:
            return False
        ok = True
        for r in range(new_min_r, new_max_r + 1):
            if grid[r][col] != bg:
                ok = False
                break
        if not ok:
            return False
        swept_min_r = min(min_r, new_min_r)
        swept_max_r = max(max_r, new_max_r)
        for r in range(swept_min_r, swept_max_r + 1):
            grid[r][col] = 0
        for r in range(new_min_r, new_max_r + 1):
            grid[r][col] = 2
    else:
        new_max_r = start_t - 1
        new_min_r = new_max_r - h + 1
        if new_min_r < 0:
            return False
        ok = True
        for r in range(new_min_r, new_max_r + 1):
            if grid[r][col] != bg:
                ok = False
                break
        if not ok:
            return False
        swept_min_r = min(min_r, new_min_r)
        swept_max_r = max(max_r, new_max_r)
        for r in range(swept_min_r, swept_max_r + 1):
            grid[r][col] = 0
        for r in range(new_min_r, new_max_r + 1):
            grid[r][col] = 2
    return True

def process_2d_vertical(grid: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, bg: int, h: int, w: int, height: int, width: int) -> bool:
    candidates_up = {}
    candidates_down = {}
    uniform_up = True
    uniform_down = True
    common_end_t = None
    common_start_t = None
    has_up = True
    has_down = True
    min_gap_up = float('inf')
    min_gap_down = float('inf')
    for c in range(min_c, max_c + 1):
        segs = get_nonbg_segments_col(grid, c, bg, height)
        best_end_above = None
        best_gap_above = float('inf')
        for s, e, l in segs:
            if l < h:
                continue
            if e < min_r:
                g = min_r - e - 1
                if g <= 8 and g < best_gap_above:
                    best_gap_above = g
                    best_end_above = e
        candidates_up[c] = (best_end_above, best_gap_above)
        if best_end_above is None:
            has_up = False
        else:
            min_gap_up = min(min_gap_up, best_gap_above)
            if common_end_t is None:
                common_end_t = best_end_above
            elif common_end_t != best_end_above:
                uniform_up = False
        best_start_below = None
        best_gap_below = float('inf')
        for s, e, l in segs:
            if l < h:
                continue
            if s > max_r:
                g = s - max_r - 1
                if g <= 8 and g < best_gap_below:
                    best_gap_below = g
                    best_start_below = s
        candidates_down[c] = (best_start_below, best_gap_below)
        if best_start_below is None:
            has_down = False
        else:
            min_gap_down = min(min_gap_down, best_gap_below)
            if common_start_t is None:
                common_start_t = best_start_below
            elif common_start_t != best_start_below:
                uniform_down = False
    best_dir = None
    best_attach = None
    best_gap = float('inf')
    if has_up and uniform_up:
        best_dir = 'down'
        best_attach = common_end_t
        best_gap = min_gap_up
    if has_down and uniform_down and min_gap_down < best_gap:
        best_dir = 'up'
        best_attach = common_start_t
        best_gap = min_gap_down
    if best_dir is None:
        return False
    if best_dir == 'down':
        new_min_r = best_attach + 1
        new_max_r = new_min_r + h - 1
        if new_max_r >= height:
            return False
    else:
        new_max_r = best_attach - 1
        new_min_r = new_max_r - h + 1
        if new_min_r < 0:
            return False
    ok = True
    for c in range(min_c, max_c + 1):
        for r in range(new_min_r, new_max_r + 1):
            if grid[r][c] != bg:
                ok = False
                break
        if not ok:
            break
    if not ok:
        return False
    swept_min_r = min(min_r, new_min_r)
    swept_max_r = max(max_r, new_max_r)
    for r in range(swept_min_r, swept_max_r + 1):
        for c in range(min_c, max_c + 1):
            grid[r][c] = 0
    for r in range(new_min_r, new_max_r + 1):
        for c in range(min_c, max_c + 1):
            grid[r][c] = 2
    return True

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    grid = [row[:] for row in g]
    height = len(grid)
    width = len(grid[0])
    bg = get_background(grid)
    components = find_components(grid, bg)
    for comp in components:
        cells, min_r, max_r, min_c, max_c, sz = comp
        hh = max_r - min_r + 1
        ww = max_c - min_c + 1
        if hh * ww != sz:
            for r, c in cells:
                grid[r][c] = bg
            continue
        moved = False
        if ww == 1:
            moved = process_vertical(grid, min_r, max_r, min_c, bg, hh, height, width)
        elif hh == 1:
            moved = process_horizontal(grid, min_r, min_c, max_c, bg, ww, width, height)
        else:
            moved = process_2d_vertical(grid, min_r, max_r, min_c, max_c, bg, hh, ww, height, width)
        if not moved:
            for r in range(min_r, max_r + 1):
                for c in range(min_c, max_c + 1):
                    grid[r][c] = bg
    return grid
```