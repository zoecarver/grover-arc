```python
from typing import List, Tuple, Set, Dict, Optional
from collections import deque

def get_neighbors(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(r + dr, c + dc) for dr, dc in dirs if 0 <= r + dr < rows and 0 <= c + dc < cols]

def find_connected_components(grid: List[List[int]]) -> List[Tuple[int, Set[Tuple[int, int]]]]:
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    visited: Set[Tuple[int, int]] = set()
    components = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 0 and (i, j) not in visited:
                color = grid[i][j]
                component: Set[Tuple[int, int]] = set()
                queue = deque([(i, j)])
                visited.add((i, j))
                component.add((i, j))
                while queue:
                    cr, cc = queue.popleft()
                    for nr, nc in get_neighbors(cr, cc, rows, cols):
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                            component.add((nr, nc))
                components.append((color, component))
    return components

def get_component_bbox(comp: Set[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not comp:
        return 0, 0, 0, 0
    rs = [r for r, c in comp]
    cs = [c for r, c in comp]
    return min(rs), max(rs), min(cs), max(cs)

def translate_set(pos: Set[Tuple[int, int]], dr: int, dc: int) -> Set[Tuple[int, int]]:
    return {(r + dr, c + dc) for r, c in pos}

def place_pixels(grid: List[List[int]], pos: Set[Tuple[int, int]], color: int):
    for r, c in pos:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            grid[r][c] = color

def get_attached_reds(grid: List[List[int]], comp_pos: Set[Tuple[int, int]], all_nonred_pos: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    rows = len(grid)
    cols = len(grid[0])
    candidate_reds = set()
    for r, c in comp_pos:
        for nr, nc in get_neighbors(r, c, rows, cols):
            if grid[nr][nc] == 2:
                candidate_reds.add((nr, nc))
    attached = set()
    for r, c in candidate_reds:
        only_this = True
        for nr, nc in get_neighbors(r, c, rows, cols):
            if (nr, nc) in all_nonred_pos and (nr, nc) not in comp_pos:
                only_this = False
                break
        if only_this:
            attached.add((r, c))
    return attached

def get_top_bar(comp: Set[Tuple[int, int]], min_c: int) -> Optional[Tuple[int, int, int]]:
    min_r, max_r, _, max_c = get_component_bbox(comp)
    h = max_r - min_r + 1
    top_row_cs = set(c - min_c for r, c in comp if r == min_r)
    if top_row_cs:
        min_top = min(top_row_cs)
        max_top = max(top_row_cs)
        length = max_top - min_top + 1
        if length == len(top_row_cs):
            return min_top, max_top, length
    return None

def get_bottom_two_red(comp_min_r: int, comp_min_c: int, reds: Set[Tuple[int, int]]) -> Optional[Tuple[int, int, int, int]]:
    bottom_rel_r = -1  # relative to comp max_r +1 would be h
    max_r = max(r for r, c in reds)  # use actual
    bottom_reds = [(r - comp_min_r, c - comp_min_c) for r, c in reds if r == max_r]
    if len(bottom_reds) == 2:
        rc1, rc2 = sorted(bottom_reds)
        dist = rc2[1] - rc1[1]
        return max_r - comp_min_r, rc1[1], rc2[1], dist
    return None

def can_span(dist: int, bar_length: int) -> bool:
    return bar_length >= dist + 1

def get_side_bottom_red(comp: Set[Tuple[int, int]], reds: Set[Tuple[int, int]], min_r: int, min_c: int, max_r: int, max_c: int, side: str) -> Optional[Tuple[int, int]]:
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    bottom_rel_r = h - 1
    target_rel_c = 0 if side == 'left' else w
    bottom_reds = [(r - min_r, c - min_c) for r, c in reds if r - min_r == bottom_rel_r and ((side == 'left' and c - min_c == 0) or (side == 'right' and c - min_c == w))]
    if len(bottom_reds) == 1:
        rr, rc = bottom_reds[0]
        return rr, rc
    return None

def build_vertical_chains(comps: List[Tuple[int, Set[Tuple[int, int]], Set[Tuple[int, int]], Set[Tuple[int, int]]]]) -> List[List[Tuple[int, Set[Tuple[int, int]], Set[Tuple[int, int]], Set[Tuple[int, int]]]]]:
    chains = []
    n = len(comps)
    def recurse(chain: List[int], used: Set[int]):
        if chain:
            this_chain = [comps[i] for i in chain]
            chains.append(this_chain)
        current_bottom_idx = chain[-1] if chain else -1
        for i in range(n):
            if i in used or i == current_bottom_idx:
                continue
            if current_bottom_idx == -1 or can_attach_upper(comps[current_bottom_idx], comps[i]):
                new_used = used.copy()
                new_used.add(i)
                new_chain = chain + [i]
                recurse(new_chain, new_used)
    recurse([], set())
    # filter maximal chains (longest non-overlapping, but for small, take all length >0 , assume disjoint in examples
    maximal_chains = [ch for ch in chains if len(ch) > 0]
    return maximal_chains

def can_attach_upper(lower: Tuple, upper: Tuple) -> bool:
    lower_color, lower_comp, _, _ = lower
    upper_color, upper_comp, upper_reds, _ = upper
    lower_min_r, _, lower_min_c, _ = get_component_bbox(lower_comp)
    upper_min_r, _, upper_min_c, _ = get_component_bbox(upper_comp)
    lower_top = get_top_bar(lower_comp, lower_min_c)
    if not lower_top:
        return False
    upper_bottom = get_bottom_two_red(upper_min_r, upper_min_c, upper_reds)
    if not upper_bottom:
        return False
    _, _, _, dist = upper_bottom
    _, _, length = lower_top
    return can_span(dist, length)

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    if rows == 0:
        return g
    cols = len(g[0])
    new_grid = [[0] * cols for _ in range(rows)]
    components = find_connected_components(g)
    non_red_comps = [(color, comp) for color, comp in components if color != 2]
    all_nonred_pos = set()
    for _, comp in non_red_comps:
        all_nonred_pos.update(comp)
    comp_with_reds = []
    for color, comp in non_red_comps:
        reds = get_attached_reds(g, comp, all_nonred_pos)
        full = comp.union(reds)
        comp_with_reds.append((color, comp, reds, full))
    # Find yellow
    yellow = None
    for item in comp_with_reds:
        if item[0] == 4:
            yellow = item
            break
    if yellow:
        color, comp, reds, full = yellow
        place_pixels(new_grid, comp, color)
        place_pixels(new_grid, reds, 2)
        yellow_min_r, yellow_max_r, yellow_min_c, yellow_max_c = get_component_bbox(comp)
        yellow_h = yellow_max_r - yellow_min_r + 1
        yellow_top_bar = get_top_bar(comp, yellow_min_c)
        yellow_second_row = yellow_min_r + 1
        yellow_second_bar_start = yellow_min_c if yellow_top_bar else yellow_min_c
        yellow_second_bar_end = yellow_max_c
        # Remove yellow from list
        comp_with_reds = [item for item in comp_with_reds if item[0] != 4]
    else:
        return new_grid  # no yellow, return empty or copy, but assume present
    # Build vertical chains from remaining
    vertical_chains = build_vertical_chains(comp_with_reds)
    # For upper vertical
    attached_upper = None
    best_length = 0
    best_score = float('inf')
    for chain in vertical_chains:
        if len(chain) > best_length or (len(chain) == best_length and 0 < best_score):
            bottom_item = chain[-1]
            bottom_color, bottom_comp, bottom_reds, _ = bottom_item
            bottom_min_r, _, bottom_min_c, _ = get_component_bbox(bottom_comp)
            bottom_bottom = get_bottom_two_red(bottom_min_r, bottom_min_c, bottom_reds)
            if bottom_bottom:
                _, _, _, dist = bottom_bottom
                if can_span(dist, yellow_top_bar[2] if yellow_top_bar else 0):
                    score = abs(dist + 1 - (yellow_top_bar[2] if yellow_top_bar else 0))
                    if len(chain) > best_length or score < best_score:
                        best_length = len(chain)
                        best_score = score
                        attached_upper = chain
    if attached_upper:
        # Place the chain above yellow
        current_min_r = yellow_min_r
        current_min_c = yellow_min_c
        current_bar_start_rel, current_bar_end_rel, _ = yellow_top_bar
        for k in range(len(attached_upper) - 1, -1, -1):  # place from bottom to top
            item = attached_upper[k]
            color, comp, reds, full = item
            min_r, max_r, min_c, max_c = get_component_bbox(comp)
            bottom_port = get_bottom_two_red(min_r, min_c, reds)
            if bottom_port:
                rel_r_red, rel_c1, rel_c2, dist = bottom_port
                target_r_red = current_min_r - 1
                target_c1 = current_min_c + current_bar_start_rel
                dr = target_r_red - (min_r + rel_r_red)
                dc = target_c1 - (min_c + rel_c1)
                translated_comp = translate_set(comp, dr, dc)
                translated_reds = translate_set(reds, dr, dc)
                place_pixels(new_grid, translated_comp, color)
                place_pixels(new_grid, translated_reds, 2)
                # Update current for next upper
                current_min_r = min_r + dr
                current_min_c = min_c + dc
                current_bar_start_rel, current_bar_end_rel, _ = get_top_bar(comp, min_c)
        # Remove the attached from comp_with_reds
        used_colors = {item[0] for item in attached_upper}
        comp_with_reds = [item for item in comp_with_reds if item[0] not in used_colors]
    # Now, remaining comps for side and horizontal
    remaining_comps = comp_with_reds
    # Find vertical chains from remaining
    vertical_chains = build_vertical_chains(remaining_comps)
    # For side attachments, select chains that have bottom side red at bottom row
    side_chains = []
    for chain in vertical_chains:
        if len(chain) > 0:
            bottom_item = chain[-1]
            b_color, b_comp, b_reds, b_full = bottom_item
            b_min_r, b_max_r, b_min_c, b_max_c = get_component_bbox(b_comp)
            left_red = get_side_bottom_red(b_comp, b_reds, b_min_r, b_min_c, b_max_r, b_max_c, 'left')
            right_red = get_side_bottom_red(b_comp, b_reds, b_min_r, b_min_c, b_max_r, b_max_c, 'right')
            if left_red or right_red:
                side_chains.append((chain, b_color, left_red is not None, right_red is not None))
    # Sort by average color, assign to left and right
    side_chains.sort(key=lambda x: x[1])
    left_chain = None
    right_chain = None
    if len(side_chains) >= 1:
        left_chain = side_chains[0][0]
    if len(side_chains) >= 2:
        right_chain = side_chains[1][0]
    # Place left chain
    if left_chain:
        # Use right red of bottom
        bottom_item = left_chain[-1]
        b_color, b_comp, b_reds, _ = bottom_item
        b_min_r, b_max_r, b_min_c, b_max_c = get_component_bbox(b_comp)
        right_red_rel_r, right_red_rel_c = get_side_bottom_red(b_comp, b_reds, b_min_r, b_min_c, b_max_r, b_max_c, 'right') or (0, 0)
        target_r = yellow_second_row
        target_c = yellow_min_c - 1
        input_red_r = b_min_r + right_red_rel_r
        input_red_c = b_min_c + right_red_rel_c
        dr = target_r - input_red_r
        dc = target_c - input_red_c
        # Place the bottom
        translated_comp = translate_set(b_comp, dr, dc)
        translated_reds = translate_set(b_reds, dr, dc)
        place_pixels(new_grid, translated_comp, b_color)
        place_pixels(new_grid, translated_reds, 2)
        # Place the rest of chain upward
        current_min_r = b_min_r + dr
        current_min_c = b_min_c + dc
        current_bar_start_rel, current_bar_end_rel, _ = get_top_bar(b_comp, b_min_c)
        for k in range(len(left_chain) - 2, -1, -1):
            item = left_chain[k]
            color, comp, reds, full = item
            min_r, max_r, min_c, max_c = get_component_bbox(comp)
            bottom_port = get_bottom_two_red(min_r, min_c, reds)
            if bottom_port:
                rel_r_red, rel_c1, rel_c2, dist = bottom_port
                target_r_red = current_min_r - 1
                target_c1 = current_min_c + current_bar_start_rel
                dr_chain = target_r_red - (min_r + rel_r_red)
                dc_chain = target_c1 - (min_c + rel_c1)
                t_comp = translate_set(comp, dr_chain, dc_chain)
                t_reds = translate_set(reds, dr_chain, dc_chain)
                place_pixels(new_grid, t_comp, color)
                place_pixels(new_grid, t_reds, 2)
                current_min_r = min_r + dr_chain
                current_min_c = min_c + dc_chain
                current_bar_start_rel, current_bar_end_rel, _ = get_top_bar(comp, min_c)
    # Similar for right chain, using left red, target_c = yellow_max_c +1
    if right_chain:
        bottom_item = right_chain[-1]
        b_color, b_comp, b_reds, _ = bottom_item
        b_min_r, b_max_r, b_min_c, b_max_c = get_component_bbox(b_comp)
        left_red_rel_r, left_red_rel_c = get_side_bottom_red(b_comp, b_reds, b_min_r, b_min_c, b_max_r, b_max_c, 'left') or (0, 0)
        target_r = yellow_second_row
        target_c = yellow_max_c + 1
        input_red_r = b_min_r + left_red_rel_r
        input_red_c = b_min_c + left_red_rel_c
        dr = target_r - input_red_r
        dc = target_c - input_red_c
        translated_comp = translate_set(b_comp, dr, dc)
        translated_reds = translate_set(b_reds, dr, dc)
        place_pixels(new_grid, translated_comp, b_color)
        place_pixels(new_grid, translated_reds, 2)
        current_min_r = b_min_r + dr
        current_min_c = b_min_c + dc
        current_bar_start_rel, current_bar_end_rel, _ = get_top_bar(b_comp, b_min_c)
        for k in range(len(right_chain) - 2, -1, -1):
            item = right_chain[k]
            color, comp, reds, full = item
            min_r, max_r, min_c, max_c = get_component_bbox(comp)
            bottom_port = get_bottom_two_red(min_r, min_c, reds)
            if bottom_port:
                rel_r_red, rel_c1, rel_c2, dist = bottom_port
                target_r_red = current_min_r - 1
                target_c1 = current_min_c + current_bar_start_rel
                dr_chain = target_r_red - (min_r + rel_r_red)
                dc_chain = target_c1 - (min_c + rel_c1)
                t_comp = translate_set(comp, dr_chain, dc_chain)
                t_reds = translate_set(reds, dr_chain, dc_chain)
                place_pixels(new_grid, t_comp, color)
                place_pixels(new_grid, t_reds, 2)
                current_min_r = min_r + dr_chain
                current_min_c = min_c + dc_chain
                current_bar_start_rel, current_bar_end_rel, _ = get_top_bar(comp, min_c)
    # Now, remaining comps for horizontal right chain
    remaining_indices = set(range(len(comp_with_reds)))
    # Remove used in side chains
    if left_chain:
        for item in left_chain:
            remaining_indices.discard(comp_with_reds.index(item))
    if right_chain:
        for item in right_chain:
            remaining_indices.discard(comp_with_reds.index(item))
    remaining_comps = [comp_with_reds[i] for i in remaining_indices]
    # Sort by color ascending
    remaining_comps.sort(key=lambda x: x[0])
    # Now, find if yellow has right red
    yellow_right_red_pos = [(r, c) for r, c in yellow[2] if c == yellow_max_c + 1 and r == yellow_second_row]
    if yellow_right_red_pos:
        attach_row = yellow_second_row
        attach_col = yellow_max_c
        rel_level = 1  # rel to yellow min_r
    else:
        # If no, perhaps no horizontal, or attach at second row without red
        attach_row = yellow_second_row
        attach_col = yellow_max_c
        rel_level = 1
    # Now, for the horizontal chain, start with first remaining if it has top bar
    current_attach_row = attach_row
    current_attach_col = attach_col
    for item in remaining_comps:
        color, comp, reds, full = item
        min_r, max_r, min_c, max_c = get_component_bbox(comp)
        top_bar = get_top_bar(comp, min_c)
        if top_bar:
            start_rel, end_rel, length = top_bar
            target_r = current_attach_row
            target_c = current_attach_col + 1
            dr = target_r - (min_r + 0)  # top rel 0
            dc = target_c - (min_c + start_rel)
            translated_comp = translate_set(comp, dr, dc)
            translated_reds = translate_set(reds, dr, dc)
            place_pixels(new_grid, translated_comp, color)
            place_pixels(new_grid, translated_reds, 2)
            # Update for next, find if this has right single red at rel r = 0 (top level) or the current rel_level adjusted
            new_min_r = min_r + dr
            new_min_c = min_c + dc
            right_red_rel = get_side_bottom_red(comp, reds, min_r, min_c, max_r, max_c, 'right')  # reuse for any row
            if right_red_rel:
                rel_r_red, rel_c_red = right_red_rel
                if rel_r_red == 0:  # at top level
                    current_attach_row = new_min_r + rel_r_red
                    current_attach_col = new_min_c + max_c - min_c + rel_c_red  # w
                else:
                    # if not at top, perhaps skip continuation or adjust
                    current_attach_row += 1  # as in train1
                    current_attach_col = new_min_c + max_c - min_c
            else:
                current_attach_row += 1
                current_attach_col = new_min_c + max_c - min_c
    return new_grid
```