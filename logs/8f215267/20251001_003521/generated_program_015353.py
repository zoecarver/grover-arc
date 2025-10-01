```python
import typing
List = typing.List
Tuple = typing.Tuple

def determine_background(g: List[List[int]]) -> int:
    """Determine the background color from the top-left border cell."""
    return g[0][0]

def flood_fill(g: List[List[int]], i: int, j: int, visited: List[List[bool]], color: int) -> List[Tuple[int, int]]:
    """Perform flood fill to find connected component of given color using stack (non-recursive).
    Returns list of (x,y) positions in the component."""
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
    """Remove connected components smaller than min_size by setting them to background.
    Uses flood_fill on unvisited non-background cells; modifies a copy of g."""
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

def detect_u(g: List[List[int]], sr: int, left: int, background: int, width: int = 11) -> Tuple[bool, int]:
    """Detect if there is a U-shaped structure starting at row sr, column left, with given width.
    Returns (valid, color) if valid U, else (False, 0)."""
    rows = len(g)
    cols = len(g[0])
    if sr + 4 >= rows or left + width > cols:
        return False, 0
    c = g[sr][left]
    if c == background:
        return False, 0
    # Check top bar
    if any(g[sr][left + jj] != c for jj in range(width)):
        return False, 0
    # Check bottom bar
    if any(g[sr + 4][left + jj] != c for jj in range(width)):
        return False, 0
    # Check middle rows: sides c, interiors background
    for m in range(1, 4):
        r = sr + m
        if g[r][left] != c or g[r][left + width - 1] != c:
            return False, 0
        if any(g[r][left + jj] != background for jj in range(1, width - 1)):
            return False, 0
    return True, c

def compute_num_fills(c: int, sr: int, left: int) -> int:
    """Compute the number of fills k for a U of color c at starting row sr and left column left."""
    if c == 1:
        return 2 if left % 2 == 1 else 1
    elif c == 2:
        return 0 if sr == 1 else 1
    else:
        return c // 2

def get_fill_positions(left: int, k: int, width: int = 11) -> List[int]:
    """Compute the absolute column positions to fill in the center row for k fills, right-aligned every 2 steps."""
    positions = []
    for i in range(k):
        rel = (width - 1) - 2 * (i + 1)
        j = left + rel
        if 1 <= rel <= width - 2:
            positions.append(j)
    return positions

def detect_and_complete_us(g: List[List[int]], background: int) -> List[List[int]]:
    """Detect U-shaped structures and complete their center rows with color-specific patterns.
    Scans for exact U matches of width 11, computes fills based on c/sr/left, fills positions in center row if background."""
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    width = 11
    for sr in range(rows - 4):
        for left in range(cols - width + 1):
            is_valid, c = detect_u(g, sr, left, background, width)
            if is_valid:
                k = compute_num_fills(c, sr, left)
                fill_js = get_fill_positions(left, k, width)
                center = sr + 2
                for j in fill_js:
                    if 0 <= j < cols and new_g[center][j] == background:
                        new_g[center][j] = c
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: determine background, remove small components, then detect and complete U structures."""
    background = determine_background(g)
    cleaned = remove_small_components(g, background)
    completed = detect_and_complete_us(cleaned, background)
    return completed
```