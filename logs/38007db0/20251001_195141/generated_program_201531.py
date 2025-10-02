```python
from typing import List

def get_frame_color(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def is_border_row(row: List[int], frame_c: int) -> bool:
    return all(x == frame_c for x in row)

def extract_panel_row(row: List[int], left: int, right: int) -> List[int]:
    content = row[left + 1 : right][:5]
    return [row[left]] + content + [row[right]]

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
    if not g:
        return []
    frame_c = get_frame_color(g)
    output: List[List[int]] = []
    H = len(g)
    if H == 0:
        return output
    W = len(g[0])
    r = 0
    section_idx = 0
    in_section = False
    current_left = None
    current_right = None
    while r < H:
        row = g[r]
        if is_border_row(row, frame_c):
            output.append([frame_c] * 7)
            if in_section:
                section_idx += 1
                in_section = False
            r += 1
            continue
        # content row
        if not in_section:
            # start section
            in_section = True
            border_pos = [j for j in range(W) if row[j] == frame_c]
            num_panels = len(border_pos) - 1
            if num_panels == 0:
                in_section = False
                r += 1
                continue
            panel_idx = choose_panel_index(section_idx, num_panels)
            panel_idx = min(panel_idx, num_panels - 1)
            current_left = border_pos[panel_idx]
            current_right = border_pos[panel_idx + 1]
        # extract if in section with valid bounds
        if in_section and current_left is not None and current_right is not None and 0 <= current_left < W and current_right <= W:
            out_row = extract_panel_row(row, current_left, current_right)
            # pad or truncate to 7 if needed, but in rules it's always 7
            if len(out_row) < 7:
                out_row += [frame_c] * (7 - len(out_row))
            elif len(out_row) > 7:
                out_row = out_row[:7]
            output.append(out_row)
        r += 1
    return output
```