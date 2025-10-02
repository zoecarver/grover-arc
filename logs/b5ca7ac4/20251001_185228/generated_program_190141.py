```python
from typing import List, Tuple, Dict, Set
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
                colors: Set[int] = set([g[i][j]])
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
                            colors.add(g[nr][nc])
                # Find boundary cells
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
                # Frame color: most common in boundary
                if boundary:
                    bound_count = Counter(g[r][c] for r, c in boundary)
                    frame = bound_count.most_common(1)[0][0]
                else:
                    frame = max(colors, key=colors.count)
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

def place_eight_shapes(g: List[List[int]], eight_shapes: List[Dict], background: int, n: int, output: List[List[int]]) -> List[Tuple[int, int, int]]:
    placed = []
    lanes = [0, 5]
    for s in eight_shapes:
        overlaps = any(max(s['min_r'], p[0]) <= min(s['max_r'], p[1]) for p in placed)
        lane = 5 if overlaps else 0
        dx = lane - s['min_c']
        for r, c in s['component']:
            nc = c + dx
            if 0 <= nc < n:
                output[r][nc] = g[r][c]
        placed.append((s['min_r'], s['max_r'], lane))
    return placed

def place_two_shapes(g: List[List[int]], two_shapes: List[Dict], background: int, n: int, output: List[List[int]]):
    lanes = [17, 12]
    lane_idx = 0
    for s in two_shapes:
        candidate_mod = lane_idx % len(lanes)
        candidate_lane = lanes[candidate_mod]
        dx = candidate_lane - s['min_c']
        fits = (s['max_c'] + dx <= n - 1) and (s['min_c'] + dx >= 0)
        if not fits:
            other_mod = 1 - candidate_mod
            other_lane = lanes[other_mod]
            other_dx = other_lane - s['min_c']
            if (s['max_c'] + other_dx <= n - 1) and (s['min_c'] + other_dx >= 0):
                dx = other_dx
            # else: keep candidate, may clip
        for r, c in s['component']:
            nc = c + dx
            if 0 <= nc < n:
                output[r][nc] = g[r][c]
        lane_idx += 1

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = find_background(g)
    all_components = find_components(g, background, n)
    sorted_comps = sort_components(all_components)
    eight_shapes = [s for s in sorted_comps if s['frame'] == 8]
    two_shapes = [s for s in sorted_comps if s['frame'] == 2]
    output = [[background] * n for _ in range(n)]
    place_eight_shapes(g, eight_shapes, background, n, output)
    place_two_shapes(g, two_shapes, background, n, output)
    return output
```