```python
def get_bar_colors(g):
    row = g[1]
    bar1 = next(c for c in row[1:5] if c != 0)
    bar2 = next(c for c in row[7:11] if c != 0)
    bar3 = next(c for c in row[13:17] if c != 0)
    bar4 = next(c for c in row[19:23] if c != 0)
    return bar1, bar2, bar3, bar4

def has_merge(bar2, bar3):
    return bar2 == 6 or bar3 == 6

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g[6:25]]
    bar1, bar2, bar3, bar4 = get_bar_colors(g)
    if not has_merge(bar2, bar3):
        return out
    protected = {bar1, bar2, bar3, bar4, 5}
    # Spread in rows with 8's
    for row in out:
        if 8 in row:
            # Spread function: spread 8's left and right until protected
            new_row = row[:]
            i = 0
            while i < len(row):
                if row[i] == 8:
                    start = i
                    while i < len(row) and row[i] == 8:
                        i += 1
                    end = i - 1
                    # spread left
                    j = start - 1
                    while j >= 0 and row[j] not in protected:
                        new_row[j] = 8
                        j -= 1
                    # spread right
                    j = end + 1
                    while j < len(row) and row[j] not in protected:
                        new_row[j] = 8
                        j += 1
                else:
                    i += 1
            row[:] = new_row
    return out
```