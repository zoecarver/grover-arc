```python
from collections import deque
import copy

def find_component(g, start_i, start_j, visited, directions):
    h = len(g)
    w = len(g[0])
    component = []
    q = deque([(start_i, start_j)])
    visited[start_i][start_j] = True
    while q:
        x, y = q.popleft()
        component.append((x, y))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 1 and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
    return component

def get_external_bg_visited(g, component, directions):
    h = len(g)
    w = len(g[0])
    bg_visited = [[False] * w for _ in range(h)]
    q = deque()
    seen_adj = set()
    for x, y in component:
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and (nx, ny) not in seen_adj:
                seen_adj.add((nx, ny))
                q.append((nx, ny))
                bg_visited[nx][ny] = True
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and not bg_visited[nx][ny]:
                bg_visited[nx][ny] = True
                q.append((nx, ny))
    return bg_visited

def get_holes(g, component, bg_visited, directions):
    h = len(g)
    w = len(g[0])
    min_r = min(x for x, _ in component)
    max_r = max(x for x, _ in component)
    min_c = min(y for _, y in component)
    max_c = max(y for _, y in component)
    holes = []
    hole_visited = [[False] * w for _ in range(h)]
    for r in range(max(0, min_r - 1), min(h, max_r + 2)):
        for c in range(max(0, min_c - 1), min(w, max_c + 2)):
            if g[r][c] == 4 and not bg_visited[r][c] and not hole_visited[r][c]:
                hole = []
                q = deque([(r, c)])
                hole_visited[r][c] = True
                while q:
                    x, y = q.popleft()
                    hole.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4 and not bg_visited[nx][ny] and not hole_visited[nx][ny]:
                            hole_visited[nx][ny] = True
                            q.append((nx, ny))
                if hole:
                    holes.append(hole)
    return holes

def handle_small_hole(out, hole, h, w, directions):
    for x, y in hole:
        out[x][y] = 8
    for x, y in hole:
        nx = x + 1
        if nx < h and y < w and out[nx][y] == 8:
            out[nx][y] = 6

def handle_protrusions(out, g, component, directions):
    h = len(out)
    w = len(out[0])
    min_r = min(x for x, _ in component)
    max_r = max(x for x, _ in component)
    for r in range(min_r + 1, max_r + 1):
        row_comp = [(x, y) for x, y in component if x == r]
        if not row_comp:
            continue
        row_cols = sorted(list(set(y for _, y in row_comp)))
        segments = []
        if row_cols:
            current = [row_cols[0]]
            for k in range(1, len(row_cols)):
                if row_cols[k] == current[-1] + 1:
                    current.append(row_cols[k])
                else:
                    segments.append(current)
                    current = [row_cols[k]]
            segments.append(current)
        if len(segments) > 1:
            right_seg = segments[-1]
            if len(right_seg) >= 3:
                right1 = right_seg[-1]
                right2 = right_seg[-2]
                out[r][right1] = 2
                if right2 >= 0 and right2 < w:
                    out[r][right2] = 2

def process_filled_component(out, g, component, holes, directions):
    h = len(out)
    w = len(out[0])
    # Fill 1's with 8
    for x, y in component:
        out[x][y] = 8
    # Handle holes
    for hole in holes:
        size = len(hole)
        if size < 3:
            handle_small_hole(out, hole, h, w, directions)
        else:
            for x, y in hole:
                out[x][y] = 6
    # Set top row to 2's
    top_r = min(x for x, _ in component)
    top_cols_set = {y for x, y in component if x == top_r}
    if top_cols_set:
        min_tc = min(top_cols_set) - 1
        max_tc = max(top_cols_set) + 1
        for c in range(max(0, min_tc), min(w, max_tc + 1)):
            out[top_r][c] = 2
    # Handle protrusions
    handle_protrusions(out, g, component, directions)
    # Add left and right column borders
    min_c = min(y for _, y in component)
    max_c = max(y for _, y in component)
    min_r = min(x for x, _ in component)
    max_r = max(x for x, _ in component)
    # Left
    left_c = min_c - 1
    if left_c >= 0:
        for rr in range(min_r, max_r + 1):
            if out[rr][left_c] == 4:
                out[rr][left_c] = 2
    # Right
    right_c = max_c + 1
    if right_c < w:
        for rr in range(min_r, max_r + 1):
            if out[rr][right_c] == 4:
                out[rr][right_c] = 2
    # Add bottom border below
    bottom_r = max_r + 1
    if bottom_r < h:
        bottom_cols_set = {y for x, y in component if x == max_r}
        if bottom_cols_set:
            min_bc = min(bottom_cols_set) - 1
            max_bc = max(bottom_cols_set) + 1
            for c in range(max(0, min_bc), min(w, max_bc + 1)):
                out[bottom_r][c] = 2
    # Add adjacent 4's to 2
    adjacent = set()
    for x, y in component:
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and out[nx][ny] == 4:
                adjacent.add((nx, ny))
    for x, y in adjacent:
        out[x][y] = 2

def process_solid_component(out, g, component, directions):
    h = len(out)
    w = len(out[0])
    # Add adjacent 4's to 2
    adjacent = set()
    for x, y in component:
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 4:
                adjacent.add((nx, ny))
    for x, y in adjacent:
        out[x][y] = 2
    # Top border
    top_r = min(x for x, _ in component)
    if top_r > 0:
        top_cols_set = {y for x, y in component if x == top_r}
        if top_cols_set:
            min_tc = min(top_cols_set) - 1
            max_tc = max(top_cols_set) + 1
            for c in range(max(0, min_tc), min(w, max_tc + 1)):
                if g[top_r - 1][c] == 4:
                    out[top_r - 1][c] = 2
    # Bottom border
    bottom_r = max(x for x, _ in component)
    height = bottom_r - top_r + 1
    bottom_cols_set = {y for x, y in component if x == bottom_r}
    if bottom_cols_set:
        min_bc = min(bottom_cols_set) - 1
        max_bc = max(bottom_cols_set) + 1
        if height > 5:
            # Color inside bottom row
            for c in range(max(0, min_bc), min(w, max_bc + 1)):
                out[bottom_r][c] = 2
        else:
            b_r = bottom_r + 1
            if b_r < h:
                for c in range(max(0, min_bc), min(w, max_bc + 1)):
                    if g[b_r][c] == 4:
                        out[b_r][c] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    out = [row[:] for row in g]
    visited = [[False] * w for _ in range(h)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] == 1 and not visited[i][j]:
                component = find_component(g, i, j, visited, directions)
                bg_visited = get_external_bg_visited(g, component, directions)
                holes = get_holes(g, component, bg_visited, directions)
                if holes:
                    process_filled_component(out, g, component, holes, directions)
                else:
                    process_solid_component(out, g, component, directions)
    return out
```