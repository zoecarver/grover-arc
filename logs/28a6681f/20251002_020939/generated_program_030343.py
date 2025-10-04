```python
from typing import List

def is_block_supported(g: List[List[int]], r: int, start: int, end: int, c: int) -> bool:
    for k in range(start, end + 1):
        if r > 0 and g[r - 1][k] == c:
            return True
        if r < 9 and g[r + 1][k] == c:
            return True
    return False

def fill_same_color_gaps(g: List[List[int]], row: List[int], r: int, max_gap: int = 3) -> List[int]:
    new_row = row[:]
    i = 0
    while i < 10:
        if new_row[i] > 1:
            c = new_row[i]
            start = i
            while i < 10 and new_row[i] == c:
                i += 1
            end = i - 1
            gap_start = i
            gap_size = 0
            while i < 10 and new_row[i] == 0:
                i += 1
                gap_size += 1
            if 1 <= gap_size <= max_gap and i < 10 and new_row[i] == c:
                right_start = i
                j = i
                while j < 10 and new_row[j] == c:
                    j += 1
                right_end = j - 1
                left_supported = is_block_supported(g, r, start, end, c)
                right_supported = is_block_supported(g, r, right_start, right_end, c)
                if left_supported and right_supported:
                    for k in range(gap_start, i):
                        new_row[k] = 1
                i = j
            # if not, i remains after gap
        else:
            i += 1
    return new_row

def fill_different_color_gaps(g: List[List[int]], row: List[int], r: int, max_gap: int = 3) -> List[int]:
    new_row = row[:]
    i = 0
    while i < 10:
        if new_row[i] > 1:
            c = new_row[i]
            start = i
            while i < 10 and new_row[i] == c:
                i += 1
            end = i - 1
            gap_start = i
            gap_size = 0
            while i < 10 and new_row[i] == 0:
                i += 1
                gap_size += 1
            if 1 <= gap_size <= max_gap and i < 10 and new_row[i] > 1:
                c2 = new_row[i]
                if c2 != c and c % 2 == 1 and c2 % 2 == 1:
                    right_start = i
                    j = i
                    while j < 10 and new_row[j] == c2:
                        j += 1
                    right_end = j - 1
                    left_supported = is_block_supported(g, r, start, end, c)
                    right_supported = is_block_supported(g, r, right_start, right_end, c2)
                    if left_supported and right_supported:
                        for k in range(gap_start, i):
                            new_row[k] = 1
                    i = j
                # else, i remains after gap, outer will process right block
        else:
            i += 1
    return new_row

def connect_support_to_ones_forward(g: List[List[int]], row: List[int], r: int, max_zeros: int = 3) -> List[int]:
    new_row = row[:]
    i = 0
    while i < 10:
        if new_row[i] > 1:
            c = new_row[i]
            start = i
            while i < 10 and new_row[i] == c:
                i += 1
            end = i - 1
            if is_block_supported(g, r, start, end, c):
                j = i
                count = 0
                while j < 10 and count < max_zeros and new_row[j] == 0:
                    j += 1
                    count += 1
                if count > 0 and j < 10 and new_row[j] == 1:
                    for k in range(i, i + count):
                        new_row[k] = 1
            # i remains after block
        else:
            i += 1
    return new_row

def connect_support_to_ones_backward(g: List[List[int]], row: List[int], r: int, max_zeros: int = 3) -> List[int]:
    new_row = row[:]
    i = 0
    while i < 10:
        if new_row[i] > 1:
            c = new_row[i]
            start = i
            while i < 10 and new_row[i] == c:
                i += 1
            end = i - 1
            if is_block_supported(g, r, start, end, c):
                j = start - 1
                count = 0
                while j >= 0 and count < max_zeros and new_row[j] == 0:
                    j -= 1
                    count += 1
                if count > 0 and j >= 0 and new_row[j] == 1:
                    for k in range(start - count, start):
                        new_row[k] = 1
            # i remains after block
        else:
            i += 1
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
    supports = {2, 3, 4, 5}
    new_g = [row[:] for row in g]
    for r in range(10):
        temp = g[r][:]
        temp = fill_same_color_gaps(g, temp, r)
        temp = fill_different_color_gaps(g, temp, r)
        temp = connect_support_to_ones_forward(g, temp, r)
        temp = connect_support_to_ones_backward(g, temp, r)
        temp = remove_stray_ones(temp, supports)
        new_g[r] = temp
    return new_g
```