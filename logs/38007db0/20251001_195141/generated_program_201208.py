```python
from typing import List

def get_frame_color(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def is_border_row(row: List[int], frame_c: int) -> bool:
    return all(x == frame_c for x in row)

def extract_panel_row(row: List[int], left: int, right: int) -> List[int]:
    left_val = row[left]
    content = row[left + 1:right][:5]
    right_val = row[right]
    return [left_val] + content + [right_val]

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
    H = len(g)
    W = len(g[0]) if g else 0
    output: List[List[int]] = []
    r = 0
    section_idx = 0
    while r < H:
        if is_border_row(g[r], frame_c):
            output.append([frame_c] * 7)
            r += 1
        else:
            # Start of a section
            first_row = g[r]
            border_pos = [j for j in range(W) if first_row[j] == frame_c]
            num_panels = len(border_pos) - 1
            if num_panels > 0:
                panel_idx = choose_panel_index(section_idx, num_panels)
                if panel_idx >= num_panels:
                    panel_idx = num_panels - 1
                left = border_pos[panel_idx]
                right = border_pos[panel_idx + 1]
                # Extract for the first row of the section
                out_row = extract_panel_row(g[r], left, right)
                output.append(out_row)
                r += 1
                # Extract for remaining rows in the section
                while r < H and not is_border_row(g[r], frame_c):
                    out_row = extract_panel_row(g[r], left, right)
                    output.append(out_row)
                    r += 1
                section_idx += 1
            else:
                # Skip section with no panels
                while r < H and not is_border_row(g[r], frame_c):
                    r += 1
    return output
```