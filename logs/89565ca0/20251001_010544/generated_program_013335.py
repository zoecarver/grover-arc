```python
from typing import List, Set, Tuple

def get_colors(g: List[List[int]]) -> Set[int]:
    colors: Set[int] = set()
    for row in g:
        for cell in row:
            if cell != 0:
                colors.add(cell)
    return colors

def get_background(colors: Set[int]) -> int:
    standard: Set[int] = {1, 2, 3, 4, 8}
    non_standard: Set[int] = colors - standard
    return next(iter(non_standard))

def get_mains_and_lengths(colors: Set[int]) -> List[Tuple[int, int]]:
    has_eight: bool = 8 in colors
    mains: List[Tuple[int, int]] = []
    if 8 in colors:
        mains.append((8, 1))
    if 1 in colors:
        length_one: int = 2 if has_eight else 1
        mains.append((1, length_one))
    if 2 in colors and has_eight:
        mains.append((2, 3))
    if 4 in colors:
        length_four: int = 2 if not has_eight else (4 if 3 not in colors else 3)
        mains.append((4, length_four))
    if 3 in colors:
        length_three: int = 4 if has_eight else (3 if 4 in colors else 2)
        mains.append((3, length_three))
    if 2 in colors and not has_eight:
        mains.append((2, 4))
    return mains

def build_row(color: int, length: int, background: int) -> List[int]:
    return [color] * length + [background] * (4 - length)

def program(g: List[List[int]]) -> List[List[int]]:
    colors: Set[int] = get_colors(g)
    background: int = get_background(colors)
    mains_lengths: List[Tuple[int, int]] = get_mains_and_lengths(colors)
    return [build_row(color, length, background) for color, length in mains_lengths]
```