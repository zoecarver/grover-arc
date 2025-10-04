```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    def get_pattern(left: List[int]) -> List[int]:
        frame = {0, 6, 7}
        leading = 0
        while leading < 5 and left[leading] in frame:
            leading += 1
        if leading == 5:
            return []
        pattern = []
        first = left[leading]
        pattern = [first] * leading
        for i in range(leading + 1, 5):
            if left[i] not in frame and left[i] != 0:
                pattern.append(left[i])
        return pattern

    def pad_pattern(p: List[int]) -> List[int]:
        while len(p) < 3:
            if p:
                p.append(p[-1])
            else:
                p.append(0)
        return p[:3]

    def is_all_one(p: List[int]) -> bool:
        return all(x == 1 for x in p)

    def apply_overlay(row: List[int], p: List[int], all_one: bool) -> List[int]:
        result = row[:]
        step = 3 if all_one else 6
        for start in range(9, 24, step):
            for k in range(len(p)):
                pos = start + k
                if pos < 24:
                    result[pos] = p[k]
        return result

    previous_p = []
    all_one_flag = False
    out = []
    for row in g:
        crop = row[6:30]
        left = row[0:5]
        p = get_pattern(left)
        current_all_one = False
        if not p:
            p = previous_p[:]
            current_all_one = all_one_flag
        else:
            original_p = p[:]
            p = pad_pattern(p)
            current_all_one = is_all_one(original_p)
            if current_all_one:
                p = [4, 7, 4]
            previous_p = p[:]
            all_one_flag = current_all_one
        if p:
            crop = apply_overlay(crop, p, current_all_one)
        out.append(crop)
    return out
```