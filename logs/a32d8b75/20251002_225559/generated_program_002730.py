```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    def crop_left_border(grid: List[List[int]]) -> List[List[int]]:
        return [row[6:30] for row in grid]

    def get_pattern(left: List[int]) -> List[int]:
        frame = {0, 6, 7}
        i = 0
        while i < 5 and left[i] in frame:
            i += 1
        if i == 5:
            return []
        first = left[i]
        pattern = [first] * i if i > 0 else [first]
        for j in range(i + 1, 5):
            if left[j] != 0:
                pattern.append(left[j])
        return pattern

    def rotate_left(p: List[int]) -> List[int]:
        if not p:
            return p
        return p[1:] + [p[0]]

    def pad_pattern(p: List[int]) -> List[int]:
        p = p[:3]
        while len(p) < 3:
            p.append(p[-1] if p else 0)
        return p

    def map_pattern(p: List[int]) -> List[int]:
        return [4 if x == 1 else x for x in p]

    def apply_overlay(row: List[int], p: List[int]) -> List[int]:
        result = row[:]
        for start in range(9, 24, 6):
            for k in range(3):
                pos = start + k
                if pos < 24:
                    result[pos] = p[k]
        return result

    cropped = crop_left_border(g)
    previous_pattern = []
    output = []
    for i in range(len(g)):
        left = g[i][0:5]
        raw = get_pattern(left)
        if raw:
            p = pad_pattern(raw)
            p = map_pattern(p)
            previous_pattern = p
        else:
            if previous_pattern:
                previous_pattern = rotate_left(previous_pattern)
            p = previous_pattern
        row = cropped[i][:]
        if p:
            row = apply_overlay(row, p)
        output.append(row)
    return output
```