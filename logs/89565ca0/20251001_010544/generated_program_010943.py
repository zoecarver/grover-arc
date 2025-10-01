```python
from typing import List, Set, Tuple

def get_colors(g: List[List[int]]) -> Set[int]:
    colors: Set[int] = set()
    for row in g:
        for val in row:
            if val != 0:
                colors.add(val)
    return colors

def determine_background(colors: Set[int]) -> int:
    standard = {1, 2, 3, 4, 8}
    extra = colors - standard
    return next(iter(extra))

def get_mains_and_lengths(colors: Set[int]) -> List[Tuple[int, int]]:
    has_eight = 8 in colors
    mains_lens: List[Tuple[int, int]] = []
    if has_eight:
        mains_lens.append((8, 1))
    if 1 in colors:
        l = 2 if has_eight else 1
        mains_lens.append((1, l))
    if 2 in colors and has_eight:
        mains_lens.append((2, 3))
    if 4 in colors:
        if has_eight:
            l = 3 if 3 in colors else 4
        else:
            l = 2
        mains_lens.append((4, l))
    elif 3 in colors:
        if has_eight:
            l = 4
        else:
            l = 2
        mains_lens.append((3, l))
    if 3 in colors and 4 in colors:
        l = 4 if has_eight else 3
        mains_lens.append((3, l))
    if 2 in colors and not has_eight:
        mains_lens.append((2, 4))
    return mains_lens

def program(g: List[List[int]]) -> List[List[int]]:
    colors = get_colors(g)
    bg = determine_background(colors)
    mains_lens = get_mains_and_lengths(colors)
    output: List[List[int]] = []
    for colr, length in mains_lens:
        row = [colr] * length + [bg] * (4 - length)
        output.append(row)
    return output
```