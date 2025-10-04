```python
from typing import List, Tuple, Dict

def touches_border(i: int, j: int, n: int) -> bool:
    return i == 0 or i == n - 1 or j == 0 or j == n - 1

def handle_red_components(g: List[List[int]], n: int) -> List[List[int]]:
    new_g = [row[:] for row in g]
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 2 and not visited[i][j]:
                component = []
                touches_top = False
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    if x == 0:
                        touches_top = True
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == 2:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(component) == 1 or touches_top:
                    for x, y in component:
                        new_g[x][y] = 0
    return new_g

def label_blue_components(g: List[List[int]], n: int) -> Tuple[List[List[int]], Dict[int, Tuple[int, int, int, int]]]:
    label_grid = [[0] * n for _ in range(n)]
    visited = [[False] * n for _ in range(n)]
    bboxes: Dict[int, Tuple[int, int, int, int]] = {}
    label = 1
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 1 and not visited[i][j]:
                min_r = max_r = i
                min_c = max_c = j
                stack = [(i, j)]
                visited[i][j] = True
                label_grid[i][j] = label
                while stack:
                    x, y = stack.pop()
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == 1:
                            visited[nx][ny] = True
                            label_grid[nx][ny] = label
                            stack.append((nx, ny))
                bboxes[label] = (min_r, max_r, min_c, max_c)
                label += 1
    return label_grid, bboxes

def find_internal_holes(g: List[List[int]], label_grid: List[List[int]], n: int) -> List[Tuple[List[Tuple[int, int]], int]]:
    visited = [[False] * n for _ in range(n)]
    holes = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0 and not visited[i][j]:
                component = []
                touches_b = touches_border(i, j, n)
                adj_labels = set()
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    if touches_border(x, y, n):
                        touches_b = True
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                            if g[nx][ny] == 0:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                            elif g[nx][ny] == 1 and label_grid[nx][ny] > 0:
                                adj_labels.add(label_grid[nx][ny])
                if not touches_b and len(adj_labels) == 1:
                    blue_id = next(iter(adj_labels))
                    holes.append((component, blue_id))
    return holes

def get_preserved_red_bbox(g: List[List[int]], n: int) -> Tuple[int, int, int, int]:
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 2 and not visited[i][j]:
                min_r = max_r = i
                min_c = max_c = j
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == 2:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                return (min_r, max_r, min_c, max_c)
    return (-1, -1, -1, -1)

def carve_hole(new_g: List[List[int]], blue_max_r: int, blue_max_c: int, h: int, w: int, n: int) -> None:
    start_r = blue_max_r - h + 1
    if start_r < 0:
        return
    for start_c in range(blue_max_c - w + 1, -1, -1):
        all_one = True
        for rr in range(start_r, start_r + h):
            if rr >= n:
                all_one = False
                break
            for cc in range(start_c, start_c + w):
                if cc >= n or new_g[rr][cc] != 1:
                    all_one = False
                    break
            if not all_one:
                break
        if all_one:
            for rr in range(start_r, start_r + h):
                for cc in range(start_c, start_c + w):
                    new_g[rr][cc] = 0
            return

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    n = len(g)
    new_g = handle_red_components(g, n)
    label_grid, bboxes = label_blue_components(new_g, n)
    holes = find_internal_holes(new_g, label_grid, n)
    red_bbox = get_preserved_red_bbox(new_g, n)
    if red_bbox[0] != -1 and len(holes) > 0:
        min_r, max_r, min_c, max_c = red_bbox
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        component, blue_id = holes[0]
        if blue_id in bboxes:
            _, b_max_r, _, b_max_c = bboxes[blue_id]
            carve_hole(new_g, b_max_r, b_max_c, h, w, n)
    for component, _ in holes:
        for x, y in component:
            new_g[x][y] = 1
    return new_g
```