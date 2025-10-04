```python
from typing import List, Dict, Tuple
from collections import deque
import copy

def get_size(grid: List[List[int]]) -> int:
    return len(grid)

def get_legend_mapping(grid: List[List[int]]) -> Dict[int, int]:
    size = get_size(grid)
    if size < 4:
        return {}
    r1 = grid[1]
    r2 = grid[2]
    r3 = grid[3]
    mapping: Dict[int, int] = {}
    col = 0
    while col < size:
        while col < size and r1[col] == 0 and r2[col] == 0 and r3[col] == 0:
            col += 1
        if col >= size:
            break
        start_col = col
        while col < size and not (r1[col] == 0 and r2[col] == 0 and r3[col] == 0):
            col += 1
        end_col = col - 1
        width = end_col - start_col + 1
        if width < 3:
            col = end_col + 1
            continue
        first = -1
        last = -1
        for c in range(start_col, end_col + 1):
            if r2[c] != 0:
                if first == -1:
                    first = c
                last = c
        if first == -1 or first == last:
            col = end_col + 1
            continue
        color = r2[first]
        if color == 5:
            col = end_col + 1
            continue
        num_holes = sum(1 for c in range(first + 1, last) if r2[c] == 0)
        mapping[num_holes] = color
        col = end_col + 1
    return mapping

def compute_holes(grid: List[List[int]], component: List[Tuple[int, int]]) -> int:
    if not component:
        return 0
    size = get_size(grid)
    empty_visited = [[False for _ in range(size)] for _ in range(size)]
    hole_count = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for x, y in component:
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < size and 0 <= ny < size and grid[nx][ny] == 0 and not empty_visited[nx][ny]:
                q = deque([(nx, ny)])
                empty_visited[nx][ny] = True
                reaches_border = False
                while q:
                    a, b = q.popleft()
                    if a == 0 or a == size - 1 or b == 0 or b == size - 1:
                        reaches_border = True
                    for ddx, ddy in directions:
                        na = a + ddx
                        nb = b + ddy
                        if 0 <= na < size and 0 <= nb < size and grid[na][nb] == 0 and not empty_visited[na][nb]:
                            empty_visited[na][nb] = True
                            q.append((na, nb))
                if not reaches_border:
                    hole_count += 1
    return hole_count

def find_and_replace_components(grid: List[List[int]], mapping: Dict[int, int]) -> List[List[int]]:
    size = get_size(grid)
    result = copy.deepcopy(grid)
    visited = [[False for _ in range(size)] for _ in range(size)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for r in range(size):
        for c in range(size):
            if result[r][c] == 5 and not visited[r][c]:
                component = []
                q = deque([(r, c)])
                visited[r][c] = True
                component.append((r, c))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < size and 0 <= ny < size and result[nx][ny] == 5 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            component.append((nx, ny))
                h = compute_holes(result, component)
                color = mapping.get(h, 0)
                for x, y in component:
                    result[x][y] = color
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    mapping = get_legend_mapping(g)
    return find_and_replace_components(g, mapping)
```