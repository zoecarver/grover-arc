```python
from typing import List, Tuple, Dict
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def find_components(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] == 1 and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 1 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(component)
    return components

def get_row_info(component: List[Tuple[int, int]]) -> Tuple[int, int, Dict[int, Tuple[int, int, int]], int]:
    if not component:
        return 0, 0, {}, 0
    min_r = min(p[0] for p in component)
    max_r = max(p[0] for p in component)
    rows_dict: Dict[int, Tuple[int, int, int]] = {}
    max_w = 0
    for r in range(min_r, max_r + 1):
        cols = [p[1] for p in component if p[0] == r]
        if cols:
            lmin = min(cols)
            lmax = max(cols)
            width = lmax - lmin + 1
            max_w = max(max_w, width)
            rows_dict[r] = (lmin, lmax, width)
    return min_r, max_r, rows_dict, max_w

def detect_holes(g: List[List[int]], component: List[Tuple[int, int]], h: int, w: int) -> Tuple[bool, set]:
    if len(component) <= 1:
        return False, set()
    temp = [row[:] for row in g]
    for i, j in component:
        temp[i][j] = 3
    visited_temp = [[False] * w for _ in range(h)]
    q = deque()
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in [0, w - 1]:
            if temp[i][j] == 4 and not visited_temp[i][j]:
                visited_temp[i][j] = True
                q.append((i, j))
    while q:
        i, j = q.popleft()
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < h and 0 <= nj < w and temp[ni][nj] == 4 and not visited_temp[ni][nj]:
                visited_temp[ni][nj] = True
                q.append((ni, nj))
    adj4 = set()
    for i, j in component:
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < h and 0 <= nj < w and temp[ni][nj] == 4:
                adj4.add((ni, nj))
    has_hole = False
    hole_pos = set()
    for ni, nj in adj4:
        if not visited_temp[ni][nj]:
            has_hole = True
            qh = deque([(ni, nj)])
            visited_temp[ni][nj] = True
            hole_pos.add((ni, nj))
            while qh:
                ii, jj = qh.popleft()
                for di, dj in dirs:
                    nni, nnj = ii + di, jj + dj
                    if 0 <= nni < h and 0 <= nnj < w and temp[nni][nnj] == 4 and not visited_temp[nni][nnj]:
                        visited_temp[nni][nnj] = True
                        qh.append((nni, nnj))
                        hole_pos.add((nni, nnj))
    return has_hole, hole_pos

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    out = copy_grid(g)
    components = find_components(g)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for comp in components:
        if not comp:
            continue
        min_r, max_r, rows_dict, max_w = get_row_info(comp)
        has_hole, hole_pos = detect_holes(g, comp, h, w)
        if has_hole:
            for i, j in comp:
                out[i][j] = 8
            for i, j in hole_pos:
                out[i][j] = 6
            global_min_c = min(j for _, j in comp)
            global_max_c = max(j for _, j in comp)
            for r in rows_dict:
                lmin, lmax, _ = rows_dict[r]
                is_top = (r == min_r)
                is_bottom = (r == max_r)
                # gaps
                if lmin > global_min_c:
                    start = global_min_c
                    end = lmin
                    color = 2 if is_top or is_bottom else 8
                    for jj in range(start, end):
                        out[r][jj] = color
                if lmax < global_max_c:
                    start = lmax + 1
                    end = global_max_c + 1 if is_top or is_bottom else global_max_c
                    color = 2 if is_top or is_bottom else 8
                    for jj in range(start, end):
                        out[r][jj] = color
            # vertical borders
            for r in rows_dict:
                if global_min_c > 0 and out[r][global_min_c - 1] == 4:
                    out[r][global_min_c - 1] = 2
                if global_max_c < w - 1 and out[r][global_max_c + 1] == 4:
                    out[r][global_max_c + 1] = 2
            # top border row
            if min_r > 0:
                tr = min_r - 1
                tlmin, tlmax, _ = rows_dict[min_r]
                startj = tlmin - 1
                endj = tlmax + 2
                for jj in range(startj, endj):
                    if 0 <= jj < w and out[tr][jj] == 4:
                        out[tr][jj] = 2
            # bottom border row
            if max_r < h - 1:
                br = max_r + 1
                blmin, blmax, _ = rows_dict[max_r]
                startj = blmin - 1
                endj = blmax + 2
                for jj in range(startj, endj):
                    if 0 <= jj < w and out[br][jj] == 4:
                        out[br][jj] = 2
        else:
            # solid
            top_r = min_r
            if top_r in rows_dict:
                tlmin, tlmax, tw = rows_dict[top_r]
                if tw < max_w:
                    for jj in range(tlmin, tlmax + 1):
                        out[top_r][jj] = 2
            # per row left right
            for r in rows_dict:
                lmin, lmax, _ = rows_dict[r]
                if lmin > 0 and out[r][lmin - 1] == 4:
                    out[r][lmin - 1] = 2
                if lmax < w - 1 and out[r][lmax + 1] == 4:
                    out[r][lmax + 1] = 2
            # top border row
            if min_r > 0:
                tr = min_r - 1
                tlmin, tlmax, _ = rows_dict[min_r]
                startj = tlmin - 1
                endj = tlmax + 2
                for jj in range(startj, endj):
                    if 0 <= jj < w and out[tr][jj] == 4:
                        out[tr][jj] = 2
            # bottom border row
            if max_r < h - 1:
                br = max_r + 1
                blmin, blmax, _ = rows_dict[max_r]
                startj = blmin - 1
                endj = blmax + 2
                for jj in range(startj, endj):
                    if 0 <= jj < w and out[br][jj] == 4:
                        out[br][jj] = 2
    return out
```