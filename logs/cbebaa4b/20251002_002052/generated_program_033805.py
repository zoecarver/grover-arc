```python
from typing import List, Tuple, Dict
import math

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [[0] * n for _ in range(n)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    # Extract components
    visited = [[False] * n for _ in range(n)]
    components = []
    for i in range(n):
        for j in range(n):
            if g[i][j] > 0 and g[i][j] != 2 and not visited[i][j]:
                color = g[i][j]
                cells = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    cells.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append({'color': color, 'cells': cells})
    # Attach reds
    pos_to_comp = {}
    for idx, comp in enumerate(components):
        for r, c in comp['cells']:
            pos_to_comp[(r, c)] = idx
    for comp in components:
        comp['reds'] = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == 2:
                touching = set()
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < n and 0 <= nj < n and (ni, nj) in pos_to_comp:
                        touching.add(pos_to_comp[(ni, nj)])
                if len(touching) == 1:
                    idx = list(touching)[0]
                    components[idx]['reds'].append((i, j))
    # Find yellow
    yellow = None
    for comp in components:
        if comp['color'] == 4:
            yellow = comp
            break
    if not yellow:
        return out
    # Place yellow
    cells = yellow['cells']
    min_r = min(r for r, c in cells)
    dr_y = n // 2 - min_r
    dc_y = 0
    for r, c in cells:
        nr = r + dr_y
        nc = c + dc_y
        if 0 <= nr < n and 0 <= nc < n:
            out[nr][nc] = 4
    for r, c in yellow['reds']:
        nr = r + dr_y
        nc = c + dc_y
        if 0 <= nr < n and 0 <= nc < n:
            out[nr][nc] = 2
    # Remaining
    remaining = [comp for comp in components if comp['color'] != 4]
    # Sort by input centroid row ascending
    def get_centroid(comp: Dict) -> float:
        cells = comp['cells']
        if not cells:
            return 0.0
        return sum(r for r, c in cells) / len(cells)
    remaining.sort(key=get_centroid)
    # Current centroid
    def update_current_centroid(out: List[List[int]], n: int) -> Tuple[float, float]:
        sum_r = 0.0
        sum_c = 0.0
        count = 0
        for i in range(n):
            for j in range(n):
                if out[i][j] != 0:
                    sum_r += i
                    sum_c += j
                    count += 1
        if count == 0:
            return n / 2, n / 2
        return sum_r / count, sum_c / count
    curr_cent_r, curr_cent_c = update_current_centroid(out, n)
    # For each remaining
    for comp in remaining:
        color = comp['color']
        cells = comp['cells']
        reds = comp['reds']
        if not cells:
            continue
        # Compute rel
        all_r = [r for r, c in cells] + [r for r, c in reds]
        all_c = [c for r, c in cells] + [c for r, c in reds]
        if not all_r:
            continue
        min_all_r = min(all_r)
        min_all_c = min(all_c)
        max_all_r = max(all_r)
        max_all_c = max(all_c)
        height = max_all_r - min_all_r + 1
        width = max_all_c - min_all_c + 1
        rel_cells = [(r - min_all_r, c - min_all_c) for r, c in cells]
        rel_reds = [(r - min_all_r, c - min_all_c) for r, c in reds]
        comp_cent_r = get_centroid(comp)
        comp_cent_c = sum(c for r, c in cells) / len(cells)
        # Dirs for score
        touch_edge = touch_top(comp) or touch_bottom(comp, n)
        dirs_score = directions if touch_edge else [(0, 1), (0, -1)]
        # Search
        best_connection = -1
        best_dist = float('inf')
        best_start_r = n
        best_start_c = n
        best_dr = 0
        best_dc = 0
        for start_r in range(n - height + 1):
            for start_c in range(n - width + 1):
                # Check valid
                valid = True
                shifted_cells = []
                for rel_r, rel_c in rel_cells:
                    nr = start_r + rel_r
                    nc = start_c + rel_c
                    if out[nr][nc] != 0 and out[nr][nc] != color:
                        valid = False
                        break
                    shifted_cells.append((nr, nc))
                if not valid:
                    continue
                valid_red = True
                shifted_reds = []
                for rel_r, rel_c in rel_reds:
                    nr = start_r + rel_r
                    nc = start_c + rel_c
                    if out[nr][nc] != 0:
                        valid_red = False
                        break
                    shifted_reds.append((nr, nc))
                if not valid_red:
                    continue
                # Connection count
                connection = 0
                # Cells adj to existing 2's
                for nr, nc in shifted_cells:
                    for dx, dy in dirs_score:
                        ar = nr + dx
                        ac = nc + dy
                        if 0 <= ar < n and 0 <= ac < n and out[ar][ac] == 2:
                            connection += 1
                # Reds adj to existing cells
                for nr, nc in shifted_reds:
                    for dx, dy in dirs_score:
                        ar = nr + dx
                        ac = nc + dy
                        if 0 <= ar < n and 0 <= ac < n and out[ar][ac] != 0:
                            connection += 1
                # Shifted cent
                shifted_cent_r = start_r + (comp_cent_r - min_all_r)
                shifted_cent_c = start_c + (comp_cent_c - min_all_c)
                dist = math.hypot(shifted_cent_r - curr_cent_r, shifted_cent_c - curr_cent_c)
                # Update best
                update = False
                if connection > best_connection:
                    update = True
                elif connection == best_connection:
                    if dist < best_dist:
                        update = True
                    elif dist == best_dist:
                        if start_r < best_start_r:
                            update = True
                        elif start_r == best_start_r:
                            if start_c < best_start_c:
                                update = True
                if update:
                    best_connection = connection
                    best_dist = dist
                    best_start_r = start_r
                    best_start_c = start_c
                    best_dr = start_r - min_all_r + min_all_r  # not needed
                    best_dc = start_c - min_all_c + min_all_c
        # Place with best
        if best_connection >= 0 and best_start_r < n:
            # Place cells
            for rel_r, rel_c in rel_cells:
                nr = best_start_r + rel_r
                nc = best_start_c + rel_c
                out[nr][nc] = color
            # Place reds
            for rel_r, rel_c in rel_reds:
                nr = best_start_r + rel_r
                nc = best_start_c + rel_c
                if 0 <= nr < n and 0 <= nc < n:
                    out[nr][nc] = 2
        else:
            # Fallback, place above left if low, right if high
            is_low = comp_cent_r < curr_cent_r
            start_r = 4
            if is_low:
                start_c = max(0, int(curr_cent_c) - width)
            else:
                start_c = min(n - width, int(curr_cent_c))
            # Shift if overlap
            while start_r + height <= n:
                overlap = False
                for rel_r, rel_c in rel_cells:
                    nr = start_r + rel_r
                    nc = start_c + rel_c
                    if out[nr][nc] != 0 and out[nr][nc] != color:
                        overlap = True
                        break
                if not overlap:
                    red_ok = True
                    for rel_r, rel_c in rel_reds:
                        nr = start_r + rel_r
                        nc = start_c + rel_c
                        if 0 <= nr < n and 0 <= nc < n and out[nr][nc] != 0:
                            red_ok = False
                            break
                if not overlap and red_ok:
                    break
                start_c += 1
                if start_c + width > n:
                    start_c = max(0, int(curr_cent_c) - width)
                    start_r += 1
            if start_r + height <= n:
                # place
                for rel_r, rel_c in rel_cells:
                    nr = start_r + rel_r
                    nc = start_c + rel_c
                    out[nr][nc] = color
                for rel_r, rel_c in rel_reds:
                    nr = start_r + rel_r
                    nc = start_c + rel_c
                    if 0 <= nr < n and 0 <= nc < n:
                        out[nr][nc] = 2
            else:
                # place below center
                start_r = int(curr_cent_r) + 1
                start_c = int(curr_cent_c) - width // 2
                # simple place without check
                for rel_r, rel_c in rel_cells:
                    nr = start_r + rel_r
                    nc = start_c + rel_c
                    if 0 <= nr < n and 0 <= nc < n:
                        out[nr][nc] = color
                for rel_r, rel_c in rel_reds:
                    nr = start_r + rel_r
                    nc = start_c + rel_c
                    if 0 <= nr < n and 0 <= nc < n:
                        out[nr][nc] = 2
        # Update current cent
        curr_cent_r, curr_cent_c = update_current_centroid(out, n)
    return out

def touch_top(comp: Dict) -> bool:
    cells = comp['cells']
    reds = comp['reds']
    min_r = min((r for r, c in cells), default = 999)
    min_red = min((r for r, c in reds), default = 999)
    return min(min_r, min_red) <= 0

def touch_bottom(comp: Dict, n: int) -> bool:
    cells = comp['cells']
    reds = comp['reds']
    max_r = max((r for r, c in cells), default = -1)
    max_red = max((r for r, c in reds), default = -1)
    return max(max_r, max_red) >= n - 1
```