```python
from typing import List, Tuple
from collections import Counter

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_tracks(g: List[List[int]], bg: int, size: int) -> List[int]:
    tracks = []
    for j in range(1, size, 2):
        has_signal = False
        consec = 0
        max_consec = 0
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

def get_signal_rows_and_colors(g: List[List[int]], tracks: List[int], bg: int, size: int) -> Tuple[List[int], List[List[int]]]:
    signal_data = []
    for r in range(size):
        row_colors = [g[r][c] for c in tracks if g[r][c] != bg and g[r][c] != 8]
        if row_colors:
            signal_data.append((r, row_colors))
    signal_data.sort(key=lambda x: x[0])
    signal_rows = [sd[0] for sd in signal_data]
    signal_colors = [sd[1] for sd in signal_data]
    return signal_rows, signal_colors

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

def find_anchor(g: List[List[int]], block_ranges: List[Tuple[int, int]], signal_colors: List[List[int]], bg: int, size: int) -> Tuple[int, int, int]:
    max_h = min(10, size // 2)
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
                for rr in range(s, s + h):
                    for cc in range(start, end + 1):
                        if cc >= size or g[rr][cc] != c:
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

def get_temp_ranges(block_ranges: List[Tuple[int, int]], num: int, w: int, base_diff: int, size: int) -> List[Tuple[int, int]]:
    temp = list(block_ranges)
    current_len = len(temp)
    if current_len >= num:
        return temp[:num]
    for _ in range(num - current_len):
        last_start = temp[-1][0]
        if current_len == 1:
            new_start = last_start + base_diff
        else:
            new_start = last_start + w
        if new_start + w - 1 >= size:
            break
        temp.append((new_start, new_start + w - 1))
        current_len += 1
    return temp[:num]

def place(out: List[List[int]], target_s: int, h: int, colors: List[int], temp_ranges: List[Tuple[int, int]], bg: int, size: int):
    num = min(len(colors), len(temp_ranges))
    for j in range(num):
        c = colors[j]
        if c == bg or c == 8:
            continue
        start_c, end_c = temp_ranges[j]
        for r in range(max(0, target_s), min(size, target_s + h)):
            for cc in range(max(0, start_c), min(size, end_c + 1)):
                if out[r][cc] == bg:
                    out[r][cc] = c

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    out = copy_grid(g)
    bg = get_background(g)
    tracks = get_tracks(g, bg, size)
    signal_rows, signal_colors = get_signal_rows_and_colors(g, tracks, bg, size)
    block_ranges = get_block_ranges(g, bg, size)
    if not block_ranges:
        return out
    ws = [end - start + 1 for start, end in block_ranges]
    if len(set(ws)) != 1:
        return out
    w = ws[0]
    starts = [start for start, _ in block_ranges]
    base_diff = starts[1] - starts[0] if len(starts) >= 2 else w + 2
    s, h, kk = find_anchor(g, block_ranges, signal_colors, bg, size)
    if s == -1:
        return out
    for i in range(len(signal_colors)):
        if i == kk:
            continue
        delta = i - kk
        if delta > 0:
            step = 2 * h - 1
            target_s = s + delta * step
        else:
            step = 2 * h + 1
            target_s = s + delta * step
        if target_s < 0 or target_s + h > size:
            continue
        colors = signal_colors[i]
        num = len(colors)
        temp_ranges = get_temp_ranges(block_ranges, num, w, base_diff, size)
        place(out, target_s, h, colors, temp_ranges, bg, size)
    return out
```