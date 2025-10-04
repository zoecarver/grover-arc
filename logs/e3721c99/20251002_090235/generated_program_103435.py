```python
from typing import List, Tuple, Dict

def find_connected_components(g: List[List[int]]) -> List[Dict]:
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != 0 and not visited[i][j]:
                c = g[i][j]
                s = []
                stack = [(i, j)]
                visited[i][j] = True
                min_r, max_r = i, i
                min_c, max_c = j, j
                while stack:
                    x, y = stack.pop()
                    s.append((x, y))
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == c:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                height = max_r - min_r + 1
                components.append({
                    'C': c,
                    'S': s,
                    'bbox': (min_r, max_r, min_c, max_c),
                    'height': height,
                    'size': len(s)
                })
    return components

def compute_hole_count(g: List[List[int]], s: List[Tuple[int, int]]) -> int:
    if not s:
        return 0
    s_set = set(s)
    rows = len(g)
    cols = len(g[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    h = 0
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 0:
                n = 0
                for dx, dy in directions:
                    ni = i + dx
                    nj = j + dy
                    if 0 <= ni < rows and 0 <= nj < cols and (ni, nj) in s_set:
                        n += 1
                if n == 4:
                    h += 1
    return h

def get_example_mapping(g: List[List[int]]) -> Dict[int, int]:
    comps = find_connected_components(g)
    mapping: Dict[int, int] = {}
    for comp in comps:
        if comp['C'] == 5 or comp['height'] != 3:
            continue
        h = compute_hole_count(g, comp['S'])
        mapping[h] = comp['C']
    return mapping

def apply_color_transformation(out: List[List[int]], g: List[List[int]], comp: Dict, mapping: Dict[int, int]):
    h = compute_hole_count(g, comp['S'])
    if h in mapping:
        target = mapping[h]
        for i, j in comp['S']:
            out[i][j] = target
    else:
        for i, j in comp['S']:
            out[i][j] = 0

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    comps = find_connected_components(g)
    mapping = get_example_mapping(g)
    for comp in comps:
        if comp['C'] == 5:
            apply_color_transformation(out, g, comp, mapping)
    return out
```