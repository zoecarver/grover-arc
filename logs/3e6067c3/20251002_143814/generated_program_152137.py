```python
from typing import List
from copy import deepcopy

def fill_eights_between_same_color(g: List[List[int]]) -> List[List[int]]:
    """
    Fills sequences of 8's in each row if they are bounded by the same non-8 color on both sides.
    This handles internal 8's in colored regions, as observed in test inputs.
    """
    g = deepcopy(g)
    for r in range(len(g)):
        row = g[r]
        i = 0
        n = len(row)
        while i < n:
            if row[i] != 8:
                i += 1
                continue
            start = i
            while i < n and row[i] == 8:
                i += 1
            end = i - 1
            # Find left bounding non-8
            l = start - 1
            while l >= 0 and row[l] == 8:
                l -= 1
            left_c = row[l] if l >= 0 else 0
            # Find right bounding non-8
            r = end + 1
            while r < n and row[r] == 8:
                r += 1
            right_c = row[r] if r < n else 0
            if left_c == right_c and left_c > 1:
                for k in range(start, end + 1):
                    row[k] = left_c
        g[r] = row
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Composes the rules to transform the grid.
    Currently handles filling internal 8's in colored regions for test validity.
    """
    g = fill_eights_between_same_color(g)
    return g
```