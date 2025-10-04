```python
from typing import List, Dict, Tuple, Set

def find_components(grid: List[List[int]]) -> List[Dict]:
    n = len(grid)
    visited = [[False] * n for _ in range(n)]
    components = []
    dirs: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if grid[i][j] != 0 and grid[i][j] != 2 and not visited[i][j]:
                color = grid[i][j]
                cells = []
                stack = [(i, j)]
                visited[i][j] = True
                minr = maxr = i
                minc = maxc = j
                while stack:
                    r, c = stack.pop()
                    cells.append((r, c))
                    minr = min(minr, r)
                    maxr = max(maxr, r)
                    minc = min(minc, c)
                    maxc = max(maxc, c)
                    for drr, dcc in dirs:
                        nr = r + drr
                        nc = c + dcc
                        if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] == color:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                if len(cells) >= 1:  # Include all
                    components.append({
                        'color': color,
                        'cells': cells,
                        'minr': minr,
                        'maxr': maxr,
                        'minc': minc,
                        'maxc': maxc
                    })
    return components

def find_attached_reds(grid: List[List[int]], components: List[Dict]) -> None:
    n = len(grid)
    cell_to_comp: Dict[Tuple[int, int], int] = {}
    for idx, comp in enumerate(components):
        for r, c in comp['cells']:
            cell_to_comp[(r, c)] = idx
    dirs: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for comp in components:
        comp['reds'] = []
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 2:
                adjacent_comps = set()
                for drr, dcc in dirs:
                    ni = i + drr
                    nj = j + dcc
                    if 0 <= ni < n and 0 <= nj < n and (ni, nj) in cell_to_comp:
                        adjacent_comps.add(cell_to_comp[(ni, nj)])
                if len(adjacent_comps) == 1:
                    comp_idx = next(iter(adjacent_comps))
                    components[comp_idx]['reds'].append((i, j))

def place_shape(output: List[List[int]], shape: Dict, dr: int, dc: int, n: int) -> List[Tuple[int, int]]:
    new_red_pos = []
    for r, c in shape['cells']:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < n and 0 <= nc < n:
            output[nr][nc] = shape['color']
    for r, c in shape.get('reds', []):
        nr = r + dr
        nc = c + dc
        if 0 <= nr < n and 0 <= nc < n:
            new_red_pos.append((nr, nc))
    return new_red_pos

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    components = find_components(g)
    if not components:
        return [[0] * n for _ in range(n)]
    find_attached_reds(g, components)
    # Find yellow
    yellow_comp = None
    for comp in components:
        if comp['color'] == 4:
            yellow_comp = comp
            break
    if not yellow_comp:
        return [[0] * n for _ in range(n)]  # No yellow, empty?
    target_minr = n // 2
    dr_y = target_minr - yellow_comp['minr']
    dc_y = 0
    output = [[0] * n for _ in range(n)]
    placed_reds: Set[Tuple[int, int]] = set()
    # Place yellow cells
    place_shape(output, yellow_comp, dr_y, dc_y, n)
    # Place yellow reds
    y_reds = yellow_comp.get('reds', [])
    for r, c in y_reds:
        nr = r + dr_y
        nc = c + dc_y
        if 0 <= nr < n and 0 <= nc < n:
            output[nr][nc] = 2
            placed_reds.add((nr, nc))
    y_minc = yellow_comp['minc'] + dc_y
    y_maxc = yellow_comp['maxc'] + dc_y
    y_width = y_maxc - y_minc + 1
    # Unplaced: all except yellow
    unplaced = [comp for comp in components if comp['color'] != 4]
    # Place dockable
    while unplaced:
        best_shape = None
        best_count = -1
        best_dr = 0
        best_dc = 0
        best_dist = float('inf')
        for s_idx in range(len(unplaced)):
            shape = unplaced[s_idx]
            s_reds = shape.get('reds', [])
            if not s_reds:
                continue
            placed_list = list(placed_reds)
            local_best_count = 0
            local_best_dr = 0
            local_best_dc = 0
            local_best_dist = float('inf')
            for sr_r, sr_c in s_reds:
                for pr_r, pr_c in placed_list:
                    dr = pr_r - sr_r
                    dc = pr_c - sr_c
                    count = 0
                    for ss_r, ss_c in s_reds:
                        nr = ss_r + dr
                        nc = ss_c + dc
                        if 0 <= nr < n and 0 <= nc < n and (nr, nc) in placed_reds:
                            count += 1
                    dist = abs(dr) + abs(dc)
                    update = False
                    if count > local_best_count:
                        update = True
                    elif count == local_best_count and dist < local_best_dist:
                        update = True
                    if update:
                        local_best_count = count
                        local_best_dr = dr
                        local_best_dc = dc
                        local_best_dist = dist
            can_place = local_best_count >= 2 or (local_best_count >= 1 and len(s_reds) == 1)
            if can_place and (local_best_count > best_count or
                              (local_best_count == best_count and local_best_dist < best_dist)):
                best_count = local_best_count
                best_dr = local_best_dr
                best_dc = local_best_dc
                best_dist = local_best_dist
                best_shape = (s_idx, shape)
        if best_shape is None:
            break
        s_idx, shape = best_shape
        # Place
        place_shape(output, shape, best_dr, best_dc, n)
        for r, c in shape.get('reds', []):
            nr = r + best_dr
            nc = c + best_dc
            if 0 <= nr < n and 0 <= nc < n:
                output[nr][nc] = 2
                placed_reds.add((nr, nc))
        del unplaced[s_idx]
    # Now remaining unplaced
    for shape in unplaced:
        s_reds = shape.get('reds', [])
        if len(s_reds) == 0:
            dr = target_minr - shape['minr']
            dc = y_minc - shape['minc']
        elif len(s_reds) == 1:
            sr_r, sr_c = s_reds[0]
            if not placed_reds:
                dr = 0
                dc = 0
            else:
                placed_list = list(placed_reds)
                min_dist = float('inf')
                best_pr_r, best_pr_c = 0, 0
                for pr_r, pr_c in placed_list:
                    dist = abs(pr_r - sr_r) + abs(pr_c - sr_c)
                    if dist < min_dist:
                        min_dist = dist
                        best_pr_r = pr_r
                        best_pr_c = pr_c
                dr = best_pr_r - sr_r
                dc = best_pr_c - sr_c
        else:
            # Assume B type
            port_row = max((r for r, _ in s_reds), default=0)
            port_reds_in_row = [(r, c) for r, c in s_reds if r == port_row]
            if len(port_reds_in_row) == 2:
                s_bottom_row = port_row
                s_left_col = min(c for _, c in port_reds_in_row)
                # Find merge_row
                candidates = [rr for rr in range(n) if sum(1 for cc in range(n) if output[rr][cc] == 2) >= 2]
                if candidates:
                    merge_row = min(candidates)
                    merge_right_col_list = [cc for cc in range(n) if output[merge_row][cc] == 2]
                    merge_right_col = max(merge_right_col_list)
                    dr = merge_row - s_bottom_row
                    dc = merge_right_col + y_width - s_left_col
                else:
                    dr = target_minr - shape['minr']
                    dc = y_minc - shape['minc']
            else:
                dr = target_minr - shape['minr']
                dc = y_minc - shape['minc']
        # Place
        place_shape(output, shape, dr, dc, n)
        for r, c in s_reds:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < n and 0 <= nc < n:
                output[nr][nc] = 2
                placed_reds.add((nr, nc))
    return output
```