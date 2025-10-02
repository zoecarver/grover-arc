```python
import collections

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    out = [row[:] for row in g]
    directions4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    directions8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    # Step 1: Flood fill outer 4's (background)
    outer_visited = [[False] * w for _ in range(h)]
    q = collections.deque()
    for i in range(h):
        for j in (0, w - 1):
            if g[i][j] == 4 and not outer_visited[i][j]:
                outer_visited[i][j] = True
                q.append((i, j))
    for j in range(w):
        for i in (0, h - 1):
            if g[i][j] == 4 and not outer_visited[i][j]:
                outer_visited[i][j] = True
                q.append((i, j))
    while q:
        x, y = q.popleft()
        for dx, dy in directions4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and not outer_visited[nx][ny]:
                outer_visited[nx][ny] = True
                q.append((nx, ny))

    # Step 2: Find connected components of 1's (4-connect)
    one_visited = [[False] * w for _ in range(h)]
    components = []
    for i in range(h):
        for j in range(w):
            if g[i][j] == 1 and not one_visited[i][j]:
                comp = []
                q = collections.deque([(i, j)])
                one_visited[i][j] = True
                comp.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions4:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 1 and not one_visited[nx][ny]:
                            one_visited[nx][ny] = True
                            q.append((nx, ny))
                            comp.append((nx, ny))
                components.append(comp)

    # Global hole visited
    hole_visited = set()

    # Step 3: Process each component
    for comp in components:
        # Find adjacent hole starts
        adjacent_hole_starts = set()
        for x, y in comp:
            for dx, dy in directions4:
                nx, ny = x + dx, y + dy
                if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and not outer_visited[nx][ny] and (nx, ny) not in hole_visited:
                    adjacent_hole_starts.add((nx, ny))
        has_hole = bool(adjacent_hole_starts)
        hole_comps = []
        if has_hole:
            for sx, sy in list(adjacent_hole_starts):
                if (sx, sy) in hole_visited:
                    continue
                hole_comp = []
                q = collections.deque([(sx, sy)])
                hole_visited.add((sx, sy))
                hole_comp.append((sx, sy))
                while q:
                    ux, uy = q.popleft()
                    for dx, dy in directions4:
                        nx, ny = ux + dx, uy + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and not outer_visited[nx][ny] and (nx, ny) not in hole_visited:
                            hole_visited.add((nx, ny))
                            q.append((nx, ny))
                            hole_comp.append((nx, ny))
                hole_comps.append(hole_comp)

        if has_hole:
            # Fill component to 8
            for x, y in comp:
                out[x][y] = 8
            # Fill holes
            for hole_comp in hole_comps:
                if not hole_comp:
                    continue
                min_r = min(x for x, y in hole_comp)
                max_r = max(x for x, y in hole_comp)
                height = max_r - min_r + 1
                if height == 1:
                    for x, y in hole_comp:
                        out[x][y] = 8
                    for x, y in hole_comp:
                        bx = x + 1
                        by = y
                        if 0 <= bx < h and 0 <= by < w and g[bx][by] == 1 and out[bx][by] == 8:
                            out[bx][by] = 6
                else:
                    for x, y in hole_comp:
                        out[x][y] = 6
        else:
            # Keep 1's, special bottom row if large run
            if comp:
                max_r = max(x for x, y in comp)
                bottom_ys = sorted(set(y for x, y in comp if x == max_r))
                if bottom_ys:
                    max_run = 1
                    current_run = 1
                    for k in range(1, len(bottom_ys)):
                        if bottom_ys[k] == bottom_ys[k - 1] + 1:
                            current_run += 1
                            max_run = max(max_run, current_run)
                        else:
                            current_run = 1
                    if max_run > 5:
                        for x, y in comp:
                            if x == max_r:
                                out[x][y] = 2

    # Step 4: Add borders - set 4's 8-adjacent to shape (original 1 or current 6/8) to 2
    for i in range(h):
        for j in range(w):
            if out[i][j] == 4:
                adjacent_to_shape = False
                for dx, dy in directions8:
                    ni = i + dx
                    nj = j + dy
                    if 0 <= ni < h and 0 <= nj < w:
                        if g[ni][nj] == 1 or out[ni][nj] in (6, 8):
                            adjacent_to_shape = True
                            break
                if adjacent_to_shape:
                    out[i][j] = 2

    return out
```