```python
from typing import List
from collections import Counter


def find_background(grid: List[List[int]]) -> int:
    """
    Identifies the background color as the most frequent value in the grid.
    """
    all_values = []
    for row in grid:
        all_values.extend(row)
    counts = Counter(all_values)
    return counts.most_common(1)[0][0]


def collect_non_background(grid: List[List[int]], background: int) -> List[int]:
    """
    Collects all non-background colors in row-major order (top to bottom, left to right).
    """
    sequence = []
    for row in grid:
        for cell in row:
            if cell != background:
                sequence.append(cell)
    return sequence


def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: finds background, collects non-background cells, and formats as singleton rows.
    """
    background = find_background(g)
    sequence = collect_non_background(g, background)
    return [[color] for color in sequence]
```