```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_tracks(g: List[List[int]], bg: int, size: int) -> List[int]:
    tracks = []
    for j in range(1, size, 2):
        has_signal = any(g[i][j] != bg for i in range(size))
        max_consec = 0
        consec = 0
        for i in range(size):
            if g[i][j] != bg:
                consec += 1
                max_consec = max(max_consec, consec)
            else:
                consec = 0
        if has_signal and max_consec == 1:
            tracks.append(j)
    return tracks

def get_signal_rows(g: List[List[int]], tracks: List[int], bg: int, size: int) -> List[int]:
    signal_set = set()
    for r in range(size):
        if any(g[r][c] != bg for c in tracks):
            signal_set.add(r)
    return sorted(signal_set)

def get_signal_colors(g: List[List[int]], signal_rows: List[int], tracks: List[int], bg: int) -> List[List[int]]:
    colors = []
    for r in signal_rows:
        row_colors = [g[r][c] for c in tracks if g[r][c] != bg and g[r][c] != 8]
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
            c = g[i][j]
            while j < size and g[i][j] == c:
                j += 1
            end = j - 1
            if end - start + 1 >= 2:
                ranges_set.add((start, end))
            j += 1
    return sorted(ranges_set)

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

def find_anchor(g: List[List[int]], block_ranges: List[Tuple[int, int]], signal_colors: List[List[int]], bg: int, size: int) -> Tuple[int, int, int]:
    max_h = min(size // 2, 10)
    for h in range(max_h, 1, -1):
        for s in range(size - h + 1):
            block_colors = []
            valid = True
            for start, end in block_ranges:
                if end >= size:
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
                        return s, h, kk
    return -1, 0, -1

def compute_gap(block_ranges: List[Tuple[int, int]], w: int) -> int:
    starts = [s for s, _ in block_ranges]
    if len(starts) >= 2:
        return starts[1] - starts[0] - w
    return 1

def extend_block_ranges(block_ranges: List[Tuple[int, int]], num_needed: int, gap: int, w: int, size: int) -> List[Tuple[int, int]]:
    temp = list(block_ranges)
    if num_needed <= len(temp):
        return temp[:num_needed]
    last_end = block_ranges[-1][1]
    while len(temp) < num_needed:
        new_start = last_end + 1 + gap
        if new_start + w - 1 >= size:
            break
        temp.append((new_start, new_start + w - 1))
        last_end = new_start + w - 1
    return temp

def place_blocks(out: List[List[int]], target_s: int, h: int, colors: List[int], temp_ranges: List[Tuple[int, int]], bg: int, size: int):
    num = min(len(colors), len(temp_ranges))
    for j in range(num):
        c = colors[j]
        if c == bg or c == 8:
            continue
        ss, ee = temp_ranges[j]
        for r in range(max(0, target_s), min(size, target_s + h)):
            for cc in range(max(0, ss), min(size, ee + 1)):
                if out[r][cc] == bg:
                    out[r][cc] = c

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    size = len(g)
    if size == 0:
        return out
    bg = get_background(g)
    tracks = get_tracks(g, bg, size)
    signal_rows = get_signal_rows(g, tracks, bg, size)
    signal_colors = get_signal_colors(g, signal_rows, tracks, bg)
    if not signal_colors:
        return out
    block_ranges = get_block_ranges(g, bg, size)
    if not block_ranges:
        return out
    widths = {e - s + 1 for s, e in block_ranges}
    if len(widths) != 1:
        return out
    w = next(iter(widths))
    s, h, kk = find_anchor(g, block_ranges, signal_colors, bg, size)
    if s == -1:
        return out
    gap = compute_gap(block_ranges, w)
    for i in range(len(signal_colors)):
        if i == kk:
            continue
        colors = signal_colors[i]
        if not colors:
            continue
        delta = i - kk
        if delta > 0:
            step = 2 * h - 1
        else:
            step = 2 * h + 1
        target_s = s + delta * step
        if target_s < 0 or target_s + h > size:
            continue
        num_needed = len(colors)
        temp_ranges = extend_block_ranges(block_ranges, num_needed, gap, w, size)
        place_blocks(out, target_s, h, colors, temp_ranges, bg, size)
    return out
```