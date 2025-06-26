PREDICATES = {
    "line": 1,
    "print": 1,
    "startswith": 2,
    "endswith": 2,
    "length": 2,
    "lt": 2,
    "leq": 2,
    "gt": 2,
    "geq": 2,
}


class InstantiationError(Exception):
    pass
class NotVariableError(Exception):
    pass
class VariableNotFoundError(Exception):
    pass
class NotANumberError(Exception):
    pass

def get_instantiation(s : str, instantiations : 'dict[str,str]') -> str:
    """
    Get the instantiation of a variable from the instantiations dictionary.
    If the variable is not instantiated, raise an InstantiationError.
    """
    if s in instantiations:
        if instantiations[s] != "":
            return instantiations[s]
        else:
            raise InstantiationError(f"s is not instantiated: {s}")
    else:
        raise VariableNotFoundError(f"Variable {s} not found in instantiations")
    
def is_variable(s : str) -> bool:
    """
    Check if a string is a variable name (i.e., starts with an uppercase letter).
    """
    return s[0].isupper()

# def check_exists(l : str, instantiations : 'dict[str,str]'):
#     """
#     Check if a variable exists in the instantiations dictionary.
#     If it does not exist, raise a VariableNotFoundError.
#     """
#     if l not in instantiations:
#         raise VariableNotFoundError(f"Variable {l} not found in instantiations")
    
def get_number(s : str) -> 'int|float':
    """
    Get the number (int or float) from a string.
    """
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            raise NotANumberError(f"Value {s} is not a number")


#######################


def line(current_line : str, l : str, instantiations : 'dict[str,str]') -> bool:
    """
    Input:
    - l: a variable representing a string
    - instantiations: a dictionary that maps variable names to their string values
    Returns:
    - True if the variable l is instantiated, False otherwise
    """
    if is_variable(l):
        # check_exists(l, instantiations)
        if instantiations[l] != "":
            return current_line == instantiations[l]
        else:
            instantiations[l] = current_line
        return True
    
    return current_line == l

def print_line(l : str, instantiations : 'dict[str,str]') -> bool:
    """
    Print the value of the variable l from the instantiations dictionary.
    If l is not a variable, print it directly.
    Returns True if the variable exists and is printed, False otherwise.
    """
    if is_variable(l):
        # check_exists(l, instantiations)
        print(instantiations[l])
        return True

    print(l)
    return False
    

def startswith(l : str, s : str, instantiations : 'dict[str,str]') -> bool:
    """
    Input:
    - l: a variable representing a string
    - s: a string to check if it is a prefix of the string in l
    - instantiations: a dictionary that maps variable names to their string values
    Returns:
    - True if the string in l1 starts with s, False otherwise
    """
    return _starts_end_with(True, l, s, instantiations)

def endswith(l : str, s : str, instantiations : 'dict[str,str]') -> bool:
    """
    Input:
    - l: a variable representing a string
    - s: a string to check if it is a suffix of the string in l
    - instantiations: a dictionary that maps variable names to their string values
    Returns:
    - True if the string in l1 ends with s, False otherwise
    """
    return _starts_end_with(False, l, s, instantiations)

def _starts_end_with(t : bool, l : str, s : str, instantiations : 'dict[str,str]') -> bool:
    """
    Wrapper. t = True for startswith, False for endswith.
    """
    if is_variable(s):
        s = get_instantiation(s, instantiations)
    
    # to allow nonsense things like checking if a constant starts with another constant
    v = l
    if is_variable(l):
        # check_exists(l, instantiations)
        v = instantiations[l]

    return (t and v.startswith(s)) or (not t and v.endswith(s))

def lt(n : str, v : str, instantiations : 'dict[str,str]') -> bool:
    """
    Check if n < v.
    """
    return lt_leq_gt_geq_wrapper("lt", n, v, instantiations)
def leq(n : str, v : str, instantiations : 'dict[str,str]') -> bool:
    """
    Check if n =< v.
    """
    return lt_leq_gt_geq_wrapper("leq", n, v, instantiations)
def gt(n : str, v : str, instantiations : 'dict[str,str]') -> bool:
    """
    Check if n > v.
    """
    return lt_leq_gt_geq_wrapper("gt", n, v, instantiations)
def geq(n : str, v : str, instantiations : 'dict[str,str]') -> bool:
    """
    Check if n >= v.
    """
    return lt_leq_gt_geq_wrapper("geq", n, v, instantiations)

def lt_leq_gt_geq_wrapper(t : str, n : str, v : str, instantiations : 'dict[str,str]') -> bool:
    """
    Check if 
    - t = lt: n < v
    - t = leq: n =< v
    - t = gt: n > v
    - t = geq: n > v
    """
    if is_variable(n):
        n = get_instantiation(n, instantiations)
    if is_variable(v):
        v = get_instantiation(v, instantiations)
    
    n_number = get_number(n)
    v_number = get_number(v)

    if t == "lt":
        return n_number < v_number
    elif t == "leq":
        return n_number <= v_number
    elif t == "gt":
        return n_number > v_number
    elif t == "geq":
        return n_number >= v_number
    
    raise ValueError(f"Unknown comparison type: {t}. Expected one of 'lt', 'leq', 'gt', 'geq'.")

def length(l : str, n : str, instantiations : 'dict[str,str]') -> bool:
    """
    Compute the length of a string and store it in the instantiations dictionary.
    """
    if is_variable(l):
        l = get_instantiation(l, instantiations)

    if is_variable(n):
        if instantiations[n] == "":
            instantiations[n] = str(len(l))
            return True
        else:
            num = get_number(instantiations[n])
            return len(l) == num

    num = get_number(n)
    return len(l) == num


