```python
from typing import List

def get_background(g: List[List[int]]) -> int:
    size = len(g)
    for row in g:
        if len(row) == size and all(x == row[0] for x in row):
            return row[0]
    return g[0][0]

def get_tracks(g: List[List[int]], bg: int) -> List[int]:
    size = len(g)
    tracks = []
    for j in range(1, size, 2):
        has_signal = False
        max_consec = 0
        consec = 0
        for i in range(size):
            if g[i][j] != bg:
                has_signal = True
                consec += 1
                max_consec = max(max_consec, consec)
            else:
                consec = 0
        if has_signal and max_consec == 1:
            tracks.append(j)
    return tracks

def get_signal_rows(g: List[List[int]], tracks: List[int], bg: int) -> List[int]:
    size = len(g)
    signal_set = set()
    for i in range(size):
        for j in tracks:
            if g[i][j] != bg:
                signal_set.add(i)
                break
    return sorted(list(signal_set))

def get_signal_colors(g: List[List[int]], signal_rows: List[int], tracks: List[int], bg: int) -> List[List[int]]:
    colors = []
    for i in signal_rows:
        row_colors = [g[i][j] for j in tracks if g[i][j] != bg]
        colors.append(row_colors)
    return colors

def get_block_ranges(g: List[List[int]], bg: int) -> List[tuple]:
    size = len(g)
    ranges_set = set()
    for i in range(size):
        j = 0
        while j < size:
            if g[i][j] == bg:
                j += 1
                continue
            start = j
            color = g[i][j]
            while j < size and g[i][j] == color:
                j += 1
            end = j - 1
            if end - start + 1 >= 2:
                ranges_set.add((start, end))
    return sorted(list(ranges_set))

def is_subsequence(a: List[int], b: List[int]) -> bool:
    if not a:
        return True
    i = 0
    for val in b:
        if i < len(a) and val == a[i]:
            i += 1
            if i == len(a):
                return True
    return i == len(a)

def find_anchor(g: List[List[int]], block_ranges: List[tuple], h: int, signal_colors: List[List[int]], bg: int, size: int) -> tuple:
    for s in range(size - h + 1):
        block_colors = []
        valid = True
        for start, end in block_ranges:
            if start >= size or end >= size:
                valid = False
                break
            c = g[s][start]
            if c == bg:
                valid = False
                break
            uniform = True
            for r in range(s, s + h):
                for cc in range(start, end + 1):
                    if cc >= size or g[r][cc] != c:
                        uniform = False
                        break
                if not uniform:
                    break
            if not uniform:
                valid = False
                break
            block_colors.append(c)
        if valid and block_colors:
            for kk, sc in enumerate(signal_colors):
                if is_subsequence(block_colors, sc):
                    return s, kk
    return -1, -1

def get_gap(block_ranges: List[tuple]) -> int:
    if len(block_ranges) < 2:
        return 0
    return block_ranges[1][0] - block_ranges[0][1] - 1

def get_temp_ranges(block_ranges: List[tuple], num: int, gap: int, h: int, size: int) -> List[tuple]:
    m = len(block_ranges)
    if num <= m:
        return block_ranges[:num]
    temp = list(block_ranges)
    last_end = block_ranges[-1][1]
    for _ in range(m, num):
        new_start = last_end + 1 + gap
        if new_start + h - 1 >= size:
            break
        new_end = new_start + h - 1
        temp.append((new_start, new_end))
        last_end = new_end
    return temp[:num]

def place_blocks(out: List[List[int]], start_r: int, colors: List[int], temp_ranges: List[tuple], h: int, bg: int, size: int):
    num = min(len(colors), len(temp_ranges))
    for bb in range(num):
        cs, ce = temp_ranges[bb]
        c = colors[bb]
        for r in range(start_r, min(start_r + h, size)):
            for cc in range(cs, min(ce + 1, size)):
                if out[r][cc] == bg:
                    out[r][cc] = c

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    bg = get_background(g)
    tracks = get_tracks(g, bg)
    if not tracks:
        return [row[:] for row in g]
    signal_rows = get_signal_rows(g, tracks, bg)
    if not signal_rows:
        return [row[:] for row in g]
    signal_colors = get_signal_colors(g, signal_rows, tracks, bg)
    block_ranges = get_block_ranges(g, bg)
    if not block_ranges:
        return [row[:] for row in g]
    h = block_ranges[0][1] - block_ranges[0][0] + 1
    for start, end in block_ranges:
        if end - start + 1 != h:
            return [row[:] for row in g]
    s_anchor, k_anchor = find_anchor(g, block_ranges, h, signal_colors, bg, size)
    if s_anchor == -1:
        return [row[:] for row in g]
    out = [row[:] for row in g]
    gap = get_gap(block_ranges)
    initial_m = len(block_ranges)
    base_df = 2 * h - 1
    base_db = 2 * h + 1
    # forward
    previous_num = len(signal_colors[k_anchor])
    current_s = s_anchor
    current_k = k_anchor
    for ii in range(1, len(signal_rows) - k_anchor):
        next_k = current_k + 1
        next_num = len(signal_colors[next_k])
        add = max(0, next_num - previous_num)
        step = base_df + add
        next_s = current_s + step
        if next_s < 0 or next_s + h > size:
            break
        temp_ranges = get_temp_ranges(block_ranges, next_num, gap, h, size)
        place_blocks(out, next_s, signal_colors[next_k], temp_ranges, h, bg, size)
        current_s = next_s
        current_k = next_k
        previous_num = next_num
    # backward
    previous_num = len(signal_colors[k_anchor])
    current_s = s_anchor
    current_k = k_anchor
    for ii in range(1, k_anchor + 1):
        next_k = current_k - 1
        next_num = len(signal_colors[next_k])
        add = max(0, next_num - previous_num)
        step = base_db + add
        next_s = current_s - step
        if next_s < 0 or next_s + h > size:
            break
        temp_ranges = get_temp_ranges(block_ranges, next_num, gap, h, size)
        place_blocks(out, next_s, signal_colors[next_k], temp_ranges, h, bg, size)
        current_s = next_s
        current_k = next_k
        previous_num = next_num
    return out
```