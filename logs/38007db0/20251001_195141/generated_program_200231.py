```python
from typing import List, Tuple

def get_frame_color(g: List[List[int]]) -> int:
    return g[0][0]

def is_border_row(row: List[int], frame_c: int) -> bool:
    return all(x == frame_c for x in row)

def get_border_positions(g: List[List[int]]) -> List[int]:
    frame_c = get_frame_color(g)
    r = 0
    H = len(g)
    while r < H and is_border_row(g[r], frame_c):
        r += 1
    if r == H:
        return []
    row = g[r]
    return [j for j in range(len(row)) if row[j] == frame_c]

def get_starts_and_rights(border_pos: List[int]) -> Tuple[List[int], List[int]]:
    if len(border_pos) < 2:
        return [], []
    return border_pos[:-1], border_pos[1:]

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
    border_pos = get_border_positions(g)
    starts, rights = get_starts_and_rights(border_pos)
    num_panels = len(starts)
    if num_panels == 0:
        frame_c = get_frame_color(g)
        return [[frame_c] * 7 for _ in g]
    frame_c = get_frame_color(g)
    H = len(g)
    output = []
    section_idx = 0
    in_content = False
    for r in range(H):
        row = g[r]
        if is_border_row(row, frame_c):
            output.append([frame_c] * 7)
            if in_content:
                section_idx += 1
                in_content = False
        else:
            if not in_content:
                in_content = True
            panel_index = choose_panel_index(section_idx, num_panels)
            if panel_index >= num_panels:
                panel_index = num_panels - 1
            s = starts[panel_index]
            right_pos = rights[panel_index]
            left_val = row[s]
            content_start = s + 1
            content = row[content_start: content_start + 5]
            right_val = row[right_pos]
            output_row = [left_val] + content + [right_val]
            output.append(output_row)
    return output
```