```python
from typing import List
from collections import Counter, deque

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int) -> List[tuple]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != bg and not visited[i][j]:
                component_pos = []
                color_set = set()
                q = deque([(i, j)])
                visited[i][j] = True
                while q:
                    x, y = q.popleft()
                    component_pos.append((x, y))
                    color_set.add(g[x][y])
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] != bg and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                components.append((component_pos, color_set))
    return components

def select_main_component(components: List[tuple]) -> list:
    max_distinct = -1
    max_size = -1
    main_pos = []
    for pos, colset in components:
        dist = len(colset)
        size = len(pos)
        if dist > max_distinct or (dist == max_distinct and size > max_size):
            max_distinct = dist
            max_size = size
            main_pos = pos
    return main_pos

def get_bounding_box(pos_list: list) -> tuple:
    if not pos_list:
        return None, None, None, None
    min_r = min(p[0] for p in pos_list)
    max_r = max(p[0] for p in pos_list)
    min_c = min(p[1] for p in pos_list)
    max_c = max(p[1] for p in pos_list)
    return min_r, max_r, min_c, max_c

def extract_pattern(g: List[List[int]], bbox: tuple) -> tuple:
    min_r, max_r, min_c, max_c = bbox
    ph = max_r - min_r + 1
    pw = max_c - min_c + 1
    pattern = [[g[min_r + i][min_c + j] for j in range(pw)] for i in range(ph)]
    return pattern, ph, pw

def get_ignored_cells(g: List[List[int]], bg: int, main_pos_set: set) -> list:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    ignored = []
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != bg and (i, j) not in main_pos_set:
                ignored.append((i, j))
    return ignored

def build_mask(ignored: list, bbox: tuple) -> tuple:
    min_r, max_r, min_c, max_c = bbox
    mh = max_r - min_r + 1
    mw = max_c - min_c + 1
    mask = [[False] * mw for _ in range(mh)]
    for r, c in ignored:
        mr = r - min_r
        mc = c - min_c
        mask[mr][mc] = True
    return mask, mh, mw

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    components = find_components(g, bg)
    main_pos = select_main_component(components)
    main_set = set(main_pos)
    main_bbox = get_bounding_box(main_pos)
    pattern, ph, pw = extract_pattern(g, main_bbox)
    ignored = get_ignored_cells(g, bg, main_set)
    rows_i = len(g)
    cols_i = len(g[0]) if rows_i > 0 else 0
    if ignored:
        ignored_bbox = get_bounding_box(ignored)
        mask, mh, mw = build_mask(ignored, ignored_bbox)
    else:
        mh = rows_i // ph if ph > 0 else 0
        mw = cols_i // pw if pw > 0 else 0
        mask = [[True] * mw for _ in range(mh)]
    out_h = mh * ph
    out_w = mw * pw
    output = [[] for _ in range(out_h)]
    for mr in range(mh):
        for lr in range(ph):
            rid = mr * ph + lr
            crow = []
            for mc in range(mw):
                if mask[mr][mc]:
                    crow.extend(pattern[lr])
                else:
                    crow.extend([bg] * pw)
            output[rid] = crow
    return output
```