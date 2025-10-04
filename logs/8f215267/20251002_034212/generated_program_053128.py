```python
from typing import List, Tuple, Dict, Set
from collections import defaultdict

def get_background_color(grid: List[List[int]]) -> int:
    """Identify the background color from the top-left cell."""
    return grid[0][0]

def find_all_connected_components(grid: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """Find all 4-connected components of non-background cells."""
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    all_comps = []
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and grid[i][j] != bg:
                c = grid[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == c:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                all_comps.append((c, component))
    return all_comps

def identify_frames(all_comps: List[Tuple[int, List[Tuple[int, int]]]], grid: List[List[int]], bg: int) -> List[Tuple[int, int, int, int, List[Tuple[int, int]]]]:
    """Identify frame components based on size, bbox, and internal background fill."""
    frames = []
    for c, comp in all_comps:
        if len(comp) < 25 or len(comp) > 30:
            continue
        min_i = min(p[0] for p in comp)
        max_i = max(p[0] for p in comp)
        min_j = min(p[1] for p in comp)
        max_j = max(p[1] for p in comp)
        h = max_i - min_i + 1
        w = max_j - min_j + 1
        if h != 5 or w != 11:
            continue
        # Check internal 3x9 all bg
        internal_count = 0
        for ii in range(min_i + 1, min_i + 4):
            for jj in range(min_j + 1, min_j + 10):
                if grid[ii][jj] == bg:
                    internal_count += 1
        if internal_count == 27:
            t = min_i
            l = min_j
            m = t + 2
            frames.append((t, l, c, m, comp))
    return frames

def compute_n_for_color(c: int, all_comps_for_c: List[List[Tuple[int, int]]], frame_comp: List[Tuple[int, int]]) -> int:
    """Compute n based on small filled squares rule for other components of color c."""
    n = 0
    for comp in all_comps_for_c:
        if comp == frame_comp:
            continue
        pp = len(comp)
        if 1 <= pp <= 8:
            min_ii = min(p[0] for p in comp)
            max_ii = max(p[0] for p in comp)
            min_jj = min(p[1] for p in comp)
            max_jj = max(p[1] for p in comp)
            hh = max_ii - min_ii + 1
            ww = max_jj - min_jj + 1
            n += 1
            if ww == hh and pp == ww * hh and 2 <= ww <= 3:
                n += (ww - 1)
    return n

def get_placement_columns(ileft: int, iright: int, n: int) -> List[int]:
    """Compute the columns in the interior for placing n 1x1 squares, right-aligned with appropriate parity."""
    if n == 0:
        return []
    rpar = iright % 2
    opp_par = 1 - rpar
    poss_opp = [col for col in range(ileft, iright + 1) if col % 2 == opp_par]
    nopp = len(poss_opp)
    if n <= nopp:
        return poss_opp[-n:]
    else:
        same_par = rpar
        poss_same = [col for col in range(ileft, iright + 1) if col % 2 == same_par]
        nsame = len(poss_same)
        return poss_same[-n:]

def fill_non_frame_cells(grid: List[List[int]], bg: int, frame_cells: Set[Tuple[int, int]]) -> List[List[int]]:
    """Fill all non-background cells not part of frames with background color."""
    rows = len(grid)
    cols = len(grid[0])
    output = [row[:] for row in grid]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != bg and (i, j) not in frame_cells:
                output[i][j] = bg
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing all rules to transform the input grid."""
    bg = get_background_color(g)
    all_comps = find_all_connected_components(g, bg)
    frames = identify_frames(all_comps, g, bg)
    comps_by_c: Dict[int, List[List[Tuple[int, int]]]] = defaultdict(list)
    for c, comp in all_comps:
        comps_by_c[c].append(comp)
    frame_cells: Set[Tuple[int, int]] = set()
    for _, _, _, _, comp in frames:
        for p in comp:
            frame_cells.add(p)
    output_grid = fill_non_frame_cells(g, bg, frame_cells)
    for t, l, c, m, frame_comp in frames:
        other_comps = [comp for comp in comps_by_c[c] if comp != frame_comp]
        n = compute_n_for_color(c, other_comps, frame_comp)
        ileft = l + 1
        iright = l + 9
        place_cols = get_placement_columns(ileft, iright, n)
        for col in place_cols:
            output_grid[m][col] = c
    return output_grid
```