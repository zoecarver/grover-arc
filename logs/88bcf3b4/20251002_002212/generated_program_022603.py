```python
from typing import List, Tuple
from collections import deque, Counter

def get_background(g: List[List[int]]) -> int:
    flat = [g[i][j] for i in range(len(g)) for j in range(len(g[0]))]
    return Counter(flat).most_common(1)[0][0]

def get_non_background_colors(g: List[List[int]], bg: int) -> set:
    colors = set()
    for row in g:
        for cell in row:
            if cell != bg:
                colors.add(cell)
    return colors

def get_all_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    positions = []
    rows_n = len(g)
    cols_n = len(g[0])
    for i in range(rows_n):
        for j in range(cols_n):
            if g[i][j] == color:
                positions.append((i, j))
    return positions

def is_vertical_bar(positions: List[Tuple[int, int]]) -> bool:
    if not positions:
        return False
    cols = {j for i, j in positions}
    if len(cols) != 1:
        return False
    col = next(iter(cols))
    rows = sorted(i for i, j in positions)
    if len(rows) != len(positions):
        return False
    for k in range(1, len(rows)):
        if rows[k] != rows[k - 1] + 1:
            return False
    return True

def is_horizontal_bar(positions: List[Tuple[int, int]]) -> bool:
    if not positions:
        return False
    rows = {i for i, j in positions}
    if len(rows) != 1:
        return False
    row = next(iter(rows))
    cols = sorted(j for i, j in positions)
    if len(cols) != len(positions):
        return False
    for k in range(1, len(cols)):
        if cols[k] != cols[k - 1] + 1:
            return False
    return True

def is_bar(positions: List[Tuple[int, int]]) -> bool:
    return is_vertical_bar(positions) or is_horizontal_bar(positions)

def get_connected_components(g: List[List[int]], color: int, bg: int) -> List[List[Tuple[int, int]]]:
    rows_n = len(g)
    cols_n = len(g[0])
    visited = [[False] * cols_n for _ in range(rows_n)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for i in range(rows_n):
        for j in range(cols_n):
            if g[i][j] == color and not visited[i][j]:
                comp = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    comp.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows_n and 0 <= ny < cols_n and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                components.append(comp)
    return components

def get_fixed_components(g: List[List[int]], bg: int) -> List[List[Tuple[int, int]]]:
    rows_n = len(g)
    cols_n = len(g[0])
    visited = [[False] * cols_n for _ in range(rows_n)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for i in range(rows_n):
        for j in range(cols_n):
            if g[i][j] != bg and not visited[i][j]:
                comp = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    comp.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows_n and 0 <= ny < cols_n and not visited[nx][ny] and g[nx][ny] != bg:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                components.append(comp)
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    out_grid = [row[:] for row in g]
    bg = get_background(g)
    colors = get_non_background_colors(g, bg)
    N_dict = {}
    for colr in colors:
        components = get_connected_components(g, colr, bg)
        has_large_nonbar = any(len(comp) > 3 and not is_bar(comp) for comp in components)
        if has_large_nonbar:
            positions = get_all_positions(g, colr)
            N_dict[colr] = len(positions)
            for i, j in positions:
                out_grid[i][j] = bg
    if not N_dict:
        return out_grid
    fixed_comps = get_fixed_components(out_grid, bg)
    rows_n = len(g)
    cols_n = len(g[0])
    filler_colors = sorted(N_dict.keys())
    for color in filler_colors:
        N = N_dict[color]
        if len(fixed_comps) < 2:
            if fixed_comps:
                comp = fixed_comps[0]
                min_r = min(r for r, c in comp)
                min_c = min(c for r, c in comp) - 1
                if min_c < 0:
                    min_c = max(c for r, c in comp) + 1
                placed = 0
                r = min_r
                while placed < N and r < rows_n:
                    if 0 <= min_c < cols_n and out_grid[r][min_c] == bg:
                        out_grid[r][min_c] = color
                        placed += 1
                    r += 1
            continue
        fixed_comps_sorted = sorted(fixed_comps, key=lambda comp: min(r for r, c in comp))
        upper = fixed_comps_sorted[0]
        lower = fixed_comps_sorted[-1]
        upper_num = len(upper)
        lower_num = len(lower)
        # upper bottom
        upper_bottom_r = max(r for r, c in upper)
        bottom_cands = [c for r, c in upper if r == upper_bottom_r]
        upper_bottom_c = round(sum(bottom_cands) / len(bottom_cands))
        # lower top
        lower_top_r = min(r for r, c in lower)
        top_cands = [c for r, c in lower if r == lower_top_r]
        lower_top_c = round(sum(top_cands) / len(top_cands))
        delta_r = lower_top_r - upper_bottom_r
        if delta_r <= 0:
            continue  # no bridge needed
        delta_c = lower_top_c - upper_bottom_c
        sign_dc = 0
        if delta_c > 0:
            sign_dc = 1
        elif delta_c < 0:
            sign_dc = -1
        candidates = set()
        # left attach
        do_left_attach = (upper_num <= lower_num)
        if do_left_attach:
            upper_sorted = sorted(upper, key=lambda p: (-p[0], p[1]))
            for p in upper_sorted:
                r, c = p
                lc = c - 1
                if 0 <= lc < cols_n:
                    candidates.add((r, lc))
        # bridge
        bridge_pos_set = set()
        if sign_dc == 0:
            bridge_col = upper_bottom_c - 1
            num_bridge = delta_r + 1
            for k in range(num_bridge):
                br = upper_bottom_r + k
                if 0 <= br < rows_n and 0 <= bridge_col < cols_n:
                    bridge_pos_set.add((br, bridge_col))
        else:
            if upper_num <= lower_num:
                num_b = delta_r
                sr = upper_bottom_r + 1
                sc = upper_bottom_c
                for k in range(num_b):
                    r = sr + k
                    if r >= rows_n:
                        break
                    incr = round(k * abs(delta_c) / delta_r)
                    c = sc + sign_dc * incr
                    if 0 <= c < cols_n:
                        bridge_pos_set.add((r, c))
            else:
                num_b = delta_r + 1
                sr = upper_bottom_r
                sc = upper_bottom_c + sign_dc
                for k in range(num_b):
                    r = sr + k
                    if r >= rows_n:
                        break
                    incr = round(k * abs(delta_c) / delta_r)
                    c = sc + sign_dc * incr
                    if 0 <= c < cols_n:
                        bridge_pos_set.add((r, c))
        candidates.update(bridge_pos_set)
        # ext
        if upper_num <= lower_num:
            # upper ext
            upper_top_r = min(r for r, c in upper)
            top_cands_u = [c for r, c in upper if r == upper_top_r]
            upper_top_c = round(sum(top_cands_u) / len(top_cands_u))
            ext_num = delta_r
            sr = upper_top_r - 1
            sc = upper_top_c
            for k in range(ext_num):
                r = sr - k
                if r < 0:
                    break
                incr = round(k * abs(delta_c) / delta_r) if delta_r > 0 else 0
                c = sc + sign_dc * incr
                if 0 <= c < cols_n:
                    candidates.add((r, c))
        else:
            # lower ext
            if bridge_pos_set:
                last_bridge = max(bridge_pos_set, key=lambda p: p[0])
                last_br, last_bc = last_bridge
            else:
                last_br = lower_top_r
                last_bc = lower_top_c
            vert_num = lower_num - 1
            for k in range(1, vert_num + 1):
                vr = lower_top_r + k
                if vr >= rows_n:
                    break
                candidates.add((vr, last_bc))
            # last vert
            last_vert_r = lower_top_r + vert_num
            last_vert_c = last_bc
            # mirror
            mirror_num = delta_r
            start_mr = last_vert_r + 1
            start_mc = last_vert_c + (-sign_dc)
            for k in range(mirror_num):
                mr = start_mr + k
                if mr >= rows_n:
                    break
                incr = k
                mc = start_mc + (-sign_dc) * incr
                if 0 <= mc < cols_n:
                    candidates.add((mr, mc))
        # now place
        cand_list = sorted(candidates, key=lambda p: (p[0], p[1]))
        placed = 0
        for r, c in cand_list:
            if out_grid[r][c] == bg and placed < N:
                out_grid[r][c] = color
                placed += 1
    return out_grid
```