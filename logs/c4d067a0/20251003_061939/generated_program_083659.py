```python
from typing import List, Tuple

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    size = len(g)
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

def get_block_ranges(g: List[List[int]], bg: int, size: int) -> List[Tuple[int, int]]:
    ranges_set = set()
    for i in range(size):
        j = 0
        while j < size:
            if g[i][j] == bg:
                j += 1
                continue
            start = j
            while j < size and g[i][j] == g[i][start]:
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

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    out = copy_grid(g)
    bg = get_background(g)
    tracks = get_tracks(g, bg, size)
    if not tracks:
        return out
    signal_rows = get_signal_rows(g, tracks, bg, size)
    if not signal_rows:
        return out
    signal_colors = get_signal_colors(g, signal_rows, tracks, bg)
    block_ranges = get_block_ranges(g, bg, size)
    found_anchor = False
    h = None
    s = None
    k = None
    distance_h = None
    if block_ranges:
        widths = {end - start + 1 for start, end in block_ranges}
        if len(widths) == 1:
            w = next(iter(widths))
            hh = w
            for ss in range(size - hh + 1):
                block_colors = []
                valid = True
                for start, end in block_ranges:
                    if start >= size or end >= size:
                        valid = False
                        break
                    c = g[ss][start]
                    if c == bg:
                        valid = False
                        break
                    uniform = True
                    for r in range(ss, ss + hh):
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
                            found_anchor = True
                            s = ss
                            k = kk
                            distance_h = block_ranges[1][0] - block_ranges[0][0] if len(block_ranges) > 1 else 2 * hh - 1
                            h = hh
                            break
                if found_anchor:
                    break
    if not found_anchor:
        h = signal_rows[1] - signal_rows[0] if len(signal_rows) >= 2 else 2
        m = max((len(sc) for sc in signal_colors), default=0)
        if m == 0:
            return out
        distance_h = 2 * h + 1
        first_col = size // 2
        block_ranges = []
        current = first_col
        for _ in range(m):
            end = current + h - 1
            if end >= size:
                break
            block_ranges.append((current, end))
            current += distance_h
        step_v = 2 * h + 1
        base = size // 2 - h + 1
    else:
        step_v = 2 * h - 1
        base = s - k * step_v
    for i in range(len(signal_rows)):
        if found_anchor and i == k:
            continue
        target_s = base + i * step_v
        if target_s < 0 or target_s + h > size:
            continue
        sc = signal_colors[i]
        temp_ranges = list(block_ranges)
        while len(temp_ranges) < len(sc):
            last_start = temp_ranges[-1][0]
            new_start = last_start + distance_h
            new_end = new_start + h - 1
            if new_end >= size:
                break
            temp_ranges.append((new_start, new_end))
        num = min(len(sc), len(temp_ranges))
        colors_use = sc[:num]
        for bb in range(num):
            cs, ce = temp_ranges[bb]
            c = colors_use[bb]
            for r in range(max(0, target_s), min(size, target_s + h)):
                for cc in range(max(0, cs), min(size, ce + 1)):
                    if out[r][cc] == bg:
                        out[r][cc] = c
    return out
```