```python
from typing import List, Dict, Tuple
from collections import deque

def find_background(g: List[List[int]]) -> int:
    count = [0] * 10
    for row in g:
        for v in row:
            if 0 <= v < 10:
                count[v] += 1
    return count.index(max(count))

def find_shapes(g: List[List[int]], frame_color: int, background: int, opposite_frame: int, eight_cells: set = None) -> List[Dict[str, int]]:
    shapes = []
    visited = [[False] * 22 for _ in range(22)]
    for i in range(22):
        for j in range(22):
            if g[i][j] == frame_color and not visited[i][j] and (eight_cells is None or (i, j) not in eight_cells):
                frame_cells = []
                q = deque([(i, j)])
                visited[i][j] = True
                frame_cells.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < 22 and 0 <= ny < 22 and not visited[nx][ny] and g[nx][ny] == frame_color:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            frame_cells.append((nx, ny))
                inner_cells = set()
                for x, y in frame_cells:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx = x + dx
                            ny = y + dy
                            if 0 <= nx < 22 and 0 <= ny < 22 and (nx, ny) not in inner_cells and g[nx][ny] != background and g[nx][ny] != opposite_frame and g[nx][ny] != frame_color:
                                inner_cells.add((nx, ny))
                all_cells = frame_cells + list(inner_cells)
                if all_cells:
                    minr = min(x for x, _ in all_cells)
                    maxr = max(x for x, _ in all_cells)
                    minc = min(y for _, y in all_cells)
                    maxc = max(y for _, y in all_cells)
                    shapes.append({'minr': minr, 'maxr': maxr, 'minc': minc, 'maxc': maxc})
    return shapes

def place_left_shapes(out: List[List[int]], g: List[List[int]], background: int, shapes: List[Dict[str, int]]):
    current_left_width = 0
    last_maxr_left = -1
    for sh in shapes:
        minr = sh['minr']
        maxr = sh['maxr']
        minc = sh['minc']
        maxc = sh['maxc']
        w = maxc - minc + 1
        if minr > last_maxr_left + 1:
            proposed_left = 0
        else:
            proposed_left = current_left_width
        # place (assume no conflict)
        for rr in range(minr, maxr + 1):
            for kk in range(w):
                oc = proposed_left + kk
                if oc < 22:
                    nv = g[rr][minc + kk]
                    if nv != background:
                        out[rr][oc] = nv
        current_left_width = max(current_left_width, proposed_left + w)
        last_maxr_left = maxr

def place_right_shapes(out: List[List[int]], g: List[List[int]], background: int, shapes: List[Dict[str, int]]):
    current_start_col = 22
    current_right_width = 0
    last_maxr_right = -1
    block_min_row = 22
    block_max_row = -1
    for sh in shapes:
        minr = sh['minr']
        maxr = sh['maxr']
        minc = sh['minc']
        maxc = sh['maxc']
        w = maxc - minc + 1
        is_new = minr > last_maxr_right
        old_start_col = current_start_col
        if is_new:
            proposed_start_col = 22 - w
            place_start_col = proposed_start_col
            current_start_col = proposed_start_col
            current_right_width = w
            block_min_row = minr
            block_max_row = maxr
        else:
            proposed_start_col = current_start_col
            conflict = False
            for rr in range(minr, maxr + 1):
                for kk in range(w):
                    oc = proposed_start_col + kk
                    if oc > 21:
                        conflict = True
                        break
                    nv = g[rr][minc + kk]
                    ov = out[rr][oc]
                    if ov != background and nv != background and ov != nv:
                        conflict = True
                        break
                if conflict:
                    break
            if conflict:
                delta = w
                old_start_col = proposed_start_col
                current_start_col -= delta
                current_right_width += delta
                # shift existing left by delta
                for rr in range(block_min_row, block_max_row + 1):
                    for cc in range(21, old_start_col - 1, -1):
                        new_cc = cc - delta
                        if new_cc >= 0:
                            out[rr][new_cc] = out[rr][cc]
                    for cc in range(old_start_col, 22):
                        out[rr][cc] = background
                place_start_col = old_start_col
                block_min_row = min(block_min_row, minr)
                block_max_row = max(block_max_row, maxr)
            else:
                place_start_col = proposed_start_col
                block_min_row = min(block_min_row, minr)
                block_max_row = max(block_max_row, maxr)
        # place
        for rr in range(minr, maxr + 1):
            for kk in range(w):
                oc = place_start_col + kk
                if 0 <= oc < 22:
                    nv = g[rr][minc + kk]
                    if nv != background:
                        out[rr][oc] = nv
        current_start_col = min(current_start_col, place_start_col)
        current_right_width = 22 - current_start_col
        last_maxr_right = max(last_maxr_right, maxr)
        if is_new:
            block_min_row = minr
            block_max_row = maxr

def program(g: List[List[int]]) -> List[List[int]]:
    background = find_background(g)
    out = [[background for _ in range(22)] for _ in range(22)]
    eight_cells = set()
    eight_shapes = find_shapes(g, 8, background, 2)
    for sh in eight_shapes:
        minr = sh['minr']
        maxr = sh['maxr']
        minc = sh['minc']
        maxc = sh['maxc']
        for rr in range(minr, maxr + 1):
            for cc in range(minc, maxc + 1):
                eight_cells.add((rr, cc))
    place_left_shapes(out, g, background, eight_shapes)
    two_shapes = find_shapes(g, 2, background, 8, eight_cells)
    place_right_shapes(out, g, background, two_shapes)
    return out
```