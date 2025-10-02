```python
from collections import deque
from typing import List

def get_background(g: List[List[int]]) -> int:
    """Identify the background color from the top-left border cell."""
    return g[0][0]

def clean_small_components(g: List[List[int]], bg: int, max_size: int = 5) -> List[List[int]]:
    """Remove small connected components (size <= max_size) of non-background colors by replacing them with background."""
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    new_g = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == bg or visited[r][c]:
                continue
            component_color = g[r][c]
            queue = deque([(r, c)])
            visited[r][c] = True
            size = 1
            component = [(r, c)]
            while queue:
                cr, cc = queue.popleft()
                for dr, dc in directions:
                    nr = cr + dr
                    nc = cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == component_color:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
                        size += 1
                        component.append((nr, nc))
            if size <= max_size:
                for pr, pc in component:
                    new_g[pr][pc] = bg
    return new_g

def has_non_bg_after(g: List[List[int]], after_row: int, bg: int) -> bool:
    """Check if there is any non-background cell after the given row."""
    rows = len(g)
    cols = len(g[0])
    for r in range(after_row, rows):
        for j in range(cols):
            if g[r][j] != bg:
                return True
    return False

def process_shape(g: List[List[int]], block_start: int, block_end: int, bg: int) -> List[List[int]]:
    """Process a block into a frame shape with pattern in the middle row."""
    rows = len(g)
    cols = len(g[0])
    h = block_end - block_start + 1
    if h < 5:
        return g
    # Find color c with most occurrences in the block
    count = {}
    for r in range(block_start, block_end + 1):
        for j in range(cols):
            color = g[r][j]
            if color != bg:
                count[color] = count.get(color, 0) + 1
    if not count:
        return g
    c = max(count, key=count.get)
    # Find L and R for c
    L = cols
    R = -1
    for r in range(block_start, block_end + 1):
        for j in range(cols):
            if g[r][j] == c:
                L = min(L, j)
                R = max(R, j)
    if R - L + 1 < 3:  # Minimal width
        return g
    # Check if last block
    is_last = not has_non_bg_after(g, block_end + 1, bg)
    # Extension rule
    extended = False
    if h == 5 and is_last and block_start > 0:
        prev_all_bg = all(g[block_start - 1][j] == bg for j in range(cols))
        is_top_full = all(g[block_start][j] == c for j in range(L, R + 1))
        if prev_all_bg and is_top_full:
            block_start -= 1
            extended = True
            # Set new top full
            for j in range(L, R + 1):
                g[block_start][j] = c
            h += 1
    # Update end
    bottom = block_start + h - 1
    top = block_start
    # Set full top and bottom
    for j in range(L, R + 1):
        g[top][j] = c
        g[bottom][j] = c
    # Set sides for all rows in block
    for r in range(top, bottom + 1):
        g[r][L] = c
        g[r][R] = c
    # Set interior of internal rows to bg
    for r in range(top + 1, bottom):
        for j in range(L + 1, R):
            g[r][j] = bg
    # Add pattern in middle row
    middle = top + 2
    if middle < bottom:
        k = (c + 1) // 2
        for i in range(1, k + 1):
            col = R - 2 * i
            if L < col < R:
                g[middle][col] = c
    return g

def find_and_process_blocks(g: List[List[int]], bg: int) -> List[List[int]]:
    """Find blocks of rows with non-background cells and process them into shapes."""
    rows = len(g)
    r = 0
    while r < rows:
        # Skip all-bg rows
        while r < rows and all(g[r][j] == bg for j in range(len(g[0]))):
            r += 1
        if r >= rows:
            break
        block_start = r
        # Find end of block
        while r < rows and not all(g[r][j] == bg for j in range(len(g[0]))):
            r += 1
        block_end = r - 1
        # Process the block
        g = process_shape(g, block_start, block_end, bg)
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: clean small components, then process blocks into shapes with patterns."""
    bg = get_background(g)
    g = clean_small_components(g, bg, 5)
    g = find_and_process_blocks(g, bg)
    return g
```