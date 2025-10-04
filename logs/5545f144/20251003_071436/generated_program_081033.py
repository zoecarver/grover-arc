```python
from typing import List
import collections

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return collections.Counter(flat).most_common(1)[0][0]

def get_small_color(g: List[List[int]], background: int) -> int:
    if not g or not g[0]:
        return background
    flat = [cell for row in g for cell in row if cell != background]
    if not flat:
        return background
    return collections.Counter(flat).most_common(1)[0][0]

def get_left_width(g: List[List[int]], background: int) -> int:
    if not g or not g[0]:
        return 0
    height = len(g)
    width = len(g[0])
    for j in range(width):
        col = [row[j] for row in g]
        first = col[0]
        if all(v == first for v in col) and first != background:
            return j
    return width

def build_output(g: List[List[int]], left_width: int, background: int, small: int) -> List[List[int]]:
    if not g:
        return []
    height = len(g)
    output = [[background] * left_width for _ in range(height)]
    input_width = len(g[0]) if g[0] else 0
    for i in range(height):
        for k in range(min(left_width, input_width)):
            if g[i][k] == small:
                output[i][k] = small
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    background = get_background(g)
    small = get_small_color(g, background)
    left_width = get_left_width(g, background)
    return build_output(g, left_width, background, small)
```