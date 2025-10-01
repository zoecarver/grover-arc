```python
import typing
List = typing.List

def determine_background(g: List[List[int]]) -> int:
    """Determine the background color from the top-left border cell."""
    return g[0][0]

def flood_fill(g: List[List[int]], i: int, j: int, visited: List[List[bool]], color: int) -> List[typing.Tuple[int, int]]:
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

def detect_and_complete_us(g: List[List[int]], background: int) -> List[List[int]]:
    """Detect U-shapes of width 11 or 12 and complete the center row based on color c."""
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    for start_row in range(rows - 4):
        for left in range(cols):
            for width in [11, 12]:
                right = left + width - 1
                if right >= cols:
                    continue
                c = new_g[start_row][left]
                if c == background:
                    continue
                # Check top full bar
                if not all(new_g[start_row][left + k] == c for k in range(width)):
                    continue
                # Check bottom full bar
                if not all(new_g[start_row + 4][left + k] == c for k in range(width)):
                    continue
                # Check middle rows have only sides as c, inner background
                valid = True
                for m in range(1, 4):
                    if new_g[start_row + m][left] != c or new_g[start_row + m][right] != c:
                        valid = False
                        break
                    for k in range(1, width - 1):
                        if new_g[start_row + m][left + k] != background:
                            valid = False
                            break
                    if not valid:
                        break
                if valid:
                    center = start_row + 2
                    if center >= rows:
                        continue
                    num = c // 2
                    if width == 11:
                        for k in range(num):
                            j = left + 8 - 2 * k
                            if 0 <= j < cols:
                                new_g[center][j] = c
                    else:  # width == 12
                        num += 1
                        for k in range(num):
                            j = left + 10 - 2 * k
                            if 0 <= j < cols:
                                new_g[center][j] = c
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: clean small components and complete U-shapes."""
    background = determine_background(g)
    cleaned = remove_small_components(g, background)
    completed = detect_and_complete_us(cleaned, background)
    return completed
```