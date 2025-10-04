```python
from typing import List
from collections import Counter

def get_content_bounds(g: List[List[int]]) -> tuple:
    """Detect the start and end of the content area based on uniform top and bottom rows."""
    h = len(g)
    if h < 2:
        return 0, h - 1, 2, 2
    # Check for uniform top rows
    top_uniform = all(all(cell == g[0][0] for cell in row) for row in g[:2])
    content_start = 2 if top_uniform else 0
    # Check for uniform bottom rows
    bottom_uniform = all(all(cell == g[-1][0] for cell in row) for row in g[-2:])
    content_end = h - 1 - (2 if bottom_uniform else 0)
    # Assume left and right frame width
    left_width = 2
    right_width = 2
    return content_start, content_end, left_width, right_width

def get_background_and_standard(g: List[List[int]], content_start: int, left_width: int, right_width: int) -> tuple:
    """Find the background color and a standard row for clean content."""
    h = len(g)
    w = len(g[0]) if g else 0
    content_rows = g[content_start : min(content_start + 5, h)]  # Sample first few content rows
    all_content_cells = []
    for row in content_rows:
        content_slice = row[left_width : w - right_width]
        all_content_cells.extend(content_slice)
    if not all_content_cells:
        bg = g[0][left_width] if g else 0
    else:
        bg = Counter(all_content_cells).most_common(1)[0][0]
    # Create standard row from first content row, filling content with bg
    if content_start >= h:
        standard = [bg] * w
    else:
        standard = g[content_start][:]
        for j in range(left_width, w - right_width):
            standard[j] = bg
    return bg, standard

def is_disturbed_row(row: List[int], standard: List[int], left_width: int, right_width: int) -> bool:
    """Check if a row is disturbed compared to standard in content area."""
    w = len(row)
    for j in range(left_width, w - right_width):
        if row[j] != standard[j]:
            return True
    return False

def reverse_disturbed_groups(g: List[List[int]], content_start: int, content_end: int, standard: List[int], left_width: int, right_width: int) -> List[List[int]]:
    """Collect and reverse groups of consecutive disturbed rows in content area."""
    disturbed_groups = []
    current_group = []
    for i in range(content_start, content_end + 1):
        row = g[i]
        if is_disturbed_row(row, standard, left_width, right_width):
            current_group.append(row[:])
        else:
            if current_group:
                disturbed_groups.append(current_group[::-1])  # Reverse within group
                current_group = []
            # Clean row, skip
    if current_group:
        disturbed_groups.append(current_group[::-1])
    return disturbed_groups

def shift_shape_right(row: List[int], standard: List[int], left_width: int, right_width: int, shift_amount: int = 1) -> List[int]:
    """Simple shift of anomaly parts right by shift_amount, filling with bg."""
    w = len(row)
    bg = standard[left_width]
    new_row = row[:]
    # Find content positions with anomaly
    for j in range(left_width, w - right_width - shift_amount):
        if row[j] != standard[j] and row[j + shift_amount] == standard[j + shift_amount]:
            new_row[j + shift_amount] = row[j]
            new_row[j] = bg
    return new_row

def place_groups_at_bottom(result: List[List[int]], disturbed_groups: List[List[List[int]]], content_start: int, content_h: int, standard: List[int], num_groups: int):
    """Place reversed groups at the bottom with 1 clean gap between groups, excess clean at top."""
    num_gaps = max(0, num_groups - 1)
    top_clean_count = content_h - sum(len(group) for group in disturbed_groups) - num_gaps
    # Add top clean
    for _ in range(top_clean_count):
        result.append(standard[:])
    # Add groups with gaps
    for idx, group in enumerate(disturbed_groups):
        for row in group:
            # Apply simple shift (creative assumption for improvement)
            shifted_row = shift_shape_right(row, standard, 2, 2, 1 if idx == 0 else 2)  # Different shift per group
            result.append(shifted_row)
        if idx < len(disturbed_groups) - 1:
            result.append(standard[:])  # Gap

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: detect frame, standard, groups, reverse and shift, place at bottom with gaps."""
    if not g or not g[0]:
        return []
    content_start, content_end, left_width, right_width = get_content_bounds(g)
    bg, standard = get_background_and_standard(g, content_start, left_width, right_width)
    content_h = content_end - content_start + 1
    # Build result with top frame
    result = [row[:] for row in g[:content_start]]
    # Get reversed groups
    disturbed_groups = reverse_disturbed_groups(g, content_start, content_end, standard, left_width, right_width)
    # Place them
    place_groups_at_bottom(result, disturbed_groups, content_start, content_h, standard, len(disturbed_groups))
    # If too short, fill with standard
    while len(result) < len(g):
        result.append(standard[:])
    # Trim if too long
    result = result[:len(g)]
    # Add bottom frame if needed
    expected_h = len(g)
    bottom_start = content_end + 1
    if len(result) < expected_h:
        result += [row[:] for row in g[bottom_start:]]
    return result
```