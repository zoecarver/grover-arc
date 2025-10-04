```python
from typing import List, Tuple
from collections import Counter, deque

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = find_background(g)
    out = [row[:] for row in g]
    colors = get_non_background_colors(g, bg)
    erased = {}
    for color in sorted(colors):
        components = get_connected_components(out, color, bg)
        erased_count = 0
        for comp in components:
            if len(comp) > 3 and not is_bar(comp):
                for r, c in comp:
                    out[r][c] = bg
                erased_count += len(comp)
        if erased_count > 0:
            erased[color] = erased_count
    fixed_comps = get_fixed_components(out, bg)
    fixed_comps.sort(key=lambda comp: min(r for r, c in comp) if comp else n)
    erased_colors = sorted(erased.keys())
    idx = 0
    for i in range(len(fixed_comps) - 1):
        upper = fixed_comps[i]
        lower = fixed_comps[i + 1]
        if not upper or not lower:
            continue
        u_max_r = max(r for r, c in upper)
        l_min_r = min(r for r, c in lower)
        delta_r = l_min_r - u_max_r - 1
        if delta_r <= 0 or idx >= len(erased_colors):
            continue
        color = erased_colors[idx]
        N = erased[color]
        u_center = sum(c for r, c in upper) / len(upper)
        l_center = sum(c for r, c in lower) / len(lower)
        delta_c = l_center - u_center
        direction = 1 if delta_c >= 0 else -1
        num_steps = min(N, delta_r)
        start_col = int(u_center)
        placed = 0
        for j in range(num_steps):
            r = u_max_r + 1 + j
            c = start_col + j * direction
            if 0 <= c < n and out[r][c] == bg:
                out[r][c] = color
                placed += 1
                N -= 1
        idx += 1
        # Extra vertical attach above upper left
        extra_c = int(u_center) - 1
        extra_r = u_max_r
        while N > 0 and extra_r >= 0 and 0 <= extra_c < n and out[extra_r][extra_c] == bg:
            out[extra_r][extra_c] = color
            N -= 1
            extra_r -= 1
    # Remaining erased placed as vertical at bottom in original centroid col
    original_centroids = {}
    for color in erased:
        positions = [(r, c) for r in range(n) for c in range(n) if g[r][c] == color]
        if positions:
            avg_c = sum(c for r, c in positions) / len(positions)
            original_centroids[color] = int(avg_c)
    for color in erased_colors:
        if color in erased:
            N = erased[color]
            c = original_centroids.get(color, 0)
            r = n - 1
            while N > 0 and r >= 0 and 0 <= c < n and out[r][c] == bg:
                out[r][c] = color
                N -= 1
                r -= 1
    return out

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_non_background_colors(g: List[List[int]], bg: int) -> set:
    colors = set()
    for row in g:
        for cell in row:
            if cell != bg:
                colors.add(cell)
    return colors

def is_vertical_bar(positions: List[Tuple[int, int]]) -> bool:
    if not positions:
        return False
    cols = {c for r, c in positions}
    if len(cols) != 1:
        return False
    col = next(iter(cols))
    rows = sorted(r for r, c in positions)
    min_r = rows[0]
    max_r = rows[-1]
    return max_r - min_r + 1 == len(rows) and len(rows) == len(set(rows))

def is_horizontal_bar(positions: List[Tuple[int, int]]) -> bool:
    if not positions:
        return False
    rows = {r for r, c in positions}
    if len(rows) != 1:
        return False
    row = next(iter(rows))
    cols = sorted(c for r, c in positions)
    min_c = cols[0]
    max_c = cols[-1]
    return max_c - min_c + 1 == len(cols) and len(cols) == len(set(cols))

def is_bar(positions: List[Tuple[int, int]]) -> bool:
    return is_vertical_bar(positions) or is_horizontal_bar(positions)

def get_connected_components(g: List[List[int]], color: int, bg: int) -> List[List[Tuple[int, int]]]:
    rows_n = len(g)
    cols_n = len(g[0]) if g else 0
    visited = [[False] * cols_n for _ in range(rows_n)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for i in range(rows_n):
        for j in range(cols_n):
            if g[i][j] == color and not visited[i][j]:
                comp = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    comp.append((x, y))
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows_n and 0 <= ny < cols_n and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                components.append(comp)
    return components

def get_fixed_components(g: List[List[int]], bg: int) -> List[List[Tuple[int, int]]]:
    rows_n = len(g)
    cols_n = len(g[0]) if g else 0
    visited = [[False] * cols_n for _ in range(rows_n)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for i in range(rows_n):
        for j in range(cols_n):
            if g[i][j] != bg and not visited[i][j]:
                comp = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    comp.append((x, y))
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows_n and 0 <= ny < cols_n and not visited[nx][ny] and g[nx][ny] != bg:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                components.append(comp)
    return components
```