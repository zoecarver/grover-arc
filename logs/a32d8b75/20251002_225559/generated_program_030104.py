```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[6:30] for row in g]
    previous_pattern = []
    consecutive_empty = 0
    for i in range(len(out)):
        left = g[i][0:5]
        pattern = get_pattern(left)
        is_empty = len(pattern) == 0
        if is_empty:
            consecutive_empty += 1
            pattern = get_empty_pattern(previous_pattern, consecutive_empty)
        else:
            consecutive_empty = 0
            previous_pattern = pattern
        if all(x == 1 for x in pattern if pattern):
            num1 = len(pattern)
            base_p = [4, 4, 7]
            rot = num1 % 3
            for _ in range(rot):
                base_p = rotate_left(base_p)
            pattern = base_p
        pattern = [4 if x == 1 else x for x in pattern]
        pattern = pad_pattern(pattern)
        if all(x == 4 for x in pattern) and any(x == 8 for x in out[i]):
            pattern = [4, 4, 7]
        step = 3 if any(x == 1 for x in left) else 6
        out[i] = apply_overlay(out[i], pattern, step)
        if is_empty and not any(x == 8 for x in out[i]):
            out[i] = normalize_header(out[i])
    return out

def get_pattern(left: List[int]) -> List[int]:
    frame = {0, 6}
    i = 0
    while i < 5 and left[i] in frame:
        i += 1
    if i == 5:
        return []
    leading7 = 0
    j = i
    while j < 5 and left[j] == 7:
        leading7 += 1
        j += 1
    if j == 5:
        return []
    base = left[j]
    j += 1
    pattern = [base] * (leading7 + 1)
    trailing7 = 0
    while j < 5 and left[j] == 7:
        trailing7 += 1
        j += 1
    pattern += [7] * trailing7
    while j < 5 and left[j] not in frame and left[j] != 0:
        pattern.append(left[j])
        j += 1
    return pattern

def rotate_left(p: List[int]) -> List[int]:
    if len(p) == 0:
        return p
    return p[1:] + [p[0]]

def get_empty_pattern(previous_p: List[int], consecutive: int) -> List[int]:
    if consecutive == 1 and previous_p:
        return rotate_left(previous_p)
    return [4, 4, 4]

def pad_pattern(p: List[int]) -> List[int]:
    p = p[:]
    while len(p) < 3:
        if p:
            p.append(p[-1])
        else:
            p.append(0)
    return p[:3]

def apply_overlay(row: List[int], p: List[int], step: int) -> List[int]:
    result = row[:]
    pos = 9
    while pos < 24:
        for k in range(len(p)):
            if pos + k < 24:
                result[pos + k] = p[k]
        pos += step
    return result

def normalize_header(row: List[int]) -> List[int]:
    result = row[:]
    i = 0
    while i < 24 and result[i] == 5:
        i += 1
    num5 = i
    if num5 < 3:
        for k in range(3 - num5):
            if i + k < 24:
                result[i + k] = 5
    i = 0
    while i < 24 and result[i] == 5:
        i += 1
    start3 = i
    num3 = 0
    while i < 24 and result[i] == 3:
        num3 += 1
        i += 1
    if num3 < 6:
        for k in range(6 - num3):
            if i + k < 24:
                result[i + k] = 3
    return result
```