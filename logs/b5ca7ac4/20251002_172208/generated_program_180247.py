```python
from collections import Counter, deque
from typing import List, Tuple, Dict, Set

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_bounding(all_cells: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    rows = [r for r, c in all_cells]
    cols = [c for r, c in all_cells]
    return min(rows), max(rows), min(cols), max(cols)

def find_connected_frames(g: List[List[int]], frame_color: int, bg: int, excluded: Set[Tuple[int, int]] = None) -> Tuple[List[Dict[str, int]], Set[Tuple[int, int]]]:
    n = 22
    visited = [[False] * n for _ in range(n)]
    shapes: List[Dict[str, int]] = []
    all_used_cells: Set[Tuple[int, int]] = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == frame_color and not visited[i][j] and (excluded is None or (i, j) not in excluded):
                frame_cells: List[Tuple[int, int]] = []
                q = deque([(i, j)])
                visited[i][j] = True
                frame_cells.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == frame_color:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            frame_cells.append((nx, ny))
                inner_cells: Set[Tuple[int, int]] = set()
                for x, y in frame_cells:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in inner_cells and g[nx][ny] != bg and g[nx][ny] != frame_color:
                                inner_cells.add((nx, ny))
                all_cells_list = frame_cells + list(inner_cells)
                if all_cells_list:
                    min_r, max_r, min_c, max_c = get_bounding(all_cells_list)
                    shapes.append({'minr': min_r, 'maxr': max_r, 'minc': min_c, 'maxc': max_c})
                    for pos in all_cells_list:
                        all_used_cells.add(pos)
    return shapes, all_used_cells

def find_left_shapes(g: List[List[int]], bg: int) -> Tuple[List[Dict[str, int]], Set[Tuple[int, int]]]:
    return find_connected_frames(g, 8, bg)

def find_right_shapes(g: List[List[int]], bg: int, left_cells: Set[Tuple[int, int]]) -> List[Dict[str, int]]:
    _, right_cells = find_connected_frames(g, 2, bg, left_cells)
    return _

def sort_shapes(shapes: List[Dict[str, int]]) -> List[Dict[str, int]]:
    return sorted(shapes, key=lambda sh: sh['minr'])

def place_left(out: List[List[int]], g: List[List[int]], bg: int, shapes: List[Dict[str, int]]):
    current_left_width = 0
    last_max_r = -1
    n = 22
    for sh in shapes:
        min_r = sh['minr']
        max_r = sh['maxr']
        min_c = sh['minc']
        max_c = sh['maxc']
        w = max_c - min_c + 1
        if min_r > last_max_r + 1:
            proposed_left = 0
        else:
            proposed_left = current_left_width
        for r in range(min_r, max_r + 1):
            for k in range(w):
                o_c = proposed_left + k
                if o_c < n:
                    n_v = g[r][min_c + k]
                    if n_v != bg:
                        out[r][o_c] = n_v
        current_left_width = max(current_left_width, proposed_left + w)
        last_max_r = max(last_max_r, max_r)

def place_right(out: List[List[int]], g: List[List[int]], bg: int, shapes: List[Dict[str, int]]):
    n = 22
    current_start_col = n
    last_max_r = -1
    block_min_row = n
    block_max_row = -1
    current_right_width = 0
    for sh in shapes:
        min_r = sh['minr']
        max_r = sh['maxr']
        min_c = sh['minc']
        max_c = sh['maxc']
        w = max_c - min_c + 1
        is_new_block = min_r > last_max_r
        proposed_start_col = n - w if is_new_block else current_start_col
        conflict = False
        if not is_new_block:
            for r in range(min_r, max_r + 1):
                for k in range(w):
                    o_c = proposed_start_col + k
                    if o_c >= n:
                        conflict = True
                        break
                    n_v = g[r][min_c + k]
                    o_v = out[r][o_c]
                    if o_v != bg and n_v != bg:
                        conflict = True
                        break
                if conflict:
                    break
        place_start_col = proposed_start_col
        if not is_new_block and conflict:
            delta = w
            old_start_col = proposed_start_col
            current_start_col -= delta
            current_right_width += delta
            for r in range(block_min_row, block_max_row + 1):
                for c in range(n - 1, old_start_col - 1, -1):
                    new_c = c - delta
                    if new_c >= 0:
                        out[r][new_c] = out[r][c]
                for c in range(old_start_col, n):
                    out[r][c] = bg
            place_start_col = old_start_col
        for r in range(min_r, max_r + 1):
            for k in range(w):
                o_c = place_start_col + k
                if 0 <= o_c < n:
                    n_v = g[r][min_c + k]
                    if n_v != bg:
                        out[r][o_c] = n_v
        if is_new_block:
            current_start_col = proposed_start_col
            current_right_width = w
            block_min_row = min_r
            block_max_row = max_r
        else:
            block_min_row = min(block_min_row, min_r)
            block_max_row = max(block_max_row, max_r)
        current_start_col = min(current_start_col, place_start_col)
        current_right_width = n - current_start_col
        last_max_r = max(last_max_r, max_r)

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    out: List[List[int]] = [[bg] * 22 for _ in range(22)]
    left_shapes, left_cells = find_left_shapes(g, bg)
    left_shapes = sort_shapes(left_shapes)
    place_left(out, g, bg, left_shapes)
    right_shapes = find_right_shapes(g, bg, left_cells)
    right_shapes = sort_shapes(right_shapes)
    place_right(out, g, bg, right_shapes)
    return out
```