```python
from typing import List

def get_frame_color(g: List[List[int]]) -> int:
    """Extracts the frame color from the top-left cell of the grid."""
    return g[0][0] if g else 0

def is_border_row(row: List[int], frame_c: int) -> bool:
    """Checks if an entire row consists only of the frame color, indicating a horizontal border."""
    return all(x == frame_c for x in row)

def get_border_positions(row: List[int], frame_c: int) -> List[int]:
    """Finds all column indices in the row where the frame color appears, indicating vertical borders."""
    return [j for j in range(len(row)) if row[j] == frame_c]

def choose_panel_index(section_idx: int, num_panels: int) -> int:
    """Selects the panel index to extract based on the section index and number of panels in the section."""
    if section_idx == 0:
        return 2
    elif section_idx == 1:
        return 0
    elif section_idx == 2:
        return 1 if num_panels == 3 else num_panels - 1
    else:
        return 0 if section_idx % 2 == 1 else num_panels - 1

def extract_panel_row(row: List[int], left: int, right: int) -> List[int]:
    """Extracts a 7-column slice for the panel: left border + up to 5 content cells + right border."""
    left_val = row[left]
    content = row[left + 1 : right][:5]
    right_val = row[right]
    return [left_val] + content + [right_val]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Processes the grid by detecting borders, selecting panels per section, and extracting 7-wide outputs."""
    if not g:
        return []
    frame_c = get_frame_color(g)
    H = len(g)
    if H == 0:
        return []
    W = len(g[0])
    output = []
    r = 0
    section_idx = 0
    while r < H:
        if is_border_row(g[r], frame_c):
            output.append([frame_c] * 7)
            r += 1
            continue
        # Start of a content section
        border_pos = get_border_positions(g[r], frame_c)
        if len(border_pos) < 2:
            # Skip invalid section with no panels
            r += 1
            continue
        lefts = border_pos[:-1]
        rights = border_pos[1:]
        num_panels = len(lefts)
        panel_idx = choose_panel_index(section_idx, num_panels)
        panel_idx = min(panel_idx, num_panels - 1)
        left = lefts[panel_idx]
        right = rights[panel_idx]
        # Extract rows for the entire section
        section_start = r
        while r < H and not is_border_row(g[r], frame_c):
            out_row = extract_panel_row(g[r], left, right)
            # Ensure exactly 7 columns by padding with frame color if necessary
            while len(out_row) < 7:
                out_row.append(frame_c)
            output.append(out_row)
            r += 1
        section_idx += 1
    return output
```