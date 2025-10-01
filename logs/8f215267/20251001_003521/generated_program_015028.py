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

def detect_u(g: List[List[int]], sr: int, left: int, background: int, width: int = 11) -> bool:
    """Detect if there is a U-shaped structure starting at row sr, column left, with given width."""
    rows = len(g)
    cols = len(g[0])
    if sr + 4 >= rows or left + width > cols:
        return False
    c = g[sr][left]
    if c == background:
        return False
    # Check top bar
    if any(g[sr][left + j] != c for j in range(width)):
        return False
    # Check bottom bar
    if any(g[sr + 4][left + j] != c for j in range(width)):
        return False
    # Check middle rows: sides c, interiors background
    for m in range(1, 4):
        r = sr + m
        if g[r][left] != c or g[r][left + width - 1] != c:
            return False
        if any(g[r][left + j] != background for j in range(1, width - 1)):
            return False
    return True

def get_fill_positions(c: int, left: int, sr: int, width: int = 11) -> List[int]:
    """Compute the absolute column positions to fill in the center row based on color c, position sr, left."""
    if c == 1:
        k = 2 if left % 2 == 1 else 1
    elif c == 2:
        k = 0 if sr == 1 else 1
    else:
        k = c // 2
    positions = []
    for i in range(k):
        rel = 8 - 2 * i
        j = left + rel
        if 1 <= rel <= width - 2:
            positions.append(j)
    return positions

def detect_and_complete_us(g: List[List[int]], background: int) -> List[List[int]]:
    """Detect U-shaped structures and complete their center rows with color-specific patterns.
    Scans for exact U matches, computes fill positions based on c/sr/left, fills k right-skipped positions in center row if background."""
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    width = 11
    for sr in range(rows - 4):
        for left in range(cols - width + 1):
            if detect_u(g, sr, left, background, width):
                c = g[sr][left]
                fills = get_fill_positions(c, left, sr, width)
                center = sr + 2
                for j in fills:
                    if 0 <= j < cols and new_g[center][j] == background:
                        new_g[center][j] = c
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: clean small components, then detect and complete U structures."""
    background = determine_background(g)
    cleaned = remove_small_components(g, background)
    completed = detect_and_complete_us(cleaned, background)
    return completed
```