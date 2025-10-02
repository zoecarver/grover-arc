```python
from typing import List

def get_frame_color(g: List[List[int]]) -> int:
    return g[0][0]

def is_border_row(row: List[int], frame_c: int) -> bool:
    return all(x == frame_c for x in row)

def get_border_positions(row: List[int], frame_c: int) -> List[int]:
    return [j for j in range(len(row)) if row[j] == frame_c]

def get_panel_starts(border_pos: List[int], W: int) -> List[int]:
    return [p for p in border_pos[:-1] if p + 7 <= W]

def choose_panel_index(section_idx: int, num_panels: int) -> int:
    if section_idx == 0:
        return 2
    elif section_idx == 1:
        return 0
    elif section_idx == 2:
        return 1 if num_panels == 3 else num_panels - 1
    else:
        return 0 if section_idx % 2 == 1 else num_panels - 1

def program(g: List[List[int]]) -> List[List[int]]:
    frame_c = get_frame_color(g)
    H = len(g)
    if H == 0:
        return []
    W = len(g[0])
    output: List[List[int]] = []
    r = 0
    section_idx = -1
    while r < H:
        row = g[r]
        if is_border_row(row, frame_c):
            output.append([frame_c] * 7)
            r += 1
            continue
        section_idx += 1
        border_pos = get_border_positions(row, frame_c)
        starts = get_panel_starts(border_pos, W)
        num_panels = len(starts)
        if num_panels == 0:
            r += 1
            continue
        panel_idx = choose_panel_index(section_idx, num_panels)
        if panel_idx >= num_panels:
            panel_idx = num_panels - 1
        start_col = starts[panel_idx]
        while r < H and not is_border_row(g[r], frame_c):
            curr_row = g[r]
            extracted = curr_row[start_col:start_col + 7]
            output.append(extracted)
            r += 1
    return output
```