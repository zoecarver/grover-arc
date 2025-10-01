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
    non_standard = colors - standard
    return next(iter(non_standard))

def has_eight(colors: Set[int]) -> bool:
    return 8 in colors

def handle_eight(colors: Set[int]) -> List[Tuple[int, int]]:
    if 8 in colors:
        return [(8, 1)]
    return []

def handle_one(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    if 1 in colors:
        length = 2 if has_eight else 1
        return [(1, length)]
    return []

def handle_two(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    if 2 in colors:
        length = 3 if has_eight else 4
        return [(2, length)]
    return []

def handle_three_four(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    has3 = 3 in colors
    has4 = 4 in colors
    res: List[Tuple[int, int]] = []
    if has4:
        if has_eight:
            l4 = 3 if has3 else 4
        else:
            l4 = 2
        res.append((4, l4))
    elif has3:
        if has_eight:
            l3 = 4
        else:
            l3 = 2
        res.append((3, l3))
    if has3 and has4:
        if has_eight:
            l3_extra = 4
        else:
            l3_extra = 3
        res.append((3, l3_extra))
    return res

def program(g: List[List[int]]) -> List[List[int]]:
    colors = get_colors(g)
    bg = determine_background(colors)
    has8 = has_eight(colors)
    mains: List[Tuple[int, int]] = []
    mains += handle_eight(colors)
    mains += handle_one(colors, has8)
    if has8:
        mains += handle_two(colors, has8)
        mains += handle_three_four(colors, has8)
    else:
        mains += handle_three_four(colors, has8)
        mains += handle_two(colors, has8)
    output: List[List[int]] = []
    for color, length in mains:
        row = [color] * length + [bg] * (4 - length)
        output.append(row)
    return output
```