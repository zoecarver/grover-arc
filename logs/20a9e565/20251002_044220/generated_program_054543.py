```python
from typing import List, Tuple
from collections import deque, defaultdict, Counter

def is_all_c(row: List[int], c: int) -> bool:
    return all(x == c for x in row)

def has_left_partial(row: List[int], c: int, w: int) -> bool:
    return len(row) == w and row[0] == c and all(x == 0 for x in row[1:])

def find_all_components(g: List[List[int]]) -> List[Tuple[int, int, int, int, int, int]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    comps = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for cc in range(cols):
            if g[r][cc] > 0 and not visited[r][cc]:
                c_val = g[r][cc]
                min_r = max_r = r
                min_cc = max_cc = cc
                q = deque([(r, cc)])
                visited[r][cc] = True
                while q:
                    rr, ccc = q.popleft()
                    min_r = min(min_r, rr)
                    max_r = max(max_r, rr)
                    min_cc = min(min_cc, ccc)
                    max_cc = max(max_cc, ccc)
                    for dr, dc in dirs:
                        nr = rr + dr
                        nc = ccc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == c_val and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                bound_w = max_cc - min_cc + 1
                if bound_w >= 3:
                    comps.append((c_val, min_r, max_r, min_cc, max_cc, bound_w))
    return comps

def select_chosen(comps: List[Tuple[int, int, int, int, int, int]]) -> Tuple[int, int]:
    if not comps:
        return 0, 0
    min_min_cc = min(comp[3] for comp in comps)
    candidates = [comp for comp in comps if comp[3] == min_min_cc]
    max_w = max(comp[5] for comp in candidates)
    for comp in candidates:
        if comp[5] == max_w:
            return comp[0], max_w
    return 0, 0

def find_components_for_c_w(g: List[List[int]], c: int, w: int) -> List[Tuple[int, List[List[int]]]]:
    if c == 0 or w == 0:
        return []
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for cc in range(cols):
            if g[r][cc] == c and not visited[r][cc]:
                min_r_comp = max_r_comp = r
                min_cc_comp = max_cc_comp = cc
                q = deque([(r, cc)])
                visited[r][cc] = True
                while q:
                    rr, ccc = q.popleft()
                    min_r_comp = min(min_r_comp, rr)
                    max_r_comp = max(max_r_comp, rr)
                    min_cc_comp = min(min_cc_comp, ccc)
                    max_cc_comp = max(max_cc_comp, ccc)
                    for dr, dc in dirs:
                        nr = rr + dr
                        nc = ccc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == c and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                bound_w = max_cc_comp - min_cc_comp + 1
                if bound_w == w:
                    small = [[c if g[rr][min_cc_comp + k] == c else 0 for k in range(w)] for rr in range(min_r_comp, max_r_comp + 1)]
                    adj_min_r, processed = process_small(small, c, w, min_r_comp)
                    components.append((adj_min_r, processed))
    return components

def process_small(small: List[List[int]], c: int, w: int, original_min_r: int) -> Tuple[int, List[List[int]]]:
    h = len(small)
    if h < 3:
        return original_min_r, small
    # Find start of bottom full block
    k = h - 1
    while k >= 0 and is_all_c(small[k], c):
        k -= 1
    k += 1
    if k > 0 and has_left_partial(small[k - 1], c, w):
        middle = small[k - 1] + [0] * w
        full_row = [c] * (2 * w)
        new_small = [full_row, middle, full_row]
        adj_min_r = original_min_r + (k - 1)
        return adj_min_r, new_small
    return original_min_r, small

def stack_components(comps: List[Tuple[int, List[List[int]]]], c: int, out_w: int) -> List[List[int]]:
    if not comps:
        return []
    comps.sort(key=lambda x: x[0])
    out_grid: List[List[int]] = []
    for i, (min_r, sub) in enumerate(comps):
        sub_h = len(sub)
        padded_sub = [row + [0] * (out_w - len(row)) for row in sub]
        if i > 0 and out_grid:
            prev_bottom = out_grid[-1]
            this_top = padded_sub[0]
            if is_all_c(prev_bottom, c) and is_all_c(this_top, c):
                if out_w >= 2:
                    spacer = [c] + [0] * (out_w - 2) + [c]
                else:
                    spacer = [c]
                out_grid.append(spacer)
        out_grid.extend(padded_sub)
    return out_grid

def fallback_mixed(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    h = n // 2
    # Find center_row with most non-zero
    center_row_idx = max(range(n), key=lambda i: sum(1 for x in g[i] if x > 0))
    # Mode c in center_row
    count = Counter(g[center_row_idx])
    mode_c = max(count, key=count.get) if count else 0
    if mode_c == 0:
        return [[0, 0] for _ in range(h)]
    # Start freq for runs of mode_c >=2
    start_freq = defaultdict(int)
    m = len(g[0])
    for r in range(n):
        j = 0
        while j < m:
            if g[r][j] == mode_c:
                start = j
                while j < m and g[r][j] == mode_c:
                    j += 1
                if j - start >= 2:
                    start_freq[start] += 1
            else:
                j += 1
    frequent_starts = sorted([j for j, f in start_freq.items() if f >= 2])
    if len(frequent_starts) < 3:
        return [[mode_c, mode_c] for _ in range(h)]
    left = frequent_starts[2]
    right = frequent_starts[-1]
    out = []
    # Top half including center
    for d in range(h):
        row_idx = center_row_idx - d
        p1 = g[row_idx][left] if 0 <= row_idx < n and 0 <= left < m else 0
        p2 = g[row_idx][right] if 0 <= row_idx < n and 0 <= right < m else 0
        pair = [p1, p2]
        if p1 > p2:
            pair.reverse()
        out.append(pair)
    # Bottom half flipped, without duplicating center
    for d in range(1, h):
        row_idx = center_row_idx + d
        p1 = g[row_idx][left] if 0 <= row_idx < n and 0 <= left < m else 0
        p2 = g[row_idx][right] if 0 <= row_idx < n and 0 <= right < m else 0
        pair = [p2, p1]
        if d == h - 1 and p1 != p2:
            pair[0] = 0
        out.append(pair)
    while len(out) < h:
        out.append([0, 0])
    return out[:h]

def program(g: List[List[int]]) -> List[List[int]]:
    comps = find_all_components(g)
    c, w = select_chosen(comps)
    if c == 0:
        return fallback_mixed(g)
    comps_list = find_components_for_c_w(g, c, w)
    if not comps_list:
        return fallback_mixed(g)
    max_out_w = max(len(sub[0]) for _, sub in comps_list)
    out_grid = stack_components(comps_list, c, max_out_w)
    return out_grid
```