```python
from typing import List, Tuple

def find_bg(grid: List[List[int]]) -> int:
    return grid[0][0]

def find_components(grid: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    visited = [[False] * width for _ in range(height)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(height):
        for j in range(width):
            if grid[i][j] == 2 and not visited[i][j]:
                min_r, max_r = i, i
                min_c, max_c = j, j
                stack = [(i, j)]
                visited[i][j] = True
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
                components.append((min_r, max_r, min_c, max_c))
    return components

def process_horizontal(grid: List[List[int]], comp: Tuple[int, int, int, int], bg: int) -> bool:
    min_r, max_r, min_c, max_c = comp
    if min_r != max_r:
        return False
    row = min_r
    height = len(grid)
    width = len(grid[0])
    w = max_c - min_c + 1
    # Find rightmost structure segment to the left
    struct_end = -1
    struct_w = 0
    current_start = -1
    for j in range(width):
        cell = grid[row][j]
        if cell != bg and cell != 2:
            if current_start == -1:
                current_start = j
        else:
            if current_start != -1 and current_start <= j - 1 < min_c:
                s_start = current_start
                s_end = j - 1
                s_w = s_end - s_start + 1
                if s_end > struct_end:
                    struct_end = s_end
                    struct_w = s_w
            current_start = -1
    if current_start != -1 and current_start < min_c:
        s_end = width - 1
        s_w = s_end - current_start + 1
        if s_end > struct_end:
            struct_end = s_end
            struct_w = s_w
    if struct_end == -1:
        return False
    place_c = struct_end + 1
    place_w = min(w, struct_w)
    if place_w != w:
        return False
    k = min_c - place_c
    if k < 0 or k > 8:
        return False
    # Check place positions are bg
    for jj in range(place_c, place_c + w):
        if jj >= width or grid[row][jj] != bg:
            return False
    # Move
    for jj in range(place_c, place_c + w):
        grid[row][jj] = 2
    for jj in range(place_c + w, max_c + 1):
        grid[row][jj] = 0
    return True

def process_vertical(grid: List[List[int]], comp: Tuple[int, int, int, int], bg: int, height: int, width: int) -> bool:
    min_r, max_r, min_c, max_c = comp
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    targets = {}
    for j in range(min_c, max_c + 1):
        # Find structure segments in column j
        structs = []
        i = 0
        while i < height:
            if 0 <= i < height and grid[i][j] != bg and grid[i][j] != 2:
                s_start = i
                while i < height and grid[i][j] != bg and grid[i][j] != 2:
                    i += 1
                structs.append((s_start, i - 1))
            else:
                i += 1
        if not structs:
            targets[j] = None
            continue
        # Find closest structure
        min_dist = float('inf')
        chosen = None
        dir_str = None
        for s_start, s_end in structs:
            if s_end < min_r:
                dist = min_r - s_end - 1
                d = 'down'
            elif s_start > max_r:
                dist = s_start - max_r - 1
                d = 'up'
            else:
                dist = 0
                d = 'stay'
            if dist < min_dist:
                min_dist = dist
                chosen = (s_start, s_end)
                dir_str = d
        if chosen is None:
            targets[j] = None
            continue
        s_start, s_end = chosen
        h_s = s_end - s_start + 1
        place_h = min(h, h_s)
        valid = True
        if dir_str == 'down':
            place_end = s_start - 1
            place_start = place_end - place_h + 1
            clear_len = place_start - min_r
            if clear_len > 8 or place_start < 0:
                valid = False
            # Check bg
            for rr in range(place_start, place_end + 1):
                if grid[rr][j] != bg:
                    valid = False
                    break
        elif dir_str == 'up':
            place_start = s_end + 1
            place_end = place_start + place_h - 1
            clear_len = max_r - place_end
            if clear_len > 8 or place_end >= height:
                valid = False
            for rr in range(place_start, place_end + 1):
                if grid[rr][j] != bg:
                    valid = False
                    break
        else:
            targets[j] = ('stay', place_start, place_h)
            continue
        if valid:
            targets[j] = (dir_str, place_start, place_h)
        else:
            targets[j] = None
    # Check if all valid and same
    valid_targets = [t for t in targets.values() if t is not None]
    if len(valid_targets) != w:
        return False
    dir_set = set(t[0] for t in valid_targets)
    ps_set = set(t[1] for t in valid_targets)
    ph_set = set(t[2] for t in valid_targets)
    if len(dir_set) != 1 or len(ps_set) != 1 or len(ph_set) != 1:
        return False
    dir_str = list(dir_set)[0]
    place_start = list(ps_set)[0]
    place_h = list(ph_set)[0]
    place_end = place_start + place_h - 1
    # Do move
    for j in range(min_c, max_c + 1):
        for r in range(place_start, place_end + 1):
            grid[r][j] = 2
    if dir_str == 'up':
        clear_from = place_end + 1
        clear_to = max_r
        for r in range(clear_from, clear_to + 1):
            for j in range(min_c, max_c + 1):
                grid[r][j] = 0
    else:  # down
        clear_from = min_r
        clear_to = place_start - 1
        for r in range(clear_from, clear_to + 1):
            for j in range(min_c, max_c + 1):
                grid[r][j] = 0
    return True

def has_structure_in_columns(grid: List[List[int]], comp: Tuple[int, int, int, int], bg: int, height: int) -> bool:
    _, _, min_c, max_c = comp
    width = len(grid[0])
    for j in range(min_c, max_c + 1):
        for i in range(height):
            if grid[i][j] != bg and grid[i][j] != 2:
                return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    height = len(out)
    if height == 0:
        return out
    width = len(out[0])
    bg = find_bg(out)
    components = find_components(out, bg)
    for comp in components:
        min_r, max_r, min_c, max_c = comp
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        moved = False
        if h == 1:
            moved = process_horizontal(out, comp, bg)
        if not moved:
            moved = process_vertical(out, comp, bg, height, width)
        if not moved:
            if h == 1 and w == 1:
                out[min_r][min_c] = bg
            elif has_structure_in_columns(out, comp, bg, height):
                for r in range(min_r, max_r + 1):
                    for c in range(min_c, max_c + 1):
                        out[r][c] = bg
            else:
                # keep top row, clear rest
                for c in range(min_c, max_c + 1):
                    out[min_r][c] = 2
                for r in range(min_r + 1, max_r + 1):
                    for c in range(min_c, max_c + 1):
                        out[r][c] = bg
    return out
```