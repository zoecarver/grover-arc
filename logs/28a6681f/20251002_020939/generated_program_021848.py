```python
from typing import List

def remove_stray_in_row(row: List[int]) -> List[int]:
    new_row = row[:]
    i = 0
    while i < 10:
        if new_row[i] == 1:
            start = i
            while i < 10 and new_row[i] == 1:
                i += 1
            end = i - 1
            # Find nearest left non-0 non-1
            left_non1 = -1
            for j in range(start - 1, -1, -1):
                if new_row[j] != 0 and new_row[j] != 1:
                    left_non1 = j
                    break
            if left_non1 == -1:
                left_sep = 999
            else:
                left_sep = start - left_non1 - 1
            remove = left_sep >= 4
            if not remove:
                # Compute right_open
                k = end + 1
                right_open = 0
                while k < 10 and new_row[k] == 0:
                    right_open += 1
                    k += 1
                if right_open >= 3:
                    remove = True
            if remove:
                for j in range(start, end + 1):
                    new_row[j] = 0
        else:
            i += 1
    return new_row

def fill_gaps_in_row(row: List[int]) -> List[int]:
    new_row = row[:]
    i = 0
    while i < 10:
        if new_row[i] != 0:
            i += 1
            continue
        start = i
        while i < 10 and new_row[i] == 0:
            i += 1
        end = i - 1
        if start == 0 or end == 9:
            continue
        left_val = new_row[start - 1]
        right_val = new_row[end + 1]
        if left_val == 0 or right_val == 0:
            continue
        if left_val == right_val or right_val == 1:
            for j in range(start, end + 1):
                new_row[j] = 1
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    output = [row[:] for row in g]
    for r in range(10):
        output[r] = remove_stray_in_row(output[r])
    for r in range(10):
        output[r] = fill_gaps_in_row(output[r])
    return output
```