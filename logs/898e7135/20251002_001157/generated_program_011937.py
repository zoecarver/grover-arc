```python
from typing import List, Tuple
from collections import deque

def find_components(grid: List[List[int]]) -> List[dict]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 0 and not visited[i][j]:
                color = grid[i][j]
                pixels: List[Tuple[int, int]] = []
                stack = [(i, j)]
                visited[i][j] = True
                min_r, min_c = i, j
                max_r, max_c = i, j
                while stack:
                    x, y = stack.pop()
                    pixels.append((x, y))
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append({
                    'color': color,
                    'pixels': pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return components

def find_frame(grid: List[List[int]], components: List[dict]) -> dict:
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque()
    for i in range(rows):
        if grid[i][0] == 0 and not visited[i][0]:
            queue.append((i, 0))
            visited[i][0] = True
        if grid[i][cols - 1] == 0 and not visited[i][cols - 1]:
            queue.append((i, cols - 1))
            visited[i][cols - 1] = True
    for j in range(cols):
        if grid[0][j] == 0 and not visited[0][j]:
            queue.append((0, j))
            visited[0][j] = True
        if grid[rows - 1][j] == 0 and not visited[rows - 1][j]:
            queue.append((rows - 1, j))
            visited[rows - 1][j] = True
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append((nx, ny))
    enclosed = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == 0 and not visited[i][j]]
    bordering = set()
    for i, j in enclosed:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + dx, j + dy
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] != 0:
                bordering.add(grid[ni][nj])
    if len(bordering) == 1:
        frame_color = list(bordering)[0]
        for comp in components:
            if comp['color'] == frame_color:
                return comp
    return None

def get_transform(comp: dict, frame: dict) -> str:
    fr1, fc1, fr2, fc2 = frame['bbox']
    f_center_r = (fr1 + fr2) / 2.0
    f_center_c = (fc1 + fc2) / 2.0
    cr1, cc1, cr2, cc2 = comp['bbox']
    c_center_r = (cr1 + cr2) / 2.0
    c_center_c = (cc1 + cc2) / 2.0
    if cc1 > fc2:
        return '180'
    if cc2 < fc1:
        if c_center_r < f_center_r:
            return '90cw'
        else:
            return 'hflip'
    if cr1 > fr2:
        return '90cw_hflip'
    return 'none'

def apply_transform(pixels: List[Tuple[int, int]], transform: str, bbox: Tuple[int, int, int, int]) -> Tuple[List[Tuple[int, int]], Tuple[int, int]]:
    r1, c1, r2, c2 = bbox
    h = r2 - r1 + 1
    w = c2 - c1 + 1
    local_pixels = [(r - r1, c - c1) for r, c in pixels]
    if transform == 'none':
        return local_pixels, (h, w)
    elif transform == 'hflip':
        new_local = [(lr, w - 1 - lc) for lr, lc in local_pixels]
        return new_local, (h, w)
    elif transform == '180':
        new_local = [(h - 1 - lr, w - 1 - lc) for lr, lc in local_pixels]
        return new_local, (h, w)
    elif transform == '90cw':
        new_local = [(lc, h - 1 - lr) for lr, lc in local_pixels]
        return new_local, (w, h)
    elif transform == '90cw_hflip':
        temp_local = [(lc, h - 1 - lr) for lr, lc in local_pixels]
        temp_h, temp_w = w, h
        new_local = [(tr, temp_w - 1 - tc) for tr, tc in temp_local]
        return new_local, (temp_h, temp_w)
    return local_pixels, (h, w)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    components = find_components(g)
    frame = find_frame(g, components)
    if not frame:
        return g  # fallback
    fr1, fc1, fr2, fc2 = frame['bbox']
    orig_h = fr2 - fr1 + 1
    orig_w = fc2 - fc1 + 1
    new_h = 2 * orig_h
    new_w = 2 * orig_w
    output = [[frame['color']] * new_w for _ in range(new_h)]
    non_singles = [comp for comp in components if len(comp['pixels']) > 1 and comp is not frame]
    non_singles.sort(key=lambda comp: comp['bbox'][0])
    current_row_start = 2
    current_col = 2
    current_row_height = 0
    for comp in non_singles:
        transform = get_transform(comp, frame)
        relative_pixels, (comp_h, comp_w) = apply_transform(comp['pixels'], transform, comp['bbox'])
        cr1, cc1, cr2, cc2 = comp['bbox']
        c_center_c = (cc1 + cc2) / 2.0
        f_center_c = (fc1 + fc2) / 2.0
        if current_col + comp_w > new_w - 2:
            current_row_start += current_row_height
            current_col = 2 if c_center_c <= f_center_c else 4
            current_row_height = comp_h
        # place
        for lr, lc in relative_pixels:
            nr = current_row_start + lr
            nc = current_col + lc
            if 0 <= nr < new_h and 0 <= nc < new_w:
                output[nr][nc] = comp['color']
        current_row_height = max(current_row_height, comp_h)
        current_col += comp_w + 2
    return output
```