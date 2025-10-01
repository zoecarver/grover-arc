```python
import copy

def program(g: List[List[int]]) -> List[List[int]]:
    h = copy.deepcopy(g)
    rows, cols = 30, 30
    visited = [[False] * cols for _ in range(rows)]
    # Get palette: distinct 1-4, ordered by first appearance column (min j where c appears)
    first_col = {}
    for i in range(rows):
        for j in range(cols):
            c = g[i][j]
            if 1 <= c <= 4 and c not in first_col:
                first_col[c] = j
    palette = sorted(first_col, key=first_col.get)  # order by min col
    if not palette:
        return h
    color_index = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 5 and not visited[i][j]:
                c = palette[color_index % len(palette)]
                color_index += 1
                stack = [(i, j)]
                visited[i][j] = True
                h[i][j] = c
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == 5 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            h[nx][ny] = c
                            stack.append((nx, ny))
    # Generalize to >4
    for i in range(rows):
        for j in range(cols):
            if g[i][j] > 4:
                h[i][j] = 0  # temporary, but flood fill above handles 5, for >5 set to 5 first? Wait, to handle >4, we can set all >4 to 5 before the loop
    # To handle >4, we can preprocess
    h = copy.deepcopy(g)
    for i in range(rows):
        for j in range(cols):
            if h[i][j] > 4:
                h[i][j] = 5
    # Then apply the flood fill on the modified h, but since we use g for ==5, but to fix, use h for everything
    # Redo with h
    visited = [[False] * cols for _ in range(rows)]
    color_index = 0
    for i in range(rows):
        for j in range(cols):
            if h[i][j] == 5 and not visited[i][j]:
                c = palette[color_index % len(palette)]
                color_index += 1
                stack = [(i, j)]
                visited[i][j] = True
                h[i][j] = c
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and h[nx][ny] == 5 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            h[nx][ny] = c
                            stack.append((nx, ny))
    return h
```