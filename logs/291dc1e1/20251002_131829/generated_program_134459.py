```python
def get_drawing(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    first_row = g[0]
    if first_row[0] == 0:
        return [row[1:] for row in g[1:]]
    else:
        return [row[:-1] for row in g[1:]]

def extract_runs(row: List[int]) -> List[List[int]]:
    runs = []
    i = 0
    n = len(row)
    while i < n:
        if row[i] != 8:
            color = row[i]
            start = i
            while i < n and row[i] == color:
                i += 1
            run = [color] * (i - start)
            runs.append(run)
        else:
            i += 1
    return runs

def get_blocks(drawing: List[List[int]]) -> List[List[int]]:
    blocks = []
    i = 0
    n = len(drawing)
    while i < n:
        if all(x == 8 for x in drawing[i]):
            i += 1
            continue
        if i + 1 < n and drawing[i] == drawing[i + 1]:
            runs = extract_runs(drawing[i])
            blocks += runs
            i += 2
        else:
            runs = extract_runs(drawing[i])
            blocks += runs
            i += 1
    return blocks

def get_max_w(blocks: List[List[int]]) -> int:
    if not blocks:
        return 0
    return max(len(b) for b in blocks)

def pad_line(line: List[int], max_w: int) -> List[int]:
    w = len(line)
    if w == max_w:
        return line
    pad_left = (max_w - w) // 2
    pad_right = max_w - w - pad_left
    return [8] * pad_left + line + [8] * pad_right

def render_blocks(blocks: List[List[int]]) -> List[List[int]]:
    if not blocks:
        return []
    max_w = get_max_w(blocks)
    output = []
    for b in blocks:
        padded = pad_line(b, max_w)
        output.append(padded)
        output.append(padded)
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    drawing = get_drawing(g)
    blocks = get_blocks(drawing)
    output = render_blocks(blocks)
    return output
```