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

def place_eight_shape(out: List[List[int]], g: List[List[int]], comp: Dict, occupied: List[List[Tuple[int, int]]], current_lane: int, global_max_r: int, n: int, lanes8: List[int]) -> Tuple[int, int]:
    if comp['min_r'] > global_max_r + 1:
        current_lane = lanes8[0]
    other_lane = lanes8[1] if current_lane == lanes8[0] else lanes8[0]
    candidates = [current_lane, other_lane]
    placed = False
    placed_lane = None
    for lane in candidates:
        lidx = lanes8.index(lane)
        overlaps = any(not (comp['max_r'] < pmin or comp['min_r'] > pmax) for pmin, pmax in occupied[lidx])
        if not overlaps:
            dx = lane - comp['min_c']
            for r, c in comp['component']:
                nc = c + dx
                if 0 <= nc < n:
                    out[r][nc] = g[r][c]
            occupied[lidx].append((comp['min_r'], comp['max_r']))
            placed = True
            placed_lane = lane
            break
    if not placed:
        lane = lanes8[0]
        lidx = 0
        dx = lane - comp['min_c']
        for r, c in comp['component']:
            nc = c + dx
            if 0 <= nc < n:
                out[r][nc] = g[r][c]
        occupied[lidx].append((comp['min_r'], comp['max_r']))
        placed_lane = lane
    global_max_r = max(global_max_r, comp['max_r'])
    current_lane = placed_lane
    return current_lane, global_max_r

def place_two_shape(out: List[List[int]], g: List[List[int]], comp: Dict, n: int) -> None:
    lane = 12 if comp['min_c'] <= 8 else 17
    dx = lane - comp['min_c']
    for r, c in comp['component']:
        nc = c + dx
        if 0 <= nc < n:
            out[r][nc] = g[r][c]

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = find_background(g)
    out = [[bg] * n for _ in range(n)]
    components = find_components(g, bg, n)
    sorted_components = sort_components(components)
    lanes8 = [0, 5]
    occupied8 = [[] for _ in lanes8]
    current_lane8 = lanes8[0]
    global_max_r8 = -1
    for comp in sorted_components:
        frame = comp['frame']
        if frame == 8:
            current_lane8, global_max_r8 = place_eight_shape(out, g, comp, occupied8, current_lane8, global_max_r8, n, lanes8)
        elif frame == 2:
            place_two_shape(out, g, comp, n)
    return out
```