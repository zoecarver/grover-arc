```python
import typing
List = typing.List
Tuple = typing.Tuple

def determine_background(g: List[List[int]]) -> int:
    """Determine the background color from the top-left border cell."""
    return g[0][0]

def flood_fill(g: List[List[int]], i: int, j: int, visited: List[List[bool]], color: int) -> List[Tuple[int, int]]:
    """Perform flood fill to find connected component of given color using stack (non-recursive)."""
    rows = len(g)
    cols = len(g[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    stack = []
    component = []
    if 0 <= i < rows and 0 <= j < cols and not visited[i][j] and g[i][j] == color:
        stack.append((i, j))
    while stack:
        x, y = stack.pop()
        if visited[x][y]:
            continue
        visited[x][y] = True
        component.append((x, y))
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                stack.append((nx, ny))
    return component

def remove_small_components(g: List[List[int]], background: int, min_size: int = 20) -> List[List[int]]:
    """Remove connected components smaller than min_size by setting them to background."""
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    visited = [[False] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != background:
                color = g[i][j]
                component = flood_fill(g, i, j, visited, color)
                if len(component) < min_size:
                    for x, y in component:
                        new_g[x][y] = background
    return new_g

def is_valid_u(g: List[List[int]], sr: int, left: int, background: int, width: int = 11) -> Tuple[bool, int]:
    """Check if there is a valid U-shape starting at row sr, column left, returning (valid, color)."""
    rows = len(g)
    cols = len(g[0])
    if sr + 4 >= rows or left + width > cols:
        return False, 0
    c = g[sr][left]
    if c == background:
        return False, 0
    # Check top bar
    top_valid = all(g[sr][left + jj] == c for jj in range(width))
    if not top_valid:
        return False, 0
    # Check bottom bar
    bottom_valid = all(g[sr + 4][left + jj] == c for jj in range(width))
    if not bottom_valid:
        return False, 0
    # Check middle rows: sides c, interiors background
    for m in range(1, 4):
        r = sr + m
        if g[r][left] != c or g[r][left + width - 1] != c:
            return False, 0
        for jj in range(1, width - 1):
            if g[r][left + jj] != background:
                return False, 0
    return True, c

def compute_num_fills(c: int, sr: int, left: int) -> int:
    """Compute the number of fills k based on color c, starting row sr, and left column."""
    if c == 1:
        return 2 if left % 2 == 1 else 1
    elif c == 2:
        return 0 if sr == 1 else 1
    else:
        return c // 2

def get_fill_positions(left: int, k: int, width: int = 11) -> List[int]:
    """Compute absolute column positions for k fills in the interior, right-aligned every 2 steps."""
    positions = []
    for i in range(k):
        rel = (width - 1) - 2 * (i + 1)
        j = left + rel
        if 1 <= rel <= width - 2:
            positions.append(j)
    return positions

def detect_and_complete_us(g: List[List[int]], background: int) -> List[List[int]]:
    """Detect valid U-shapes and complete their center rows with color-specific fill patterns."""
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    width = 11
    for sr in range(rows - 4):
        for left in range(cols - width + 1):
            valid, c = is_valid_u(g, sr, left, background, width)
            if valid:
                k = compute_num_fills(c, sr, left)
                fill_js = get_fill_positions(left, k, width)
                center = sr + 2
                for j in fill_js:
                    if 0 <= j < cols and new_g[center][j] == background:
                        new_g[center][j] = c
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: determine background, remove small components, then complete U-shapes."""
    background = determine_background(g)
    cleaned = remove_small_components(g, background)
    completed = detect_and_complete_us(cleaned, background)
    return completed
```