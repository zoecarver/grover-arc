```python
from typing import List, Tuple
import collections

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    h = len(g)
    w = len(g[0])
    count = collections.Counter()
    for i in range(h):
        for j in range(w):
            count[g[i][j]] += 1
    return count.most_common(1)[0][0]

def find_components(g: List[List[int]], background: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != background and not visited[i][j]:
                color = g[i][j]
                pos = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    pos.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, pos))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    background = find_background(g)
    components = find_components(g, background)
    n = len(components)
    if n == 0:
        return [[background] * w for _ in range(h)]
    # Compute info for each component
    info = []
    for idx, (color, pos) in enumerate(components):
        if not pos:
            continue
        min_r = min(r for r, c in pos)
        max_r = max(r for r, c in pos)
        size = len(pos)
        rel = [(r - min_r, c) for r, c in pos]
        info.append((min_r, max_r, size, color, rel))
    total_non0 = sum(s for _, _, s, _, _ in info)
    half = total_non0 / 2.0
    # Union-Find for row overlap graph
    parent = list(range(n))
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(x, y):
        px = find(x)
        py = find(y)
        if px != py:
            parent[px] = py
    for i in range(n):
        for j in range(i + 1, n):
            min_ri, max_ri = info[i][0], info[i][1]
            min_rj, max_rj = info[j][0], info[j][1]
            if max(min_ri, min_rj) <= min(max_ri, max_rj):
                union(i, j)
    # Find groups
    groups = collections.defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)
    # Decide groups
    top_rels = []
    bottom_rels = []
    for group_list in groups.values():
        if not group_list:
            continue
        group_size = sum(info[i][2] for i in group_list)
        if group_size > half:
            # All to bottom
            for i in group_list:
                _, _, _, color, rel = info[i]
                bottom_rels.append((color, rel))
        else:
            if len(group_list) == 1:
                i = group_list[0]
                _, _, _, color, rel = info[i]
                top_rels.append((color, rel))
            else:
                # Split: max size to top, others to bottom
                max_s = max(info[i][2] for i in group_list)
                top_i = [i for i in group_list if info[i][2] == max_s]
                bottom_i = [i for i in group_list if info[i][2] < max_s]
                for i in top_i:
                    _, _, _, color, rel = info[i]
                    top_rels.append((color, rel))
                for i in bottom_i:
                    _, _, _, color, rel = info[i]
                    bottom_rels.append((color, rel))
    # Create new grid
    new_g = [[background] * w for _ in range(h)]
    # Place top
    for color, rel in top_rels:
        for dr, c in rel:
            r = dr
            if 0 <= r < h and 0 <= c < w:
                new_g[r][c] = max(new_g[r][c], color)
    # Place bottom
    for color, rel in bottom_rels:
        if not rel:
            continue
        max_dr = max(dr for dr, _ in rel)
        for dr, c in rel:
            r = dr - max_dr + (h - 1)
            if 0 <= r < h and 0 <= c < w:
                new_g[r][c] = max(new_g[r][c], color)
    return new_g
```