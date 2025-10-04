```python
def program(g: List[List[int]]) -> List[List[int]]:
    return [[0 if cell == 5 else cell for cell in row] for row in g]
```