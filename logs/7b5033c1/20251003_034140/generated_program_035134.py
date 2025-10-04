```python
from collections import Counter
from typing import List

def find_background(grid: List[List[int]]) -> int:
    flat = [cell for row in grid for cell in row]
    counts = Counter(flat)
    return counts.most_common(1)[0][0]

def extract_sequence(grid: List[List[int]], bg: int) -> List[int]:
    seq = []
    for row in grid:
        for cell in row:
            if cell != bg:
                seq.append(cell)
    return seq

def format_output(seq: List[int]) -> List[List[int]]:
    return [[color] for color in seq]

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    seq = extract_sequence(g, bg)
    return format_output(seq)
```