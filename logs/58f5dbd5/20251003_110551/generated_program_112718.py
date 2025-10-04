```python
from typing import List

def get_bg(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def find_blocks(g: List[List[int]], bg: int) -> List[dict]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    blocks = []
    for i in range(h - 4):
        for j in range(w - 4):
            c = g[i][j]
            if c == bg:
                continue
            is_block = True
            for di in range(5):
                for dj in range(5):
                    if g[i + di][j + dj] != c:
                        is_block = False
                        break
                if not is_block:
                    break
            if is_block:
                blocks.append({'r': i, 'c': j, 'color': c})
    return blocks

def build_map(starts: List[int], size: int) -> List[int]:
    if not starts:
        return list(range(size))  # fallback
    out_map = []
    first_start = starts[0]
    if first_start > 0:
        out_map.append(0)
    prev_end = first_start - 1
    for idx, s in enumerate(starts):
        if idx > 0 and s > starts[idx - 1] + 5:
            out_map.append(starts[idx - 1] + 5)
        for k in range(5):
            out_map.append(s + k)
        prev_end = s + 4
    if prev_end < size - 1:
        out_map.append(prev_end + 1)
    return out_map

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    bg = get_bg(g)
    blocks = find_blocks(g, bg)
    row_starts = sorted(set(b['r'] for b in blocks))
    col_starts = sorted(set(b['c'] for b in blocks))
    row_map = build_map(row_starts, h)
    col_map = build_map(col_starts, w)
    h_out = len(row_map)
    w_out = len(col_map)
    out = [[bg for _ in range(w_out)] for _ in range(h_out)]
    # fill using map
    for i_out in range(h_out):
        i_in = row_map[i_out]
        for j_out in range(w_out):
            j_in = col_map[j_out]
            out[i_out][j_out] = g[i_in][j_in]
    # override blocks with patterns (solid for now)
    for b in blocks:
        r = b['r']
        c = b['color']
        start_i_out = row_map.index(r)
        start_j_out = col_map.index(b['c'])
        for k in range(5):
            for l in range(5):
                # solid pattern
                out[start_i_out + k][start_j_out + l] = c
                # example frame pattern (to improve)
                # if k == 0 or k == 4 or l == 0 or l == 4 or (k == 2 and l == 2):
                #     out[start_i_out + k][start_j_out + l] = c
                # else:
                #     out[start_i_out + k][start_j_out + l] = bg
    return out
```