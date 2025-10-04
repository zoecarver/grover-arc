```python
from typing import List, Tuple
from collections import deque, defaultdict, Counter

def get_five_height(g: List[List[int]]) -> int:
    positions = [(i, j) for i in range(len(g)) for j in range(len(g[i])) if g[i][j] == 5]
    if not positions:
        return 0
    min_r = min(r for r, _ in positions)
    max_r = max(r for r, _ in positions)
    return max_r - min_r + 1

def is_all_c(row: List[int], c: int) -> bool:
    return all(x == c for x in row)

def has_sparse_row(grid: List[List[int]], c: int) -> bool:
    for row in grid:
        if len(row) >= 2 and row[0] == c and row[-1] == c and not is_all_c(row, c):
            return True
    return False

def find_all_components(g: List[List[int]]) -> List[Tuple[int, int, int, int, int, int]]:
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    comps = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for cc in range(cols):
            if g[r][cc] > 0 and not visited[r][cc]:
                c_val = g[r][cc]
                min_rr, max_rr = r, r
                min_cc, max_cc = cc, cc
                q = deque([(r, cc)])
                visited[r][cc] = True
                while q:
                    rr, ccc = q.popleft()
                    min_rr = min(min_rr, rr)
                    max_rr = max(max_rr, rr)
                    min_cc = min(min_cc, ccc)
                    max_cc = max(max_cc, ccc)
                    for dr, dc in dirs:
                        nr, nc = rr + dr, ccc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == c_val and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                bound_w = max_cc - min_cc + 1
                if bound_w >= 3:
                    comps.append((c_val, min_rr, max_rr, min_cc, max_cc, bound_w))
    return comps

def select_chosen(comps: List[Tuple[int, int, int, int, int, int]]) -> Tuple[int, int]:
    if not comps:
        return 0, 0
    min_min_c = min(comp[3] for comp in comps)
    candidates = [comp for comp in comps if comp[3] == min_min_c]
    max_w = max(comp[5] for comp in candidates)
    for comp in candidates:
        if comp[5] == max_w:
            return comp[0], max_w
    return 0, 0

def process_small(small: List[List[int]], c: int, w: int, original_min_r: int) -> Tuple[int, List[List[int]]]:
    h_small = len(small)
    if h_small < 3:
        return original_min_r, small
    found_i = -1
    for i in range(h_small - 2):
        mid_row = small[i + 1]
        if (is_all_c(small[i], c) and
            len(mid_row) == w and mid_row[0] == c and mid_row[-1] == c and not is_all_c(mid_row, c) and
            is_all_c(small[i + 2], c)):
            found_i = i
    if found_i == -1:
        return original_min_r, small
    mid = small[found_i + 1] + [0] * w
    full_row = [c] * (2 * w)
    new_small = [full_row[:], mid, full_row[:]]
    adj_min_r = original_min_r + found_i
    return adj_min_r, new_small

def find_components_for_c_w(g: List[List[int]], c: int, w: int) -> List[Tuple[int, List[List[int]]]]:
    if c == 0 or w == 0:
        return []
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    res = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for cc in range(cols):
            if g[r][cc] == c and not visited[r][cc]:
                min_r_comp, max_r_comp = r, r
                min_c_comp, max_c_comp = cc, cc
                q = deque([(r, cc)])
                visited[r][cc] = True
                while q:
                    cr, ccc = q.popleft()
                    min_r_comp = min(min_r_comp, cr)
                    max_r_comp = max(max_r_comp, cr)
                    min_c_comp = min(min_c_comp, ccc)
                    max_c_comp = max(max_c_comp, ccc)
                    for dr, dc in dirs:
                        nr, nc = cr + dr, ccc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == c and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                bound_w_comp = max_c_comp - min_c_comp + 1
                if bound_w_comp == w:
                    small = [[g[rr][min_c_comp + k] if g[rr][min_c_comp + k] == c else 0 for k in range(w)] for rr in range(min_r_comp, max_r_comp + 1)]
                    orig_min_r = min_r_comp
                    adj_min_r, processed_small = process_small(small, c, w, orig_min_r)
                    res.append((adj_min_r, processed_small))
    return res

def stack_components(comps: List[Tuple[int, List[List[int]]]], c: int, orig_w: int) -> List[List[int]]:
    if not comps:
        return []
    comps = sorted(comps, key=lambda x: x[0])
    max_w = orig_w
    for _, sg in comps:
        if sg:
            max_w = max(max_w, len(sg[0]))
    stacked = []
    for idx, (_, sg) in enumerate(comps):
        if idx > 0:
            prev_bottom = stacked[-1]
            curr_top = sg[0] if sg else [0] * max_w
            if is_all_c(prev_bottom, c) and is_all_c(curr_top, c):
                spacer_len = max_w
                spacer = [c] + [0] * (spacer_len - 2) + [c] if spacer_len >= 2 else [c] * spacer_len
                stacked.append(spacer)
        for row in sg:
            padded_len = max_w
            padded = row + [0] * (padded_len - len(row))
            stacked.append(padded)
    return stacked

def generate_repeating(old_grid: List[List[int]], c: int, w: int, target_h: int) -> List[List[int]]:
    if not old_grid:
        return []
    curr_w = len(old_grid[0])
    start_full = is_all_c(old_grid[0], c)
    new_grid = []
    for i in range(target_h):
        if (start_full and i % 2 == 0) or (not start_full and i % 2 == 1):
            row = [c] * curr_w
        else:
            row = [c] + [0] * (curr_w - 2) + [c] if curr_w >= 2 else [c] * curr_w
        new_grid.append(row)
    return new_grid

def fallback_mixed(g: List[List[int]], target_h: int) -> List[List[int]]:
    if not g or target_h == 0:
        return []
    rows, cols = len(g), len(g[0])
    # center row with max non-zeros
    center_r = 0
    max_nz = -1
    for r in range(rows):
        nz = sum(1 for cell in g[r] if cell > 0)
        if nz > max_nz:
            max_nz = nz
            center_r = r
    # mode c global
    count = Counter(cell for row in g for cell in row if cell > 0)
    mode_c = count.most_common(1)[0][0] if count else 0
    if mode_c == 0:
        return [[0, 0] for _ in range(target_h)]
    # start freq for runs >=2 of same >0
    start_freq = defaultdict(int)
    for r in range(rows):
        j = 0
        while j < cols:
            if g[r][j] > 0:
                start = j
                curr = g[r][j]
                j += 1
                while j < cols and g[r][j] == curr:
                    j += 1
                if j - start >= 2:
                    start_freq[start] += 1
            else:
                j += 1
    frequent_starts = sorted(s for s, f in start_freq.items() if f >= 2)
    if len(frequent_starts) < 2:
        return [[mode_c, mode_c] for _ in range(target_h)]
    left_pos = frequent_starts[2] if len(frequent_starts) >= 3 else frequent_starts[0]
    right_pos = frequent_starts[-1]
    # build top and bottom
    half = target_h // 2
    top_rows = []
    for d in range(half):
        r = center_r - d
        p0 = g[r][left_pos] if 0 <= r < rows and 0 <= left_pos < cols else 0
        p1 = g[r][right_pos] if 0 <= r < rows and 0 <= right_pos < cols else 0
        top_rows.append([p0, p1])
    top_rows = top_rows[::-1]  # reverse to from top
    bottom_rows = []
    for d in range(1, target_h - half + 1):
        r = center_r + d
        p0 = g[r][right_pos] if 0 <= r < rows and 0 <= right_pos < cols else 0
        p1 = g[r][left_pos] if 0 <= r < rows and 0 <= left_pos < cols else 0
        if d == target_h - half and p0 != p1:
            p0 = 0
        bottom_rows.append([p0, p1])
    return top_rows + bottom_rows

def program(g: List[List[int]]) -> List[List[int]]:
    original_g = [row[:] for row in g]
    five_h = get_five_height(original_g)
    g = [[0 if cell == 5 else cell for cell in row] for row in g]
    comps = find_all_components(g)
    if not comps:
        return fallback_mixed(g, five_h)
    c, w = select_chosen(comps)
    if c == 0:
        return fallback_mixed(g, five_h)
    processed_comps = find_components_for_c_w(g, c, w)
    stacked = stack_components(processed_comps, c, w)
    if len(stacked) > 3 and has_sparse_row(stacked, c):
        stacked = generate_repeating(stacked, c, w, five_h)
    return stacked
```