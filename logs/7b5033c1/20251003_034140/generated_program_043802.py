```python
from collections import Counter
from typing import List

def flatten_grid(grid: List[List[int]]) -> List[int]:
    result = []
    for row in grid:
        result.extend(row)
    return result

def find_background(grid: List[List[int]]) -> int:
    flat = flatten_grid(grid)
    count = Counter(flat)
    return max(count, key=count.get)

def extract_sequence(grid: List[List[int]], bg: int) -> List[int]:
    result = []
    for row in grid:
        for cell in row:
            if cell != bg:
                result.append(cell)
    return result

def to_vertical_list(sequence: List[int]) -> List[List[int]]:
    return [[x] for x in sequence]

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    seq = extract_sequence(g, bg)
    return to_vertical_list(seq)
```