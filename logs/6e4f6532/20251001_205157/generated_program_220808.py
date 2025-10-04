```python
from typing import List
from collections import Counter

def find_background(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    flat = [cell for row in grid for cell in row]
    count = Counter(flat)
    return count.most_common(1)[0][0]

def identify_dividing_bars(grid: List[List[int]], background: int) -> List[tuple]:
    if not grid or not grid[0]:
        return []
    h = len(grid)
    w = len(grid[0])
    bars = []
    c = 0
    while c < w:
        col = [grid[r][c] for r in range(h)]
        if len(set(col)) == 1 and col[0] != background:
            start = c
            color = col[0]
            c += 1
            while c < w:
                col_next = [grid[r][c] for r in range(h)]
                if len(set(col_next)) == 1 and col_next[0] == color:
                    c += 1
                else:
                    break
            end = c - 1
            bars.append((start, end, color))
        else:
            c += 1
    return bars

def identify_panels(bars: List[tuple], h: int, w: int) -> List[tuple]:
    if not bars:
        return [(0, w - 1, 0, h - 1)] if w > 0 and h > 0 else []
    panels = []
    left = 0
    for start, end, _ in bars:
        if left < start:
            panels.append((left, start - 1, 0, h - 1))
        left = end + 1
    if left < w:
        panels.append((left, w - 1, 0, h - 1))
    return panels

def merge_small_shapes(grid: List[List[int]], panels: List[tuple], background: int) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for p_left, p_right, p_top, p_bottom in panels:
        small_pixels = []
        for r in range(p_top, p_bottom + 1):
            for c in range(p_left, p_right + 1):
                cell = new_grid[r][c]
                if cell in (2, 4, 9) and cell != background:
                    neighbors = sum(1 for dr, dc in directions
                                    if (p_top <= r + dr <= p_bottom and p_left <= c + dc <= p_right and
                                        new_grid[r + dr][c + dc] == cell))
                    if neighbors <= 1:  # 1-2 pixels (self + at most 1 neighbor)
                        small_pixels.append((r, c, cell))
        # Merge: change up to 3 small to background, place in bottom-left of panel
        for r, c, color in small_pixels[:3]:
            new_grid[r][c] = background
        place_c = p_left
        for r, c, color in small_pixels[:3]:
            if p_bottom < len(new_grid) and place_c < len(new_grid[0]):
                new_grid[p_bottom][place_c] = color
            place_c += 1
    return new_grid

def transform_maroon_shapes(grid: List[List[int]], panels: List[tuple], background: int) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    h = len(grid)
    for p_left, p_right, p_top, p_bottom in panels:
        moved = set()
        for r in range(p_top, p_bottom + 1):
            for c in range(p_left, p_right + 1):
                if new_grid[r][c] == 8 and (r, c) not in moved:
                    # Simple shift up by up to 5 rows, avoiding overlap
                    shift = min(5, r - p_top)
                    new_r = r - shift
                    if new_r != r:
                        new_grid[new_r][c] = 8
                        new_grid[r][c] = background
                        moved.add((new_r, c))
                        moved.add((r, c))
    return new_grid

def reposition_light_blue(grid: List[List[int]], panels: List[tuple], background: int) -> List[List[int]]:
    new_grid = [row[:] for row in grid]
    red_yellow_pos = []
    for p_left, p_right, p_top, p_bottom in panels:
        for r in range(p_top, p_bottom + 1):
            for c in range(p_left, p_right + 1):
                if new_grid[r][c] in (2, 4):
                    red_yellow_pos.append((r, c))
    for p_left, p_right, p_top, p_bottom in panels:
        moved = set()
        for r in range(p_top, p_bottom + 1):
            for c in range(p_left, p_right + 1):
                if new_grid[r][c] == 9 and (r, c) not in moved:
                    if red_yellow_pos:
                        # Move to right of first red/yellow in same row if possible
                        tr, tc = next((pr, pc) for pr, pc in red_yellow_pos if pr == r and p_left <= pc + 1 <= p_right), red_yellow_pos[0]
                        new_c = tc + 1 if p_left <= tc + 1 <= p_right else tc
                        if new_c != c:
                            new_grid[r][c] = background
                            new_grid[r][new_c] = 9
                            moved.add((r, c))
                            moved.add((r, new_c))
                    else:
                        # If no red/yellow, leave as is
                        pass
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    background = find_background(g)
    bars = identify_dividing_bars(g, background)
    h = len(g)
    w = len(g[0])
    panels = identify_panels(bars, h, w)
    grid = merge_small_shapes(g, panels, background)
    grid = transform_maroon_shapes(grid, panels, background)
    grid = reposition_light_blue(grid, panels, background)
    return grid
```