```python
from typing import List
from collections import Counter

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def remove_small_components(g: List[List[int]], bg: int, threshold: int, rows: int, cols: int) -> None:
    if threshold <= 0:
        return
    visited = [[False] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != bg and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                c_comp = g[i][j]
                size = 0
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    size += 1
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx = x + dx
                            ny = y + dy
                            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == c_comp:
                                visited[nx][ny] = True
                                stack.append((nx, ny))
                if size < threshold:
                    for x, y in component:
                        g[x][y] = bg

def fill_bars(result: List[List[int]], g: List[List[int]], bg: int, rows: int, cols: int) -> None:
    # Block for L=1, R=11
    for i in range(rows - 4):
        L = 1
        R = 11
        if R >= cols:
            continue
        c = g[i][L]
        if c == bg:
            continue
        if not all(g[i][j] == c for j in range(L, R + 1)):
            continue
        if not all(g[i + 4][j] == c for j in range(L, R + 1)):
            continue
        thin_ok = True
        for k in range(1, 4):
            rk = i + k
            if g[rk][L] != c or g[rk][R] != c:
                thin_ok = False
                break
            if not all(g[rk][j] == bg for j in range(L + 1, R)):
                thin_ok = False
                break
        if not thin_ok:
            continue
        m = i + 2
        if c != 4:
            result[m][7] = c
            result[m][9] = c
        else:
            has_middle = any(g[m][j] != bg and g[m][j] != c for j in range(R + 1, cols))
            has_other = any(
                any(g[i + kk][j] != bg and g[i + kk][j] != c for j in range(R + 1, cols))
                for kk in (1, 3)
            )
            if has_middle:
                pass
            elif has_other:
                result[m][9] = c
            else:
                result[m][7] = c
                result[m][9] = c

    # Block for L=2, R=12
    for i in range(rows - 4):
        L = 2
        R = 12
        if R >= cols:
            continue
        c = g[i][L]
        if c == bg:
            continue
        if not all(g[i][j] == c for j in range(L, R + 1)):
            continue
        if not all(g[i + 4][j] == c for j in range(L, R + 1)):
            continue
        thin_ok = True
        for k in range(1, 4):
            rk = i + k
            if g[rk][L] != c or g[rk][R] != c:
                thin_ok = False
                break
            if not all(g[rk][j] == bg for j in range(L + 1, R)):
                thin_ok = False
                break
        if not thin_ok:
            continue
        m = i + 2
        if c == 1:
            result[m][L + 8] = c
        elif c == 3:
            result[m][L + 6] = c
            result[m][L + 8] = c
        elif c == 5:
            result[m][L + 4] = c
            result[m][L + 6] = c
            result[m][L + 8] = c

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    bg = find_background(g)
    result = [row[:] for row in g]
    fill_bars(result, g, bg, rows, cols)
    remove_small_components(result, bg, 7, rows, cols)
    return result
```