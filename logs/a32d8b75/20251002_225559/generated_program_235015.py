```python
from typing import List

def get_pattern(left: List[int]) -> List[int]:
    frame = {0, 6, 7}
    i = 0
    leading = 0
    while i < 5 and left[i] in frame:
        leading += 1
        i += 1
    if i == 5:
        return []
    first = left[i]
    if first in frame:
        return []
    pattern = [first] * leading
    if leading == 0:
        pattern = [first]
    for j in range(i + 1, 5):
        if left[j] != 0:
            pattern.append(left[j])
    return pattern

def rotate_left(p: List[int]) -> List[int]:
    if not p:
        return []
    return p[1:] + [p[0]]

def pad_pattern(p: List[int]) -> List[int]:
    while len(p) < 3:
        if p:
            p.append(p[-1])
        else:
            p.append(0)
    return p[:3]

def map_pattern(p: List[int]) -> List[int]:
    return [4 if x == 1 else x for x in p]

def normalize_header(row: List[int]) -> List[int]:
    row = row[:]
    # Extend 5's to 3
    i = 0
    num5 = 0
    while i < len(row) and row[i] == 5:
        num5 += 1
        i += 1
    if num5 < 3:
        for j in range(3 - num5):
            if i + j < len(row):
                row[i + j] = 5
    # Extend 3's to 6
    start3 = 0
    while start3 < len(row) and row[start3] == 5:
        start3 += 1
    i = start3
    num3 = 0
    while i < len(row) and row[i] == 3:
        num3 += 1
        i += 1
    if num3 < 6:
        for j in range(6 - num3):
            if i + j < len(row):
                row[i + j] = 3
    return row

def apply_overlay(row: List[int], p: List[int]) -> List[int]:
    result = row[:]
    for start in range(9, 24, 6):
        for k in range(len(p)):
            pos = start + k
            if pos < 24:
                result[pos] = p[k]
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    height = len(g)
    crop = [row[6:30] for row in g]
    previous_pattern = []
    for r in range(height):
        left = g[r][0:5]
        pattern = get_pattern(left)
        original_len = len(pattern)
        if not pattern:
            if previous_pattern:
                pattern = rotate_left(previous_pattern)
            original_len = len(pattern)
        previous_pattern = pattern
        p = map_pattern(pattern)
        p = pad_pattern(p)
        if original_len == 0:
            crop[r] = normalize_header(crop[r])
        crop[r] = apply_overlay(crop[r], p)
    return crop
```