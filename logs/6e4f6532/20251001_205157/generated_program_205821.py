```python
from typing import List

def extract_columns(g: List[List[int]]) -> List[List[int]]:
    """Extract columns from the grid."""
    if not g:
        return []
    height = len(g)
    width = len(g[0])
    return [[g[i][j] for i in range(height)] for j in range(width)]

def apply_gravity(col: List[int], empty: int = 0) -> List[int]:
    """Apply gravity to a column: move non-empty values to the bottom."""
    non_empty = [x for x in col if x != empty]
    num_empty = len(col) - len(non_empty)
    return [empty] * num_empty + non_empty

def build_grid(columns: List[List[int]]) -> List[List[int]]:
    """Build grid from list of columns."""
    if not columns:
        return []
    height = len(columns[0])
    width = len(columns)
    return [[columns[j][i] for j in range(width)] for i in range(height)]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: apply gravity to each column."""
    columns = extract_columns(g)
    new_columns = [apply_gravity(col) for col in columns]
    return build_grid(new_columns)
```