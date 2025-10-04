```python
from typing import List, Tuple

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    return [row[:] for row in g]

def find_adjacent_zeros(g: List[List[int]]) -> List[Tuple[int, int]]:
    n = len(g)
    zeros = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == 0:
                adjacent = any(
                    0 <= i + di < n and 0 <= j + dj < n and g[i + di][j + dj] == 1
                    for di, dj in directions
                )
                if adjacent:
                    zeros.append((i, j))
    return zeros

def get_bbox(positions: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not positions:
        return None, None, None, None
    min_r = min(i for i, _ in positions)
    max_r = max(i for i, _ in positions)
    min_c = min(j for _, j in positions)
    max_c = max(j for _, j in positions)
    return min_r, max_r, min_c, max_c

def is_solid_zero_rect(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int) -> bool:
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    count = sum(1 for i in range(min_r, max_r + 1) for j in range(min_c, max_c + 1) if g[i][j] == 0)
    return count == h * w

def find_red_positions(g: List[List[int]]) -> List[Tuple[int, int]]:
    n = len(g)
    reds = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == 2:
                reds.append((i, j))
    return reds

def get_red_connection_type(g: List[List[int]], reds: List[Tuple[int, int]]) -> str:
    n = len(g)
    has_above_connection = False
    has_below_connection = False
    for i, j in reds:
        # Check below (2 above 1)
        if i + 1 < n and g[i + 1][j] == 1:
            has_above_connection = True
        # Check above (2 below 1)
        if i - 1 >= 0 and g[i - 1][j] == 1:
            has_below_connection = True
    has_vertical = has_above_connection or has_below_connection
    if not has_vertical:
        return "side"
    if has_above_connection:
        return "above"
    # Below
    if not reds:
        return "none"
    min_r_red = min(i for i, _ in reds)
    max_r_red = max(i for i, _ in reds)
    height_red = max_r_red - min_r_red + 1
    if height_red == 1:
        return "below_single"
    return "below_multi"

def should_absorb_red(connection_type: str) -> bool:
    return connection_type in ("above", "below_single")

def find_protrusions(g: List[List[int]], h: int, w: int, n: int) -> List[Tuple[int, int]]:
    candidates = []
    for start_r in range(n - h + 1):
        for start_c in range(n - w + 1):
            # Check all 1s
            all_ones = all(g[start_r + ii][start_c + jj] == 1 for ii in range(h) for jj in range(w))
            if not all_ones:
                continue
            # Check right adjacent
            right_c = start_c + w
            right_ok = right_c == n or all(g[start_r + ii][right_c] == 3 for ii in range(h))
            if right_ok:
                candidates.append((start_r, start_c))
    return candidates

def choose_best_protrusion(candidates: List[Tuple[int, int]], hole_center_r: float, hole_center_c: float, h: int, w: int) -> Tuple[int, int]:
    if not candidates:
        return None  # Assume always finds
    best = candidates[0]
    min_dist = float('inf')
    for cand in candidates:
        sr, sc = cand
        src_r = sr + (h - 1) / 2.0
        src_c = sc + (w - 1) / 2.0
        dist = abs(hole_center_r - src_r) + abs(hole_center_c - src_c)
        if dist < min_dist:
            min_dist = dist
            best = cand
    return best

def set_rectangle_to_zero(out: List[List[int]], start_r: int, start_c: int, h: int, w: int):
    for ii in range(h):
        for jj in range(w):
            out[start_r + ii][start_c + jj] = 0

def set_positions_to_one(out: List[List[int]], positions: List[Tuple[int, int]]):
    for i, j in positions:
        out[i][j] = 1

def set_reds_to_zero(out: List[List[int]], reds: List[Tuple[int, int]]):
    for i, j in reds:
        out[i][j] = 0

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    n = len(g)
    zero_pos = find_adjacent_zeros(g)
    if not zero_pos:
        return out
    min_r, max_r, min_c, max_c = get_bbox(zero_pos)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    if len(zero_pos) != h * w or not is_solid_zero_rect(g, min_r, max_r, min_c, max_c):
        return out  # Assume valid
    reds = find_red_positions(g)
    conn_type = get_red_connection_type(g, reds)
    absorb = should_absorb_red(conn_type)
    hole_center_r = min_r + (h - 1) / 2.0
    hole_center_c = min_c + (w - 1) / 2.0
    if absorb and reds:
        set_reds_to_zero(out, reds)
        set_positions_to_one(out, zero_pos)
    else:
        candidates = find_protrusions(g, h, w, n)
        best = choose_best_protrusion(candidates, hole_center_r, hole_center_c, h, w)
        if best:
            sr, sc = best
            set_rectangle_to_zero(out, sr, sc, h, w)
        set_positions_to_one(out, zero_pos)
    return out
```