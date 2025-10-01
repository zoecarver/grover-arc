```python
from typing import List, Tuple
from collections import Counter

def find_background(grid: List[List[int]]) -> int:
    flat = [cell for row in grid for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_zero_positions(grid: List[List[int]]) -> List[Tuple[int, int]]:
    positions = []
    rows = len(grid)
    if rows == 0:
        return positions
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                positions.append((r, c))
    return positions

def find_zero_bounds(zeros: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not zeros:
        raise ValueError("No zero positions found")
    min_r = min(p[0] for p in zeros)
    max_r = max(p[0] for p in zeros)
    min_c = min(p[1] for p in zeros)
    max_c = max(p[1] for p in zeros)
    return min_r, max_r, min_c, max_c

def find_stack_colors(grid: List[List[int]], bg: int, min_r: int, max_r: int, min_c: int, max_c: int) -> List[int]:
    col_counts = {c: 0 for c in range(min_c, max_c + 1)}
    rows_n = len(grid)
    for r in range(min_r, min_r + (max_r - min_r + 1) if max_r >= min_r else 0):
        if r >= rows_n:
            break
        for c in range(min_c, max_c + 1):
            val = grid[r][c]
            if val != 0 and val != bg:
                col_counts[c] += 1
    if all(count == 0 for count in col_counts.values()):
        raise ValueError("No stack colors found")
    stack_c = max(col_counts, key=col_counts.get)
    colors = []
    for r in range(min_r, max_r + 1):
        if r >= len(grid):
            break
        val = grid[r][stack_c]
        if val != 0 and val != bg:
            colors.append(val)
    return colors

def count_large_components(grid: List[List[int]], color: int) -> int:
    rows = len(grid)
    if rows == 0:
        return 0
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    count = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == color and not visited[r][c]:
                size = 0
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    size += 1
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == color:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                if size >= 3:
                    count += 1
    return count

def build_output(colors: List[int], component_counts: List[int], width: int, height: int) -> List[List[int]]:
    output = [[0] * width for _ in range(height)]
    for i in range(len(colors)):
        colr = colors[i]
        num = component_counts[i]
        row = 2 * i + 1
        pos = 1
        for j in range(num):
            if pos < width:
                output[row][pos] = colr
                pos += 1
                if pos < width:
                    output[row][pos] = 0
                    pos += 1
                else:
                    break
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    zeros = find_zero_positions(g)
    if not zeros:
        raise ValueError("No zeros in grid")
    min_r, max_r, min_c, max_c = find_zero_bounds(zeros)
    width = max_c - min_c + 1
    colors = find_stack_colors(g, bg, min_r, max_r, min_c, max_c)
    num_colors = len(colors)
    height = 2 * num_colors + 1
    component_counts = [count_large_components(g, colr) for colr in colors]
    output = build_output(colors, component_counts, width, height)
    return output
```