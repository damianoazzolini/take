def is_int(s : str) -> bool:
    """
    Check if a string can be converted to an integer.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s : str) -> bool:
    """
    Check if a string can be converted to a float.
    """
    if not is_int(s): # I want to avoid things like '1' being considered a float
        try:
            float(s)
            return True
        except ValueError:
            return False
    return False

def wrap_sort(aggregate_lines : 'list[str]', reverse : bool) -> str:
    """
    This function is used to sort the lines of a file.
    It returns a list of strings that can be sorted.
    """
    aggregate_lines = [line.rstrip('\n') for line in aggregate_lines]
    new_data : 'list[str] | list[int|float]' = []
    all_numbers : bool = True
    for v in aggregate_lines:
        if is_int(v):
            new_data.append(int(v))
        elif is_float(v):
            new_data.append(float(v))
        else:
            all_numbers = False
            break

    if not all_numbers:
        new_data = aggregate_lines

    sorted_lines = sorted(new_data, reverse=reverse)

    return '\n'.join([str(s) for s in sorted_lines])