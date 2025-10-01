```python
from typing import List, Set

def extract_colors(g: List[List[int]]) -> Set[int]:
    colors: Set[int] = set()
    for row in g:
        for val in row:
            if val != 0:
                colors.add(val)
    return colors

def find_background(colors: Set[int]) -> int:
    standard = {1, 2, 3, 4, 8}
    non_standard = colors - standard
    return next(iter(non_standard))

def handle_eight(colors: Set[int], bg: int) -> List[List[int]]:
    if 8 not in colors:
        return []
    return [[8, bg, bg, bg]]

def handle_one(colors: Set[int], bg: int) -> List[List[int]]:
    if 1 not in colors:
        return []
    length = 2 if 8 in colors else 1
    return [[1] * length + [bg] * (4 - length)]

def handle_two_with_eight(colors: Set[int], bg: int) -> List[List[int]]:
    if 2 not in colors or 8 not in colors:
        return []
    return [[2, 2, 2, bg]]

def handle_three_four(colors: Set[int], bg: int) -> List[List[int]]:
    rows: List[List[int]] = []
    has_e = 8 in colors
    has_3 = 3 in colors
    has_4 = 4 in colors
    if has_4:
        l4 = 2
        if has_e:
            l4 = 4 if not has_3 else 3
        else:
            l4 = 2
        rows.append([4] * l4 + [bg] * (4 - l4))
    if has_3:
        l3 = 2 if not has_e else 4
        if has_4 and not has_e:
            l3 = 3
        elif has_4 and has_e:
            rows.append([3] * l3 + [bg] * (4 - l3))
        else:
            rows.append([3] * l3 + [bg] * (4 - l3))
    return rows

def handle_two_no_eight(colors: Set[int], bg: int) -> List[List[int]]:
    if 2 in colors and 8 not in colors:
        return [[2, 2, 2, 2]]
    return []

def program(g: List[List[int]]) -> List[List[int]]:
    colors = extract_colors(g)
    bg = find_background(colors)
    rows = (
        handle_eight(colors, bg) +
        handle_one(colors, bg) +
        handle_two_with_eight(colors, bg) +
        handle_three_four(colors, bg) +
        handle_two_no_eight(colors, bg)
    )
    return rows
```