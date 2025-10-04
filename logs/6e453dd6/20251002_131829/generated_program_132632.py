```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    height = len(g)
    if height == 0:
        return g
    width = len(g[0])
    # Find c, the column index of the 5's
    c = -1
    for j in range(width):
        if all(row[j] == 5 for row in g):
            c = j
            break
    if c == -1:
        return [row[:] for row in g]
    # Find blocks: maximal consecutive rows with at least one 0 in 0 to c-1
    blocks = []
    i = 0
    while i < height:
        if all(g[i][j] != 0 for j in range(c)):
            i += 1
            continue
        block_start = i
        while i < height and any(g[i][j] == 0 for j in range(c)):
            i += 1
        blocks.append(list(range(block_start, i)))
    # Copy input to output
    output = [row[:] for row in g]
    # Process each block
    for block in blocks:
        # Compute m = min trailing in the block
        trailings = []
        for ri in block:
            zero_positions = [j for j in range(c) if g[ri][j] == 0]
            if zero_positions:
                end = max(zero_positions)
                trailing = c - 1 - end
                trailings.append(trailing)
        if not trailings:
            continue
        m = min(trailings)
        # Process each row in the block
        for ri in block:
            zero_positions = [j for j in range(c) if g[ri][j] == 0]
            if not zero_positions:
                continue
            start = min(zero_positions)
            end = max(zero_positions)
            len_p = end - start + 1
            trailing = c - 1 - end
            shift = min(m, trailing)
            new_start = start + shift
            # Create new left part
            new_left = [6] * c
            for jj in range(len_p):
                new_left[new_start + jj] = g[ri][start + jj]
            # Set the left part
            output[ri][:c] = new_left
            # Check for 2's
            has_internal_6 = any(g[ri][j] == 6 for j in range(start, end + 1))
            new_end = new_start + len_p - 1
            if new_end == c - 1 and has_internal_6:
                for jj in range(c + 1, width):
                    output[ri][jj] = 2
    return output
```