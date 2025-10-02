```python
from collections import Counter, deque
from typing import List, Tuple, Dict, Set

directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_background(grid: List[List[int]]) -> int:
    """Find the most common value as background."""
    if not grid or not grid[0]:
        return 0
    flat = [cell for row in grid for cell in row]
    return Counter(flat).most_common(1)[0][0]

def extract_components(grid: List[List[int]], bg: int) -> List[List[Tuple[int, int, int]]]:
    """Extract 4-connected non-background components."""
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components: List[List[Tuple[int, int, int]]] = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != bg and not visited[i][j]:
                comp: List[Tuple[int, int, int]] = []
                q = deque([(i, j)])
                visited[i][j] = True
                comp.append((i, j, grid[i][j]))
                while q:
                    r, c = q.popleft()
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] != bg:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                            comp.append((nr, nc, grid[nr][nc]))
                if comp:
                    components.append(comp)
    return components

def get_refs_and_specials(components: List[List[Tuple[int, int, int]]], bg: int) -> Tuple[Set[int], Dict[int, List[Tuple[int, int]]]]:
    """Identify special values and their isolated reference positions."""
    special_values: Set[int] = set()
    refs: Dict[int, List[Tuple[int, int]]] = {}
    for comp in components:
        if len(comp) == 1:
            r, c, v = comp[0]
            if v != bg:
                special_values.add(v)
                if v not in refs:
                    refs[v] = []
                refs[v].append((r, c))
    return special_values, refs

def get_delta_for_comp(comp: List[Tuple[int, int, int]], special_values: Set[int], refs: Dict[int, List[Tuple[int, int]]], bg: int, cols: int) -> Tuple[int, int]:
    """Compute shift delta for a component based on its special value and references."""
    comp_count = Counter(v for _, _, v in comp)
    possible = [v for v in special_values if v in comp_count]
    if not possible:
        return 0, 0
    min_cnt = min(comp_count[v] for v in possible)
    candidates = [v for v in possible if comp_count[v] == min_cnt]
    special_v = min(candidates)
    special_pos = [(r, c) for r, c, vv in comp if vv == special_v]
    if not special_pos:
        return 0, 0
    n = len(special_pos)
    key_r = sum(r for r, _ in special_pos) / n
    key_c = sum(c for _, c in special_pos) / n
    ref_pos_list = refs.get(special_v, [])
    if not ref_pos_list:
        return 0, 0
    m = len(ref_pos_list)
    ref_r = sum(r for r, _ in ref_pos_list) / m
    ref_c = sum(c for _, c in ref_pos_list) / m
    rs = [r for r, _, _ in comp]
    cs = [c for _, c, _ in comp]
    min_r = min(rs)
    max_r = max(rs)
    min_c = min(cs)
    max_c = max(cs)
    span_r = max_r - min_r + 1
    span_c = max_c - min_c + 1
    ref_c_rounded = round(ref_c)
    is_edge = (ref_c_rounded == 0 or ref_c_rounded == cols - 1)
    delta_r = 0
    delta_c = 0
    if is_edge:
        delta_r = round(ref_r - key_r)
        delta_c = 0
        if span_r == span_c and key_r < ref_r:
            delta_c = -1
    else:
        delta_c = round(ref_c - key_c)
        delta_r = 0
    return delta_r, delta_c

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to transform the grid according to the puzzle rules."""
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    bg = get_background(g)
    components = extract_components(g, bg)
    special_values, refs = get_refs_and_specials(components, bg)
    new_grid = [[bg] * cols for _ in range(rows)]
    # Place isolated components
    for comp in components:
        if len(comp) == 1:
            r, c, v = comp[0]
            new_grid[r][c] = v
    # Place large components with computed shifts
    for comp in components:
        if len(comp) > 1:
            dr, dc = get_delta_for_comp(comp, special_values, refs, bg, cols)
            for r, c, v in comp:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    new_grid[nr][nc] = v
    return new_grid
```