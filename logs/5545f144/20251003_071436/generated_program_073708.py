```python
def find_background(g):
    flat = [item for row in g for item in row]
    count = {}
    for item in flat:
        if item in count:
            count[item] += 1
        else:
            count[item] = 1
    max_count = 0
    b = flat[0] if flat else 0
    for item, c in count.items():
        if c > max_count:
            max_count = c
            b = item
    return b

def find_constant_columns(g):
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    constant = []
    for j in range(w):
        if h == 0:
            continue
        first = g[0][j]
        is_const = True
        for i in range(1, h):
            if g[i][j] != first:
                is_const = False
                break
        if is_const:
            constant.append((j, first))
    return constant

def find_feature(g, b, s):
    flat = [item for row in g for item in row]
    seen = set()
    for item in flat:
        if item != b and item != s:
            seen.add(item)
    if seen:
        return next(iter(seen))
    return b

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    b = find_background(g)
    const = find_constant_columns(g)
    sep = [j for j, v in const if v != b]
    if sep:
        s = const[sep[0]][1]
        f = find_feature(g, b, s)
    else:
        s = None
        flat_set = set(item for row in g for item in row)
        if len(flat_set) > 1:
            f = next(item for item in flat_set if item != b)
        else:
            f = b
    k = len(sep)
    w = len(g[0])
    section_size = w if k == 0 else (w - k) // (k + 1)
    starts = [0]
    for p in sep:
        starts.append(p + 1)
    h = len(g)
    output = [[b for _ in range(section_size)] for _ in range(h)]
    num_sections = k + 1
    threshold = num_sections / 2.0
    for i in range(h):
        for j in range(section_size):
            votes = []
            for m in range(num_sections):
                start = starts[m]
                pos = start + j
                if pos < w:
                    val = g[i][pos]
                    if val != s:
                        votes.append(val)
            count_f = sum(1 for v in votes if v == f)
            if count_f > threshold:
                output[i][j] = f
    return output
```