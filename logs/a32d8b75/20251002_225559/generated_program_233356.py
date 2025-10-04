```python
from typing import List

def crop_left_border(g: List[List[int]]) -> List[List[int]]:
    """
    Rule: Remove the left border consisting of the first 6 columns (indices 0-5),
    which contain the frame (6's) and margin patterns. The interior content starts
    at index 6 and goes to the end (index 29 for 30-column inputs), resulting in
    24 columns per row. This extracts the main puzzle image from the bordered input.
    Applicable to all examples as the main content is consistently positioned after
    the left border.
    """
    return [row[6:30] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    return crop_left_border(g)
```