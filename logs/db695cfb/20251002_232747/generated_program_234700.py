```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def get_all_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    positions = []
    for r in range(len(g)):
        for c in range(len(g[0])):
            if g[r][c] == color:
                positions.append((r, c))
    return positions

def is_on_line(r: int, c: int, r1: int, c1: int, r2: int, c2: int) -> bool:
    dr = r2 - r1
    dc = c2 - c1
    adr = abs(dr)
    adc = abs(dc)
    if adr != adc or adr == 0:
        return False
    step_r = 1 if dr > 0 else -1 if dr < 0 else 0
    step_c = 1 if dc > 0 else -1 if dc < 0 else 0
    if step_r == 0 and step_c == 0:
        return False
    if step_r != 0:
        if (r - r1) % step_r != 0:
            return False
        k = (r - r1) // step_r
    else:
        k = (c - c1) // step_c
    if k <= 0 or k >= adr:
        return False
    expected_r = r1 + k * step_r
    expected_c = c1 + k * step_c
    return r == expected_r and c == expected_c

def fill_line(grid: List[List[int]], r1: int, c1: int, r2: int, c2: int, color: int) -> None:
    bg = get_background(grid)
    dr = r2 - r1
    dc = c2 - c1
    adr = abs(dr)
    adc = abs(dc)
    if adr != adc or adr == 0:
        return
    step_r = 1 if dr > 0 else -1 if dr < 0 else 0
    step_c = 1 if dc > 0 else -1 if dc < 0 else 0
    current_r = r1
    current_c = c1
    k = 0
    while k <= adr:
        if grid[current_r][current_c] == bg:
            grid[current_r][current_c] = color
        if k == adr:
            break
        current_r += step_r
        current_c += step_c
        k += 1

def fill_direction(grid: List[List[int]], r: int, c: int, step_r: int, step_c: int, color: int) -> None:
    bg = get_background(grid)
    current_r = r + step_r
    current_c = c + step_c
    rows = len(grid)
    cols = len(grid[0])
    while 0 <= current_r < rows and 0 <= current_c < cols:
        if grid[current_r][current_c] == bg:
            grid[current_r][current_c] = color
        current_r += step_r
        current_c += step_c

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    bg = get_background(g)
    has_six = any(6 in row for row in g)
    original_ones = get_all_positions(g, 1)
    original_sixes = get_all_positions(g, 6) if has_six else []
    # Fill lines for 1
    for i in range(len(original_ones)):
        for j in range(i + 1, len(original_ones)):
            r1, c1 = original_ones[i]
            r2, c2 = original_ones[j]
            fill_line(grid, r1, c1, r2, c2, 1)
    # Fill lines for 6
    for i in range(len(original_sixes)):
        for j in range(i + 1, len(original_sixes)):
            r1, c1 = original_sixes[i]
            r2, c2 = original_sixes[j]
            fill_line(grid, r1, c1, r2, c2, 6)
    # Find blocking 6's on 1's lines
    blocking = set()
    for i in range(len(original_ones)):
        for j in range(i + 1, len(original_ones)):
            r1, c1 = original_ones[i]
            r2, c2 = original_ones[j]
            dr = r2 - r1
            dc = c2 - c1
            if abs(dr) != abs(dc) or abs(dr) == 0:
                continue
            for sr, sc in original_sixes:
                if is_on_line(sr, sc, r1, c1, r2, c2):
                    blocking.add((sr, sc))
    # For each blocking, determine slope type and fill perpendicular
    for sr, sc in blocking:
        slope_positive = None
        found_pair = False
        for i in range(len(original_ones)):
            for j in range(i + 1, len(original_ones)):
                r1, c1 = original_ones[i]
                r2, c2 = original_ones[j]
                dr = r2 - r1
                dc = c2 - c1
                if abs(dr) != abs(dc) or abs(dr) == 0:
                    continue
                if is_on_line(sr, sc, r1, c1, r2, c2):
                    slope_positive = (dr * dc > 0)
                    found_pair = True
                    break
            if found_pair:
                break
        if slope_positive is None:
            continue
        if slope_positive:
            # positive, perpendicular negative
            fill_direction(grid, sr, sc, -1, 1, 6)
            fill_direction(grid, sr, sc, 1, -1, 6)
        else:
            # negative, perpendicular positive
            fill_direction(grid, sr, sc, -1, -1, 6)
            fill_direction(grid, sr, sc, 1, 1, 6)
    return grid
```