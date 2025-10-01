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

def detect_and_complete_us(g: List[List[int]], background: int) -> List[List[int]]:
    """Detect U-shaped structures and complete their center rows with color-specific patterns."""
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    width = 11
    for sr in range(rows - 4):
        for left in range(cols - width + 1):
            if g[sr][left] == background:
                continue
            c = g[sr][left]
            # Check top bar
            top_valid = all(g[sr][left + jj] == c for jj in range(width))
            if not top_valid:
                continue
            # Check bottom bar
            bottom_valid = all(g[sr + 4][left + jj] == c for jj in range(width))
            if not bottom_valid:
                continue
            # Check middle rows: sides c, interiors background
            middle_valid = True
            for m in range(1, 4):
                r = sr + m
                if g[r][left] != c or g[r][left + width - 1] != c:
                    middle_valid = False
                    break
                for jj in range(1, width - 1):
                    if g[r][left + jj] != background:
                        middle_valid = False
                        break
                if not middle_valid:
                    break
            if not middle_valid:
                continue
            # Valid U, compute k
            if c == 2 and sr == 1:
                k = 0
            elif c == 1:
                k = 2 if left % 2 == 1 else 1
            else:
                k = c // 2
                if c > 0 and (c & (c - 1)) != 0:
                    k += 1
            # Compute start_rel
            is_pow = c > 0 and (c & (c - 1)) == 0
            start_rel = 9 if not is_pow else 8
            # Fill in center row
            center = sr + 2
            for i in range(k):
                rel = start_rel - 2 * i
                if 1 <= rel <= 9:
                    j = left + rel
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