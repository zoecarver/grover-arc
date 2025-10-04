```python
from collections import Counter
from typing import List

def get_mode_block_size(row: List[int], start: int, end: int, S: int) -> int:
    blocks = []
    j = start
    while j <= end:
        if row[j] == S:
            size = 0
            while j <= end and row[j] == S:
                size += 1
                j += 1
            blocks.append(size)
        else:
            j += 1
    if not blocks:
        return 0
    count = Counter(blocks)
    return count.most_common(1)[0][0]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return g
    height = len(g)
    if height == 0:
        return g
    width = len(g[0])
    if width == 0:
        return g
    B = g[0][0]
    out = [list(row) for row in g]
    for i in range(height):
        row = out[i]
        if all(x == B for x in row):
            continue
        inner_all_2 = all(x == 2 for x in row[1:width-1])
        if inner_all_2:
            continue
        poss_S = sorted(set(row[j] for j in range(1, width-1)) - {B, 2})
        for S in poss_S:
            K = get_mode_block_size(row, 2, width - 3, S)
            if K == 0:
                continue
            # split triple S
            for p in range(2, width - 2):
                if p + 2 <= width - 2 and out[i][p] == S and out[i][p + 1] == S and out[i][p + 2] == S:
                    out[i][p + 1] = B
            # special end double nonS double S
            if width >= 7 and out[i][width - 6] != S and out[i][width - 5] != S and out[i][width - 4] == S and out[i][width - 3] == S and out[i][width - 2] == 2:
                out[i][width - 5] = S
                out[i][width - 3] = B
            # end double S
            if width >= 5 and out[i][width - 4] == S and out[i][width - 3] == S:
                out[i][width - 3] = B
            # fill triple nonS
            for p in range(3, width - 3):
                if out[i][p - 1] == S and out[i][p] != S and out[i][p + 1] != S and out[i][p + 2] != S and out[i][p + 3] == S:
                    out[i][p + 1] = S
            # fill double nonS between
            for p in range(3, width - 3):
                if out[i][p - 1] == S and out[i][p] != S and out[i][p + 1] != S and out[i][p + 2] == S:
                    left_size = 1
                    k = p - 2
                    while k >= 2 and out[i][k] == S:
                        left_size += 1
                        k -= 1
                    right_size = 1
                    k = p + 3
                    while k <= width - 3 and out[i][k] == S:
                        right_size += 1
                        k += 1
                    change_pos = None
                    if left_size == K and right_size < K:
                        change_pos = p + 1
                    elif right_size == K and left_size < K:
                        change_pos = p
                    elif left_size < K and right_size < K:
                        if left_size >= right_size:
                            change_pos = p
                        else:
                            change_pos = p + 1
                    if change_pos is not None and 1 <= change_pos < width - 1:
                        out[i][change_pos] = S
    return out
```