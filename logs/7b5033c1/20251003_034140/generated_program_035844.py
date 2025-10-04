```python
from typing import List
import collections
import itertools

def flatten_grid(grid: List[List[int]]) -> List[int]:
    """
    Flattens the 2D grid into a 1D list in row-major order.
    Handles the observation that processing occurs in row-major traversal.
    """
    return list(itertools.chain.from_iterable(grid))

def compute_frequencies(flat: List[int]) -> collections.Counter:
    """
    Computes the frequency count of all colors in the flattened grid.
    Handles the rule that background is the most frequent color, requiring global counts.
    """
    return collections.Counter(flat)

def identify_background(frequencies: collections.Counter) -> int:
    """
    Identifies the background color as the most frequent one.
    Handles the observation that background dominates the grid frequency.
    """
    return max(frequencies, key=frequencies.get)

def determine_first_appearance_order(flat: List[int], background: int) -> List[int]:
    """
    Determines the order of first appearances of non-background colors in the flattened list.
    Handles the rule that colors are ordered by their initial encounter in row-major order.
    """
    seen = set()
    order = []
    for cell in flat:
        if cell != background and cell not in seen:
            seen.add(cell)
            order.append(cell)
    return order

def build_vertical_stack(order: List[int], frequencies: collections.Counter) -> List[List[int]]:
    """
    Builds the output as a vertical stack of singleton lists, grouped by color order and total counts.
    Handles the transformation to serialize non-background cells by color groups into 1xN format.
    """
    return list(itertools.chain.from_iterable([[color]] * frequencies[color] for color in order))

def program(g: List[List[int]]) -> List[List[int]]:
    flat = flatten_grid(g)
    frequencies = compute_frequencies(flat)
    background = identify_background(frequencies)
    color_order = determine_first_appearance_order(flat, background)
    return build_vertical_stack(color_order, frequencies)
```