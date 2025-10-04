```python
from typing import List
from collections import Counter, deque

def get_background(g: List[List[int]]) -> int:
    """Identify the background color as the most frequent color."""
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_special(g: List[List[int]], bg: int, counts: dict) -> int:
    """Identify the special color as the non-background color with minimal count, tie broken by smallest value."""
    non_bg_counts = {k: v for k, v in counts.items() if k != bg and v > 0}
    if not non_bg_counts:
        return -1
    return min(non_bg_counts, key=lambda k: (non_bg_counts[k], k))

def get_special_positions(g: List[List[int]], special: int, height: int, width: int) -> List[tuple[int, int]]:
    """Get all positions of the special color in the current grid."""
    return [(r, c) for r in range(height) for c in range(width) if g[r][c] == special]

def get_component(g: List[List[int]], start_r: int, start_c: int, bg: int, height: int, width: int) -> set[tuple[int, int]]:
    """Find the connected component of non-background cells starting from (start_r, start_c) using 4-connectivity."""
    queue = deque([(start_r, start_c)])
    visited = set([(start_r, start_c)])
    component = set()
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while queue:
        r, c = queue.popleft()
        component.add((r, c))
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and g[nr][nc] != bg and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return component

def align_horizontal(g: List[List[int]], special_pos: List[tuple[int, int]], anchor_c: int, bg: int, height: int, width: int) -> List[List[int]]:
    """Align components containing special cells horizontally to the target column."""
    new_g = [row[:] for row in g]
    processed = set()
    for sr, sc in special_pos:
        if (sr, sc) in processed:
            continue
        component = get_component(new_g, sr, sc, bg, height, width)
        comp_special = [(pr, pc) for pr, pc in special_pos if (pr, pc) in component]
        for p in comp_special:
            processed.add(p)
        # Pick the special with minimal row for shift calculation
        pick = min(comp_special, key=lambda p: p[0])
        shift = anchor_c - pick[1]
        # Collect moves
        moves = []
        for rr, cc in component:
            new_cc = cc + shift
            if 0 <= new_cc < width:
                moves.append((rr, new_cc, new_g[rr][cc]))
        # Clear old positions
        for rr, cc in component:
            new_g[rr][cc] = bg
        # Place new positions (overwrite if necessary)
        for rr, new_cc, val in moves:
            new_g[rr][new_cc] = val
    return new_g

def align_vertical(g: List[List[int]], special_pos: List[tuple[int, int]], anchor_r: int, special: int, bg: int, height: int, width: int) -> List[List[int]]:
    """Align single special cells vertically to the target row, keeping column."""
    new_g = [row[:] for row in g]
    for r, c in special_pos:
        shift_v = anchor_r - r
        new_r = r + shift_v
        if 0 <= new_r < height:
            # Overwrite target if necessary
            new_g[new_r][c] = special
        new_g[r][c] = bg
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing the rules to transform the grid."""
    height = len(g)
    if height == 0:
        return g
    width = len(g[0])
    bg = get_background(g)
    flat = [cell for row in g for cell in row]
    counts = Counter(flat)
    # Get colors sorted by increasing count, then increasing value
    all_colors = sorted(counts, key=lambda k: (counts[k], k))
    rare_colors = [c for c in all_colors if c != bg and counts[c] <= 4]
    new_g = [row[:] for row in g]
    for special in rare_colors:
        special_pos = get_special_positions(new_g, special, height, width)
        if not special_pos:
            continue
        singles = [pos for pos in special_pos if len(get_component(new_g, pos[0], pos[1], bg, height, width)) == 1]
        if len(singles) == 0:
            continue
        if len(singles) == 1:
            # Horizontal alignment
            anchor_r, anchor_c = singles[0]
            new_g = align_horizontal(new_g, special_pos, anchor_c, bg, height, width)
        else:
            # Vertical alignment, anchor is the leftmost (min c, tie min r)
            anchor = min(singles, key=lambda p: (p[1], p[0]))
            anchor_r = anchor[0]
            new_g = align_vertical(new_g, special_pos, anchor_r, special, bg, height, width)
    return new_g
```