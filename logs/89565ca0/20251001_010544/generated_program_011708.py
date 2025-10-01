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
    return [(8, 1)] if 8 in colors else []

def handle_one(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    if 1 not in colors:
        return []
    length = 2 if has_eight else 1
    return [(1, length)]

def handle_two(colors: Set[int], with_eight: bool) -> List[Tuple[int, int]]:
    if 2 not in colors:
        return []
    length = 3 if with_eight else 4
    return [(2, length)]

def handle_three_four(colors: Set[int], has_eight: bool, mains: List[Tuple[int, int]]) -> None:
    has_three = 3 in colors
    has_four = 4 in colors
    if not (has_three or has_four):
        return
    if has_eight:
        if has_four:
            length_four = 3 if has_three else 4
            mains.append((4, length_four))
        if has_three:
            mains.append((3, 4))
    else:
        if has_four:
            mains.append((4, 2))
        if has_three:
            length_three = 3 if has_four else 2
            mains.append((3, length_three))

def get_mains_and_lengths(colors: Set[int]) -> List[Tuple[int, int]]:
    has_eight = 8 in colors
    mains: List[Tuple[int, int]] = []
    mains.extend(handle_eight(colors))
    mains.extend(handle_one(colors, has_eight))
    if has_eight:
        mains.extend(handle_two(colors, True))
    handle_three_four(colors, has_eight, mains)
    if not has_eight:
        mains.extend(handle_two(colors, False))
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