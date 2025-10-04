```python
from typing import List, Tuple
import copy

def is_structure(val: int, bg: int) -> bool:
    return val != bg and val != 0 and val != 2

def is_empty(val: int, bg: int) -> bool:
    return val == bg or val == 0

def vertical_seg_len(grid: List[List[int]], col: int, row: int, bg: int) -> int:
    height = len(grid)
    # Find start
    start = row
    while start > 0 and is_structure(grid[start - 1][col], bg):
        start -= 1
    # Find end
    end = row
    while end < height - 1 and is_structure(grid[end + 1][col], bg):
        end += 1
    return end - start + 1

def get_nonbg_segments_row(grid_row: List[int], bg: int) -> List[Tuple[int, int, int]]:
    segments = []
    n = len(grid_row)
    i = 0
    while i < n:
        if is_structure(grid_row[i], bg):
            start = i
            while i < n and is_structure(grid_row[i], bg):
                i += 1
            end = i - 1
            length = end - start + 1
            segments.append((start, end, length))
        else:
            i += 1
    return segments

def find_components(grid: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    height = len(grid)
    if height == 0:
        return []
    width = len(grid[0])
    visited = [[False] * width for _ in range(height)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(height):
        for c in range(width):
            if grid[r][c] == 2 and not visited[r][c]:
                min_r, max_r, min_c, max_c = r, r, c, c
                stack = [(r, c)]
                visited[r][c] = True
                size = 1
                while stack:
                    x, y = stack.pop()
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width and grid[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            size += 1
                bb_h = max_r - min_r + 1
                bb_w = max_c - min_c + 1
                if size == bb_h * bb_w:
                    components.append((min_r, max_r, min_c, max_c))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(g)
    if not grid:
        return grid
    bg = grid[0][0]
    height = len(grid)
    width = len(grid[0])
    components = find_components(grid, bg)
    components.sort(key=lambda b: (b[0], b[2]))
    for min_r, max_r, min_c, max_c in components:
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        # Check if still 2's
        still_present = False
        for i in range(min_r, max_r + 1):
            for j in range(min_c, max_c + 1):
                if grid[i][j] == 2:
                    still_present = True
                    break
            if still_present:
                break
        if not still_present:
            continue
        possible_moves = []
        # Vertical moves
        for s in range(height):
            if all(is_structure(grid[s][j], bg) for j in range(min_c, max_c + 1)):
                # Down attach (above s)
                if s > max_r:
                    new_max_r = s - 1
                    new_min_r = new_max_r - h + 1
                    if new_min_r >= 0:
                        gap_size = s - max_r - 1
                        if 0 <= gap_size <= 8:
                            gap_ok = all(
                                all(is_empty(grid[rr][j], bg) for j in range(min_c, max_c + 1))
                                for rr in range(max_r + 1, s)
                            )
                            if gap_ok:
                                place_ok = all(
                                    all(is_empty(grid[rr][j], bg) for j in range(min_c, max_c + 1))
                                    for rr in range(new_min_r, new_max_r + 1)
                                )
                                if place_ok:
                                    score = min(vertical_seg_len(grid, j, s, bg) for j in range(min_c, max_c + 1))
                                    possible_moves.append(('vertical_down', new_min_r, new_max_r, min_c, max_c, gap_size, score))
                # Up attach (below s)
                if s < min_r:
                    new_min_r = s + 1
                    new_max_r = new_min_r + h - 1
                    if new_max_r < height:
                        gap_size = min_r - s - 1
                        if 0 <= gap_size <= 8:
                            gap_ok = all(
                                all(is_empty(grid[rr][j], bg) for j in range(min_c, max_c + 1))
                                for rr in range(s + 1, min_r)
                            )
                            if gap_ok:
                                place_ok = all(
                                    all(is_empty(grid[rr][j], bg) for j in range(min_c, max_c + 1))
                                    for rr in range(new_min_r, new_max_r + 1)
                                )
                                if place_ok:
                                    score = min(vertical_seg_len(grid, j, s, bg) for j in range(min_c, max_c + 1))
                                    possible_moves.append(('vertical_up', new_min_r, new_max_r, min_c, max_c, gap_size, score))
        # Horizontal moves if h == 1
        if h == 1:
            r = min_r
            segments = get_nonbg_segments_row(grid[r], bg)
            # Left attaches
            for start, end, seg_len in segments:
                if end >= min_c:
                    continue
                s = end
                new_min_c = s + 1
                new_max_c = s + w
                if new_max_c >= min_c:
                    continue
                gap_size = min_c - new_max_c - 1
                if gap_size < 0 or gap_size > 8:
                    continue
                gap_ok = all(is_empty(grid[r][cc], bg) for cc in range(new_max_c + 1, min_c))
                if not gap_ok:
                    continue
                place_ok = all(is_empty(grid[r][cc], bg) for cc in range(new_min_c, new_max_c + 1))
                if place_ok:
                    score = seg_len
                    possible_moves.append(('horizontal_left', min_r, max_r, new_min_c, new_max_c, gap_size, score))
            # Right attaches
            for start, end, seg_len in segments:
                if start <= max_c:
                    continue
                s = start
                new_max_c = s - 1
                new_min_c = s - w
                if new_min_c <= max_c:
                    continue
                gap_size = new_min_c - max_c - 1
                if gap_size < 0 or gap_size > 8:
                    continue
                gap_ok = all(is_empty(grid[r][cc], bg) for cc in range(max_c + 1, new_min_c))
                if not gap_ok:
                    continue
                place_ok = all(is_empty(grid[r][cc], bg) for cc in range(new_min_c, new_max_c + 1))
                if place_ok:
                    score = seg_len
                    possible_moves.append(('horizontal_right', min_r, max_r, new_min_c, new_max_c, gap_size, score))
        if not possible_moves:
            # Erase to bg
            for i in range(min_r, max_r + 1):
                for j in range(min_c, max_c + 1):
                    grid[i][j] = bg
            continue
        # Choose best
        def move_key(move):
            typ, _, _, _, _, gap, score = move
            is_horiz = 'horizontal' in typ
            pri = -score
            sec = gap
            tert = -1 if is_horiz and h == 1 else 0  # prefer horizontal for h=1 with higher tert (smaller number)
            return (pri, sec, tert)
        possible_moves.sort(key=move_key)
        best = possible_moves[0]
        typ, nr_min, nr_max, nc_min, nc_max, _, _ = best
        # Perform move
        # Place 2's
        for i in range(nr_min, nr_max + 1):
            for j in range(nc_min, nc_max + 1):
                grid[i][j] = 2
        # Clear original to 0
        for i in range(min_r, max_r + 1):
            for j in range(min_c, max_c + 1):
                grid[i][j] = 0
        # Clear gap to 0
        if typ == 'vertical_down':
            for i in range(max_r + 1, nr_min):
                for j in range(min_c, max_c + 1):
                    grid[i][j] = 0
        elif typ == 'vertical_up':
            for i in range(nr_max + 1, min_r):
                for j in range(min_c, max_c + 1):
                    grid[i][j] = 0
        elif typ == 'horizontal_left':
            for j in range(nc_max + 1, min_c):
                for i in range(min_r, max_r + 1):
                    grid[i][j] = 0
        elif typ == 'horizontal_right':
            for j in range(max_c + 1, nc_min):
                for i in range(min_r, max_r + 1):
                    grid[i][j] = 0
    return grid
```