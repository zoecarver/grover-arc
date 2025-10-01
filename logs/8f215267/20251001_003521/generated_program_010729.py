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
    """Detect U-shaped structures and complete their center rows with color-specific patterns."""
    new_g = [row[:] for row in g]
    rows = len(g)
    cols = len(g[0])
    for top_row in range(rows - 4):
        j = 0
        while j < cols:
            if new_g[top_row][j] == background:
                j += 1
                continue
            c = new_g[top_row][j]
            start = j
            while j < cols and new_g[top_row][j] == c:
                j += 1
            w = j - start
            if w < 11:
                continue
            left = start
            bottom_row = top_row + 4
            if bottom_row >= rows:
                continue
            # Check bottom bar matches exactly
            bottom_match = all(new_g[bottom_row][left + k] == c for k in range(w))
            if not bottom_match:
                continue
            # Check middle rows have only sides as c, inners background
            valid = True
            for m in range(1, 4):
                mr = top_row + m
                if new_g[mr][left] != c or new_g[mr][left + w - 1] != c:
                    valid = False
                    break
                for k in range(1, w - 1):
                    if new_g[mr][left + k] != background:
                        valid = False
                        break
                if not valid:
                    break
            if not valid:
                continue
            # Valid U, complete center row
            center_row = top_row + 2
            num_additional = c // 2
            if c % 2 == 1:
                num_additional = (c + 1) // 2 + (1 if left == 1 else 0)
            first_rel = w - 3
            for ii in range(num_additional):
                rel = first_rel - 2 * ii
                if rel < 1:
                    break
                pos = left + rel
                if 0 <= pos < cols:
                    new_g[center_row][pos] = c
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: clean noise and complete U structures."""
    bg = determine_background(g)
    cleaned = remove_small_components(g, bg, min_size=20)
    completed = detect_and_complete_us(cleaned, bg)
    return completed
```