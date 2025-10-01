```python
import typing

List = typing.List

def determine_background(g: List[List[int]]) -> int:
    """Determine the background color from the top-left border cell."""
    return g[0][0]

def is_power_of_two(n: int) -> bool:
    """Check if n is a power of two."""
    return n > 0 and (n & (n - 1)) == 0

def flood_fill(g: List[List[int]], i: int, j: int, visited: List[List[bool]], color: int) -> List[typing.Tuple[int, int]]:
    """Perform flood fill to find connected component of given color using stack (non-recursive)."""
    rows = len(g)
    cols = len(g[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    stack = []
    if 0 <= i < rows and 0 <= j < cols and not visited[i][j] and g[i][j] == color:
        stack.append((i, j))
    component = []
    while stack:
        x, y = stack.pop()
        if visited[x][y]:
            continue
        visited[x][y] = True
        component.append((x, y))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
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

def find_and_complete_us(g: List[List[int]], background: int, new_g: List[List[int]]):
    """Detect U-shaped structures and complete the middle bar if color is power of two."""
    rows = len(g)
    cols = len(g[0])
    for start_row in range(1, rows - 4):
        for left in range(1, cols - 10):
            # Check top row full of same color
            c = g[start_row][left]
            if c == background:
                continue
            full_top = all(g[start_row][j] == c for j in range(left, left + 11))
            if not full_top:
                continue
            # Check bottom row full
            full_bottom = all(g[start_row + 4][j] == c for j in range(left, left + 11))
            if not full_bottom:
                continue
            # Check middle rows have only sides
            is_u = True
            for r in range(1, 4):
                if g[start_row + r][left] != c or g[start_row + r][left + 10] != c:
                    is_u = False
                    break
                for j in range(left + 1, left + 10):
                    if g[start_row + r][j] == c:
                        is_u = False
                        break
                if not is_u:
                    break
            if not is_u:
                continue
            # It's a U, complete middle if power of two
            middle = start_row + 2
            if is_power_of_two(c):
                num_additional = (c + 1) // 2
                for k in range(num_additional):
                    rel = 10 - 2 * (k + 1)
                    j_pos = left + rel
                    if 0 <= j_pos < cols:
                        new_g[middle][j_pos] = c

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: remove small components, then complete U shapes."""
    background = determine_background(g)
    new_g = remove_small_components(g, background)
    find_and_complete_us(g, background, new_g)
    return new_g
```