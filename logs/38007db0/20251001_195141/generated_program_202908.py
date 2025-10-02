```python
from typing import List

def get_frame_color(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def is_border_row(row: List[int], frame_c: int) -> bool:
    return all(x == frame_c for x in row)

def get_border_positions(row: List[int], frame_c: int) -> List[int]:
    return [j for j in range(len(row)) if row[j] == frame_c]

def choose_panel_index(section_idx: int, num_panels: int) -> int:
    if num_panels == 0:
        return 0
    cand = 0
    if section_idx == 0:
        cand = 2
    elif section_idx == 1:
        cand = 0
    elif section_idx == 2:
        cand = 1 if num_panels == 3 else num_panels - 1
    else:
        cand = 0 if section_idx % 2 == 1 else num_panels - 1
    return min(cand, num_panels - 1)

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
    H = len(g)
    frame_c = get_frame_color(g)
    output = []
    r = 0
    section_idx = 0
    while r < H:
        row = g[r]
        if is_border_row(row, frame_c):
            output.append([frame_c] * 7)
            r += 1
            continue
        # Start of section
        border_pos = get_border_positions(row, frame_c)
        valid_indices = [i for i in range(len(border_pos) - 1) if border_pos[i] + 7 <= len(g[0])]
        num_panels = len(valid_indices)
        if num_panels == 0:
            # Skip empty section
            r += 1
            while r < H and not is_border_row(g[r], frame_c):
                r += 1
            continue
        panel_idx = choose_panel_index(section_idx, num_panels)
        chosen_i = valid_indices[panel_idx]
        left = border_pos[chosen_i]
        right = border_pos[chosen_i + 1]
        # Process section
        while r < H and not is_border_row(g[r], frame_c):
            curr_row = g[r]
            out_row = extract_panel_row(curr_row, left, right, frame_c)
            output.append(out_row)
            r += 1
        section_idx += 1
    return output
```