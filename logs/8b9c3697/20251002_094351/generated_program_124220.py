```python
from typing import List, Tuple
from collections import defaultdict

def find_components(grid: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    height = len(grid)
    if height == 0:
        return []
    width = len(grid[0])
    visited = [[False] * width for _ in range(height)]
    comps = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(height):
        for j in range(width):
            if grid[i][j] == 2 and not visited[i][j]:
                minr = maxr = i
                minc = maxc = j
                size = 0
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    size += 1
                    minr = min(minr, x)
                    maxr = max(maxr, x)
                    minc = min(minc, y)
                    maxc = max(maxc, y)
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < height and 0 <= ny < width and grid[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                bb_h = maxr - minr + 1
                bb_w = maxc - minc + 1
                if size == bb_h * bb_w:
                    comps.append((minr, maxr, minc, maxc))
    return comps

def get_nonbg_segments_row(grid_row: List[int], bg: int) -> List[Tuple[int, int, int]]:
    segments = []
    n = len(grid_row)
    i = 0
    while i < n:
        if grid_row[i] != bg and grid_row[i] != 2:
            start = i
            while i < n and grid_row[i] != bg and grid_row[i] != 2:
                i += 1
            end = i - 1
            l = end - start + 1
            segments.append((start, end, l))
        else:
            i += 1
    return segments

def get_nonbg_segments_col(grid: List[List[int]], col: int, bg: int) -> List[Tuple[int, int, int]]:
    segments = []
    m = len(grid)
    i = 0
    while i < m:
        if grid[i][col] != bg and grid[i][col] != 2:
            start = i
            while i < m and grid[i][col] != bg and grid[i][col] != 2:
                i += 1
            end = i - 1
            l = end - start + 1
            segments.append((start, end, l))
        else:
            i += 1
    return segments

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    grid = [row[:] for row in g]
    bg = grid[0][0]
    height = len(grid)
    width = len(grid[0])
    components = find_components(grid, bg)
    components.sort(key=lambda x: (x[0], x[2]))
    for min_r, max_r, min_c, max_c in components:
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        possible = []
        # Vertical moves
        # Down
        col_start_to_l = {j: {} for j in range(min_c, max_c + 1)}
        for j in range(min_c, max_c + 1):
            segs = get_nonbg_segments_col(grid, j, bg)
            for start, end, l in segs:
                if start > max_r:
                    dist = start - max_r - 1
                    if dist <= 8:
                        col_start_to_l[j][start] = l
        possible_starts = set()
        for j in col_start_to_l:
            for s in col_start_to_l[j]:
                possible_starts.add(s)
        for t in sorted(possible_starts):
            ls = []
            all_have = True
            for j in range(min_c, max_c + 1):
                if t in col_start_to_l[j]:
                    ls.append(col_start_to_l[j][t])
                else:
                    all_have = False
                    break
            if all_have and len(ls) == w:
                min_l = min(ls)
                new_start = t - h
                if new_start > max_r:
                    new_end = new_start + h - 1
                    if new_end < height:
                        place_ok = all(grid[r][c] == bg for r in range(new_start, new_end + 1) for c in range(min_c, max_c + 1))
                        if place_ok:
                            gap_size = new_start - max_r - 1
                            if gap_size > 0 and gap_size <= 8:
                                gap_ok = all(grid[r][c] == bg for r in range(max_r + 1, new_start) for c in range(min_c, max_c + 1))
                                if gap_ok:
                                    possible.append((min_l, gap_size, 'down', new_start))
        # Up
        col_end_to_l = {j: {} for j in range(min_c, max_c + 1)}
        for j in range(min_c, max_c + 1):
            segs = get_nonbg_segments_col(grid, j, bg)
            for start, end, l in segs:
                if end < min_r:
                    dist = min_r - end - 1
                    if dist <= 8:
                        col_end_to_l[j][end] = l
        possible_ends = set()
        for j in col_end_to_l:
            for e in col_end_to_l[j]:
                possible_ends.add(e)
        for t in sorted(possible_ends, reverse=True):
            ls = []
            all_have = True
            for j in range(min_c, max_c + 1):
                if t in col_end_to_l[j]:
                    ls.append(col_end_to_l[j][t])
                else:
                    all_have = False
                    break
            if all_have and len(ls) == w:
                min_l = min(ls)
                new_start = t + 1
                new_end = new_start + h - 1
                if new_end < min_r:
                    if new_start >= 0:
                        place_ok = all(grid[r][c] == bg for r in range(new_start, new_end + 1) for c in range(min_c, max_c + 1))
                        if place_ok:
                            gap_size = min_r - new_end - 1
                            if gap_size > 0 and gap_size <= 8:
                                gap_ok = all(grid[r][c] == bg for r in range(new_end + 1, min_r) for c in range(min_c, max_c + 1))
                                if gap_ok:
                                    possible.append((min_l, gap_size, 'up', new_start))
        # Horizontal if h == 1
        if h == 1:
            row = min_r
            segs = get_nonbg_segments_row(grid[row], bg)
            # Left
            for st, en, ll in segs:
                if en < min_c:
                    place_start = en + 1
                    place_end = place_start + w - 1
                    if place_end < min_c:
                        gap_size = min_c - place_end - 1
                        if gap_size > 0 and gap_size <= 8:
                            place_ok = all(grid[row][c] == bg for c in range(place_start, place_end + 1))
                            if place_ok:
                                gap_ok = all(grid[row][c] == bg for c in range(place_end + 1, min_c))
                                if gap_ok:
                                    possible.append((ll, gap_size, 'left', place_start))
            # Right
            for st, en, ll in segs:
                if st > max_c:
                    place_end = st - 1
                    place_start = place_end - w + 1
                    if place_start > max_c:
                        gap_size = place_start - max_c - 1
                        if gap_size > 0 and gap_size <= 8:
                            place_ok = all(grid[row][c] == bg for c in range(place_start, place_end + 1))
                            if place_ok:
                                gap_ok = all(grid[row][c] == bg for c in range(max_c + 1, place_start))
                                if gap_ok:
                                    possible.append((ll, gap_size, 'right', place_start))
        # Select best
        if possible:
            possible.sort(key=lambda x: (-x[0], x[1]))
            score, gap_size, ddir, param = possible[0]
            if ddir in ['up', 'down']:
                new_start = param
                new_end = new_start + h - 1
                for r in range(new_start, new_end + 1):
                    for c in range(min_c, max_c + 1):
                        grid[r][c] = 2
                clear_min = min(min_r, new_start)
                clear_max = max(max_r, new_end)
                for r in range(clear_min, clear_max + 1):
                    for c in range(min_c, max_c + 1):
                        if not (new_start <= r <= new_end):
                            grid[r][c] = 0
            else:
                row = min_r
                place_start = param
                place_end = place_start + w - 1
                for c in range(place_start, place_end + 1):
                    grid[row][c] = 2
                clear_min = min(min_c, place_start)
                clear_max = max(max_c, place_end)
                for c in range(clear_min, clear_max + 1):
                    if not (place_start <= c <= place_end):
                        grid[row][c] = 0
        else:
            for r in range(min_r, max_r + 1):
                for c in range(min_c, max_c + 1):
                    grid[r][c] = bg
    return grid
```