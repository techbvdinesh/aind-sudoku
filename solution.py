assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    """
        Build all Sudoku boxes
    """
    return [s+t for s in a for t in b]


def find_DiagonalNumbers():
    """
    Find diagonal boxes
    """
    dunit_values =[[rows[int(iloop)-1] + iloop for iloop in cols]]
    reverse_cols = cols[::-1]
    reverse_rows = rows[::-1]
    gunit_values = [[reverse_rows[int(iloop)-1] + iloop for iloop in reverse_cols]]
    return dunit_values + gunit_values


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Construct all boxs
unitlist = row_units + column_units + square_units + find_DiagonalNumbers()
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)    



def assign_value(values, box, value):
    """
    Assigns a value to a given box. If it updates the board record it.
    """
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    twin_box = [box for box in values.keys() if len(values[box]) == 2] 
  # Discover twin boxes with 2 digit
    for box in twin_box:
        test = values[box]
        for unit_lines in units[box]:
            for box_unit in unit_lines:
                if (box_unit != box and values[box_unit] == test): # Discover naked twins that has same digit
                    for box_unit2 in unit_lines: # Scan through the others boxes that has same digit in row, column and 3*3 block
                        if values[box_unit2] != test: # eliminate the value that has common to the naked twin primes
                            values = assign_value(values, box_unit2, values[box_unit2].replace(test[0], ''))
                            values = assign_value(values, box_unit2, values[box_unit2].replace(test[1], ''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    allcollection = []
    allnumbers = '123456789'
    if len(grid) == 81:
        for char in grid:
          if char == '.':
            allcollection.append(allnumbers)
          else:
            allcollection.append(char)
        zipped = dict(zip(boxes, allcollection))
        
        return zipped
    else:
        raise ValueError('not correct length')

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values is None:
       raise ValueError('values is null')

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
                values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    orginal_digit = '123456789'
    for x in unitlist:
      for d in orginal_digit:
          dplaces = [box for box in x if d in values[box]]
          if len(dplaces) == 1:
            values[dplaces[0]] = d
       
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
   
    values = grid_values(grid)
    values = search(values)
    return values
  
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
