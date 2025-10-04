```python
from typing import List, Tuple
from collections import deque

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    nrows = len(g)
    ncols = len(g[0])
    border_set = set()
    # top
    for c in g[0]:
        border_set.add(c)
    # bottom
    for c in g[nrows - 1]:
        border_set.add(c)
    # left
    for r in range(nrows):
        border_set.add(g[r][0])
    # right
    for r in range(nrows):
        border_set.add(g[r][ncols - 1])
    # find common color on all borders
    common = None
    count = 0
    for col in border_set:
        on_top = col in g[0]
        on_bottom = col in g[nrows - 1]
        on_left = any(g[r][0] == col for r in range(nrows))
        on_right = any(g[r][ncols - 1] == col for r in range(nrows))
        if on_top and on_bottom and on_left and on_right:
            common = col
            count += 1
    if count == 1:
        return common
    # fallback to most common on border
    border_count = {}
    for r in range(nrows):
        border_count[g[r][0]] = border_count.get(g[r][0], 0) + 1
        border_count[g[r][ncols - 1]] = border_count.get(g[r][ncols - 1], 0) + 1
    for c in g[0]:
        border_count[c] = border_count.get(c, 0) + 1
    for c in g[nrows - 1]:
        border_count[c] = border_count.get(c, 0) + 1
    return max(border_count, key=border_count.get)

def find_components(g: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    nrows = len(g)
    ncols = len(g[0])
    visited = [[False] * ncols for _ in range(nrows)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(nrows):
        for c in range(ncols):
            if g[r][c] != bg and not visited[r][c]:
                color = g[r][c]
                comp = []
                q = deque([(r, c)])
                visited[r][c] = True
                while q:
                    cr, cc = q.popleft()
                    comp.append((cr, cc))
                    for dr, dc in dirs:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < nrows and 0 <= nc < ncols and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                components.append((color, comp))
    return components

def are_adjacent(comp1: List[Tuple[int, int]], comp2: List[Tuple[int, int]]) -> bool:
    s2 = set(comp2)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r, c in comp1:
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (nr, nc) in s2:
                return True
    return False

def select_seed_component(components: List[Tuple[int, List[Tuple[int, int]]]]) -> Tuple[int, List[Tuple[int, int]]]:
    if not components:
        return 0, []
    max_size = max(len(comp) for _, comp in components)
    candidates = []
    for idx, (col, comp) in enumerate(components):
        size = len(comp)
        touches_diff_large = False
        for jdx, (other_col, other_comp) in enumerate(components):
            if idx != jdx and col != other_col and len(other_comp) == max_size and are_adjacent(comp, other_comp):
                touches_diff_large = True
                break
        if touches_diff_large:
            candidates.append((size, col, idx))
    if candidates:
        candidates.sort()
        _, _, seed_idx = candidates[0]
    else:
        # fallback to smallest size, then smallest color
        min_size = min(len(comp) for _, comp in components)
        min_cands = [(col, idx) for idx, (col, comp) in enumerate(components) if len(comp) == min_size]
        min_cands.sort(key=lambda x: x[0])
        seed_idx = min_cands[0][1]
    return components[seed_idx]

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def expand_down(g: List[List[int]], seed_color: int, seed_comp: List[Tuple[int, int]], bg: int) -> List[List[int]]:
    new_grid = copy_grid(g)
    nrows = len(g)
    ncols = len(g[0])
    # fill original
    for r, c in seed_comp:
        new_grid[r][c] = seed_color
    # find seed rows
    seed_rows = set(r for r, _ in seed_comp)
    max_seed_r = max(seed_rows) if seed_rows else 0
    # fill horizontal in seed rows
    for sr in seed_rows:
        seed_cols = [c for rr, cc in seed_comp if rr == sr]
        if not seed_cols:
            continue
        min_c = min(seed_cols)
        max_c = max(seed_cols)
        # extend left from min_c
        left = min_c
        while left > 0 and new_grid[sr][left - 1] == bg:
            left -= 1
        # extend right from max_c
        right = max_c
        while right < ncols - 1 and new_grid[sr][right + 1] == bg:
            right += 1
        for c in range(left, right + 1):
            if new_grid[sr][c] == bg:
                new_grid[sr][c] = seed_color
    # now row by row down from max_seed_r +1
    current_r = max_seed_r
    while current_r < nrows - 1:
        current_r += 1
        # get previous filled cols
        prev_filled = [c for c in range(ncols) if new_grid[current_r - 1][c] == seed_color]
        if not prev_filled:
            break
        # starting cols in current
        start_cols = [c for c in prev_filled if new_grid[current_r][c] == bg]
        if not start_cols:
            break
        # group into intervals
        s = sorted(set(start_cols))
        intervals = []
        l = s[0]
        for i in range(1, len(s)):
            if s[i] == s[i - 1] + 1:
                continue
            intervals.append((l, s[i - 1]))
            l = s[i]
        intervals.append((l, s[-1]))
        num_int = len(intervals)
        new_ints = []
        for i_int, (st, en) in enumerate(intervals):
            is_single = num_int == 1
            is_leftmost = i_int == 0
            is_rightmost = i_int == num_int - 1
            # extend left
            new_st = st
            if is_single or is_leftmost:
                # full extend left to wall or edge
                tmp = st
                while tmp > 0 and new_grid[current_r][tmp - 1] == bg:
                    tmp -= 1
                new_st = tmp
            # extend right
            new_en = en
            if is_single or is_rightmost:
                # full extend right to wall or edge
                tmp = en
                while tmp < ncols - 1 and new_grid[current_r][tmp + 1] == bg:
                    tmp += 1
                new_en = tmp
            else:
                # for middle, no extend or by1?
                # in examples no middle
                new_en = en
                if new_grid[current_r][en + 1] == bg:
                    new_en = en + 1
                new_st = st
                if new_grid[current_r][st - 1] == bg:
                    new_st = st - 1
            # fill all bg in [new_st, new_en]
            for c in range(new_st, new_en + 1):
                if new_grid[current_r][c] == bg:
                    new_grid[current_r][c] = seed_color
    return new_grid

# For up spread, mirror the down, but reverse the grid rows

def reverse_rows(g: List[List[int]]) -> List[List[int]]:
    return g[::-1]

def expand_up(g: List[List[int]], seed_color: int, seed_comp: List[Tuple[int, int]], bg: int) -> List[List[int]]:
    nrows = len(g)
    # reverse rows for up = down in reversed
    rev_g = reverse_rows(g)
    # adjust seed comp rows to reversed, row' = nrows -1 - r
    rev_seed = [(nrows - 1 - r, c) for r, c in seed_comp]
    rev_exp = expand_down(rev_g, seed_color, rev_seed, bg)
    # reverse back
    return reverse_rows(rev_exp)

def get_mean_row(seed_comp: List[Tuple[int, int]], nrows: int) -> float:
    if not seed_comp:
        return 0.5
    total_r = sum(r for r, _ in seed_comp)
    return total_r / len(seed_comp) / (nrows - 1)

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    components = find_components(g, bg)
    seed_color, seed_comp = select_seed_component(components)
    if not seed_comp:
        return g
    nrows = len(g)
    mean_norm = get_mean_row(seed_comp, nrows)
    new_grid = copy_grid(g)
    # always fill original
    for r, c in seed_comp:
        new_grid[r][c] = seed_color
    # determine direction
    if mean_norm < 0.4:
        # down
        new_grid = expand_down(new_grid, seed_color, seed_comp, bg)
    elif mean_norm > 0.6:
        # up
        new_grid = expand_up(new_grid, seed_color, seed_comp, bg)
    else:
        # both
        new_grid = expand_down(new_grid, seed_color, seed_comp, bg)
        # then up from the updated
        # but to simple, expand up on original + seed
        temp = expand_up(copy_grid(new_grid), seed_color, seed_comp, bg)
        for r in range(nrows):
            for c in range(len(g[0])):
                if temp[r][c] == seed_color and new_grid[r][c] == bg:
                    new_grid[r][c] = seed_color
    return new_grid
```