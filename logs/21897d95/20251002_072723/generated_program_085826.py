```python
def transpose_grid(g: List[List[int]]) -> List[List[int]]:
    """Transposes the input grid, swapping rows and columns."""
    if not g or not g[0]:
        return []
    return [list(row) for row in zip(*g)]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: applies transposition as the core transformation."""
    return transpose_grid(g)
```