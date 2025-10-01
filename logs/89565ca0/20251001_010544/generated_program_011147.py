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

def handle_eight(colors: Set[int]) -> List[Tuple[int, int]]:
    if 8 in colors:
        return [(8, 1)]
    return []

def handle_one(colors: Set[int]) -> List[Tuple[int, int]]:
    has_eight = 8 in colors
    if 1 in colors:
        return [(1, 2 if has_eight else 1)]
    return []

def handle_two_with_eight(colors: Set[int]) -> List[Tuple[int, int]]:
    if 2 in colors and 8 in colors:
        return [(2, 3)]
    return []

def handle_three_four(colors: Set[int]) -> List[Tuple[int, int]]:
    has_eight = 8 in colors
    has_three = 3 in colors
    has_four = 4 in colors
    res: List[Tuple[int, int]] = []
    if has_four:
        l4 = 3 if has_eight and has_three else (4 if has_eight else 2)
        res.append((4, l4))
        if has_three:
            l3 = 4 if has_eight else 3
            res.append((3, l3))
    elif has_three:
        l3 = 4 if has_eight else 2
        res.append((3, l3))
    return res

def handle_two_no_eight(colors: Set[int]) -> List[Tuple[int, int]]:
    if 2 in colors and 8 not in colors:
        return [(2, 4)]
    return []

def get_mains_and_lengths(colors: Set[int]) -> List[Tuple[int, int]]:
    mains = (
        handle_eight(colors) +
        handle_one(colors) +
        handle_two_with_eight(colors) +
        handle_three_four(colors) +
        handle_two_no_eight(colors)
    )
    return mains

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