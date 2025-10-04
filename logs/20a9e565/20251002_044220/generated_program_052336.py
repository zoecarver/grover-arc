```python
import collections
from typing import List, Tuple

def find_all_components(g: List[List[int]]) -> List[Tuple[int, int, int, int, int, int]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for cc in range(cols):
            if g[r][cc] > 0 and not visited[r][cc]:
                c = g[r][cc]
                min_rr = max_rr = r
                min_ccc = max_ccc = cc
                stack = [(r, cc)]
                visited[r][cc] = True
                while stack:
                    cr, ccc = stack.pop()
                    min_rr = min(min_rr, cr)
                    max_rr = max(max_rr, cr)
                    min_ccc = min(min_ccc, ccc)
                    max_ccc = max(max_ccc, ccc)
                    for dr, dc in dirs:
                        nr = cr + dr
                        nc = ccc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == c and not visited[nr][nc]:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                bound_w = max_ccc - min_ccc + 1
                if bound_w >= 3:
                    components.append((c, min_rr, max_rr, min_ccc, max_ccc, bound_w))
    return components

def select_chosen(comps: List[Tuple[int, int, int, int, int, int]]) -> Tuple[int, int]:
    if not comps:
        return 0, 0
    min_min_c = min(comp[3] for comp in comps)
    candidates = [comp for comp in comps if comp[3] == min_min_c]
    chosen = max(candidates, key=lambda x: x[5])
    return chosen[0], chosen[5]

def find_components_for_c_w(g: List[List[int]], c: int, w: int) -> List[Tuple[int, List[List[int]]]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    comps = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for cc in range(cols):
            if g[r][cc] == c and not visited[r][cc]:
                min_rr = max_rr = r
                min_ccc = max_ccc = cc
                q = collections.deque([(r, cc)])
                visited[r][cc] = True
                while q:
                    cr, ccc = q.popleft()
                    min_rr = min(min_rr, cr)
                    max_rr = max(max_rr, cr)
                    min_ccc = min(min_ccc, ccc)
                    max_ccc = max(max_ccc, ccc)
                    for dr, dc in dirs:
                        nr = cr + dr
                        nc = ccc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == c and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                bound_w = max_ccc - min_ccc + 1
                if bound_w == w:
                    h = max_rr - min_rr + 1
                    small = [[c if g[i][j] == c else 0 for j in range(min_ccc, min_ccc + w)] for i in range(min_rr, max_rr + 1)]
                    min_rr_sub, processed_small = process_small(small, c, w, min_rr)
                    comps.append((min_rr, processed_small))
    comps.sort(key=lambda x: x[0])
    return comps

def process_small(small: List[List[int]], c: int, w: int, original_min_r: int) -> Tuple[int, List[List[int]]]:
    h = len(small)
    if h == 0:
        return original_min_r, small
    full_indices = [k for k in range(h) if all(x == c for x in small[k])]
    if len(full_indices) == 2:
        f1, f2 = full_indices
        if f2 - f1 == 2:
            mid_k = f1 + 1
            mid_row = small[mid_k]
            if len(mid_row) == w and mid_row[0] == c and all(x == 0 for x in mid_row[1:]):
                new_w = 2 * w
                top = [c] * new_w
                mid = [c] + [0] * (new_w - 1)
                bot = [c] * new_w
                new_small = [top, mid, bot]
                min_rr_sub = original_min_r + f1
                return min_rr_sub, new_small
    return original_min_r, small

def is_all_c(row: List[int], c: int) -> bool:
    return all(x == c for x in row)

def stack_components(comps: List[Tuple[int, List[List[int]]]], c: int, w: int) -> List[List[int]]:
    if not comps:
        return []
    out_w = len(comps[0][1][0]) if comps[0][1] else w
    output = []
    for i in range(len(comps)):
        min_r, small = comps[i]
        if i > 0 and output and is_all_c(output[-1], c) and small and is_all_c(small[0], c):
            spacer = [c] + [0] * (out_w - 2) + [c]
            output.append(spacer)
        output.extend(small)
    return output

def compute_start_freq(g: List[List[int]]) -> List[int]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    freq = [0] * (cols - 1)
    for r in range(rows):
        j = 0
        while j < cols - 1:
            if g[r][j] > 0 and g[r][j + 1] == g[r][j]:
                if j == 0 or g[r][j - 1] != g[r][j] or g[r][j - 1] <= 0:
                    freq[j] += 1
                j += 2
                while j < cols - 1 and g[r][j] == g[r][j - 1]:
                    j += 1
                continue
            j += 1
    return freq

def fallback_mixed(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    freq = compute_start_freq(g)
    center_r = max(range(n), key=lambda r: sum(1 for x in g[r] if x > 0))
    row = g[center_r]
    color_count = collections.Counter(x for x in row if x > 0)
    if not color_count:
        return []
    mode_c = max(color_count, key=color_count.get)
    center_starts = []
    cols_m1 = len(row) - 1
    for j in range(cols_m1):
        if row[j] == mode_c == row[j + 1] and freq[j] >= 2 and (j == 0 or row[j - 1] != mode_c or row[j - 1] <= 0):
            center_starts.append(j)
    if len(center_starts) < 3:
        return []
    third_start = center_starts[2]
    last_start = center_starts[-1]
    left_col = third_start
    right_col = last_start + 1
    out_h = n // 2
    if out_h == 0:
        return []
    half = out_h // 2
    bottom_num = out_h - half
    top_pairs = []
    current_r = center_r
    for _ in range(half):
        if current_r < 0:
            top_pairs.append([0, 0])
            continue
        top_pairs.append([g[current_r][left_col], g[current_r][right_col]])
        current_r -= 1
    bottom_pairs = []
    current_r = center_r + 1
    for i in range(bottom_num):
        if current_r >= n:
            bottom_pairs.append([0, 0])
            current_r += 1
            continue
        p_left = g[current_r][right_col]
        p_right = g[current_r][left_col]
        if i == bottom_num - 1 and p_left != p_right:
            p_left = 0
        bottom_pairs.append([p_left, p_right])
        current_r += 1
    return top_pairs + bottom_pairs

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    all_comps = find_all_components(g)
    if not all_comps:
        return fallback_mixed(g)
    chosen_c, chosen_w = select_chosen(all_comps)
    if chosen_c == 0:
        return fallback_mixed(g)
    comps = find_components_for_c_w(g, chosen_c, chosen_w)
    output = stack_components(comps, chosen_c, chosen_w)
    return output
```