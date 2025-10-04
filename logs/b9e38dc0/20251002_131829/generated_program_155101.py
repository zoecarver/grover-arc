```python
from typing import List, Tuple, Dict

def find_background(g: List[List[int]]) -> int:
    """Find the background color as the most frequent color."""
    h = len(g)
    if h == 0:
        return 0
    w = len(g[0])
    count: Dict[int, int] = {}
    for i in range(h):
        for j in range(w):
            color = g[i][j]
            count[color] = count.get(color, 0) + 1
    if not count:
        return 0
    return max(count, key=count.get)

def get_components(g: List[List[int]], bg: int, h: int, w: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """Find all 8-connected components of non-background colors."""
    visited = [[False] * w for _ in range(h)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for i in range(h):
        for j in range(w):
            if not visited[i][j] and g[i][j] != bg:
                color = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def is_adjacent(comp1: List[Tuple[int, int]], comp2: List[Tuple[int, int]]) -> bool:
    """Check if two components are adjacent (8-connectivity)."""
    comp2_set = set(comp2)
    for x, y in comp1:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if (nx, ny) in comp2_set:
                    return True
    return False

def find_adjacent_pairs(components: List[Tuple[int, List[Tuple[int, int]]]]) -> List[Tuple[Tuple[int, List[Tuple[int, int]]], Tuple[int, List[Tuple[int, int]]]]]:
    """Find all pairs of different non-background components that are adjacent."""
    pairs = []
    n = len(components)
    for i in range(n):
        for j in range(i + 1, n):
            c1 = components[i]
            c2 = components[j]
            if c1[0] != c2[0] and is_adjacent(c1[1], c2[1]):
                pairs.append((c1, c2))
    return pairs

def select_expanding(pairs: List[Tuple[Tuple[int, List[Tuple[int, int]]], Tuple[int, List[Tuple[int, int]]]]] ) -> Tuple[int, List[Tuple[int, int]]]:
    """Select the expanding component as the smaller one in adjacent pairs."""
    if not pairs:
        return (0, [])
    min_size = float('inf')
    selected = (0, [])
    for p1, p2 in pairs:
        size1 = len(p1[1])
        size2 = len(p2[1])
        if size1 < size2:
            candidate_size = size1
            candidate = p1
        else:
            candidate_size = size2
            candidate = p2
        if candidate_size < min_size:
            min_size = candidate_size
            selected = candidate
    return selected

def get_centers(positions: List[Tuple[int, int]]) -> Tuple[float, float]:
    """Compute center of positions."""
    if not positions:
        return 0.0, 0.0
    avg_row = sum(p[0] for p in positions) / len(positions)
    avg_col = sum(p[1] for p in positions) / len(positions)
    return avg_row, avg_col

def expand_horizontal(g: List[List[int]], seed_color: int, seed_pos: List[Tuple[int, int]], structure_pos: List[Tuple[int, int]], bg: int, h: int, w: int, away_dir: int) -> List[List[int]]:
    """Expand horizontally in the away direction (simple half-grid fill)."""
    out = [row[:] for row in g]
    seed_y = get_centers(seed_pos)[1]
    if away_dir < 0:
        min_c, max_c = 0, min(int(seed_y), w - 1)
    else:
        min_c, max_c = max(int(seed_y), 0), w - 1
    for i in range(h):
        for j in range(min_c, max_c + 1):
            if out[i][j] == bg:
                out[i][j] = seed_color
    return out

def expand_vertical(g: List[List[int]], seed_color: int, seed_pos: List[Tuple[int, int]], structure_pos: List[Tuple[int, int]], bg: int, h: int, w: int, away_dir: int) -> List[List[int]]:
    """Expand vertically in the away direction (simple half-grid fill)."""
    out = [row[:] for row in g]
    seed_x = get_centers(seed_pos)[0]
    if away_dir < 0:
        min_r, max_r = 0, min(int(seed_x), h - 1)
    else:
        min_r, max_r = max(int(seed_x), 0), h - 1
    for j in range(w):
        for i in range(min_r, max_r + 1):
            if out[i][j] == bg:
                out[i][j] = seed_color
    return out

def determine_expansion_type(seed_pos: List[Tuple[int, int]], structure_pos: List[Tuple[int, int]], h: int, w: int) -> Tuple[str, int]:
    """Determine type (horizontal/vertical) and away direction based on relative position."""
    seed_x, seed_y = get_centers(seed_pos)
    struct_x, struct_y = get_centers(structure_pos) if structure_pos else (seed_x, seed_y)
    dx = struct_y - seed_y
    dy = struct_x - seed_x
    if abs(dx) > abs(dy):
        # Horizontal
        direction = 1 if dx > 0 else -1
        away_dir = -direction
        return 'horizontal', away_dir
    else:
        # Vertical
        direction = 1 if dy > 0 else -1
        away_dir = -direction
        return 'vertical', away_dir

def expand_component(g: List[List[int]], seed_color: int, seed_pos: List[Tuple[int, int]], structure_pos: List[Tuple[int, int]], bg: int, h: int, w: int) -> List[List[int]]:
    """Expand the seed component using direction-based fill."""
    out = [row[:] for row in g]
    if not seed_pos:
        return out
    exp_type, away_dir = determine_expansion_type(seed_pos, structure_pos, h, w)
    if exp_type == 'horizontal':
        out = expand_horizontal(out, seed_color, seed_pos, structure_pos, bg, h, w, away_dir)
    else:
        out = expand_vertical(out, seed_color, seed_pos, structure_pos, bg, h, w, away_dir)
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing the rules to transform the grid."""
    h = len(g)
    if h == 0:
        return g
    w = len(g[0])
    bg = find_background(g)
    components = get_components(g, bg, h, w)
    pairs = find_adjacent_pairs(components)
    seed_info = select_expanding(pairs)
    seed_color, seed_pos = seed_info
    if len(seed_pos) == 0:
        return [row[:] for row in g]
    # Find structure for the selected seed (assume first pair contains it)
    structure_pos = []
    structure_color = 0
    for p1, p2 in pairs:
        if p1[0] == seed_color:
            structure_color = p2[0]
            structure_pos = p2[1]
            break
        elif p2[0] == seed_color:
            structure_color = p1[0]
            structure_pos = p1[1]
            break
    out = expand_component(g, seed_color, seed_pos, structure_pos, bg, h, w)
    return out
```