```python
def get_background(g: List[List[int]]) -> int:
    for row in g:
        if len(set(row)) == 1:
            return row[0]
    return g[0][0]

def get_tracks(g: List[List[int]], background: int) -> List[int]:
    size = len(g)
    tracks = []
    for j in range(1, min(8, size), 2):
        has_signal = False
        consecutive = 0
        for i in range(size):
            if g[i][j] != background:
                has_signal = True
                consecutive += 1
                if consecutive >= 2:
                    break
            else:
                consecutive = 0
        if has_signal and consecutive < 2:
            tracks.append(j)
    return tracks

def get_signal_rows(g: List[List[int]], tracks: List[int], background: int) -> List[int]:
    size = len(g)
    signal_rows = set()
    for i in range(size):
        for j in tracks:
            if g[i][j] != background:
                signal_rows.add(i)
                break
    return sorted(list(signal_rows))

def get_block_ranges(g: List[List[int]], background: int) -> List[tuple]:
    size = len(g)
    ranges = set()
    for i in range(size):
        j = 0
        while j < size:
            if g[i][j] == background:
                j += 1
                continue
            start = j
            color = g[i][j]
            while j < size and g[i][j] == color:
                j += 1
            end = j - 1
            if end - start + 1 >= 2:
                ranges.add((start, end))
    return sorted(list(ranges))

def get_block_width(block_ranges: List[tuple]) -> int:
    if not block_ranges:
        return 0
    return block_ranges[0][1] - block_ranges[0][0] + 1

def get_filled_frame(g: List[List[int]], signal_rows: List[int], tracks: List[int], block_ranges: List[tuple], background: int) -> int:
    size = len(g)
    h = get_block_width(block_ranges)
    if h == 0:
        return 0
    for start in range(size - h + 1):
        is_filled = True
        for rg in block_ranges:
            if g[start][rg[0]] == background:
                is_filled = False
                break
        if is_filled:
            # find which frame
            for f, s_row in enumerate(signal_rows, 1):
                match = True
                for t, rg in zip(tracks, block_ranges):
                    color = g[start][rg[0]]
                    if g[s_row][t] != color:
                        match = False
                        break
                if match:
                    return f
    return 1  # default to first

def place_frame(out: List[List[int]], start: int, h: int, frame_idx: int, tracks: List[int], signal_rows: List[int], block_ranges: List[tuple], background: int):
    size = len(out)
    if start < 0 or start + h > size:
        return
    s_row = signal_rows[frame_idx - 1]
    for k in range(h):
        r = start + k
        if r >= size:
            break
        for t_idx, rg in enumerate(block_ranges):
            t = tracks[t_idx] if t_idx < len(tracks) else None
            color = g[s_row][t] if t is not None and g[s_row][t] != background else background
            if color != background:
                for j in range(rg[0], rg[1] + 1):
                    out[r][j] = color

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    background = get_background(g)
    tracks = get_tracks(g, background)
    signal_rows = get_signal_rows(g, tracks, background)
    n_frames = len(signal_rows)
    if n_frames == 0:
        return out
    block_ranges = get_block_ranges(g, background)
    if not block_ranges:
        return out
    h = get_block_width(block_ranges)
    filled_frame = get_filled_frame(g, signal_rows, tracks, block_ranges, background)
    d = signal_rows[1] - signal_rows[0] if n_frames > 1 else 2
    last_signal = signal_rows[-1]
    step_after = 2 * h - 1
    initial_after = last_signal + h - d + 1
    current_start = initial_after
    for i in range(filled_frame + 1, n_frames + 1):
        place_frame(out, current_start, h, i, tracks, signal_rows, block_ranges, background)
        current_start += step_after
    step_before = 2 * h + 1
    current_start = g[0][0]  # dummy
    if filled_frame > 1:
        current_start = the filled start - step_before
        for i in range(filled_frame - 1, 0, -1):
            place_frame(out, current_start, h, i, tracks, signal_rows, block_ranges, background)
            current_start -= step_before
    return out
```