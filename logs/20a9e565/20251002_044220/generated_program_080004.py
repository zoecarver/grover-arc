```python
from typing import List
from collections import deque, Counter, defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n = len(g)
    if n == 0:
        return []
    m = len(g[0]) if g[0] else 0
    # Find 5's positions
    five_pos = [(r, c) for r in range(n) for c in range(m) if 0 <= c < len(g[r]) and g[r][c] == 5]
    if not five_pos:
        return []
    min_r5 = min(r for r, c in five_pos)
    max_r5 = max(r for r, c in five_pos)
    # Find components
    visited = [[False] * m for _ in range(n)]
    comps: List[tuple] = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(n):
        for cc in range(m):
            if 0 <= cc < len(g[r]) and g[r][cc] > 0 and not visited[r][cc]:
                c_val = g[r][cc]
                q = deque([(r, cc)])
                visited[r][cc] = True
                min_rr, max_rr = r, r
                min_ccc, max_ccc = cc, cc
                while q:
                    rr, ccc = q.popleft()
                    min_rr = min(min_rr, rr)
                    max_rr = max(max_rr, rr)
                    min_ccc = min(min_ccc, ccc)
                    max_ccc = max(max_ccc, ccc)
                    for dr, dc in dirs:
                        nr, nc = rr + dr, ccc + dc
                        if 0 <= nr < n and 0 <= nc < m and 0 <= nc < len(g[nr]) and not visited[nr][nc] and g[nr][nc] == c_val:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                ww = max_ccc - min_ccc + 1
                if ww >= 3:
                    comps.append((c_val, min_rr, max_rr, min_ccc, max_ccc, ww))
    if not comps:
        return fallback_mixed(g)
    # Select chosen
    min_min_cc = min(comp[3] for comp in comps)
    candidates = [comp for comp in comps if comp[3] == min_min_cc]
    chosen_comp = max(candidates, key=lambda x: x[5])
    c, _, _, min_cc, _, w = chosen_comp
    # Find intersecting components with exact w
    intersecting = []
    for comp in comps:
        if comp[0] == c and comp[5] == w:
            c_min_r, c_max_r = comp[1], comp[2]
            if max(c_min_r, min_r5) <= min(c_max_r, max_r5):
                intersecting.append(comp)
    if not intersecting:
        return fallback_mixed(g)
    # Take leftmost intersecting
    intersecting.sort(key=lambda x: x[3])
    sel_comp = intersecting[0]
    c = sel_comp[0]
    min_r = sel_comp[1]
    max_r = sel_comp[2]
    comp_min_cc = sel_comp[3]
    # Extract small
    small = []
    for rr in range(min_r, max_r + 1):
        row = [g[rr][ccc] if 0 <= ccc < len(g[rr]) and g[rr][ccc] == c else 0 for ccc in range(comp_min_cc, comp_min_cc + w)]
        small.append(row)
    # Process for sandwich (bottom-most)
    h_small = len(small)
    merged = False
    new_small = None
    i = h_small - 3
    while i >= 0:
        row_i = small[i]
        row_ip1 = small[i + 1]
        row_ip2 = small[i + 2]
        if (len(row_i) == w and all(x == c for x in row_i) and
            len(row_ip1) == w and row_ip1[0] == c and all(x == 0 for x in row_ip1[1:]) and
            len(row_ip2) == w and all(x == c for x in row_ip2)):
            new_w = 2 * w
            full_row = [c] * new_w
            mid_row = row_ip1 + [0] * w
            new_small = [full_row, mid_row, full_row]
            merged = True
            break
        i -= 1
    if merged:
        return new_small
    # Check for repeating
    has_both_sparse = any(len(row) == w and row[0] == c and row[-1] == c and not all(x == c for x in row) for row in small)
    if h_small > 3 and has_both_sparse:
        h_out = max_r5 - min_r5
        if h_out <= 0:
            h_out = n // 2
        start_full = len(small[0]) == w and all(x == c for x in small[0])
        out = []
        for ii in range(h_out):
            if (ii % 2 == 0) == start_full:
                out.append([c] * w)
            else:
                if w >= 2:
                    out.append([c] + [0] * (w - 2) + [c])
                else:
                    out.append([c])
        return out
    # Otherwise, return small as is
    return small

def fallback_mixed(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0]) if g[0] else 0
    # Center row
    def nz_count(row: List[int]) -> int:
        return sum(1 for x in row if x > 0)
    center_row = max(range(n), key=lambda r: nz_count(g[r]))
    row = g[center_row]
    non_zeros = [x for x in row if x > 0]
    if not non_zeros:
        return []
    cnt = Counter(non_zeros)
    mode_c = cnt.most_common(1)[0][0]
    # Start freq
    start_freq = defaultdict(int)
    for r in range(n):
        j = 0
        while j < m:
            if 0 <= j < len(g[r]) and g[r][j] == mode_c:
                start_j = j
                while j < m and 0 <= j < len(g[r]) and g[r][j] == mode_c:
                    j += 1
                if j - start_j >= 2:
                    start_freq[start_j] += 1
            else:
                j += 1
    frequent_starts = sorted(j for j, f in start_freq.items() if f >= 2)
    if len(frequent_starts) < 3:
        h = n // 2
        return [[mode_c, mode_c] for _ in range(h)]
    p1 = frequent_starts[2]
    p2 = frequent_starts[-1]
    h = n // 2
    out = []
    # Upper including center
    for d in range(center_row + 1):
        r = center_row - d
        l = g[r][p1] if 0 <= p1 < len(g[r]) else 0
        ri = g[r][p2] if 0 <= p2 < len(g[r]) else 0
        out.append([l, ri])
        if len(out) == h:
            return out
    # Lower
    for d in range(1, n - center_row):
        r = center_row + d
        l = g[r][p2] if 0 <= p2 < len(g[r]) else 0
        ri = g[r][p1] if 0 <= p1 < len(g[r]) else 0
        pair = [l, ri]
        if len(out) == h - 1:
            pair[0] = 0
        out.append(pair)
        if len(out) == h:
            return out
    # Pad if needed
    while len(out) < h:
        out.append([0, 0])
    return out[:h]
```