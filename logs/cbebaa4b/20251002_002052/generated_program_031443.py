```python
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def find_components(grid):
    n = len(grid)
    visited = [[False] * n for _ in range(n)]
    components = []
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0 and grid[i][j] != 2 and not visited[i][j]:
                color = grid[i][j]
                cells = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    cells.append((x, y))
                    for di, dj in directions:
                        nx, ny = x + di, y + dj
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and grid[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if cells:
                    minr = min(r for r, c in cells)
                    maxr = max(r for r, c in cells)
                    minc = min(c for r, c in cells)
                    maxc = max(c for r, c in cells)
                    comp = {
                        'color': color,
                        'cells': cells,
                        'reds': [],
                        'minr': minr,
                        'maxr': maxr,
                        'minc': minc,
                        'maxc': maxc
                    }
                    components.append(comp)
    return components

def find_attached_reds(grid, components):
    n = len(grid)
    pos_to_comp = {}
    for idx, comp in enumerate(components):
        for r, c in comp['cells']:
            pos_to_comp[(r, c)] = idx
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 2:
                touching_comps = set()
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < n and (ni, nj) in pos_to_comp:
                        touching_comps.add(pos_to_comp[(ni, nj)])
                if len(touching_comps) == 1:
                    comp_idx = next(iter(touching_comps))
                    components[comp_idx]['reds'].append((i, j))

def can_place_shape(comp, dr, dc, out, n):
    color = comp['color']
    for r, c in comp['cells']:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < n and 0 <= nc < n:
            if out[nr][nc] != 0 and out[nr][nc] != color:
                return False
    return True

def place_shape(out, comp, dr, dc, n):
    color = comp['color']
    new_reds = []
    for r, c in comp['cells']:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < n and 0 <= nc < n:
            out[nr][nc] = color
    for r, c in comp['reds']:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < n and 0 <= nc < n:
            out[nr][nc] = 2
            new_reds.append((nr, nc))
    return new_reds

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [[0] * n for _ in range(n)]
    components = find_components(g)
    find_attached_reds(g, components)
    yellow = next((c for c in components if c['color'] == 4), None)
    if not yellow:
        return out
    components.remove(yellow)
    dr_y = n // 2 - yellow['minr']
    dc_y = 0
    if can_place_shape(yellow, dr_y, dc_y, out, n):
        new_reds = place_shape(out, yellow, dr_y, dc_y, n)
        placed_reds = set(new_reds)
    else:
        placed_reds = set()
    components.sort(key=lambda x: sum(r for r, _ in x['cells']) / len(x['cells']))
    for comp in components:
        best_num_match = 0
        best_dr = 0
        best_dc = 0
        best_dist = float('inf')
        for s_r, s_c in comp['reds']:
            for p_r, p_c in placed_reds:
                dr = p_r - s_r
                dc = p_c - s_c
                if can_place_shape(comp, dr, dc, out, n):
                    num_match = sum(1 for sr2, sc2 in comp['reds'] if (sr2 + dr, sc2 + dc) in placed_reds)
                    dist = abs(dr) + abs(dc)
                    if num_match > best_num_match or (num_match == best_num_match and dist < best_dist):
                        best_num_match = num_match
                        best_dr = dr
                        best_dc = dc
                        best_dist = dist
        if best_num_match > 0:
            place_shape(out, comp, best_dr, best_dc, n)
            new_reds = [(r + best_dr, c + best_dc) for r, c in comp['reds'] if 0 <= r + best_dr < n and 0 <= c + best_dc < n]
            for nr, nc in new_reds:
                placed_reds.add((nr, nc))
        else:
            comp_cent = sum(r for r, _ in comp['cells']) / len(comp['cells'])
            yellow_cent = sum(r for r, _ in yellow['cells']) / len(yellow['cells'])
            h_comp = comp['maxr'] - comp['minr'] + 1
            w_comp = comp['maxc'] - comp['minc'] + 1
            y_w = yellow['maxc'] - yellow['minc'] + 1
            if comp_cent < yellow_cent:
                dy = (n // 2) - h_comp
                left = dc_y
            else:
                dy = (n // 2 + (yellow['maxr'] - yellow['minr'])) + 1
                left = dc_y
                bottom_reds_row = max((r for r, c in comp['reds']), default=0)
                if bottom_reds_row == comp['maxr'] and len(comp['reds']) >= 2:
                    left = dc_y + y_w
                    dy = (n // 2 + (yellow['maxr'] - yellow['minr'])) - (comp['maxr'] - comp['minr'])
            dx = 0
            placed = False
            while dx < n - w_comp and not placed:
                test_left = left + dx
                if can_place_shape(comp, dy, test_left, out, n):
                    place_shape(out, comp, dy, test_left, n)
                    new_reds = [(r + dy, c + test_left) for r, c in comp['reds'] if 0 <= r + dy < n and 0 <= c + test_left < n]
                    for nr, nc in new_reds:
                        placed_reds.add((nr, nc))
                    placed = True
                dx += 1
            if not placed:
                dy += 1
                dx = 0
                while dy < n - h_comp and not placed:
                    while dx < n - w_comp and not placed:
                        test_left = left + dx
                        if can_place_shape(comp, dy, test_left, out, n):
                            place_shape(out, comp, dy, test_left, n)
                            new_reds = [(r + dy, c + test_left) for r, c in comp['reds'] if 0 <= r + dy < n and 0 <= c + test_left < n]
                            for nr, nc in new_reds:
                                placed_reds.add((nr, nc))
                            placed = True
                        dx += 1
                    dx = 0
                    dy += 1
    return out
```