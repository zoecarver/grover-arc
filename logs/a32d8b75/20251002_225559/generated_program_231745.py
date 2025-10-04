```python
from typing import List

def get_pattern(left: List[int]) -> List[int]:
    """Extract pattern from left 5 columns based on leading frame colors."""
    frame = {0, 6, 7}
    leading = 0
    i = 0
    while i < 5 and left[i] in frame:
        leading += 1
        i += 1
    if i == 5:
        return []
    first = left[i]
    pattern = [first] * leading
    for j in range(i + 1, 5):
        if left[j] != 0:
            pattern.append(left[j])
    return pattern

def normalize_header(crop: List[int]) -> List[int]:
    """Extend initial runs of 5 and 3 to 3 and 6 respectively by overwriting next cells."""
    # Extend 5's to 3
    num5 = 0
    i = 0
    while i < len(crop) and crop[i] == 5:
        num5 += 1
        i += 1
    if num5 < 3:
        for j in range(3 - num5):
            if i + j < len(crop):
                crop[i + j] = 5
    # Re-find start of 3's after possible overwrite
    start3 = 0
    while start3 < len(crop) and crop[start3] == 5:
        start3 += 1
    num3 = 0
    i = start3
    while i < len(crop) and crop[i] == 3:
        num3 += 1
        i += 1
    if num3 < 6:
        for j in range(6 - num3):
            if i + j < len(crop):
                crop[i + j] = 3
    return crop

def apply_overlay(crop: List[int], pattern: List[int]) -> List[int]:
    """Apply pattern overlay starting from position 9, every 6 positions, replacing first 3."""
    p = pattern[:]
    # Pad to 3 with last element
    while len(p) < 3 and p:
        p.append(p[-1])
    p = p[:3]
    result = crop[:]
    # Handle 1's by replacing with 4
    p = [4 if x == 1 else x for x in p]
    for start in range(9, 24, 6):
        for k in range(3):
            if start + k < 24:
                result[start + k] = p[k]
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: crop, extract pattern with carry/cycle, normalize header, apply overlay."""
    if not g:
        return []
    height = len(g)
    current_pattern: List[int] = []
    consecutive_empty = 0
    result: List[List[int]] = []
    for r in range(height):
        row = g[r]
        left = row[:5]
        crop = row[6:30][:]  # copy
        pattern = get_pattern(left)
        if not pattern:
            consecutive_empty += 1
            pattern = current_pattern
            if consecutive_empty > 1 and pattern:
                pattern = pattern[1:] + [pattern[0]]
        else:
            consecutive_empty = 0
            current_pattern = pattern
        # Normalize header if applicable (assume for all)
        crop = normalize_header(crop)
        # Apply overlay if pattern
        if pattern:
            crop = apply_overlay(crop, pattern)
        result.append(crop)
    return result
```