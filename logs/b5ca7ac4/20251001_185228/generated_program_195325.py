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
                current_color = g[i][j]
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
                        if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and g[nr][nc] == current_color:
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

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = find_background(g)
    components = find_components(g, bg, n)
    frame_comps = [c for c in components if c['frame'] in (2, 8)]
    sorted_comps = sort_components(frame_comps)
    out = [[bg] * n for _ in range(n)]
    occupied8 = [[], []]
    lanes8 = [0, 5]
    for comp in sorted_comps:
        if comp['frame'] == 8:
            placed = False
            for lidx, lane in enumerate(lanes8):
                overlaps = any(comp['min_r'] <= pmax and comp['max_r'] >= pmin for pmin, pmax in occupied8[lidx])
                if not overlaps:
                    dx = lane - comp['min_c']
                    for r in range(comp['min_r'], comp['max_r'] + 1):
                        for c in range(comp['min_c'], comp['max_c'] + 1):
                            nc = c + dx
                            if 0 <= nc < n:
                                out[r][nc] = g[r][c]
                    occupied8[lidx].append((comp['min_r'], comp['max_r']))
                    placed = True
                    break
            if not placed:
                lane = lanes8[0]
                dx = lane - comp['min_c']
                for r in range(comp['min_r'], comp['max_r'] + 1):
                    for c in range(comp['min_c'], comp['max_c'] + 1):
                        nc = c + dx
                        if 0 <= nc < n:
                            out[r][nc] = g[r][c]
                occupied8[0].append((comp['min_r'], comp['max_r']))
        else:  # frame == 2
            lane = 12 if comp['min_c'] <= 8 else 17
            dx = lane - comp['min_c']
            for r in range(comp['min_r'], comp['max_r'] + 1):
                for c in range(comp['min_c'], comp['max_c'] + 1):
                    nc = c + dx
                    if 0 <= nc < n:
                        out[r][nc] = g[r][c]
    return out
```