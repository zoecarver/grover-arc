```python
from typing import List
from collections import Counter

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return g
    n = len(g)
    # Find background: most common value
    flat = [cell for row in g for cell in row]
    background = Counter(flat).most_common(1)[0][0]
    # Copy the grid
    h = [row[:] for row in g]
    # Function to slide right in a row
    def slide_right_row(row, background, n):
        non_bg = [x for x in row if x != background]
        new_row = [background] * n
        for idx in range(len(non_bg)):
            new_row[n - len(non_bg) + idx] = non_bg[idx]
        return new_row
    # Slide right each row
    for i in range(n):
        h[i] = slide_right_row(h[i], background, n)
    # Function to bubble up in a column
    def bubble_up_column(col, background, n):
        non_bg = [x for x in col if x != background]
        new_col = [background] * n
        for idx in range(len(non_bg)):
            new_col[idx] = non_bg[idx]
        return new_col
    # Bubble up each column
    for j in range(n):
        col = [h[i][j] for i in range(n)]
        new_col = bubble_up_column(col, background, n)
        for i in range(n):
            h[i][j] = new_col[i]
    return h
```