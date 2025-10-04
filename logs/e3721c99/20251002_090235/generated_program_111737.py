```python
def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    return copy_grid(g)
```