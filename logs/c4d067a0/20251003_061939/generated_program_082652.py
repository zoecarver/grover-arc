```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    for row in g:
        if all(x == row[0] for x in row):
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

def get_block_ranges(g: List[List[int]], bg: int) -> List[Tuple[int, int]]:
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
                    if g[r][cc] != c:
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

def get_temp_ranges(block_ranges: List[Tuple[int, int]], num_place: int, gap: int, h: int, size: int) -> List[Tuple[int, int]]:
    num_anchor = len(block_ranges)
    if num_place <= num_anchor:
        return block_ranges[:num_place]
    temp = list(block_ranges)
    if not temp:
        return []
    last_end = temp[-1][1]
    for _ in range(num_anchor, num_place):
        next_start = last_end + 1 + gap
        if next_start + h - 1 >= size:
            break
        next_end = next_start + h - 1
        temp.append((next_start, next_end))
        last_end = next_end
    return temp

def place_blocks(out: List[List[int]], place_s: int, h: int, temp_ranges: List[Tuple[int, int]], colors: List[int], bg: int, size: int):
    num = min(len(colors), len(temp_ranges))
    for bb in range(num):
        cs, ce = temp_ranges[bb]
        c = colors[bb]
        for r in range(place_s, place_s + h):
            if r >= size:
                break
            for cc in range(cs, ce + 1):
                if cc >= size:
                    break
                if out[r][cc] == bg:
                    out[r][cc] = c

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    bg = get_background(g)
    tracks = get_tracks(g, bg, size)
    signal_rows = get_signal_rows(g, tracks, bg)
    signal_colors = get_signal_colors(g, signal_rows, tracks, bg)
    block_ranges = get_block_ranges(g, bg)
    if not block_ranges:
        return copy_grid(g)
    w = block_ranges[0][1] - block_ranges[0][0] + 1
    if any(br[1] - br[0] + 1 != w for br in block_ranges):
        return copy_grid(g)
    h = w
    s, k = find_anchor(g, block_ranges, h, signal_colors, bg, size)
    if s == -1:
        return copy_grid(g)
    num_anchor = len(block_ranges)
    gap = block_ranges[1][0] - block_ranges[0][1] - 1 if num_anchor >= 2 else 0
    out = copy_grid(g)
    for j in range(len(signal_colors)):
        if j == k:
            continue
        colors_j = signal_colors[j]
        num_place = len(colors_j)
        if num_place == 0:
            continue
        delta_idx = j - k
        if delta_idx > 0:
            step = 2 * h - 1
            place_s = s + delta_idx * step
        else:
            step = 2 * h + 1
            place_s = s + delta_idx * step
        if place_s < 0 or place_s + h > size:
            continue
        temp_ranges = get_temp_ranges(block_ranges, num_place, gap, h, size)
        place_blocks(out, place_s, h, temp_ranges, colors_j, bg, size)
    return out
```