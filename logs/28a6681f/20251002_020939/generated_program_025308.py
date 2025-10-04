```python
from typing import List

def fill_same_color_gaps(row: List[int], max_gap: int) -> List[int]:
    new_row = row[:]
    i = 0
    while i < 10:
        if new_row[i] > 1:
            c = new_row[i]
            while i < 10 and new_row[i] == c:
                i += 1
            gap_start = i
            gap_size = 0
            while i < 10 and new_row[i] == 0:
                i += 1
                gap_size += 1
            if 1 <= gap_size <= max_gap and i < 10 and new_row[i] == c:
                for k in range(gap_start, i):
                    new_row[k] = 1
                while i < 10 and new_row[i] == c:
                    i += 1
        else:
            i += 1
    return new_row

def fill_different_color_gaps(row: List[int], max_gap: int) -> List[int]:
    new_row = row[:]
    i = 0
    while i < 10:
        if new_row[i] > 1:
            c = new_row[i]
            while i < 10 and new_row[i] == c:
                i += 1
            gap_start = i
            gap_size = 0
            while i < 10 and new_row[i] == 0:
                i += 1
                gap_size += 1
            if 1 <= gap_size <= max_gap and i < 10 and new_row[i] > 1 and new_row[i] != c and (c % 2 == 1) and (new_row[i] % 2 == 1):
                for k in range(gap_start, i):
                    new_row[k] = 1
                c2 = new_row[i]
                while i < 10 and new_row[i] == c2:
                    i += 1
        else:
            i += 1
    return new_row

def connect_support_to_ones(row: List[int], max_zeros: int) -> List[int]:
    new_row = row[:]
    i = 0
    while i < 10:
        if new_row[i] > 1:
            c = new_row[i]
            while i < 10 and new_row[i] == c:
                i += 1
            count = 0
            j = i
            while j < 10 and count < max_zeros and new_row[j] == 0:
                count += 1
                j += 1
            if count > 0 and j < 10 and new_row[j] == 1:
                for k in range(i, i + count):
                    new_row[k] = 1
        else:
            i += 1
    return new_row

def connect_support_to_ones_backward(row: List[int], max_zeros: int) -> List[int]:
    new_row = row[:]
    i = 9
    while i >= 0:
        if new_row[i] > 1:
            c = new_row[i]
            temp_i = i
            while temp_i >= 0 and new_row[temp_i] == c:
                temp_i -= 1
            start = temp_i + 1
            j = start - 1
            count = 0
            k = j
            while k >= 0 and count < max_zeros and new_row[k] == 0:
                count += 1
                k -= 1
            if count > 0 and k >= 0 and new_row[k] == 1:
                for m in range(k + 1, k + 1 + count):
                    new_row[m] = 1
            i = start - 1
        else:
            i -= 1
    return new_row

def remove_stray_ones(row: List[int], supports: set) -> List[int]:
    new_row = row[:]
    i = 0
    while i < 10:
        if new_row[i] == 1:
            start = i
            while i < 10 and new_row[i] == 1:
                i += 1
            end = i - 1
            has_support = False
            if start > 0 and new_row[start - 1] in supports:
                has_support = True
            if end < 9 and new_row[end + 1] in supports:
                has_support = True
            if not has_support:
                for k in range(start, end + 1):
                    new_row[k] = 0
        else:
            i += 1
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    result = [row[:] for row in g]
    supports = {2, 3, 4, 5}
    max_gap = 3
    max_zeros = 3
    for r in range(10):
        row = result[r]
        row = fill_same_color_gaps(row, max_gap)
        row = fill_different_color_gaps(row, max_gap)
        row = connect_support_to_ones(row, max_zeros)
        row = connect_support_to_ones_backward(row, max_zeros)
        row = remove_stray_ones(row, supports)
        result[r] = row
    return result
```