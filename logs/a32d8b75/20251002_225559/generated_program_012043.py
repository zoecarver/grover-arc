```python
def crop_right_part(g: List[List[int]]) -> List[List[int]]:
    """Crops the input grid to remove the left 6 columns, preserving the main content on the right."""
    return [row[6:] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    return crop_right_part(g)
```