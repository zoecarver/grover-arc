```python
from collections import deque
from typing import List

def max_component_size(g: List[List[int]], c: int) -> int:
    if not g or not g[0]:
        return 0
    height = len(g)
    width = len(g[0])
    visited = [[False] * width for _ in range(height)]
    max_s = 0
    for r in range(height):
        for col in range(width):
            if g[r][col] == c and not visited[r][col]:
                q = deque([(r, col)])
                visited[r][col] = True
                size = 1
                while q:
                    rr, cc = q.popleft()
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr = rr + dr
                        nc = cc + dc
                        if 0 <= nr < height and 0 <= nc < width and g[nr][nc] == c and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                            size += 1
                max_s = max(max_s, size)
    return max_s

def find_filler(g: List[List[int]]) -> int:
    present = set()
    height = len(g)
    if height == 0:
        return 0
    width = len(g[0])
    for r in range(height):
        for col in range(width):
            if g[r][col] > 0:
                present.add(g[r][col])
    if not present:
        return 0
    comp_sizes = {c: max_component_size(g, c) for c in present}
    filler = min(comp_sizes, key=comp_sizes.get)
    return filler

def get_main_ordered(main_set: set) -> List[int]:
    ordered = []
    specials = [c for c in main_set if c > 5]
    if specials:
        ordered.append(max(specials))
    if 4 in main_set:
        ordered.append(4)
    if 3 in main_set and 1 not in main_set:
        ordered.append(3)
    if 2 in main_set:
        ordered.append(2)
    if 1 in main_set:
        ordered.append(1)
    if 3 in main_set and 1 in main_set:
        ordered.append(3)
    return ordered

def program(g: List[List[int]]) -> List[List[int]]:
    filler = find_filler(g)
    present = set()
    height = len(g)
    if height == 0:
        return []
    width = len(g[0])
    for r in range(height):
        for col in range(width):
            if g[r][col] > 0:
                present.add(g[r][col])
    main_set = present - {filler}
    main_ordered = get_main_ordered(main_set)
    n = len(main_ordered)
    if n == 0:
        return []
    result = []
    for i in range(n):
        c = main_ordered[i]
        if i == 0:
            k = 1
        elif i == 1:
            k = 2
        elif i < n - 1:
            k = 3
        else:
            k = 4
        row = [c] * k + [filler] * (4 - k)
        result.append(row)
    return result
```