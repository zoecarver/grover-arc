```python
from collections import Counter
from typing import List

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    counter = Counter(flat)
    return max(counter, key=counter.get)

def find_color_order(g: List[List[int]], bg: int) -> List[int]:
    seen = set()
    order = []
    for row in g:
        for cell in row:
            if cell != bg and cell not in seen:
                seen.add(cell)
                order.append(cell)
    return order

def count_colors(g: List[List[int]]) -> Counter:
    flat = [cell for row in g for cell in row]
    return Counter(flat)

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    order = find_color_order(g, bg)
    counts = count_colors(g)
    result = []
    for color in order:
        count = counts[color]
        for _ in range(count):
            result.append([color])
    return result
```