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

def complete_us(cleaned: List[List[int]], bg: int) -> List[List[int]]:
    """Detect and complete U-shaped structures by filling patterns in the center row based on color and width type."""
    rows = len(cleaned)
    if rows == 0:
        return cleaned
    cols = len(cleaned[0])
    for sr in range(rows - 4):
        for l in range(cols - 10):
            c = cleaned[sr][l]
            if c == bg:
                continue
            # Check top bar: 11 cells
            top_ok = all(cleaned[sr][j] == c for j in range(l, l + 11))
            if not top_ok:
                continue
            # Check bottom bar: 11 cells
            bottom_ok = all(cleaned[sr + 4][j] == c for j in range(l, l + 11))
            if not bottom_ok:
                continue
            # Check middle rows: sides c, interiors bg
            mid_ok = True
            for dr in range(1, 4):
                if cleaned[sr + dr][l] != c or cleaned[sr + dr][l + 10] != c:
                    mid_ok = False
                    break
                for j in range(l + 1, l + 10):
                    if cleaned[sr + dr][j] != bg:
                        mid_ok = False
                        break
                if not mid_ok:
                    break
            if not mid_ok:
                continue
            # Valid U, check if wide (extra cell at l+11 in top and bottom)
            is_wide = (l + 11 < cols and cleaned[sr][l + 11] == c and cleaned[sr + 4][l + 11] == c)
            # Compute k based on c and is_wide
            if c == 1:
                k = 1 + (1 if is_wide else 0)
            elif c == 2:
                k = 1 if is_wide else 0
            else:
                k = c // 2
            k = min(k, 4)
            # Fill rightmost k even-relative positions in center row
            center = sr + 2
            for i in range(k):
                j = l + 10 - 2 * (i + 1)
                cleaned[center][j] = c
    return cleaned

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: remove small components, then complete U structures."""
    bg = determine_background(g)
    cleaned = remove_small_components(g, bg, min_size=20)
    completed = complete_us(cleaned, bg)
    return completed
```