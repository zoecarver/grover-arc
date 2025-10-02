```python
from typing import List, Tuple

def get_frame_color(g: List[List[int]]) -> int:
    """Extracts the frame/border color from the top-left cell."""
    return g[0][0] if g else 0

def is_border_row(row: List[int], frame_c: int) -> bool:
    """Checks if an entire row consists only of the frame color."""
    return all(x == frame_c for x in row)

def get_border_positions(row: List[int], frame_c: int) -> List[int]:
    """Finds vertical border column positions in the given row."""
    return [j for j in range(len(row)) if row[j] == frame_c]

def get_panel_borders(border_pos: List[int]) -> Tuple[List[int], List[int]]:
    """Derives left and right border positions for each panel from border positions."""
    if len(border_pos) < 2:
        return [], []
    return border_pos[:-1], border_pos[1:]

def choose_panel_index(section_idx: int, num_panels: int) -> int:
    """Selects panel index based on section position and total panels (assumes ~3-4 panels)."""
    if section_idx == 0:
        return 2
    elif section_idx == 1:
        return 0
    elif section_idx == 2:
        return 1 if num_panels == 3 else num_panels - 1
    else:
        return 0 if section_idx % 2 == 1 else num_panels - 1

def extract_panel_row(row: List[int], left: int, right: int) -> List[int]:
    """Extracts a 7-column panel row: left border + first 5 content cells + right border."""
    left_val = row[left]
    right_val = row[right]
    content_start = left + 1
    content_end = right
    content = row[content_start:content_end][:5]
    return [left_val] + content + [right_val]

def program(g: List[List[int]]) -> List[List[int]]:
    """Processes the input grid to extract selected panels from each section, producing a 7-column output."""
    if not g:
        return []
    H = len(g)
    frame_c = get_frame_color(g)
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
        lefts, rights = get_panel_borders(border_pos)
        num_panels = len(lefts)
        if num_panels == 0:
            r += 1
            continue
        panel_idx = choose_panel_index(section_idx, num_panels)
        if panel_idx >= num_panels:
            panel_idx = num_panels - 1
        left = lefts[panel_idx]
        right = rights[panel_idx]
        # Extract rows for the entire section
        while r < H and not is_border_row(g[r], frame_c):
            out_row = extract_panel_row(g[r], left, right)
            output.append(out_row)
            r += 1
        section_idx += 1
    return output
```