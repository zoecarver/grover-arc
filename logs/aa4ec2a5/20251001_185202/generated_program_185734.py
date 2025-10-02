```python
from typing import List
from collections import deque

def get_dimensions(g: List[List[int]]) -> tuple:
    H = len(g)
    W = len(g[0]) if H > 0 else 0
    return H, W

def get_line_positions(g: List[List[int]]) -> set:
    lines = set()
    H, W = get_dimensions(g)
    for r in range(H):
        for c in range(W):
            if g[r][c] == 1:
                lines.add((r, c))
    return lines

def get_outer_fours(g: List[List[int]]) -> set:
    H, W = get_dimensions(g)
    if H == 0 or W == 0:
        return set()
    visited = set()
    q = deque()
    # top row
    for c in range(W):
        if g[0][c] == 4:
            pos = (0, c)
            q.append(pos)
            visited.add(pos)
    # bottom row
    for c in range(W):
        if g[H - 1][c] == 4:
            pos = (H - 1, c)
            if pos not in visited:
                q.append(pos)
                visited.add(pos)
    # left column, excluding corners
    for r in range(1, H - 1):
        if g[r][0] == 4:
            pos = (r, 0)
            if pos not in visited:
                q.append(pos)
                visited.add(pos)
    # right column, excluding corners
    for r in range(1, H - 1):
        if g[r][W - 1] == 4:
            pos = (r, W - 1)
            if pos not in visited:
                q.append(pos)
                visited.add(pos)
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and g[nr][nc] == 4 and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc))
    return visited

def get_holes(g: List[List[int]], outer: set) -> set:
    H, W = get_dimensions(g)
    holes = set()
    for r in range(H):
        for c in range(W):
            if g[r][c] == 4 and (r, c) not in outer:
                holes.add((r, c))
    return holes

def get_components(g: List[List[int]]) -> List[set]:
    H, W = get_dimensions(g)
    lines = get_line_positions(g)
    visited = set()
    components = []
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for start_r, start_c in lines:
        if (start_r, start_c) in visited:
            continue
        comp = set()
        q = deque([(start_r, start_c)])
        visited.add((start_r, start_c))
        comp.add((start_r, start_c))
        while q:
            r, c = q.popleft()
            for dr, dc in dirs4:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and g[nr][nc] == 1 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
                    comp.add((nr, nc))
        if comp:
            components.append(comp)
    return components

def get_to_fill_8(components: List[set], holes: set, H: int, W: int) -> set:
    to_fill_8 = set()
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for comp in components:
        has_hole = False
        for r, c in comp:
            for dr, dc in dirs4:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and (nr, nc) in holes:
                    has_hole = True
                    break
            if has_hole:
                break
        if has_hole:
            to_fill_8.update(comp)
    return to_fill_8

def get_border_positions(lines: set, outer: set, H: int, W: int) -> set:
    border = set()
    dirs8 = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    for r, c in outer:
        for dr, dc in dirs8:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W and (nr, nc) in lines:
                border.add((r, c))
                break
    return border

def program(g: List[List[int]]) -> List[List[int]]:
    H, W = get_dimensions(g)
    lines = get_line_positions(g)
    outer = get_outer_fours(g)
    holes = get_holes(g, outer)
    components = get_components(g)
    to_fill_8 = get_to_fill_8(components, holes, H, W)
    border = get_border_positions(lines, outer, H, W)
    output = [[4] * W for _ in range(H)]
    for r, c in lines:
        if (r, c) not in to_fill_8:
            output[r][c] = 1
    for r, c in to_fill_8:
        output[r][c] = 8
    for r, c in holes:
        output[r][c] = 6
    for r, c in border:
        output[r][c] = 2
    return output
```