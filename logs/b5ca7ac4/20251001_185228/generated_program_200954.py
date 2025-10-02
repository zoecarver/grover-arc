```python
from typing import List, Dict, Tuple
from collections import Counter

def find_background(g: List[List[int]]) -> int:
    n = len(g)
    count = Counter()
    for i in range(n):
        for j in range(n):
            count[g[i][j]] += 1
    return count.most_common(1)[0][0]

def find_components(g: List[List[int]], background: int, n: int) -> List[Dict]:
    visited = [[False] * n for _ in range(n)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] != background and not visited[i][j]:
                component = []
                stack: List[Tuple[int, int]] = [(i, j)]
                visited[i][j] = True
                min_r, max_r = i, i
                min_c, max_c = j, j
                while stack:
                    r, c = stack.pop()
                    component.append((r, c))
                    min_r = min(min_r, r)
                    max_r = max(max_r, r)
                    min_c = min(min_c, c)
                    max_c = max(max_c, c)
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and g[nr][nc] != background:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                boundary = set()
                for r, c in component:
                    is_boundary = False
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if not (0 <= nr < n and 0 <= nc < n) or g[nr][nc] == background:
                            is_boundary = True
                            break
                    if is_boundary:
                        boundary.add((r, c))
                if boundary:
                    bound_count = Counter(g[r][c] for r, c in boundary)
                    frame = bound_count.most_common(1)[0][0]
                else:
                    all_count = Counter(g[r][c] for r, c in component)
                    frame = all_count.most_common(1)[0][0]
                comp_dict = {
                    'component': component,
                    'min_r': min_r,
                    'max_r': max_r,
                    'min_c': min_c,
                    'max_c': max_c,
                    'frame': frame
                }
                components.append(comp_dict)
    return components

def place_eight_components(out: List[List[int]], g: List[List[int]], eight_comps: List[Dict], n: int, bg: int) -> None:
    lanes8 = [0, 5]
    occupied8 = [[] for _ in lanes8]
    global_max_r8 = -1
    current_lane_idx8 = 0
    for comp in eight_comps:
        if comp['min_r'] > global_max_r8 + 1:
            current_lane_idx8 = 0
        candidates = [lanes8[current_lane_idx8], lanes8[1 - current_lane_idx8]]
        placed = False
        for lane in candidates:
            lidx = lanes8.index(lane)
            overlap = any(comp['min_r'] <= pmax and comp['max_r'] >= pmin for pmin, pmax in occupied8[lidx])
            if not overlap:
                dx = lane - comp['min_c']
                for r, c in comp['component']:
                    nc = c + dx
                    if 0 <= nc < n:
                        out[r][nc] = g[r][c]
                occupied8[lidx].append((comp['min_r'], comp['max_r']))
                current_lane_idx8 = lidx
                placed = True
                break
        if not placed:
            lane = lanes8[0]
            lidx = 0
            dx = lane - comp['min_c']
            for r, c in comp['component']:
                nc = c + dx
                if 0 <= nc < n:
                    out[r][nc] = g[r][c]
            occupied8[lidx].append((comp['min_r'], comp['max_r']))
            current_lane_idx8 = 0
        global_max_r8 = max(global_max_r8, comp['max_r'])

def place_two_components(out: List[List[int]], g: List[List[int]], two_comps: List[Dict], n: int) -> None:
    lanes2 = [17, 12]
    occupied2 = [[] for _ in lanes2]
    for comp in two_comps:
        if comp['min_c'] > 8:
            try_lanes = [17, 12]
        else:
            try_lanes = [12, 17]
        placed = False
        for lane in try_lanes:
            lidx = lanes2.index(lane)
            overlap = any(comp['min_r'] <= pmax and comp['max_r'] >= pmin for pmin, pmax in occupied2[lidx])
            if not overlap:
                dx = lane - comp['min_c']
                for r, c in comp['component']:
                    nc = c + dx
                    if 0 <= nc < n:
                        out[r][nc] = g[r][c]
                occupied2[lidx].append((comp['min_r'], comp['max_r']))
                placed = True
                break
        if not placed:
            lane = try_lanes[0]
            lidx = lanes2.index(lane)
            dx = lane - comp['min_c']
            for r, c in comp['component']:
                nc = c + dx
                if 0 <= nc < n:
                    out[r][nc] = g[r][c]
            occupied2[lidx].append((comp['min_r'], comp['max_r']))

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = find_background(g)
    components = find_components(g, bg, n)
    eight_comps = sorted([c for c in components if c['frame'] == 8], key=lambda c: (c['min_r'], c['min_c']))
    two_comps = sorted([c for c in components if c['frame'] == 2], key=lambda c: (c['min_r'], c['min_c']))
    out = [[bg] * n for _ in range(n)]
    place_eight_components(out, g, eight_comps, n, bg)
    place_two_components(out, g, two_comps, n)
    return out
```