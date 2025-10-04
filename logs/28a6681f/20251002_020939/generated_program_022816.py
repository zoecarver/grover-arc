```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    output_grid = [row[:] for row in g]
    supporting = {2, 3, 4, 5}
    n = 10
    for i in range(n):
        new_row = output_grid[i][:]
        # Same color fill
        for start in range(n):
            if new_row[start] > 1:
                c = new_row[start]
                for end in range(start + 2, n):
                    if new_row[end] == c:
                        all_zero = True
                        for m in range(start + 1, end):
                            if new_row[m] != 0:
                                all_zero = False
                                break
                        if all_zero:
                            for m in range(start + 1, end):
                                new_row[m] = 1
        # Connect fill
        for start in range(n):
            if new_row[start] > 1:
                pos = start + 1
                zeros = 0
                while pos < n and new_row[pos] == 0 and zeros < 3:
                    pos += 1
                    zeros += 1
                if pos < n and new_row[pos] == 1 and zeros > 0:
                    for m in range(start + 1, pos):
                        new_row[m] = 1
        # Removal of unsupported 1 groups
        j = 0
        while j < n:
            if new_row[j] == 1:
                group_start = j
                while j < n and new_row[j] == 1:
                    j += 1
                group_end = j - 1
                supported = False
                if group_start > 0 and new_row[group_start - 1] in supporting:
                    supported = True
                if group_end < n - 1 and new_row[group_end + 1] in supporting:
                    supported = True
                if not supported:
                    for m in range(group_start, group_end + 1):
                        new_row[m] = 0
            else:
                j += 1
        output_grid[i] = new_row
    return output_grid
```