```python
from typing import List, Tuple
from collections import Counter

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    flat = [g[i][j] for i in range(rows) for j in range(cols)]
    background = Counter(flat).most_common(1)[0][0]
    fill = 3
    special = 2
    grid = [row[:] for row in g]
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == special and not visited[i][j]:
                positions = []
                stack = [(i, j)]
                visited[i][j] = True
                min_r = max_r = i
                min_c = max_c = j
                while stack:
                    x, y = stack.pop()
                    positions.append((x, y))
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == special:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                h = max_r - min_r + 1
                w = max_c - min_c + 1
                if len(positions) == h * w:
                    components.append({
                        'min_r': min_r, 'max_r': max_r, 'min_c': min_c, 'max_c': max_c, 'h': h, 'w': w, 'positions': positions
                    })
    for comp in components:
        min_r = comp['min_r']
        max_r = comp['max_r']
        min_c = comp['min_c']
        max_c = comp['max_c']
        h = comp['h']
        w = comp['w']
        valid_moves = []
        # up
        wall_r = -1
        for rr in range(min_r - 1, -1, -1):
            all_wall = all(g[rr][cc] != background and g[rr][cc] != special for cc in range(min_c, max_c + 1))
            if all_wall:
                clear = all(g[rrr][cc] == background for rrr in range(rr + 1, min_r) for cc in range(min_c, max_c + 1))
                if clear:
                    wall_r = rr
                    break
        if wall_r != -1:
            m = min_r - wall_r - 1
            if m <= 8:
                seg_ok = True
                for cc in range(min_c, max_c + 1):
                    l = cc
                    while l > 0 and g[wall_r][l - 1] != background and g[wall_r][l - 1] != special:
                        l -= 1
                    r = cc
                    while r < cols - 1 and g[wall_r][r + 1] != background and g[wall_r][r + 1] != special:
                        r += 1
                    if r - l + 1 > 4:
                        seg_ok = False
                        break
                if seg_ok and m >= h:
                    valid_moves.append((m, 0, wall_r, 'up'))
        # down
        wall_r = rows
        for rr in range(max_r + 1, rows):
            all_wall = all(g[rr][cc] != background and g[rr][cc] != special for cc in range(min_c, max_c + 1))
            if all_wall:
                clear = all(g[rrr][cc] == background for rrr in range(max_r + 1, rr) for cc in range(min_c, max_c + 1))
                if clear:
                    wall_r = rr
                    break
        if wall_r < rows:
            m = wall_r - max_r - 1
            if m <= 8:
                seg_ok = True
                for cc in range(min_c, max_c + 1):
                    l = cc
                    while l > 0 and g[wall_r][l - 1] != background and g[wall_r][l - 1] != special:
                        l -= 1
                    r = cc
                    while r < cols - 1 and g[wall_r][r + 1] != background and g[wall_r][r + 1] != special:
                        r += 1
                    if r - l + 1 > 4:
                        seg_ok = False
                        break
                if seg_ok and m >= h:
                    valid_moves.append((m, 2, wall_r, 'down'))
        # left
        wall_c = -1
        for cc in range(min_c - 1, -1, -1):
            all_wall = all(g[rr][cc] != background and g[rr][cc] != special for rr in range(min_r, max_r + 1))
            if all_wall:
                clear = all(g[rr][ccc] == background for ccc in range(cc + 1, min_c) for rr in range(min_r, max_r + 1))
                if clear:
                    wall_c = cc
                    break
        if wall_c != -1:
            m = min_c - wall_c - 1
            if m <= 8:
                seg_ok = True
                for rr in range(min_r, max_r + 1):
                    u = rr
                    while u > 0 and g[u - 1][wall_c] != background and g[u - 1][wall_c] != special:
                        u -= 1
                    d = rr
                    while d < rows - 1 and g[d + 1][wall_c] != background and g[d + 1][wall_c] != special:
                        d += 1
                    if d - u + 1 > 4:
                        seg_ok = False
                        break
                if seg_ok and m >= w:
                    valid_moves.append((m, 1, wall_c, 'left'))
        # right
        wall_c = cols
        for cc in range(max_c + 1, cols):
            all_wall = all(g[rr][cc] != background and g[rr][cc] != special for rr in range(min_r, max_r + 1))
            if all_wall:
                clear = all(g[rr][ccc] == background for ccc in range(max_c + 1, cc) for rr in range(min_r, max_r + 1))
                if clear:
                    wall_c = cc
                    break
        if wall_c < cols:
            m = wall_c - max_c - 1
            if m <= 8:
                seg_ok = True
                for rr in range(min_r, max_r + 1):
                    u = rr
                    while u > 0 and g[u - 1][wall_c] != background and g[u - 1][wall_c] != special:
                        u -= 1
                    d = rr
                    while d < rows - 1 and g[d + 1][wall_c] != background and g[d + 1][wall_c] != special:
                        d += 1
                    if d - u + 1 > 4:
                        seg_ok = False
                        break
                if seg_ok and m >= w:
                    valid_moves.append((m, 3, wall_c, 'right'))
        if valid_moves:
            valid_moves.sort()
            _, _, wall_pos, dir_name = valid_moves[0]
            # perform move
            if dir_name == 'up':
                place_r = wall_pos + 1
                # placement
                for ii in range(h):
                    pr = place_r + ii
                    for jj in range(w):
                        grid[pr][min_c + jj] = special
                # fill original
                for r in range(min_r, max_r + 1):
                    for c in range(min_c, max_c + 1):
                        grid[r][c] = fill
                # fill remaining between
                rem_start = place_r + h
                rem_end = min_r - 1
                for r in range(rem_start, rem_end + 1):
                    for c in range(min_c, max_c + 1):
                        grid[r][c] = fill
            elif dir_name == 'down':
                place_r_end = wall_pos - 1
                place_r_start = place_r_end - h + 1
                # placement
                for ii in range(h):
                    pr = place_r_start + ii
                    for jj in range(w):
                        grid[pr][min_c + jj] = special
                # fill original
                for r in range(min_r, max_r + 1):
                    for c in range(min_c, max_c + 1):
                        grid[r][c] = fill
                # fill remaining between
                rem_start = max_r + 1
                rem_end = place_r_start - 1
                for r in range(rem_start, rem_end + 1):
                    for c in range(min_c, max_c + 1):
                        grid[r][c] = fill
            elif dir_name == 'left':
                place_c = wall_pos + 1
                # placement
                for ii in range(h):
                    pr = min_r + ii
                    for jj in range(w):
                        pc = place_c + jj
                        grid[pr][pc] = special
                # fill original
                for r in range(min_r, max_r + 1):
                    for c in range(min_c, max_c + 1):
                        grid[r][c] = fill
                # fill remaining between
                rem_start = place_c + w
                rem_end = min_c - 1
                for c in range(rem_start, rem_end + 1):
                    for r in range(min_r, max_r + 1):
                        grid[r][c] = fill
            else:  # right
                place_c_end = wall_pos - 1
                place_c_start = place_c_end - w + 1
                # placement
                for ii in range(h):
                    pr = min_r + ii
                    for jj in range(w):
                        pc = place_c_start + jj
                        grid[pr][pc] = special
                # fill original
                for r in range(min_r, max_r + 1):
                    for c in range(min_c, max_c + 1):
                        grid[r][c] = fill
                # fill remaining between
                rem_start = max_c + 1
                rem_end = place_c_start - 1
                for c in range(rem_start, rem_end + 1):
                    for r in range(min_r, max_r + 1):
                        grid[r][c] = fill
        else:
            set_color = background
            if background == 0 and len(comp['positions']) > 1:
                set_color = fill
            for pos in comp['positions']:
                grid[pos[0]][pos[1]] = set_color
    return grid
```