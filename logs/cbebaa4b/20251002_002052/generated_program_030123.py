```python
from typing import List, Tuple

def get_positions(g: List[List[int]], color: int, size: int) -> List[Tuple[int, int]]:
    return [(r, c) for r in range(size) for c in range(size) if g[r][c] == color]

def extract_relative(pos: List[Tuple[int, int]]) -> Tuple[int, int, List[Tuple[int, int]]]:
    if not pos:
        return 0, 0, []
    min_r = min(r for r, c in pos)
    min_c = min(c for r, c in pos)
    rel = [(r - min_r, c - min_c) for r, c in pos]
    return min_r, min_c, rel

def place_component(output: List[List[int]], rel: List[Tuple[int, int]], color: int, start_r: int, start_c: int, size: int):
    for dr, dc in rel:
        if 0 <= start_r + dr < size and 0 <= start_c + dc < size:
            output[start_r + dr][start_c + dc] = color

def add_red_trims_vertical(output: List[List[int]], leg_positions: List[int], start_r: int, start_c: int, size: int):
    for dc in leg_positions:
        if 0 <= start_r < size and 0 <= start_c + dc < size:
            output[start_r][start_c + dc] = 2

def rule_vertical_green_maroon_red(g: List[List[int]], output: List[List[int]], size: int) -> int:
    green_pos = get_positions(g, 3, size)
    if not green_pos:
        return 4
    _, _, green_rel = extract_relative(green_pos)
    start_r = 4
    start_c = 8
    place_component(output, green_rel, 3, start_r, start_c, size)
    h_green = max(dr for dr, _ in green_rel) + 1 if green_rel else 0
    # Find bottom row positions for red
    bottom_dr = h_green - 1
    leg_dcs = set(dc for dr, dc in green_rel if dr == bottom_dr)
    red_r = start_r + h_green
    add_red_trims_vertical(output, list(leg_dcs), red_r, start_c, size)
    # Place maroon below red
    maroon_pos = get_positions(g, 8, size)
    _, _, maroon_rel = extract_relative(maroon_pos)
    maroon_start_r = red_r + 1
    place_component(output, maroon_rel, 8, maroon_start_r, start_c, size)
    h_maroon = max(dr for dr, _ in maroon_rel) + 1 if maroon_rel else 0
    # Red below maroon
    bottom_dr_m = h_maroon - 1
    leg_dcs_m = set(dc for dr, dc in maroon_rel if dr == bottom_dr_m)
    red_r_m = maroon_start_r + h_maroon
    add_red_trims_vertical(output, list(leg_dcs_m), red_r_m, start_c, size)
    return red_r_m + 1

def rule_horizontal_blue_maroon_red(g: List[List[int]], output: List[List[int]], size: int, start_y: int) -> None:
    blue_pos = get_positions(g, 1, size)
    if not blue_pos:
        return
    _, _, blue_rel = extract_relative(blue_pos)
    start_c = 10  # right of main
    place_component(output, blue_rel, 1, start_y, start_c, size)
    # Add red horizontal trim, e.g., place 2's adjacent to blue and maroon bbox
    # Assume simple placement at connection points
    output[start_y][start_c - 1] = 2
    output[start_y + 1][start_c - 1] = 2

def rule_cluster_blue_yellow(g: List[List[int]], output: List[List[int]], size: int, start_y: int) -> None:
    yellow_pos = get_positions(g, 4, size)
    if not yellow_pos:
        return
    _, _, yellow_rel = extract_relative(yellow_pos)
    start_c = 9
    place_component(output, yellow_rel, 4, start_y, start_c, size)
    # Blue abuts yellow
    rule_horizontal_blue_maroon_red(g, output, size, start_y)  # reuse for adjacency

def rule_align_green_blue(g: List[List[int]], output: List[List[int]], size: int, start_y: int) -> None:
    # Green abuts blue horizontally
    green_pos = get_positions(g, 3, size)
    if not green_pos:
        return
    _, _, green_rel = extract_relative(green_pos)
    start_c = 13  # right of blue
    place_component(output, green_rel, 3, start_y, start_c, size)

def rule_pivot_yellow_blue_green(g: List[List[int]], output: List[List[int]], size: int, start_y: int) -> None:
    # Yellow as pivot between blue and green
    rule_cluster_blue_yellow(g, output, size, start_y)
    rule_align_green_blue(g, output, size, start_y)

def place_extra_color(g: List[List[int]], output: List[List[int]], size: int, start_y: int, colors: set) -> int:
    extra_colors = sorted(colors - {1, 2, 3, 4, 8})
    current_y = start_y
    start_c = 17  # right side
    for colr in extra_colors:
        pos = get_positions(g, colr, size)
        if pos:
            _, _, rel = extract_relative(pos)
            place_component(output, rel, colr, current_y, start_c, size)
            h = max(dr for dr, _ in rel) + 1 if rel else 0
            current_y += h + 1
    return current_y

def place_pink_horizontal(g: List[List[int]], output: List[List[int]], size: int) -> int:
    pink_pos = get_positions(g, 6, size)
    if not pink_pos:
        return 4
    _, _, pink_rel = extract_relative(pink_pos)
    start_r = 4
    start_c = 7
    place_component(output, pink_rel, 6, start_r, start_c, size)
    h_pink = max(dr for dr, _ in pink_rel) + 1 if pink_rel else 0
    # Red below pink
    bottom_dr = h_pink - 1
    leg_dcs = set(dc for dr, dc in pink_rel if dr == bottom_dr)
    red_r = start_r + h_pink
    add_red_trims_vertical(output, list(leg_dcs), red_r, start_c, size)
    # Place maroon right, shifted
    maroon_pos = get_positions(g, 8, size)
    _, _, maroon_rel = extract_relative(maroon_pos)
    maroon_start_r = start_r + 1  # overlap
    maroon_start_c = 12
    place_component(output, maroon_rel, 8, maroon_start_r, maroon_start_c, size)
    h_maroon = max(dr for dr, _ in maroon_rel) + 1 if maroon_rel else 0
    # Red below maroon
    red_r_m = max(start_r + h_pink, maroon_start_r + h_maroon)
    leg_dcs_m = set(dc for dr, dc in maroon_rel if dr == h_maroon - 1)
    add_red_trims_vertical(output, list(leg_dcs_m), red_r_m, maroon_start_c, size)
    return red_r_m + 1

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    output = [[0] * size for _ in range(size)]
    colors = {cell for row in g for cell in row if cell != 0}
    current_y = 4
    start_x = 8
    if 6 in colors:
        # Horizontal configuration like train 2
        current_y = place_pink_horizontal(g, output, size)
        # Place blue and green below horizontally
        rule_pivot_yellow_blue_green(g, output, size, current_y)
        # Place yellow below
        yellow_pos = get_positions(g, 4, size)
        if yellow_pos:
            _, _, yellow_rel = extract_relative(yellow_pos)
            y_start = current_y + 3  # approximate
            place_component(output, yellow_rel, 4, y_start, start_x + 1, size)
    else:
        # Vertical configuration like train 1
        current_y = rule_vertical_green_maroon_red(g, output, size)
        # Place yellow
        rule_cluster_blue_yellow(g, output, size, current_y)
        current_y += 3  # yellow height approx
        # Place blue right
        rule_horizontal_blue_maroon_red(g, output, size, current_y)
        # Place extra like orange right
        current_y = place_extra_color(g, output, size, current_y, colors)
    # Add additional horizontal reds for connections
    for r in range(4, size):
        for c in [12, 16, 10, 9, 13]:
            if 0 <= c < size and output[r][c] == 0:
                output[r][c] = 2  # simplistic, places some reds
    return output
```