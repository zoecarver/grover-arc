```python
def get_background_color(g):
    counts = [0] * 16
    for row in g[6:24]:
        for cell in row:
            if cell != 0 and cell != 5:
                counts[cell] += 1
    max_count = max(counts)
    for c in range(16):
        if counts[c] == max_count:
            return c
    return 3  # default

def shift_content(g, bg):
    width = len(g[0])
    height_out = 19
    grid = [[bg for _ in range(width)] for _ in range(height_out)]
    for i in range(6, 24):
        out_i = i - 6
        if out_i >= height_out:
            break
        for j in range(width):
            cell = g[i][j]
            if cell != 0 and cell != 5:
                grid[out_i][j] = cell
    # copy last row
    if height_out > 0:
        grid[height_out - 1] = grid[height_out - 2][:]
    return grid

def get_maroon_pos(g):
    min_i = 100
    max_i = -1
    min_j = 100
    max_j = -1
    width = len(g[0])
    for i in range(6, 24):
        for j in range(width):
            if g[i][j] == 8:
                min_i = min(min_i, i)
                max_i = max(max_i, i)
                min_j = min(min_j, j)
                max_j = max(max_j, j)
    if min_i == 100:
        return 0, 0, 0, 0  # default if none
    return min_j, min_i - 6, max_j, max_i - 6

def calculate_span(grid, bg, y1, y2, width):
    # leftmost non-bg right +1
    left_start = width
    for j in range(width):
        is_non_bg = any(grid[i][j] != bg for i in range(max(0, y1), min(19, y2 + 1)))
        if is_non_bg:
            left_start = min(left_start, j)
    start_span = left_start + 1 if left_start < width else 0
    start_span = max(0, start_span)
    # rightmost non-bg left -1
    right_end = -1
    for j in range(width - 1, -1, -1):
        is_non_bg = any(grid[i][j] != bg for i in range(max(0, y1), min(19, y2 + 1)))
        if is_non_bg:
            right_end = max(right_end, j)
    end_span = right_end - 1 if right_end >= 0 else width - 1
    end_span = min(width - 1, end_span)
    if start_span > end_span:
        start_span = 0
        end_span = width - 1
    return start_span, end_span

def find_left_start_end(grid, bg, start, width):
    left_start_y = 100
    left_end_y = -1
    for i in range(19):
        for j in range(start):
            if grid[i][j] != bg:
                left_start_y = min(left_start_y, i)
                left_end_y = max(left_end_y, i)
                break
    return left_start_y, left_end_y

def find_right_end_y(grid, bg, end, width):
    right_end_y = -1
    for i in range(19):
        for j in range(end + 1, width):
            if grid[i][j] != bg:
                right_end_y = max(right_end_y, i)
                break
    return right_end_y

def program(g):
    bg = get_background_color(g)
    grid = shift_content(g, bg)
    width = len(g[0])
    x1, y1, x2, y2 = get_maroon_pos(g)
    if y1 < 0 or y2 >= 19:
        return grid  # edge case
    maroon_width = x2 - x1 + 1
    maroon_height = y2 - y1 + 1
    start, end = calculate_span(grid, bg, y1, y2, width)
    right_x = max(0, end - maroon_width + 1)

    left_start_y, left_end_y = find_left_start_end(grid, bg, start, width)
    right_end_y = find_right_end_y(grid, bg, end, width)

    # up verticals
    # internal up
    for j in range(max(0, x1), min(width, x2 + 1)):
        for i in range(0, y1):
            if grid[i][j] == bg:
                grid[i][j] = 8
    # right up
    for j in range(max(0, right_x), min(width, right_x + maroon_width)):
        for i in range(0, y1):
            if grid[i][j] == bg:
                grid[i][j] = 8
    # left up if condition
    place_left_up = left_start_y < 100 and (y1 - left_start_y) <= maroon_width + 1
    if place_left_up:
        for j in range(max(0, start), min(width, start + maroon_width)):
            for i in range(0, y1):
                if grid[i][j] == bg:
                    grid[i][j] = 8

    # horizontal shorts and connects
    pos_list = []
    pos_list.append((start, start + maroon_width - 1))
    pos_list.append((x1, x2))
    pos_list.append((right_x, right_x + maroon_width - 1))
    # place shorts
    for px1, px2 in pos_list:
        for j in range(max(0, px1), min(width, px2 + 1)):
            for i in range(max(0, y1), min(19, y2 + 1)):
                if grid[i][j] == bg:
                    grid[i][j] = 8
    # connect gaps if no block above
    sorted_pos = sorted([p for p in pos_list if p[0] <= p[1]], key=lambda p: p[0])
    for k in range(len(sorted_pos) - 1):
        g_start = sorted_pos[k][1] + 1
        g_end = sorted_pos[k + 1][0] - 1
        if g_start > g_end:
            continue
        can_connect = True
        for ii in range(0, y1):
            for jj in range(g_start, g_end + 1):
                if jj >= width or grid[ii][jj] != bg:
                    can_connect = False
                    break
            if not can_connect:
                break
        if can_connect:
            for jj in range(g_start, g_end + 1):
                for ii in range(max(0, y1), min(19, y2 + 1)):
                    if jj < width and grid[ii][jj] == bg:
                        grid[ii][jj] = 8

    # down
    down_y1 = y2 + 1
    down_y2 = 13
    if down_y1 <= down_y2:
        down_pos = []
        place_left_down = left_end_y > y2 and (left_end_y - y2 >= maroon_width + 1)
        if place_left_down:
            l_x1 = start
            l_x2 = min(width - 1, start + maroon_width - 1)
            down_pos.append((l_x1, l_x2))
            for j in range(l_x1, l_x2 + 1):
                for i in range(down_y1, min(19, down_y2 + 1)):
                    if grid[i][j] == bg:
                        grid[i][j] = 8
        # internal
        i_x1 = x1
        i_x2 = x2
        down_pos.append((i_x1, i_x2))
        for j in range(max(0, i_x1), min(width, i_x2 + 1)):
            for i in range(down_y1, min(19, down_y2 + 1)):
                if grid[i][j] == bg:
                    grid[i][j] = 8
        # down connect positions include right
        down_connect_pos = down_pos + [(right_x, min(width - 1, right_x + maroon_width - 1))]
        down_height = down_y2 - down_y1 + 1
        if down_height == maroon_height:
            sorted_down_pos = sorted(down_connect_pos, key=lambda p: p[0])
            c_min_x = sorted_down_pos[0][0]
            c_max_x = sorted_down_pos[-1][1]
            for i in range(down_y1, min(19, down_y2 + 1)):
                for j in range(max(0, c_min_x), min(width, c_max_x + 1)):
                    if grid[i][j] == bg:
                        grid[i][j] = 8

    # bottom full
    bottom_y1 = 14
    bottom_y2 = min(18, 14 + maroon_height - 1)
    if down_pos:
        start_full = min(p[0] for p in down_pos)
        if right_end_y <= 13:
            end_full = width - 1
        else:
            end_full = max(p[1] for p in down_pos)
    else:
        start_full = x1
        end_full = x2
    for i in range(max(0, bottom_y1), min(19, bottom_y2 + 1)):
        for j in range(max(0, start_full), min(width, end_full + 1)):
            if grid[i][j] == bg:
                grid[i][j] = 8

    return grid
```