```python
from typing import List
from collections import deque

def flood_fill(r: int, c: int, color: int, g: List[List[int]], n: int, visited: List[List[bool]]) -> List[tuple]:
    q = deque()
    q.append((r, c))
    visited[r][c] = True
    cells = []
    while q:
        x, y = q.popleft()
        cells.append((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == color:
                visited[nx][ny] = True
                q.append((nx, ny))
    return cells

def flood_fill_no_visit(r: int, c: int, color: int, g: List[List[int]], n: int) -> List[tuple]:
    q = deque()
    q.append((r, c))
    cells = []
    visited_temp = set([(r, c)])
    while q:
        x, y = q.popleft()
        cells.append((x, y))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in visited_temp and g[nx][ny] == color:
                visited_temp.add((nx, ny))
                q.append((nx, ny))
    return cells

def get_col_start_framed(min_r: int, min_c: int) -> int:
    if min_r >= 10:
        return 0
    else:
        if min_c >= 12:
            return 5
        else:
            return 0

def get_col_start_unframed(min_c: int) -> int:
    center = min_c + 2
    if center < 11:
        return 12
    else:
        return 17

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    b = g[0][0]
    visited = [[False] * n for _ in range(n)]
    objects = []
    for i in range(n):
        for j in range(n):
            if not visited[i][j] and g[i][j] != b and g[i][j] != 8:
                c = g[i][j]
                component = flood_fill(i, j, c, g, n, visited)
                f_set = set()
                adj_f = set()
                for x, y in component:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n:
                            col_adj = g[nx][ny]
                            if col_adj != c and col_adj != b:
                                f_set.add(col_adj)
                                if col_adj == list(f_set)[0] if f_set else False:
                                    adj_f.add((nx, ny))
                if len(f_set) == 1:
                    f = list(f_set)[0]
                    frame_cells = []
                    for sx, sy in adj_f:
                        frame_comp = flood_fill_no_visit(sx, sy, f, g, n)
                        frame_cells.extend(frame_comp)
                    object_cells_set = set(component)
                    for fc in frame_cells:
                        object_cells_set.add(fc)
                    object_cells = list(object_cells_set)
                    for x, y in frame_cells:
                        visited[x][y] = True
                    min_r = min(x for x, _ in object_cells)
                    min_c = min(y for _, y in object_cells)
                    is_framed = (f == 8)
                    obj_dict = {
                        'cells': [(x, y, g[x][y]) for x, y in object_cells],
                        'min_r': min_r,
                        'min_c': min_c,
                        'is_framed': is_framed
                    }
                    objects.append(obj_dict)
                else:
                    min_r = min(x for x, _ in component)
                    min_c = min(y for _, y in component)
                    is_framed = False
                    obj_dict = {
                        'cells': [(x, y, g[x][y]) for x, y in component],
                        'min_r': min_r,
                        'min_c': min_c,
                        'is_framed': is_framed
                    }
                    objects.append(obj_dict)
    framed = [o for o in objects if o['is_framed']]
    unframed = [o for o in objects if not o['is_framed']]
    framed.sort(key=lambda o: (o['min_r'], o['min_c']))
    unframed.sort(key=lambda o: (o['min_r'], o['min_c']))
    new_g = [[b for _ in range(n)] for _ in range(n)]
    for o in framed:
        min_r = o['min_r']
        min_c = o['min_c']
        col_start = get_col_start_framed(min_r, min_c)
        for x, y, colr in o['cells']:
            new_y = col_start + (y - min_c)
            new_g[x][new_y] = colr
    for o in unframed:
        min_c = o['min_c']
        col_start = get_col_start_unframed(min_c)
        for x, y, colr in o['cells']:
            new_y = col_start + (y - min_c)
            new_g[x][new_y] = colr
    return new_g
```