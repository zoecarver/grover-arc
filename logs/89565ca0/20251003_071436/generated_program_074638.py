```python
from typing import List, Set

def get_colors(g: List[List[int]]) -> Set[int]:
    colors = set()
    for row in g:
        for cell in row:
            if cell != 0:
                colors.add(cell)
    return colors

def get_filler(colors: Set[int]) -> int:
    standard = {1, 2, 3, 4, 8}
    for c in colors:
        if c not in standard:
            return c
    raise ValueError("No filler color found")

def get_bar_order(colors: Set[int]) -> List[int]:
    bars = []
    if 8 in colors:
        bars.append(8)
    if 1 in colors:
        bars.append(1)
    if 4 in colors:
        if 2 in colors:
            bars.append(2)
        bars.append(4)
        if 3 in colors:
            bars.append(3)
    else:
        if 3 in colors:
            bars.append(3)
        if 2 in colors:
            bars.append(2)
    return bars

def get_lengths(bars: List[int], colors: Set[int]) -> List[int]:
    has_8 = 8 in colors
    has_3 = 3 in colors
    has_4 = 4 in colors
    lengths = []
    for c in bars:
        if c == 8:
            lengths.append(1)
        elif c == 1:
            lengths.append(2 if has_8 else 1)
        elif c == 2:
            lengths.append(3 if has_8 else 4)
        elif c == 4:
            lengths.append(4 if not has_3 else 3)
        elif c == 3:
            lengths.append(4 if has_4 else 2)
        else:
            lengths.append(0)
    return lengths

def program(g: List[List[int]]) -> List[List[int]]:
    colors = get_colors(g)
    filler = get_filler(colors)
    bars = get_bar_order(colors)
    lengths = get_lengths(bars, colors)
    output = []
    for i in range(len(bars)):
        c = bars[i]
        l = lengths[i]
        row = [c] * l + [filler] * (4 - l)
        output.append(row)
    return output
```