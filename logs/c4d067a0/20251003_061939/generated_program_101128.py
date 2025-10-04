```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    size = len(g)
    if size == 0:
        return 0
    for row in g:
        if len(set(row)) == 1:
            return row[0]
    return g[0][0]

def get_tracks(g: List[List[int]], bg: int, size: int) -> List[int]:
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

def get_signal_rows(g: List[List[int]], tracks: List[int], bg: int, size: int) -> List[int]:
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

def get_block_ranges(g: List[List[int]], bg: int, size: int) -> List[Tuple[int, int]]:
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

def find_anchor(g: List[List[int]], block_ranges: List[Tuple[int, int]], h: int, signal_colors: List[List[int]], bg: int, size: int) -> Tuple[int, int]:
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

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def extend_ranges(block_ranges: List[Tuple[int, int]], num_needed: int, diff_start: int, h: int, size: int) -> List[Tuple[int, int]]:
    temp = list(block_ranges)
    while len(temp) < num_needed:
        last_start = temp[-1][0]
        new_start = last_start + diff_start
        if new_start + h - 1 >= size:
            break
        new_end = new_start + h - 1
        temp.append((new_start, new_end))
    return temp

def place_blocks(out: List[List[int]], target_start: int, h: int, colors: List[int], temp_ranges: List[Tuple[int, int]], bg: int, size: int):
    num = min(len(colors), len(temp_ranges))
    for jj in range(num):
        c = colors[jj]
        st, en = temp_ranges[jj]
        for r in range(target_start, min(target_start + h, size)):
            for cc in range(st, min(en + 1, size)):
                if out[r][cc] == bg:
                    out[r][cc] = c

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    bg = get_background(g)
    tracks = get_tracks(g, bg, size)
    signal_rows = get_signal_rows(g, tracks, bg, size)
    signal_colors = get_signal_colors(g, signal_rows, tracks, bg)
    if not signal_colors:
        return copy_grid(g)
    block_ranges = get_block_ranges(g, bg, size)
    if not block_ranges:
        h = 2
        first_start = size // 2 - (h - 1) // 2
        diff_start = 2 * h + 1
        step_v = 2 * h + 1
        start_row = size // 2 - h // 2
        out = copy_grid(g)
        for ii in range(len(signal_colors)):
            sc = signal_colors[ii]
            if not sc:
                continue
            num = len(sc)
            temp_ranges = []
            curr_start = first_start
            for _ in range(num):
                st = curr_start
                en = st + h - 1
                if en >= size:
                    break
                temp_ranges.append((st, en))
                curr_start += diff_start
            target_r = start_row + ii * step_v
            if target_r >= 0 and target_r + h <= size:
                place_blocks(out, target_r, h, sc, temp_ranges, bg, size)
        return out
    widths = {en - st + 1 for st, en in block_ranges}
    if len(widths) != 1:
        return copy_grid(g)
    h = next(iter(widths))
    anchor_s, anchor_k = find_anchor(g, block_ranges, h, signal_colors, bg, size)
    if anchor_s == -1:
        h = 2
        first_start = size // 2 - (h - 1) // 2
        diff_start = 2 * h + 1
        step_v = 2 * h + 1
        start_row = size // 2 - h // 2
        out = copy_grid(g)
        for ii in range(len(signal_colors)):
            sc = signal_colors[ii]
            if not sc:
                continue
            num = len(sc)
            temp_ranges = []
            curr_start = first_start
            for _ in range(num):
                st = curr_start
                en = st + h - 1
                if en >= size:
                    break
                temp_ranges.append((st, en))
                curr_start += diff_start
            target_r = start_row + ii * step_v
            if target_r >= 0 and target_r + h <= size:
                place_blocks(out, target_r, h, sc, temp_ranges, bg, size)
        return out
    out = copy_grid(g)
    if len(block_ranges) > 1:
        diff_start = block_ranges[1][0] - block_ranges[0][0]
    else:
        diff_start = 2 * h - 1
    step_f = 2 * h - 1
    step_b = 2 * h + 1
    # place for anchor as well, to fill if partial
    sc_anchor = signal_colors[anchor_k]
    num_anchor = len(sc_anchor)
    temp_anchor = extend_ranges(block_ranges, num_anchor, diff_start, h, size)
    place_blocks(out, anchor_s, h, sc_anchor, temp_anchor, bg, size)
    for ii in range(len(signal_colors)):
        if ii == anchor_k:
            continue
        sc = signal_colors[ii]
        num = len(sc)
        delta = ii - anchor_k
        if delta > 0:
            step = step_f
        else:
            step = step_b
        target_s = anchor_s + delta * step
        if target_s < 0 or target_s + h > size:
            continue
        temp_ranges = extend_ranges(block_ranges, num, diff_start, h, size)
        place_blocks(out, target_s, h, sc, temp_ranges, bg, size)
    return out
```