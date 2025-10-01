```python
from typing import List, Set

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

def build_row(color: int, length: int, bg: int) -> List[int]:
    return [color] * length + [bg] * (4 - length)

def get_eight_row(colors: Set[int], bg: int) -> List[List[int]]:
    if 8 not in colors:
        return []
    return [build_row(8, 1, bg)]

def get_one_row(colors: Set[int], bg: int, has_eight: bool) -> List[List[int]]:
    if 1 not in colors:
        return []
    length = 2 if has_eight else 1
    return [build_row(1, length, bg)]

def get_two_row(colors: Set[int], bg: int, length: int) -> List[List[int]]:
    if 2 not in colors:
        return []
    return [build_row(2, length, bg)]

def get_three_four_rows(colors: Set[int], bg: int, has_eight: bool) -> List[List[int]]:
    rows: List[List[int]] = []
    has3 = 3 in colors
    has4 = 4 in colors
    if has4:
        l4 = 2
        if has_eight:
            l4 = 4 if not has3 else 3
        rows.append(build_row(4, l4, bg))
    if has3:
        l3 = 4 if has_eight else 2
        if has4 and not has_eight:
            l3 = 3
        rows.append(build_row(3, l3, bg))
    return rows

def program(g: List[List[int]]) -> List[List[int]]:
    colors = get_colors(g)
    bg = determine_background(colors)
    has_eight = 8 in colors
    rows = get_eight_row(colors, bg)
    rows += get_one_row(colors, bg, has_eight)
    if has_eight:
        rows += get_two_row(colors, bg, 3)
    rows += get_three_four_rows(colors, bg, has_eight)
    if not has_eight:
        rows += get_two_row(colors, bg, 4)
    return rows
```