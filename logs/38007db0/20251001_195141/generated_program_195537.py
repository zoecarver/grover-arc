```python
from typing import List

def get_frame_color(g: List[List[int]]) -> int:
    return g[0][0]

def is_border_row(row: List[int], frame_c: int) -> bool:
    return all(x == frame_c for x in row)

def get_panel_starts(W: int) -> List[int]:
    starts = []
    s = 0
    while s + 7 <= W:
        starts.append(s)
        s += 6
    return starts

def get_block_index(r: int) -> int:
    return (r - 1) // 6

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    H = len(g)
    W = len(g[0])
    frame_c = get_frame_color(g)
    starts = get_panel_starts(W)
    num_panels = len(starts)
    output = []
    for r in range(W):
        if r >= H:
            output.append([frame_c] * 7)
            continue
        input_row = g[r]
        if is_border_row(input_row, frame_c):
            output.append([frame_c] * 7)
        else:
            block_idx = get_block_index(r)
            if block_idx % 2 == 0:
                p = num_panels - 1
            else:
                p = 0
            s = starts[p]
            out_row = input_row[s:s + 7]
            output.append(out_row)
    return output
```