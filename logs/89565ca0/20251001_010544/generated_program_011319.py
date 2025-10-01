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

def handle_one(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    if 1 in colors:
        length = 2 if has_eight else 1
        return [(1, length)]
    return []

def handle_two_with_eight(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    if 2 in colors and has_eight:
        return [(2, 3)]
    return []

def handle_two_no_eight(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    if 2 in colors and not has_eight:
        return [(2, 4)]
    return []

def handle_three_four(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    result = []
    if 4 in colors:
        length_four = 3 if has_eight and 3 in colors else (4 if has_eight else 2)
        result.append((4, length_four))
    elif 3 in colors:
        length_three = 4 if has_eight else 2
        result.append((3, length_three))
    if 3 in colors and 4 in colors:
        length_three_extra = 4 if has_eight else 3
        result.append((3, length_three_extra))
    return result

def get_mains_and_lengths(colors: Set[int]) -> List[Tuple[int, int]]:
    has_eight = 8 in colors
    mains = (
        handle_eight(colors) +
        handle_one(colors, has_eight) +
        handle_two_with_eight(colors, has_eight) +
        handle_three_four(colors, has_eight) +
        handle_two_no_eight(colors, has_eight)
    )
    return mains

def program(g: List[List[int]]) -> List[List[int]]:
    colors = get_colors(g)
    background = determine_background(colors)
    mains_lengths = get_mains_and_lengths(colors)
    output: List[List[int]] = []
    for color, length in mains_lengths:
        row = [color] * length + [background] * (4 - length)
        output.append(row)
    return output
```