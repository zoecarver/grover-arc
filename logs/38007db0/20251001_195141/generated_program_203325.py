```python
from typing import List

def get_frame_color(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def is_border_row(row: List[int], frame_c: int) -> bool:
    return all(x == frame_c for x in row)

def get_border_positions(row: List[int], frame_c: int) -> List[int]:
    return [j for j in range(len(row)) if row[j] == frame_c]

def choose_panel_index(section_idx: int, num_panels: int) -> int:
    if section_idx == 0:
        return 2
    elif section_idx == 1:
        return 0
    elif section_idx == 2:
        return 1 if num_panels == 3 else num_panels - 1
    else:
        return 0 if section_idx % 2 == 1 else num_panels - 1

def extract_panel_row(row: List[int], left: int, right: int, frame_c: int) -> List[int]:
    W = len(row)
    lval = row[left] if left < W else frame_c
    rval = row[right] if right < W else frame_c
    content = row[left + 1 : right][:5]
    out_row = [lval] + content + [rval]
    while len(out_row) < 7:
        out_row.append(frame_c)
    return out_row[:7]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    frame_c = get_frame_color(g)
    H = len(g)
    output = []
    r = 0
    section_idx = 0
    while r < H:
        row = g[r]
        if is_border_row(row, frame_c):
            output.append([frame_c] * 7)
            r += 1
            continue
        border_pos = get_border_positions(row, frame_c)
        num_panels = len(border_pos) - 1 if len(border_pos) >= 2 else 0
        if num_panels == 0:
            while r < H and not is_border_row(g[r], frame_c):
                r += 1
            continue
        lefts = border_pos[:-1]
        rights = border_pos[1:]
        panel_idx = min(choose_panel_index(section_idx, num_panels), num_panels - 1)
        left = lefts[panel_idx]
        right = rights[panel_idx]
        while r < H and not is_border_row(g[r], frame_c):
            out_row = extract_panel_row(g[r], left, right, frame_c)
            output.append(out_row)
            r += 1
        section_idx += 1
    return output
```