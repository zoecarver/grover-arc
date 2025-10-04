```python
from typing import List, Tuple
import copy

def find_components(grid: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    height = len(grid)
    if height == 0:
        return []
    width = len(grid[0])
    visited = [[False] * width for _ in range(height)]
    comps = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
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
                    for dx, dy in dirs:
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

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(g)
    if not grid or not grid[0]:
        return grid
    height = len(grid)
    width = len(grid[0])
    bg = grid[0][0]
    special = 8
    components = find_components(grid, bg)
    components.sort(key=lambda x: (x[0], x[2]))
    dir_priority = {'left': 0, 'up': 1, 'right': 2, 'down': 3}
    for comp in components:
        r1, r2, c1, c2 = comp
        h = r2 - r1 + 1
        w = c2 - c1 + 1
        still_two = all(grid[i][j] == 2 for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))
        if not still_two:
            continue
        valid_moves = []
        if h == 1 and w == 1:
            poss_dirs = ['left', 'up', 'right', 'down']
        elif h == 1:
            poss_dirs = ['left', 'right']
        elif w == 1:
            poss_dirs = ['up', 'down']
        else:
            poss_dirs = ['up', 'down']
        for dname in poss_dirs:
            is_vertical = dname in ['up', 'down']
            is_decreasing = dname in ['up', 'left']
            curr_r1 = r1
            curr_c1 = c1
            steps = 0
            while steps < 8:
                if is_vertical:
                    if is_decreasing:
                        entering_i = curr_r1 - 1
                        if entering_i < 0:
                            break
                        entering_slice = [grid[entering_i][j] for j in range(c1, c2 + 1)]
                        if all(v == bg for v in entering_slice):
                            steps += 1
                            curr_r1 -= 1
                        else:
                            break
                    else:
                        entering_i = curr_r1 + h - 1 + 1
                        if entering_i >= height:
                            break
                        entering_slice = [grid[entering_i][j] for j in range(c1, c2 + 1)]
                        if all(v == bg for v in entering_slice):
                            steps += 1
                            curr_r1 += 1
                        else:
                            break
                else:
                    if is_decreasing:
                        entering_j = curr_c1 - 1
                        if entering_j < 0:
                            break
                        entering_slice = [grid[r1][entering_j] for _ in range(h)]
                        if all(v == bg for v in entering_slice):
                            steps += 1
                            curr_c1 -= 1
                        else:
                            break
                    else:
                        entering_j = curr_c1 + w - 1 + 1
                        if entering_j >= width:
                            break
                        entering_slice = [grid[r1][entering_j] for _ in range(h)]
                        if all(v == bg for v in entering_slice):
                            steps += 1
                            curr_c1 += 1
                        else:
                            break
            can_extra = steps < 8
            entering_slice = []
            if is_vertical:
                if is_decreasing:
                    entering_i = curr_r1 - 1
                    can_extra = can_extra and entering_i >= 0
                    if can_extra:
                        entering_slice = [grid[entering_i][j] for j in range(c1, c2 + 1)]
                else:
                    entering_i = curr_r1 + h - 1 + 1
                    can_extra = can_extra and entering_i < height
                    if can_extra:
                        entering_slice = [grid[entering_i][j] for j in range(c1, c2 + 1)]
            else:
                if is_decreasing:
                    entering_j = curr_c1 - 1
                    can_extra = can_extra and entering_j >= 0
                    if can_extra:
                        entering_slice = [grid[r1][entering_j] for _ in range(h)]
                else:
                    entering_j = curr_c1 + w - 1 + 1
                    can_extra = can_extra and entering_j < width
                    if can_extra:
                        entering_slice = [grid[r1][entering_j] for _ in range(h)]
            if can_extra and len(set(entering_slice)) == 1 and entering_slice and entering_slice[0] != bg and entering_slice[0] != 2 and entering_slice[0] == special:
                steps += 1
                if is_vertical:
                    if is_decreasing:
                        curr_r1 -= 1
                    else:
                        curr_r1 += 1
                else:
                    if is_decreasing:
                        curr_c1 -= 1
                    else:
                        curr_c1 += 1
            if is_vertical:
                new_r1 = curr_r1
                new_r2 = new_r1 + h - 1
                new_c1 = c1
                new_c2 = c2
                if new_r2 >= height:
                    continue
            else:
                new_c1 = curr_c1
                new_c2 = new_c1 + w - 1
                new_r1 = r1
                new_r2 = r2
                if new_c2 >= width:
                    continue
            touches = True
            if is_vertical:
                for jj in range(c1, c2 + 1):
                    strip_touches = False
                    for ii in range(new_r1, new_r2 + 1):
                        if grid[ii][jj] != bg and grid[ii][jj] != 2:
                            strip_touches = True
                            break
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            ni = ii + dx
                            nj = jj + dy
                            if 0 <= ni < height and 0 <= nj < width and grid[ni][nj] != bg and grid[ni][nj] != 2:
                                strip_touches = True
                                break
                        if strip_touches:
                            break
                    if not strip_touches:
                        touches = False
                        break
            else:
                strip_touches = False
                for jj in range(new_c1, new_c2 + 1):
                    ii = r1
                    if grid[ii][jj] != bg and grid[ii][jj] != 2:
                        strip_touches = True
                        break
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni = ii + dx
                        nj = jj + dy
                        if 0 <= ni < height and 0 <= nj < width and grid[ni][nj] != bg and grid[ni][nj] != 2:
                            strip_touches = True
                            break
                    if strip_touches:
                        break
                if not strip_touches:
                    touches = False
            if touches:
                prio = dir_priority[dname]
                valid_moves.append((steps, prio, new_r1, new_r2, new_c1, new_c2, dname))
        if valid_moves:
            valid_moves.sort(key=lambda x: (x[0], x[1]))
            _, _, new_r1, new_r2, new_c1, new_c2, dname = valid_moves[0]
            is_vertical = dname in ['up', 'down']
            is_decreasing = dname in ['up', 'left']
            for i in range(new_r1, new_r2 + 1):
                for j in range(new_c1, new_c2 + 1):
                    grid[i][j] = 2
            if is_vertical:
                if is_decreasing:
                    clear_start = new_r2 + 1
                    clear_end = r2
                    if clear_start <= clear_end:
                        for i in range(clear_start, clear_end + 1):
                            for j in range(c1, c2 + 1):
                                grid[i][j] = 0
                else:
                    for i in range(r1, r2 + 1):
                        for j in range(c1, c2 + 1):
                            grid[i][j] = 0
                    clear_start = r2 + 1
                    clear_end = new_r1 - 1
                    if clear_start <= clear_end:
                        for i in range(clear_start, clear_end + 1):
                            for j in range(c1, c2 + 1):
                                grid[i][j] = 0
            else:
                if is_decreasing:
                    clear_start = new_c2 + 1
                    clear_end = c2
                    if clear_start <= clear_end:
                        for j in range(clear_start, clear_end + 1):
                            for i in range(r1, r2 + 1):
                                grid[i][j] = 0
                else:
                    for j in range(c1, c2 + 1):
                        for i in range(r1, r2 + 1):
                            grid[i][j] = 0
                    clear_start = c2 + 1
                    clear_end = new_c1 - 1
                    if clear_start <= clear_end:
                        for j in range(clear_start, clear_end + 1):
                            for i in range(r1, r2 + 1):
                                grid[i][j] = 0
        else:
            for i in range(r1, r2 + 1):
                for j in range(c1, c2 + 1):
                    grid[i][j] = bg
    return grid
```