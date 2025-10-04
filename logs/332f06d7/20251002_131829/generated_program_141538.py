```python
from typing import List, Tuple
import sys

def find_red_component(i: int, j: int, g: List[List[int]], visited: List[List[bool]]) -> List[Tuple[int, int]]:
    n = len(g)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    component = []
    stack = [(i, j)]
    visited[i][j] = True
    while stack:
        x, y = stack.pop()
        component.append((x, y))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 2 and not visited[nx][ny]:
                visited[nx][ny] = True
                stack.append((nx, ny))
    return component

def has_qualifying_blue_run(g: List[List[int]], x: int, y: int, n: int) -> bool:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 1:
            # Horizontal run
            row = g[nx]
            left = ny
            while left > 0 and row[left - 1] == 1:
                left -= 1
            right = ny
            while right < n - 1 and row[right + 1] == 1:
                right += 1
            if right - left + 1 >= 3:
                return True
            # Vertical run
            col = [g[r][ny] for r in range(n)]
            up = nx
            while up > 0 and col[up - 1] == 1:
                up -= 1
            down = nx
            while down < n - 1 and col[down + 1] == 1:
                down += 1
            if down - up + 1 >= 3:
                return True
    return False

def handle_red_bars(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    new_g = [row[:] for row in g]
    visited = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if new_g[i][j] == 2 and not visited[i][j]:
                component = find_red_component(i, j, new_g, visited)
                supported = False
                for x, y in component:
                    if has_qualifying_blue_run(new_g, x, y, n):
                        supported = True
                        break
                if not supported:
                    for x, y in component:
                        new_g[x][y] = 0
    return new_g

def find_enclosed_zeros(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    components = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0 and not visited[i][j]:
                component = []
                touches_boundary = (i == 0 or i == n - 1 or j == 0 or j == n - 1)
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    if x == 0 or x == n - 1 or y == 0 or y == n - 1:
                        touches_boundary = True
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 0 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if not touches_boundary:
                    components.append(component)
    return components

def fill_enclosed_zeros(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    components = find_enclosed_zeros(g)
    for component in components:
        for x, y in component:
            new_g[x][y] = 1
    return new_g

def separation_trim(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    new_g = [row[:] for row in g]
    for i in range(n):
        j = 0
        while j < n:
            if new_g[i][j] != 1:
                j += 1
                continue
            start = j
            while j < n and new_g[i][j] == 1:
                j += 1
            end = j - 1
            run_len = end - start + 1
            separated = False
            if start > 0 and new_g[i][start - 1] == 3 and start - 2 >= 0 and new_g[i][start - 2] == 1:
                separated = True
            if separated and run_len >= 3:
                for k in range(start, end + 1):
                    new_g[i][k] = 0
                for up_rows in range(1, run_len):
                    prev_i = i - up_rows
                    if prev_i < 0:
                        break
                    for k in range(start, end + 1):
                        if new_g[prev_i][k] == 1:
                            new_g[prev_i][k] = 0
    return new_g

def trim_overhang(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    new_g = [row[:] for row in g]
    for i in range(1, n):
        j = 0
        while j < n:
            if new_g[i][j] == 3:
                j += 1
                continue
            start = j
            while j < n and new_g[i][j] != 3:
                j += 1
            end = j - 1
            min_rmost = float('inf')
            for k in range(i):
                rmost = -1
                has_non3 = False
                for c in range(start, end + 1):
                    if g[k][c] != 3:
                        has_non3 = True
                    if g[k][c] == 1:
                        rmost = max(rmost, c)
                if has_non3:
                    if rmost == -1:
                        rmost = start - 1
                    min_rmost = min(min_rmost, rmost)
            if min_rmost == float('inf'):
                allowed_end = start - 1
            else:
                allowed_end = min_rmost + 1
            for c in range(max(start, allowed_end + 1), end + 1):
                if new_g[i][c] == 1:
                    new_g[i][c] = 0
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    new_g = handle_red_bars(g)
    new_g = fill_enclosed_zeros(new_g)
    new_g = separation_trim(new_g)
    new_g = trim_overhang(new_g)
    return new_g
```