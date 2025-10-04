```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    H = len(g)
    output = [[0] * 7 for _ in range(H)]
    for i in range(H):
        row = g[i]
        for j in range(8, min(8 + 7, len(row))):
            k = j - 8
            if k < 7:
                output[i][k] = row[j]
    return output
```