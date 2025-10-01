```python
def program(g: List[List[int]]) -> List[List[int]]:
    h = [row[:] for row in g]
    for r in range(len(h)):
        for c in range(len(h[r])):
            if h[r][c] > 4:
                h[r][c] = 0
    return h
```