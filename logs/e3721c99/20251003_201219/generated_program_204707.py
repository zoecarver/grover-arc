```python
from typing import List, Tuple, Optional
from collections import deque

def find_separator(g: List[List[int]]) -> Tuple[Optional[str], Optional[int]]:
    n = len(g)
    for i in range(n):
        if all(g[i][j] == 1 for j in range(n)):
            return 'h', i
    for j in range(n):
        if all(g[i][j] == 1 for i in range(n)):
            return 'v', j
    return None, -1

def get_num_fives_in_side(g: List[List[int]], n: int, is_side: callable) -> int:
    return sum(1 for i in range(n) for j in range(n) if is_side(i, j) and g[i][j] == 5)

def get_legend_picture_areas(g: List[List[int]], type_sep: str, sep_idx: int, n: int) -> Tuple[callable, callable]:
    if type_sep == 'h':
        def is_legend(r: int, c: int) -> bool:
            return 0 <= r < sep_idx and 0 <= c < n
        def is_picture(r: int, c: int) -> bool:
            return sep_idx < r < n and 0 <= c < n
        return is_legend, is_picture
    else:  # 'v'
        def is_left(r: int, c: int) -> bool:
            return 0 <= r < n and 0 <= c < sep_idx
        def is_right(r: int, c: int) -> bool:
            return 0 <= r < n and sep_idx < c < n
        num_left = get_num_fives_in_side(g, n, is_left)
        num_right = get_num_fives_in_side(g, n, is_right)
        if num_right == 0:
            return is_right, is_left
        else:
            return is_left, is_right

def find_components_in_area(g: List[List[int]], is_area: callable, n: int, target_val: Optional[int] = None) -> List[Tuple[int, List[Tuple[int, int]]]]:
    visited = [[False] * n for _ in range(n)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if is_area(i, j) and not visited[i][j]:
                val = g[i][j]
                if target_val is not None:
                    if val != target_val:
                        continue
                else:
                    if val == 0 or val == 5 or val == 1:
                        continue
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and is_area(nx, ny) and not visited[nx][ny] and g[nx][ny] == val:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(comp) >= 5:
                    components.append((val, comp))
    return components

def compute_holes(g: List[List[int]], comp: List[Tuple[int, int]], n: int) -> int:
    if not comp:
        return 0
    min_r = min(r for r, c in comp)
    max_r = max(r for r, c in comp)
    min_c = min(c for r, c in comp)
    max_c = max(c for r, c in comp)
    if min_r == max_r or min_c == max_c:
        return 0
    visited = [[False] * n for _ in range(n)]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    q = deque()
    for r in [min_r, max_r]:
        for c in range(min_c, max_c + 1):
            if g[r][c] == 0 and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    for c in [min_c, max_c]:
        for r in range(min_r + 1, max_r):
            if g[r][c] == 0 and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if min_r <= nr <= max_r and min_c <= nc <= max_c and g[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                q.append((nr, nc))
    h = 0
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if g[r][c] == 0 and not visited[r][c]:
                h += 1
                q2 = deque([(r, c)])
                visited[r][c] = True
                while q2:
                    rr, cc = q2.popleft()
                    for dr, dc in dirs:
                        nr2, nc2 = rr + dr, cc + dc
                        if min_r <= nr2 <= max_r and min_c <= nc2 <= max_c and g[nr2][nc2] == 0 and not visited[nr2][nc2]:
                            visited[nr2][nc2] = True
                            q2.append((nr2, nc2))
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    type_sep, sep_idx = find_separator(g)
    if type_sep is None:
        return [row[:] for row in g]
    is_legend, is_picture = get_legend_picture_areas(g, type_sep, sep_idx, n)
    mapping = {}
    legend_comps = find_components_in_area(g, is_legend, n)
    for color, comp in legend_comps:
        h = compute_holes(g, comp, n)
        mapping[h] = color
    output = [row[:] for row in g]
    picture_comps = find_components_in_area(g, is_picture, n, target_val=5)
    for _, comp in picture_comps:
        h = compute_holes(g, comp, n)
        fill_color = mapping.get(h, 5)
        for r, c in comp:
            output[r][c] = fill_color
    return output
```