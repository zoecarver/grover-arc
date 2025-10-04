```python
import copy

def flip_l3(g: List[List[int]]) -> List[List[int]]:
    """Rule for splitting horizontal runs of length 3: flip middle if both adjacent colors same and different from run, else flip right end to left adjacent if left different."""
    h = copy.deepcopy(g)
    for r in range(len(g)):
        row = g[r]
        n = len(row)
        for i in range(n - 2):
            c = row[i]
            if row[i] == row[i + 1] == row[i + 2] == c:
                l_exists = i > 0
                r_exists = i + 3 < n
                left_c = row[i - 1] if l_exists else None
                right_c = row[i + 3] if r_exists else None
                if (l_exists and left_c != c) and (r_exists and right_c != c) and left_c == right_c:
                    h[r][i + 1] = left_c  # flip middle
                elif l_exists and left_c != c:
                    h[r][i + 2] = left_c  # flip right end to left
    return h

def flip_l2(g: List[List[int]]) -> List[List[int]]:
    """Rule for splitting horizontal runs of length 2: flip second pixel to left adjacent color if left different."""
    h = copy.deepcopy(g)
    for r in range(len(g)):
        row = g[r]
        n = len(row)
        for i in range(n - 1):
            c = row[i]
            if row[i] == row[i + 1] == c:
                l_exists = i > 0
                left_c = row[i - 1] if l_exists else None
                if l_exists and left_c != c:
                    h[r][i + 1] = left_c  # flip second to left
    return h

def flip_l4(g: List[List[int]]) -> List[List[int]]:
    """Rule for splitting horizontal runs of length 4: flip two middle pixels to left adjacent color if both adjacent same and different from run."""
    h = copy.deepcopy(g)
    for r in range(len(g)):
        row = g[r]
        n = len(row)
        for i in range(n - 3):
            c = row[i]
            if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == c:
                l_exists = i > 0
                r_exists = i + 4 < n
                left_c = row[i - 1] if l_exists else None
                right_c = row[i + 4] if r_exists else None
                if l_exists and r_exists and left_c != c and right_c != c and left_c == right_c:
                    h[r][i + 1] = left_c
                    h[r][i + 2] = left_c
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    """Compose rules: apply l2, then l3, then l4, then l2 again to handle chains."""
    h = flip_l2(g)
    h = flip_l3(h)
    h = flip_l4(h)
    h = flip_l2(h)
    return h
```