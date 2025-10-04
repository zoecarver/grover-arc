```python
from typing import List, Tuple
from collections import Counter

def find_background(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    flat = [cell for row in grid for cell in row]
    count = Counter(flat)
    return count.most_common(1)[0][0]

def identify_dividing_bars(grid: List[List[int]], background: int) -> List[Tuple[int, int, int]]:
    if not grid or not grid[0]:
        return []
    h, w = len(grid), len(grid[0])
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

def identify_panels(bars: List[Tuple[int, int, int]], h: int, w: int) -> List[Tuple[int, int, int, int]]:
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

def find_maroon_components(g: List[List[int]], background: int) -> List[Tuple[List[Tuple[int, int]], int]]:
    if not g or not g[0]:
        return []
    height, width = len(g), len(g[0])
    visited = [[False] * width for _ in range(height)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(height):
        for j in range(width):
            if not visited[i][j] and g[i][j] == 8:
                num = 8
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny] and g[nx][ny] == 8:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if component:
                    components.append((component, num))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    out = [row[:] for row in g]
    h = len(g)
    w = len(g[0])
    bg = find_background(g)
    bars = identify_dividing_bars(g, bg)
    panels = identify_panels(bars, h, w)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Merge small shapes per panel
    for panel in panels:
        left, right, top, bottom = panel
        local_visited = set()
        local_small = []
        for r in range(top, bottom + 1):
            for c in range(left, right + 1):
                if out[r][c] in (2, 4, 9) and (r, c) not in local_visited:
                    num = out[r][c]
                    component = []
                    stack = [(r, c)]
                    local_visited.add((r, c))
                    while stack:
                        x, y = stack.pop()
                        component.append((x, y, num))
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if top <= nx <= bottom and left <= ny <= right and 0 <= nx < h and 0 <= ny < w and (nx, ny) not in local_visited and out[nx][ny] == num:
                                local_visited.add((nx, ny))
                                stack.append((nx, ny))
                    if len(component) <= 2:
                        local_small.extend(component)
        # Clear all local small
        for x, y, num in local_small:
            out[x][y] = bg
        # Place up to 3 starting from left at bottom
        to_place = local_small[:3]
        place_col = left
        for i in range(len(to_place)):
            if place_col > right:
                break
            _, _, num = to_place[i]
            out[bottom][place_col] = num
            place_col += 1
    # Shift maroon components up
    maroon_comps = find_maroon_components(out, bg)
    maroon_comps.sort(key=lambda comp: max(i for i, j in comp[0]), reverse=True)
    for comp in maroon_comps:
        comp_pos = comp[0]
        if not comp_pos:
            continue
        cols = set(j for i, j in comp_pos)
        min_space = float('inf')
        for j in cols:
            min_i_j = min(i for i, jj in comp_pos if jj == j)
            r = min_i_j - 1
            space = 0
            while 0 <= r and out[r][j] == bg:
                space += 1
                r -= 1
            min_space = min(min_space, space)
        shift = min(5, min_space)
        if shift > 0:
            # Clear original
            for i, j in comp_pos:
                out[i][j] = bg
            # Place shifted up
            for i, j in comp_pos:
                new_i = i - shift
                if 0 <= new_i < h:
                    out[new_i][j] = 8
    # Reposition 9's right to left per row
    for r in range(h):
        for c in range(w - 1, -1, -1):
            if out[r][c] == 9:
                found = False
                for panel in panels:
                    pl, pr, pt, pb = panel
                    if pt <= r <= pb and pl <= c <= pr:
                        red_yellow_pos = [cc for cc in range(pl, pr + 1) if out[r][cc] in (2, 4)]
                        if red_yellow_pos:
                            candidates = [cc for cc in red_yellow_pos if cc < c]
                            if candidates:
                                target_c = max(candidates)
                            else:
                                target_c = red_yellow_pos[0]
                            new_c = target_c + 1
                            if pl <= new_c <= pr and out[r][new_c] == bg:
                                out[r][new_c] = 9
                                out[r][c] = bg
                                found = True
                                break
                # If not moved, stay
    return out
```