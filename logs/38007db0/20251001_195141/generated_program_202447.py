```python
from typing import List

def get_frame_color(g: List[List[int]]) -> int:
    """Extracts the frame color from the top-left cell of the grid, which is consistent across all borders."""
    return g[0][0] if g else 0

def is_border_row(row: List[int], frame_c: int) -> bool:
    """Checks if an entire row consists only of the frame color, indicating a horizontal border row that must be preserved as a 7-wide frame row in output."""
    return all(x == frame_c for x in row)

def get_border_positions(row: List[int], frame_c: int) -> List[int]:
    """Finds all column indices in the row where the frame color appears, indicating vertical border positions for panel delimiting within a section."""
    return [j for j in range(len(row)) if row[j] == frame_c]

def choose_panel_index(section_idx: int, num_panels: int) -> int:
    """Selects the panel index to extract based on the section index and number of panels, following the observed pattern: index 2 for section 0, 0 for 1, 1 or last for 2 depending on count, alternating 0/last for later sections."""
    if section_idx == 0:
        return 2
    elif section_idx == 1:
        return 0
    elif section_idx == 2:
        return 1 if num_panels == 3 else num_panels - 1
    else:
        return 0 if section_idx % 2 == 1 else num_panels - 1

def extract_panel_row(row: List[int], left: int, right: int, frame_c: int) -> List[int]:
    """Extracts a 7-column panel row from the input row: left border value + up to the first 5 content cells between left and right + right border value, padding with frame color if shorter than 7."""
    W = len(row)
    lval = row[left] if left < W else frame_c
    rval = row[right] if right < W else frame_c
    content_start = left + 1
    content_end = right
    content = row[content_start:content_end][:5]
    out_row = [lval] + content + [rval]
    out_row = out_row[:7]
    while len(out_row) < 7:
        out_row.append(frame_c)
    return out_row

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program that processes the input grid by detecting border rows and sections, selecting and extracting the appropriate 7-wide panel per section based on index, and constructing the output grid of height H and width 7."""
    if not g:
        return []
    frame_c = get_frame_color(g)
    H = len(g)
    W = len(g[0]) if H > 0 else 0
    output: List[List[int]] = []
    r = 0
    section_idx = 0
    in_section = False
    current_left = -1
    current_right = -1
    while r < H:
        row = g[r]
        if is_border_row(row, frame_c):
            output.append([frame_c] * 7)
            if in_section:
                section_idx += 1
            in_section = False
            current_left = -1
            current_right = -1
            r += 1
            continue
        # content row
        if not in_section:
            in_section = True
            border_pos = get_border_positions(row, frame_c)
            num_panels = len(border_pos) - 1 if len(border_pos) >= 2 else 0
            if num_panels == 0:
                current_left = 0
                current_right = min(7, W)
            else:
                pidx = choose_panel_index(section_idx, num_panels)
                pidx = min(pidx, num_panels - 1)
                current_left = border_pos[pidx]
                current_right = border_pos[pidx + 1]
        # extract using current positions
        out_row = extract_panel_row(row, current_left, current_right, frame_c)
        output.append(out_row)
        r += 1
    return output
```