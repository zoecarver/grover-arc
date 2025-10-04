```python
def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def remap_colors(g: List[List[int]]) -> List[List[int]]:
    mapping = {0: 0, 1: 5, 2: 2, 3: 1, 4: 4, 6: 6, 8: 3}
    h = copy_grid(g)
    for i in range(30):
        for j in range(30):
            h[i][j] = mapping.get(h[i][j], 0)
    return h

def reverse_rows(g: List[List[int]]) -> List[List[int]]:
    h = copy_grid(g)
    h.reverse()
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    normalized = remap_colors(g)
    reversed_normalized = reverse_rows(normalized)
    # Remap back to original color ids (inverse mapping)
    inverse_mapping = {0: 0, 5: 1, 2: 2, 1: 3, 4: 4, 6: 6, 3: 8}
    h = copy_grid(reversed_normalized)
    for i in range(30):
        for j in range(30):
            h[i][j] = inverse_mapping.get(h[i][j], 0)
    return h
```