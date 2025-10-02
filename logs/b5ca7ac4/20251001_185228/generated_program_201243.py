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

def place_eights(out: List[List[int]], g: List[List[int]], eight_comps: List[Dict], n: int) -> None:
    if not eight_comps:
        return
    lanes8 = [0, 5]
    i = 0
    while i < len(eight_comps):
        block = [eight_comps[i]]
        current_max_r = eight_comps[i]['max_r']
        j = i + 1
        while j < len(eight_comps):
            comp = eight_comps[j]
            if comp['min_r'] > current_max_r + 1:
                break
            block.append(comp)
            current_max_r = max(current_max_r, comp['max_r'])
            j += 1
        lane_idx = 0
        for comp in block:
            lane = lanes8[lane_idx % len(lanes8)]
            dx = lane - comp['min_c']
            place_component(out, g, comp, dx, n)
            lane_idx += 1
        i = j

def place_twos(out: List[List[int]], g: List[List[int]], two_comps: List[Dict], n: int) -> None:
    for comp in two_comps:
        lane = 12 if comp['min_c'] <= 8 else 17
        dx = lane - comp['min_c']
        place_component(out, g, comp, dx, n)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = find_background(g)
    comps = find_components(g, bg, n)
    eight_comps = sort_components([c for c in comps if c['frame'] == 8])
    two_comps = sort_components([c for c in comps if c['frame'] == 2])
    out = [[bg for _ in range(n)] for _ in range(n)]
    place_eights(out, g, eight_comps, n)
    place_twos(out, g, two_comps, n)
    return out
```