```python
import collections

def find_max_run(g):
    if not g or not g[0]:
        return 0
    rows = len(g)
    cols = len(g[0])
    max_w = 0
    for r in range(rows):
        curr_len = 1
        for c in range(1, cols):
            if g[r][c] == g[r][c - 1] and g[r][c] > 0:
                curr_len += 1
                max_w = max(max_w, curr_len)
            else:
                curr_len = 1
    return max_w

def find_chosen_c(g, w):
    if w < 3:
        return 0, 0
    rows = len(g)
    cols = len(g[0])
    min_start_j = cols
    chosen_c = 0
    for r in range(rows):
        for j in range(cols - w + 1):
            cj = g[r][j]
            if cj > 0 and all(g[r][j + k] == cj for k in range(1, w)):
                if j < min_start_j:
                    min_start_j = j
                    chosen_c = cj
    return chosen_c, min_start_j

def is_all_c(row, c):
    return all(x == c for x in row)

def process_small(small, c, w, min_rr, max_rr):
    h_small = len(small)
    has_only_left = any(small[rr][0] == c and all(x == 0 for x in small[rr][1:]) for rr in range(h_small))
    has_only_right = any(small[rr][-1] == c and all(x == 0 for x in small[rr][:-1]) for rr in range(h_small))
    if has_only_left and not has_only_right:
        full_rel = [rr for rr in range(h_small) if is_all_c(small[rr], c)]
        if len(full_rel) == 2 and full_rel[1] - full_rel[0] == 2:
            f1 = full_rel[0]
            f2 = full_rel[1]
            sub = small[f1:f2 + 1]
            mir_sub = []
            for roww in sub:
                mir = roww[::-1]
                new_row = roww + mir
                mir_sub.append(new_row)
            return min_rr + f1, mir_sub  # adjust min_rr to the sub start
    return min_rr, small

def find_components(g, c, w):
    if c == 0:
        return []
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for cc in range(cols):
            if g[r][cc] == c and not visited[r][cc]:
                min_rr = max_rr = r
                min_ccc = max_ccc = cc
                q = collections.deque([(r, cc)])
                visited[r][cc] = True
                while q:
                    rr, ccc = q.popleft()
                    min_rr = min(min_rr, rr)
                    max_rr = max(max_rr, rr)
                    min_ccc = min(min_ccc, ccc)
                    max_ccc = max(max_ccc, ccc)
                    for dr, dc in dirs:
                        nr, nc = rr + dr, ccc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == c and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                bound_w = max_ccc - min_ccc + 1
                if bound_w == w:
                    small = [[g[rr][min_ccc + k] if g[rr][min_ccc + k] == c else 0 for k in range(w)] for rr in range(min_rr, max_rr + 1)]
                    min_rr_sub, small = process_small(small, c, w, min_rr, max_rr)
                    components.append((min_rr_sub, small))
    return components

def stack_components(components, c):
    if not components:
        return []
    components.sort(key=lambda x: x[0])
    total = []
    for i, (_, small) in enumerate(components):
        if i > 0 and is_all_c(total[-1], c) and is_all_c(small[0], c):
            ww = len(total[-1])
            if ww >= 2:
                sparse = [c] + [0] * (ww - 2) + [c]
            else:
                sparse = [c] * ww
            total.append(sparse)
        total.extend(small)
    return total

def mixed_rule(g):
    rows = len(g)
    cols = len(g[0])
    # find center
    max_sum = -1
    center = 0
    for r in range(rows):
        s = sum(1 for x in g[r] if x > 0)
        if s > max_sum:
            max_sum = s
            center = r
    half = 7
    # find bar starts freq
    start_freq = collections.defaultdict(int)
    for r in range(rows):
        j = 0
        while j < cols - 1:
            if g[r][j] > 0 and g[r][j] == g[r][j + 1]:
                start_jj = j
                run_len = 1
                j += 1
                while j < cols - 1 and g[r][j + 1] == g[r][j]:
                    j += 1
                    run_len += 1
                j += 1
                if run_len == 2:
                    start_freq[start_jj] += 1
            else:
                j += 1
    bar_starts = [jj for jj, freq in start_freq.items() if freq >= 2]
    bar_starts.sort()
    if len(bar_starts) < 3:
        return []
    left_sample = bar_starts[2] + 1
    right_sample = bar_starts[-1]
    # top
    top_list = []
    for ii in range(half):
        rr = center - ii
        if 0 <= rr < rows:
            p0 = g[rr][left_sample] if 0 <= left_sample < cols else 0
            p1 = g[rr][right_sample] if 0 <= right_sample < cols else 0
            pair = [p0, p1]
            if p0 != p1 and p0 > 0 and p1 > 0:
                pair.reverse()
            top_list.append(pair)
        else:
            top_list.append([0, 0])
    # bottom
    bottom_list = []
    for ii in range(half):
        rr = center + 1 + ii
        if 0 <= rr < rows:
            p0 = g[rr][left_sample] if 0 <= left_sample < cols else 0
            p1 = g[rr][right_sample] if 0 <= right_sample < cols else 0
            pair = [p0, p1]
            bottom_list.append(pair)
        else:
            bottom_list.append([0, 0])
    return top_list + bottom_list

def program(g: List[List[int]]) -> List[List[int]]:
    max_w = find_max_run(g)
    if max_w < 3:
        return mixed_rule(g)
    c, _ = find_chosen_c(g, max_w)
    components = find_components(g, c, max_w)
    total_rows = stack_components(components, c)
    return total_rows
```