```python
from typing import List, Tuple

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

def get_background(g: List[List[int]]) -> int:
    size = len(g)
    if size == 0:
        return 0
    bg = g[0][0]
    for row in g:
        if len(set(row)) == 1:
            return row[0]
    return bg

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
    signal_set = set()
    for i in range(size):
        for j in tracks:
            if g[i][j] != bg:
                signal_set.add(i)
                break
    signal_rows = sorted(list(signal_set))
    signal_colors = []
    for i in signal_rows:
        row_colors = [g[i][j] for j in tracks if g[i][j] != bg and g[i][j] != 8]
        signal_colors.append(row_colors)
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
    return list(ranges_set)

def find_anchor(g: List[List[int]], block_ranges: List[Tuple[int, int]], signal_colors: List[List[int]], bg: int, size: int, signal_rows: List[int]) -> Tuple[int, int, int, List[Tuple[int, int]], int]:
    anchor_s = -1
    anchor_h = -1
    anchor_kk = -1
    anchor_br = None
    anchor_w = -1
    for hh in range(size // 2, 1, -1):
        for ss in range(size - hh + 1):
            br_sorted = sorted(block_ranges, key=lambda x: x[0])
            widths = {e - s + 1 for s, e in br_sorted}
            if len(widths) != 1:
                continue
            ww = next(iter(widths))
            block_cs = []
            valid = True
            for st, en in br_sorted:
                if st >= size or en >= size:
                    valid = False
                    break
                cc = g[ss][st]
                if cc == bg:
                    valid = False
                    break
                is_uniform = True
                for rr in range(ss, ss + hh):
                    for ccc in range(st, en + 1):
                        if ccc >= size or g[rr][ccc] != cc:
                            is_uniform = False
                            break
                    if not is_uniform:
                        break
                if not is_uniform:
                    valid = False
                    break
                block_cs.append(cc)
            if valid and len(block_cs) == len(br_sorted):
                for kkk, sc in enumerate(signal_colors):
                    if sc and is_subsequence(block_cs, sc):
                        anchor_s = ss
                        anchor_h = hh
                        anchor_kk = kkk
                        anchor_br = br_sorted
                        anchor_w = ww
                        return anchor_s, anchor_h, anchor_kk, anchor_br, anchor_w
        if anchor_s != -1:
            break
    return -1, -1, -1, None, -1

def extend_block_ranges(br: List[Tuple[int, int]], num: int, gap: int, w: int, size: int) -> List[Tuple[int, int]]:
    temp = list(br)
    while len(temp) < num:
        if not temp:
            break
        last_e = temp[-1][1]
        new_s = last_e + 1 + gap
        if new_s + w - 1 >= size:
            break
        new_e = new_s + w - 1
        temp.append((new_s, new_e))
    return temp

def place_blocks(out: List[List[int]], start_r: int, h: int, colors: List[int], temp_br: List[Tuple[int, int]], bg: int, size: int):
    num = min(len(colors), len(temp_br))
    for b in range(num):
        st, en = temp_br[b]
        c = colors[b]
        for r in range(start_r, start_r + h):
            if 0 <= r < size:
                for cc in range(st, en + 1):
                    if cc < size and out[r][cc] == bg:
                        out[r][cc] = c

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    if size == 0:
        return []
    bg = get_background(g)
    tracks = get_tracks(g, bg, size)
    signal_rows, signal_colors = get_signal_rows_and_colors(g, tracks, bg, size)
    num_signals = len(signal_rows)
    if num_signals == 0:
        return [row[:] for row in g]
    block_ranges = get_block_ranges(g, bg, size)
    anchor_s, anchor_h, anchor_kk, anchor_br, anchor_w = find_anchor(g, block_ranges, signal_colors, bg, size, signal_rows)
    out = [row[:] for row in g]
    if anchor_s != -1:
        br_sorted = sorted(anchor_br, key=lambda x: x[0])
        gap = br_sorted[1][0] - br_sorted[0][1] - 1 if len(br_sorted) >= 2 else 1
        step_f = 2 * anchor_h - 1
        step_b = 2 * anchor_h + 1
        for kkk in range(num_signals):
            if kkk == anchor_kk:
                continue
            colors = signal_colors[kkk]
            if not colors:
                continue
            delta = kkk - anchor_kk
            dstep = step_f if delta > 0 else step_b
            ss = anchor_s + delta * dstep
            if ss < 0 or ss + anchor_h > size:
                continue
            num = len(colors)
            temp_br = extend_block_ranges(br_sorted, num, gap, anchor_w, size)
            place_blocks(out, ss, anchor_h, colors, temp_br, bg, size)
    else:
        h = 2
        w = 2
        max_n = max((len(sc) for sc in signal_colors), default=0)
        if max_n == 0:
            return out
        first_st_c = size // 2
        default_br = []
        curr_s = first_st_c
        for _ in range(max_n):
            en = curr_s + w - 1
            if en >= size:
                break
            default_br.append((curr_s, en))
            curr_s += 2 * w + 1
        gap = default_br[1][0] - default_br[0][1] - 1 if len(default_br) >= 2 else 1
        step_b = 2 * h + 1
        last_ss = size - h - 1
        curr_ss = last_ss
        for kkk in range(num_signals - 1, -1, -1):
            colors = signal_colors[kkk]
            if not colors:
                curr_ss -= step_b
                continue
            if curr_ss < 0 or curr_ss + h > size:
                curr_ss -= step_b
                continue
            num = len(colors)
            temp_br = extend_block_ranges(default_br, num, gap, w, size)
            place_blocks(out, curr_ss, h, colors, temp_br, bg, size)
            curr_ss -= step_b
    return out
```