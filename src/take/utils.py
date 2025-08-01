class bcolors:
    ERROR = '\033[91m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

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

def wrap_sort(aggregate_lines : 'list[tuple[str,str]]', reverse : bool) -> 'list[str | int | float]':
    """
    This function is used to sort the lines of a file.
    It returns a list of strings that can be sorted.
    """
    aggregate_lines = [(line[0], line[1].rstrip('\n')) for line in aggregate_lines]
    # aggregate_lines = [line.rstrip('\n') for line in aggregate_lines]
    new_data : 'list[tuple[str,int|float]]' = []
    all_numbers : bool = True
    for name, v in aggregate_lines:
        if is_int(v):
            new_data.append((name, int(v)))
        elif is_float(v):
            new_data.append((name, float(v)))
        else:
            all_numbers = False
            break

    if not all_numbers:
        new_data = aggregate_lines

    return sorted(new_data, key=lambda x: x[1], reverse=reverse)
