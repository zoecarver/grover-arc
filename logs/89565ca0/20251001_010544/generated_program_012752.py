```python
from typing import List, Set, Tuple

def get_colors(g: List[List[int]]) -> Set[int]:
    """Extracts the set of unique non-zero colors from the input grid, ignoring positions and zeros."""
    colors: Set[int] = set()
    for row in g:
        for val in row:
            if val != 0:
                colors.add(val)
    return colors

def determine_background(colors: Set[int]) -> int:
    """Identifies the background color as the unique non-standard color (not in {1,2,3,4,8})."""
    standard = {1, 2, 3, 4, 8}
    non_standard = colors - standard
    return next(iter(non_standard))

def has_eight(colors: Set[int]) -> bool:
    """Checks if color 8 is present in the colors set."""
    return 8 in colors

def get_eight_row(colors: Set[int]) -> List[Tuple[int, int]]:
    """Handles the rule for color 8: always length 1 if present, as the first row."""
    if 8 in colors:
        return [(8, 1)]
    return []

def get_one_row(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    """Handles the rule for color 1: length 2 if 8 present, else 1, if present."""
    if 1 not in colors:
        return []
    length = 2 if has_eight else 1
    return [(1, length)]

def get_two_row_with_eight(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    """Handles the rule for color 2 when 8 is present: length 3 if both present."""
    if has_eight and 2 in colors:
        return [(2, 3)]
    return []

def get_three_four_rows(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    """Handles the interdependent rules for colors 3 and 4: prioritizes 4, adds extra 3 if both present, with lengths adjusted by 8's presence."""
    res: List[Tuple[int, int]] = []
    if 4 in colors:
        length = 3 if has_eight and 3 in colors else (4 if has_eight else 2)
        res.append((4, length))
    elif 3 in colors:
        length = 4 if has_eight else 2
        res.append((3, length))
    if 3 in colors and 4 in colors:
        extra_length = 4 if has_eight else 3
        res.append((3, extra_length))
    return res

def get_two_row_no_eight(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    """Handles the rule for color 2 when 8 is absent: length 4 if present."""
    if not has_eight and 2 in colors:
        return [(2, 4)]
    return []

def get_mains_and_lengths(colors: Set[int], has_eight: bool) -> List[Tuple[int, int]]:
    """Composes all color-specific rules into an ordered list of (color, length) pairs for output rows."""
    mains = (
        get_eight_row(colors) +
        get_one_row(colors, has_eight) +
        get_two_row_with_eight(colors, has_eight) +
        get_three_four_rows(colors, has_eight) +
        get_two_row_no_eight(colors, has_eight)
    )
    return mains

def build_output_row(color: int, length: int, background: int) -> List[int]:
    """Builds a single output row: repeats the color for the given length, pads with background to 4 columns."""
    return [color] * length + [background] * (4 - length)

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: extracts colors, determines background and eight presence, computes mains and lengths, builds padded rows."""
    colors = get_colors(g)
    background = determine_background(colors)
    has_eight_flag = has_eight(colors)
    mains_lens = get_mains_and_lengths(colors, has_eight_flag)
    output: List[List[int]] = []
    for color, length in mains_lens:
        row = build_output_row(color, length, background)
        output.append(row)
    return output
```