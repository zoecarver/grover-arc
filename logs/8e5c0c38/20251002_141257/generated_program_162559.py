```python
from collections import Counter, deque
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [g[r][c] for r in range(len(g)) for c in range(len(g[0]))]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                color = g[r][c]
                component = []
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def compute_holes(g: List[List[int]], color: int, component: List[Tuple[int, int]]) -> int:
    if not component:
        return 0
    rows, cols = len(g), len(g[0])
    fg = set(component)
    outside_visited = set()
    q = deque()
    for r in range(rows):
        for c in [0, cols - 1]:
            pos = (r, c)
            if pos not in fg and pos not in outside_visited:
                q.append(pos)
                outside_visited.add(pos)
    for c in range(cols):
        for r in [0, rows - 1]:
            pos = (r, c)
            if pos not in fg and pos not in outside_visited:
                q.append(pos)
                outside_visited.add(pos)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            pos = (nx, ny)
            if 0 <= nx < rows and 0 <= ny < cols and pos not in fg and pos not in outside_visited:
                outside_visited.add(pos)
                q.append(pos)
    hole_visited = set()
    holes = 0
    for r in range(rows):
        for c in range(cols):
            pos = (r, c)
            if pos not in fg and pos not in outside_visited and pos not in hole_visited:
                q = deque([pos])
                hole_visited.add(pos)
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        npos = (nx, ny)
                        if 0 <= nx < rows and 0 <= ny < cols and npos not in fg and npos not in outside_visited and npos not in hole_visited:
                            hole_visited.add(npos)
                            q.append(npos)
                holes += 1
    return holes

def apply_top_single_removal(g: List[List[int]], components: List[Tuple[int, List[Tuple[int, int]]]], bg: int) -> List[List[int]]:
    new_g = [row[:] for row in g]
    for color, comp in components:
        if len(comp) > 2:
            min_r = min(r for r, _ in comp)
            row_cols = sorted(c for r, c in comp if r == min_r)
            i = 0
            n = len(row_cols)
            while i < n:
                start = i
                while i < n and row_cols[i] == row_cols[start] + (i - start):
                    i += 1
                if i - start == 1:
                    new_g[min_r][row_cols[start]] = bg
    return new_g

def apply_holes1_left_removal(g: List[List[int]], components: List[Tuple[int, List[Tuple[int, int]]]], bg: int) -> List[List[int]]:
    new_g = [row[:] for row in g]
    for color, comp in components:
        if compute_holes(g, color, comp) == 1 and comp:
            min_c = min(c for _, c in comp)
            for r, c in comp:
                if c == min_c:
                    new_g[r][c] = bg
    return new_g

def apply_holes0_left_vertical2_removal(g: List[List[int]], components: List[Tuple[int, List[Tuple[int, int]]]], bg: int) -> List[List[int]]:
    new_g = [row[:] for row in g]
    rows = len(g)
    for color, comp in components:
        if compute_holes(g, color, comp) == 0 and len(comp) > 2 and comp:
            min_c = min(c for _, c in comp)
            r = 0
            while r < rows:
                if g[r][min_c] == color:
                    run_start = r
                    r += 1
                    while r < rows and g[r][min_c] == color:
                        r += 1
                    run_length = r - run_start
                    if run_length == 2:
                        new_g[run_start][min_c] = bg
                        new_g[run_start + 1][min_c] = bg
                else:
                    r += 1
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    components = find_components(g, bg)
    new_g = apply_top_single_removal(g, components, bg)
    new_g = apply_holes1_left_removal(new_g, components, bg)
    new_g = apply_holes0_left_vertical2_removal(new_g, components, bg)
    return new_g
```