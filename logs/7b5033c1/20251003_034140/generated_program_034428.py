```python
from typing import List
import collections

def count_frequencies(grid: List[List[int]]) -> collections.Counter:
    flat = [cell for row in grid for cell in row]
    return collections.Counter(flat)

def find_background(counter: collections.Counter) -> int:
    return max(counter, key=counter.get)

def find_color_order(grid: List[List[int]], background: int) -> List[int]:
    seen = set()
    order = []
    for row in grid:
        for cell in row:
            if cell != background and cell not in seen:
                seen.add(cell)
                order.append(cell)
    return order

def build_output(order: List[int], counter: collections.Counter) -> List[List[int]]:
    result = []
    for color in order:
        for _ in range(counter[color]):
            result.append([color])
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    freq = count_frequencies(g)
    bg = find_background(freq)
    ord_colors = find_color_order(g, bg)
    return build_output(ord_colors, freq)
```