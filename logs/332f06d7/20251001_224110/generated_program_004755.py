```python
def touches_border(i: int, j: int, n: int) -> bool:
    return i == 0 or i == n - 1 or j == 0 or j == n - 1

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    new_g = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = [[False] * n for _ in range(n)]
    persisted = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == 2 and not visited[i][j]:
                stack = [(i, j)]
                visited[i][j] = True
                component = [(i, j)]
                touches_top = (i == 0)
                touches_bottom = (i == n - 1)
                min_r = i
                max_r = i
                min_c = j
                max_c = j
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == 2:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            component.append((nx, ny))
                            touches_top = touches_top or (nx == 0)
                            touches_bottom = touches_bottom or (nx == n - 1)
                            min_r = min(min_r, nx)
                            max_r = max(max_r, nx)
                            min_c = min(min_c, ny)
                            max_c = max(max_c, ny)
                size = len(component)
                if size == 1 or touches_top:
                    for x, y in component:
                        new_g[x][y] = 0
                else:
                    persisted.append((min_r, max_r, min_c, max_c, touches_bottom))
    visited = [[False] * n for _ in range(n)]
    max_size = 0
    main_minr = main_maxr = main_minc = main_maxc = 0
    for i in range(n):
        for j in range(n):
            if new_g[i][j] == 1 and not visited[i][j]:
                stack = [(i, j)]
                visited[i][j] = True
                c_size = 1
                b_minr = b_maxr = i
                b_minc = b_maxc = j
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and new_g[nx][ny] == 1:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            c_size += 1
                            b_minr = min(b_minr, nx)
                            b_maxr = max(b_maxr, nx)
                            b_minc = min(b_minc, ny)
                            b_maxc = max(b_maxc, ny)
                if c_size > max_size:
                    max_size = c_size
                    main_minr = b_minr
                    main_maxr = b_maxr
                    main_minc = b_minc
                    main_maxc = b_maxc
    if max_size > 0 and persisted:
        height_b = main_maxr - main_minr + 1
        width_b = main_maxc - main_minc + 1
        for min_r, max_r, min_c, max_c, touches_btm in persisted:
            h = max_r - min_r + 1
            w = max_c - min_c + 1
            row_start_base = main_minr + (height_b - h) // 2
            col_start_base = main_minc + (width_b - w) // 2
            if touches_btm:
                row_start = row_start_base + 1
                col_start = main_maxc - w + 1
            else:
                row_start = row_start_base
                col_start = col_start_base
            for rr in range(h):
                r = row_start + rr
                for cc in range(w):
                    c = col_start + cc
                    if main_minr <= r <= main_maxr and main_minc <= c <= main_maxc and new_g[r][c] == 1:
                        new_g[r][c] = 0
    visited = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if new_g[i][j] == 0 and not visited[i][j] and not touches_border(i, j, n):
                stack = [(i, j)]
                visited[i][j] = True
                component = [(i, j)]
                touches_border_flag = touches_border(i, j, n)
                touches_blue = False
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                            if new_g[nx][ny] == 0:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                                component.append((nx, ny))
                                touches_border_flag = touches_border_flag or touches_border(nx, ny, n)
                            elif new_g[nx][ny] == 1:
                                touches_blue = True
                if not touches_border_flag and touches_blue:
                    for x, y in component:
                        if g[x][y] == 0:
                            new_g[x][y] = 1
    return new_g
```