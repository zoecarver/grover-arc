```python
from typing import List

def crop_left_border(g: List[List[int]]) -> List[List[int]]:
    """Crops the left 6 columns to extract the main content area."""
    return [row[6:30] for row in g]

def get_pattern(left: List[int]) -> List[int]:
    """Extracts the pattern from the left 5 columns, skipping frame values and repeating the first non-frame."""
    frame = {0, 6, 7}
    i = 0
    leading = 0
    while i < 5 and left[i] in frame:
        leading += 1
        i += 1
    if i == 5:
        return []
    first = left[i]
    pattern = [first] * leading if leading > 0 else [first]
    for j in range(i + 1, 5):
        if left[j] != 0:
            pattern.append(left[j])
    return pattern

def map_1_to_4(pattern: List[int], has_8: bool) -> List[int]:
    """Maps 1 to 4 in the pattern if 8 is present in the grid."""
    if not has_8:
        return pattern
    return [4 if x == 1 else x for x in pattern]

def pad_to_3(pattern: List[int]) -> List[int]:
    """Pads the pattern to exactly 3 elements by repeating the last element."""
    p = pattern[:]
    while len(p) < 3:
        if p:
            p.append(p[-1])
        else:
            p.append(0)
    return p[:3]

def rotate_left(p: List[int]) -> List[int]:
    """Rotates the pattern left by one position."""
    if not p:
        return p
    return p[1:] + [p[0]]

def get_empty_pattern(previous_p: List[int], consecutive_empty: int) -> List[int]:
    """Determines the pattern for empty left columns based on consecutive count."""
    if consecutive_empty == 1 and previous_p:
        return rotate_left(previous_p)
    if consecutive_empty > 1:
        return [4, 4, 4]
    return []

def normalize_header(row: List[int]) -> List[int]:
    """Normalizes headers by extending leading 5s to 3 and following 3s to 6."""
    row_out = row[:]
    # Extend 5s to 3
    i = 0
    num5 = 0
    while i < 24 and row_out[i] == 5:
        num5 += 1
        i += 1
    if num5 < 3:
        for j in range(3 - num5):
            if i + j < 24:
                row_out[i + j] = 5
    # Extend 3s to 6
    start3 = 0
    while start3 < 24 and row_out[start3] == 5:
        start3 += 1
    i = start3
    num3 = 0
    while i < 24 and row_out[i] == 3:
        num3 += 1
        i += 1
    if num3 < 6:
        for j in range(6 - num3):
            if i + j < 24:
                row_out[i + j] = 3
    return row_out

def special_accent(p: List[int], row: List[int], has_8: bool) -> List[int]:
    """Applies special accent for all-4 patterns on rows containing 8."""
    if not has_8 or not all(x == 4 for x in p):
        return p
    return [4, 4, 7]

def apply_overlay(row: List[int], p: List[int]) -> List[int]:
    """Applies the pattern overlay starting from position 9, every 6 positions."""
    result = row[:]
    for start in range(9, 24, 6):
        for k in range(3):
            pos = start + k
            if pos < 24:
                result[pos] = p[k]
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    """Composes all rules to transform the input grid."""
    cropped_g = crop_left_border(g)
    h = len(cropped_g)
    has_8 = any(8 in row for row in cropped_g)
    out = []
    previous_p = []
    consecutive_empty = 0
    for r in range(h):
        left = g[r][:5]
        row = cropped_g[r][:]
        orig_p = get_pattern(left)
        is_empty = len(orig_p) == 0
        if is_empty:
            consecutive_empty += 1
            p = get_empty_pattern(previous_p, consecutive_empty)
        else:
            consecutive_empty = 0
            mapped_p = map_1_to_4(orig_p, has_8)
            p = pad_to_3(mapped_p)
        previous_p = p
        if is_empty and len(p) == 0:
            row_out = normalize_header(row)
        else:
            accent_p = special_accent(p, row, has_8)
            row_out = apply_overlay(row, accent_p)
        out.append(row_out)
    return out
```