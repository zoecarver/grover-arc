```python
from typing import List

def find_special_color(g: List[List[int]]) -> int:
    """Find the special non-zero color in the grid."""
    colors = set()
    for row in g:
        for val in row:
            if val != 0:
                colors.add(val)
    return list(colors)[0] if colors else 0

def fill_gaps_in_row(row: List[int], special: int) -> List[int]:
    """Fill gaps between special color positions in the row with 1."""
    new_row = row[:]
    positions = [i for i, val in enumerate(row) if val == special]
    if len(positions) < 2:
        return new_row
    positions.sort()
    for idx in range(len(positions) - 1):
        start = positions[idx] + 1
        end = positions[idx + 1]
        for j in range(start, end):
            new_row[j] = 1
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: copy grid and fill horizontal gaps with 1 between special colors."""
    if not g or not g[0]:
        return g
    result = [row[:] for row in g]
    special = find_special_color(g)
    if special == 0:
        return result
    for r in range(len(result)):
        result[r] = fill_gaps_in_row(result[r], special)
    return result
```