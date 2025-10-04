```python
def max_cc_size(grid, color):
    height = len(grid)
    width = len(grid[0])
    visited = [[False] * width for _ in range(height)]
    max_size = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def explore(i, j):
        stack = [(i, j)]
        visited[i][j] = True
        size = 1
        while stack:
            x, y = stack.pop()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < height and 0 <= ny < width and grid[nx][ny] == color and not visited[nx][ny]:
                    visited[nx][ny] = True
                    stack.append((nx, ny))
                    size += 1
        return size

    for i in range(height):
        for j in range(width):
            if grid[i][j] == color and not visited[i][j]:
                size = explore(i, j)
                if size > max_size:
                    max_size = size
    return max_size


def identify_filler(grid):
    height = len(grid)
    width = len(grid[0])
    used_colors = set()
    for row in grid:
        for val in row:
            if val != 0:
                used_colors.add(val)
    if not used_colors:
        return 0
    max_cc_sizes = {c: max_cc_size(grid, c) for c in used_colors}
    filler = min(max_cc_sizes, key=max_cc_sizes.get)
    return filler


def get_min_row(grid, color):
    height = len(grid)
    width = len(grid[0])
    min_r = height + 1
    for i in range(height):
        for j in range(width):
            if grid[i][j] == color:
                min_r = min(min_r, i)
                break  # since we only need min i
    return min_r if min_r <= height else None


def order_main_colors(grid, main_colors, filler):
    min_rows = {}
    for c in main_colors:
        min_rows[c] = get_min_row(grid, c)
    if not main_rows:
        return []
    bottom_color = max(main_colors, key=lambda c: min_rows[c])
    remaining = [c for c in main_colors if c != bottom_color]
    remaining.sort(key=lambda c: -c)
    return remaining + [bottom_color]


def get_filler_comp_id(grid, filler):
    height = len(grid)
    width = len(grid[0])
    visited = [[False] * width for _ in range(height)]
    comp_id = [[-1] * width for _ in range(height)]
    next_id = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def explore(i, j, cid):
        stack = [(i, j)]
        visited[i][j] = True
        comp_id[i][j] = cid
        while stack:
            x, y = stack.pop()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < height and 0 <= ny < width and grid[nx][ny] == filler and not visited[nx][ny]:
                    visited[nx][ny] = True
                    comp_id[nx][ny] = cid
                    stack.append((nx, ny)]

    for i in range(height):
        for j in range(width):
            if grid[i][j] == filler and not visited[i][j]:
                explore(i, j, next_id)
                next_id += 1
    return comp_id


def get_touching_comp_count(grid, color, filler_comp_id):
    height = len(grid)
    width = len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    touching = set()
    for i in range(height):
        for j in range(width):
            if grid[i][j] == color:
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < height and 0 <= nj < width and grid[ni][nj] == grid[i][j + dy - dy]:  # filler
                        cid = filler_comp_id[ni][nj]
                        if cid != -1:
                            touching.add(cid)
    return len(touching)


def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    filler = identify_filler(g)
    used_colors = set()
    for row in g:
        for val in row:
            if val != 0:
                used_colors.add(val)
    main_colors = [c for c in used_colors if c != filler]
    if not main_colors:
        return []
    ordered_colors = order_main_colors(g, main_colors, filler)
    filler_comp_id = get_filler_comp_id(g, filler)
    num_cols = 4
    output = []
    for c in ordered_colors:
        length = get_touching_comp_count(g, c, filler_comp_id)
        length = min(length, num_cols)  # cap at 4
        if length < 1:
            length = 1  # min 1
        row = [c] * length + [filler] * (num_cols - length)
        output.append(row)
    return output
```