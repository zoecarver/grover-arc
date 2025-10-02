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

def sort_components(components: List[Dict]) -> List[Dict]:
    return sorted(components, key=lambda s: (s['min_r'], s['min_c']))

def place_component(out: List[List[int]], g: List[List[int]], comp: Dict, dx: int, n: int) -> None:
    for r, c in comp['component']:
        nc = c + dx
        if 0 <= nc < n:
            out[r][nc] = g[r][c]

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = find_background(g)
    comps = find_components(g, bg, n)
    relevant = [c for c in comps if c['frame'] in (2, 8)]
    sorted_comps = sort_components(relevant)
    out = [[bg] * n for _ in range(n)]
    lanes8 = [0, 5]
    global_max_r8 = -1
    current_lane_idx8 = 0
    lanes2 = [12, 17]
    for comp in sorted_comps:
        minr = comp['min_r']
        maxr = comp['max_r']
        minc = comp['min_c']
        frame = comp['frame']
        if frame == 8:
            if minr > global_max_r8 + 1:
                current_lane_idx8 = 0
            lane_idx = current_lane_idx8
            lane = lanes8[lane_idx]
            dx = lane - minc
            place_component(out, g, comp, dx, n)
            global_max_r8 = max(global_max_r8, maxr)
            current_lane_idx8 = 1 - lane_idx
        else:  # frame == 2
            lane = lanes2[0] if minc <= 8 else lanes2[1]
            dx = lane - minc
            place_component(out, g, comp, dx, n)
    return out
```