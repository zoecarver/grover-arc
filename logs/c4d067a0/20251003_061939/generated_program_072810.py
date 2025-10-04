```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    size = len(g)
    for row in g:
        if len(set(row)) == 1:
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
                if consec > max_consec:
                    max_consec = consec
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

def find_anchor(g: List[List[int]], block_ranges: List[Tuple[int, int]], signal_colors: List[List[int]], h: int, size: int) -> Tuple[int, int, bool]:
    for s in range(size - h + 1):
        block_cols = []
        valid = True
        for br in block_ranges:
            cs, ce = br
            the_color = None
            for r in range(s, s + h):
                row_color = None
                row_valid = True
                for c in range(cs, ce + 1):
                    cell = g[r][c]
                    if cell == 0 or cell == g[0][0] and g[0][0] == 0:  # avoid bg check here, but assume
                        if cell != bg: wait no, in check we already have !=bg implicitly
                    if cell == bg:
                        row_valid = False
                        break
                    if row_color is None:
                        row_color = cell
                    elif cell != row_color:
                        row_valid = False
                        break
                if not row_valid:
                    valid = False
                    break
                if the_color is None:
                    the_color = row_color
                elif row_color != the_color:
                    valid = False
                    break
            if not valid:
                break
            block_cols.append(the_color)
        if valid and block_cols:
            for k in range(len(signal_colors)):
                if is_subsequence(block_cols, signal_colors[k]):
                    return s, k, True
    return 0, 0, False

def get_gap(block_ranges: List[Tuple[int, int]]) -> int:
    if len(block_ranges) < 2:
        return 0
    return block_ranges[1][0] - block_ranges[0][1] - 1

def extend_ranges_for_placement(block_ranges: List[Tuple[int, int]], h: int, gap: int, needed: int, size: int) -> List[Tuple[int, int]]:
    curr_ranges = list(block_ranges)
    while len(curr_ranges) < needed:
        last_end = curr_ranges[-1][1]
        new_start = last_end + 1 + gap
        new_end = new_start + h - 1
        if new_end >= size:
            break
        curr_ranges.append((new_start, new_end))
    return curr_ranges

def place_at(out: List[List[int]], pos: int, h: int, colors: List[int], ranges: List[Tuple[int, int]], bg: int, size: int):
    if pos < 0 or pos + h > size:
        return
    num = min(len(colors), len(ranges))
    for ii in range(num):
        c = colors[ii]
        cs, ce = ranges[ii]
        for r in range(pos, pos + h):
            for cc in range(cs, ce + 1):
                if out[r][cc] == bg:
                    out[r][cc] = c

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    bg = get_bg(g)
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
    for br in block_ranges:
        if br[1] - br[0] + 1 != h:
            return [row[:] for row in g]  # inconsistent, but assume not
    s, kk, found = find_anchor(g, block_ranges, signal_colors, h, size)
    if not found:
        return [row[:] for row in g]
    out = [row[:] for row in g]
    df = 2 * h - 1
    db = 2 * h + 1
    gap = get_gap(block_ranges)
    num_blocks = len(block_ranges)
    for j in range(len(signal_colors)):
        if j == kk:
            continue
        delta = j - kk
        dstep = df if delta > 0 else db
        pos = s + delta * dstep
        colors_j = signal_colors[j]
        curr_ranges = extend_ranges_for_placement(block_ranges, h, gap, len(colors_j), size)
        place_at(out, pos, h, colors_j, curr_ranges, bg, size)
    return out
```