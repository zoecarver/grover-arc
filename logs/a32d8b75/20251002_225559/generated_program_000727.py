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

def apply_overlay(row: List[int], pattern: List[int]) -> List[int]:
    result = row[:]
    p = pad_pattern(pattern)
    p = [4 if x == 1 else x for x in p]
    for start in range(9, 24, 6):
        for k in range(3):
            pos = start + k
            if pos < 24:
                result[pos] = p[k]
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    result = []
    previous_pattern = []
    for row in g:
        crop = row[6:30]
        left = row[0:5]
        pattern = get_pattern(left)
        if not pattern:
            pattern = rotate_left(previous_pattern)
        crop = apply_overlay(crop, pattern)
        result.append(crop)
        if get_pattern(left):
            previous_pattern = get_pattern(left)
        else:
            previous_pattern = pattern
    for row in result:
        for i in range(len(row)):
            if row[i] == 0 or row[i] == 6:
                row[i] = 9
    return result
```