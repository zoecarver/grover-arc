```python
from typing import List, Set, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    grid = [row[:] for row in g]
    b = g[0][0]
    directions4: List[Tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    directions8: List[Tuple[int, int]] = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == 0 and dj == 0)]

    def is_valid(x: int, y: int) -> bool:
        return 0 <= x < n and 0 <= y < n

    def get_used_colors(grid: List[List[int]], b: int) -> Set[int]:
        s: Set[int] = set()
        for row in grid:
            for cell in row:
                if cell != b:
                    s.add(cell)
        return s

    used = get_used_colors(grid, b)

    # Rule: Identify and color qualifying 2x2 squares to 3 (green)
    def color_qualifying_squares(grid: List[List[int]], b: int, used: Set[int]) -> List[List[int]]:
        new_grid = [row[:] for row in grid]
        for c in used:
            if c == 0:
                continue
            for i in range(n - 1):
                for j in range(n - 1):
                    if (new_grid[i][j] == c and new_grid[i][j + 1] == c and
                        new_grid[i + 1][j] == c and new_grid[i + 1][j + 1] == c):
                        # Check horizontal adjacent non-b non-c
                        has_adj = False
                        for di in [0, 1]:
                            for dx in [0, 1]:
                                x = i + di
                                y = j + dx
                                # left
                                if is_valid(x, y - 1) and new_grid[x][y - 1] != b and new_grid[x][y - 1] != c:
                                    has_adj = True
                                # right
                                if is_valid(x, y + 1) and new_grid[x][y + 1] != b and new_grid[x][y + 1] != c:
                                    has_adj = True
                        if has_adj:
                            new_grid[i][j] = 3
                            new_grid[i][j + 1] = 3
                            new_grid[i + 1][j] = 3
                            new_grid[i + 1][j + 1] = 3
        return new_grid

    grid = color_qualifying_squares(grid, b, used)

    # Rule: Identify stem color (first color adjacent to 3, including 0)
    stem: int = None
    for d in list(used) + ([0] if 0 not in used else []):
        if d == b or d == 3:
            continue
        attached = False
        for x in range(n):
            for y in range(n):
                if grid[x][y] == 3:
                    for di, dj in directions4:
                        nx = x + di
                        ny = y + dj
                        if is_valid(nx, ny) and grid[nx][ny] == d:
                            attached = True
                            break
                if attached:
                    break
            if attached:
                break
        if attached:
            stem = d
            break

    # Rule: Color stem components if same row as 3 or 8-adjacent to 3
    if stem is not None:
        rows_with_green: Set[int] = set()
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 3:
                    rows_with_green.add(i)
                    break
        visited = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if grid[i][j] == stem and not visited[i][j]:
                    component: List[Tuple[int, int]] = []
                    stack = [(i, j)]
                    visited[i][j] = True
                    has_same_row = i in rows_with_green
                    attached_to_green = False
                    while stack:
                        x, y = stack.pop()
                        component.append((x, y))
                        # Check 8-adjacent to 3
                        for di, dj in directions8:
                            nx = x + di
                            ny = y + dj
                            if is_valid(nx, ny) and grid[nx][ny] == 3:
                                attached_to_green = True
                                break
                        if attached_to_green and has_same_row:
                            break  # optimization
                        for di, dj in directions4:
                            nx = x + di
                            ny = y + dj
                            if is_valid(nx, ny) and grid[nx][ny] == stem and not visited[nx][ny]:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                    if has_same_row or attached_to_green:
                        for x, y in component:
                            grid[x][y] = 5

    # Rule: Color 0 components attached to blue=1 with upward attachment
    if 1 in used:
        blue = 1
        visited = [[False] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 0 and not visited[i][j]:
                    component: List[Tuple[int, int]] = []
                    has_up_blue = False
                    attached_to_blue = False
                    stack = [(i, j)]
                    visited[i][j] = True
                    while stack:
                        x, y = stack.pop()
                        component.append((x, y))
                        # Check up blue
                        if x > 0 and grid[x - 1][y] == blue:
                            has_up_blue = True
                        # Check attached to blue 4-way
                        for di, dj in directions4:
                            nx = x + di
                            ny = y + dj
                            if is_valid(nx, ny) and grid[nx][ny] == blue:
                                attached_to_blue = True
                                break
                        for di, dj in directions4:
                            nx = x + di
                            ny = y + dj
                            if is_valid(nx, ny) and grid[nx][ny] == 0 and not visited[nx][ny]:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                    if attached_to_blue and has_up_blue:
                        for x, y in component:
                            grid[x][y] = 5

    # Rule: Color isolated 0's (size 1, no adjacent non-b) to 5
    visited = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0 and not visited[i][j]:
                component: List[Tuple[int, int]] = []
                adj_non_b = 0
                stack = [(i, j)]
                visited[i][j] = True
                is_size_one = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for di, dj in directions4:
                        nx = x + di
                        ny = y + dj
                        if is_valid(nx, ny):
                            if grid[nx][ny] == 0 and not visited[nx][ny]:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                                is_size_one = False
                            elif grid[nx][ny] != b:
                                adj_non_b += 1
                if is_size_one and adj_non_b == 0:
                    for x, y in component:
                        grid[x][y] = 5

    return grid
```