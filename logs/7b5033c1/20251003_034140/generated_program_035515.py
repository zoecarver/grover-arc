```python
from collections import Counter
from typing import List

def find_background(grid: List[List[int]]) -> int:
    """
    Identifies the background color as the most frequent color in the grid.
    """
    flat = [cell for row in grid for cell in row]
    counts = Counter(flat)
    return counts.most_common(1)[0][0]

def extract_non_background_sequence(grid: List[List[int]], background: int) -> List[int]:
    """
    Extracts non-background cells in row-major order.
    """
    sequence = []
    for row in grid:
        for cell in row:
            if cell != background:
                sequence.append(cell)
    return sequence

def format_as_vertical_stack(sequence: List[int]) -> List[List[int]]:
    """
    Formats the sequence of colors as a list of singleton lists for vertical output.
    """
    return [[color] for color in sequence]

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    seq = extract_non_background_sequence(g, bg)
    return format_as_vertical_stack(seq)
```