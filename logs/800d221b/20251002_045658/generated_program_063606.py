```python
from typing import List, Tuple, Dict, Set
import collections

def get_components(g: List[List[int]], n: int, dirs: List[Tuple[int, int]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    visited = [[False] * n for _ in range(n)]
    components = []
    for i in range(n):
        for j in range(n):
            if not visited[i][j] and g[i][j] != 0:
                color = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    four_dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    eight_dir = four_dir + [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    components = get_components(g, n, four_dir)
    small_list = [(color, comp, len(comp)) for color, comp in components if len(comp) <= 3]
    large_list = [(color, comp, len(comp)) for color, comp in components if color != 0 and len(comp) > 3]
    pixel_to_size: Dict[Tuple[int, int], int] = {}
    for _, comp, size in small_list:
        for pos in comp:
            pixel_to_size[pos] = size
    for large_color, large_cells, _ in large_list:
        touch: Dict[Tuple[int, int], int] = {}
        for x, y in large_cells:
            s_size: Dict[int, int] = {}
            for dx, dy in eight_dir:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and g[nx][ny] != 0 and g[nx][ny] != large_color:
                    s_c = g[nx][ny]
                    sz = pixel_to_size.get((nx, ny), 0)
                    if sz > 0:
                        s_size[s_c] = max(s_size.get(s_c, 0), sz)
            if s_size:
                max_sz = max(s_size.values())
                candidates = [sc for sc, sz in s_size.items() if sz == max_sz]
                chosen = max(candidates)
                touch[(x, y)] = chosen
        if not touch:
            continue
        min_dist: Dict[Tuple[int, int], int] = {}
        color_sets: Dict[Tuple[int, int], Set[int]] = {}
        queue = collections.deque()
        for (x, y), c in touch.items():
            min_dist[(x, y)] = 0
            color_sets[(x, y)] = {c}
            queue.append((x, y, c, 0))
        while queue:
            x, y, c, d = queue.popleft()
            for dx, dy in four_dir:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == large_color:
                    new_d = d + 1
                    key = (nx, ny)
                    if key not in min_dist:
                        min_dist[key] = new_d
                        color_sets[key] = {c}
                        queue.append((nx, ny, c, new_d))
                    elif new_d == min_dist[key]:
                        color_sets[key].add(c)
                    # No update if new_d > min_dist[key], as BFS ensures minimal
        for (x, y), s in color_sets.items():
            if len(s) == 1:
                out[x][y] = next(iter(s))
    return out
```