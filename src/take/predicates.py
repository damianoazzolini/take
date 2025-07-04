PREDICATES = {
    # arity 1
    "line": 1,
    "print": 1,
    "println": 1,
    # arity 2
    "startswith": 2,
    "endswith": 2,
    "length": 2,
    "lt": 2,
    "leq": 2,
    "gt": 2,
    "geq": 2,
    "eq": 2,
    "capitalize": 2,
    "line_number": 2,
    "contains": 2,
    "strip": 2,
    # arity 4
    "split_select": 4,
    "replace": 4
}


class InstantiationError(Exception):
    pass
class NotVariableError(Exception):
    pass
class VariableNotFoundError(Exception):
    pass
class NotANumberError(Exception):
    pass
class NotAnIntegerError(Exception):
    pass

def is_instantiated(s : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Check if a variable is instantiated in the instantiations dictionary.
    Returns True if the variable is instantiated, False otherwise.
    """
    if s in instantiations:
        return instantiations[s] != None
    else:
        raise VariableNotFoundError(f"Variable {s} not found in instantiations")


def get_instantiation(s : str, instantiations : 'dict[str,str|None]') -> str:
    """
    Get the instantiation of a variable from the instantiations dictionary.
    If the variable is not instantiated, raise an InstantiationError.
    """
    if is_instantiated(s, instantiations):
        return instantiations[s]
    #     else:
    raise InstantiationError(f"s is not instantiated: {s}")
    # else:
    #     raise VariableNotFoundError(f"Variable {s} not found in instantiations")
    
def is_variable(s : str) -> bool:
    """
    Check if a string is a variable name (i.e., starts with an uppercase letter).
    """
    return s[0].isupper()


def get_constant(s : str) -> str:
    """
    To escape quotes
    """
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    else:
        return s


def get_integer(s : str) -> int:
    """
    Get the integer from a string.
    If the string cannot be converted to an integer, raise NotANumberError.
    """
    try:
        return int(s)
    except ValueError:
        raise NotAnIntegerError(f"Value {s} is not an integer")


def get_number(s : str) -> 'int|float':
    """
    Get the number (int or float) from a string.
    """
    try:
        return get_integer(s)
    except NotAnIntegerError:
        try:
            return float(s)
        except ValueError:
            raise NotANumberError(f"Value {s} is not a number")


#######################


def line(current_line : str, l : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Input:
    - l: a variable representing a string
    - instantiations: a dictionary that maps variable names to their string values
    Returns:
    - True if the variable l is instantiated, False otherwise
    """
    if is_variable(l):
        # check_exists(l, instantiations)
        if is_instantiated(l, instantiations):
            return current_line == instantiations[l]
        else:
            instantiations[l] = current_line
        return True
    
    return current_line == l

def print_line(l : str, instantiations : 'dict[str,str|None]', with_newline : bool = False) -> bool:
    """
    Print the value of the variable l from the instantiations dictionary.
    If l is not a variable, print it directly.
    Returns True if the variable exists and is printed, False otherwise.
    """
    if is_variable(l):
        print(instantiations[l], end="\n" if with_newline else "")
    else:
        print(l, end="\n" if with_newline else "")
    return True
    

def startswith(l : str, s : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Input:
    - l: a variable representing a string
    - s: a string to check if it is a prefix of the string in l
    - instantiations: a dictionary that maps variable names to their string values
    Returns:
    - True if the string in l1 starts with s, False otherwise
    """
    return _starts_end_with(True, l, s, instantiations)

def endswith(l : str, s : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Input:
    - l: a variable representing a string
    - s: a string to check if it is a suffix of the string in l
    - instantiations: a dictionary that maps variable names to their string values
    Returns:
    - True if the string in l1 ends with s, False otherwise
    """
    return _starts_end_with(False, l, s, instantiations)

def _starts_end_with(t : bool, l : str, s : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Wrapper. t = True for startswith, False for endswith.
    """
    if is_variable(s):
        s = get_instantiation(s, instantiations)
    else:
        s = get_constant(s)
    
    # to allow nonsense things like checking if a constant starts with another constant
    if is_variable(l):
        # check_exists(l, instantiations)
        l = get_instantiation(l, instantiations)

    # print(f"Checking if {l} {'starts' if t else 'ends'} with {s}")
    return (t and l.startswith(s)) or (not t and l.endswith(s))

def lt(n : str, v : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Check if n < v.
    """
    return lt_leq_gt_geq_eq_wrapper("lt", n, v, instantiations)
def leq(n : str, v : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Check if n =< v.
    """
    return lt_leq_gt_geq_eq_wrapper("leq", n, v, instantiations)
def gt(n : str, v : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Check if n > v.
    """
    return lt_leq_gt_geq_eq_wrapper("gt", n, v, instantiations)
def geq(n : str, v : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Check if n >= v.
    """
    return lt_leq_gt_geq_eq_wrapper("geq", n, v, instantiations)
def eq(n : str, v : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Check if n == v.
    """
    return lt_leq_gt_geq_eq_wrapper("eq", n, v, instantiations)

def lt_leq_gt_geq_eq_wrapper(t : str, n : str, v : str, instantiations : 'dict[str,str|None]') -> bool:
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
    elif t == "eq":
        return n_number == v_number
    
    raise ValueError(f"Unknown comparison type: {t}. Expected one of 'lt', 'leq', 'gt', 'geq', 'eq'.")

def length(l : str, n : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Compute the length of a string and store it in the instantiations dictionary.
    """
    if is_variable(l):
        l = get_instantiation(l, instantiations)

    if is_variable(n):
        if is_instantiated(n, instantiations):
            num = get_number(instantiations[n])
            return len(l) == num
        else:
            instantiations[n] = str(len(l))
            return True

    num = get_number(n)
    return len(l) == num


def capitalize(l: str, s: str, instantiations: 'dict[str,str|None]') -> bool:
    """
    Capitalize the string in l and store it in s.
    If s is a variable, store the capitalized string in it.
    If s is not a variable, check if it matches the capitalized string.
    """
    if is_variable(l):
        l = get_instantiation(l, instantiations)

    capitalized = l.capitalize()

    if is_variable(s):
        if instantiations[s] == None:
            instantiations[s] = capitalized
            return True
        else:
            return instantiations[s] == capitalized

    return capitalized == s


def split_select(l: str, v: str, p: str, l1: str, instantiations: 'dict[str,str|None]') -> bool:
    """
    Split the string l at each occurrence of v, then select the part at position p and store it in l1.
    If l1 is a variable, store the selected part in it.
    If l1 is not a variable, check if it matches the selected part.
    """
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    
    if is_variable(v):
        v = get_instantiation(v, instantiations)
    else:
        v = get_constant(v)
    if v == "space":
        v = " "
    

    if is_variable(p):
        p = get_instantiation(p, instantiations)
    
    parts = l.split(v)
    
    p_number = get_integer(p)

    if is_variable(l1):
        if not is_instantiated(l1, instantiations):
            if p_number < len(parts):
                instantiations[l1] = parts[p_number]
                return True
            else:
                return False
        else:
            return p_number < len(parts) and instantiations[l1] == parts[p_number]
    
    if p_number < len(parts):
        return parts[p_number] == l1
    return False


def replace(l: str, old: str, new: str, l1 : str, instantiations: 'dict[str,str|None]') -> bool:
    """
    Replace all occurrences of old in l with new.
    If l is a variable, replace the value in the instantiations dictionary.
    If l is not a variable, check if it matches the replaced string.
    """
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    if is_variable(old):
        old = get_instantiation(old, instantiations)
    if is_variable(new):
        new = get_instantiation(new, instantiations)
    
    replaced = l.replace(old, new)

    if is_variable(l1):
        if not is_instantiated(l1, instantiations):
            instantiations[l1] = replaced
            return True
        else:
            return instantiations[l1] == replaced
    
    return replaced == l1


def line_number(l: str, n: str, current_idx : int, instantiations: 'dict[str,str|None]') -> bool:
    """
    Get the line number of the string l.
    The line number is 1-based and it is passed in current_idx from the main loop.
    """
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    
    if is_variable(n):
        if not is_instantiated(n, instantiations):
            instantiations[n] = str(current_idx + 1)
            return True
        else:
            return instantiations[n] == str(current_idx + 1)
    
    return get_integer(n) == current_idx + 1


def contains(l: str, s: str, instantiations: 'dict[str,str|None]') -> bool:
    """
    Check if the string l contains the substring s.
    If l is a variable, get its value from the instantiations dictionary.
    If s is a variable, get its value from the instantiations dictionary.
    """
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    
    if is_variable(s):
        s = get_instantiation(s, instantiations)
    
    return s in l


def strip(l : str, l1 : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Strip leading and trailing whitespace from the string l.
    If l is a variable, get its value from the instantiations dictionary.
    If l1 is a variable, store the stripped string in it.
    If l1 is not a variable, check if it matches the stripped string.
    """
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    
    stripped = l.strip()

    if is_variable(l1):
        if not is_instantiated(l1, instantiations):
            instantiations[l1] = stripped
            return True
        else:
            return instantiations[l1] == stripped
    
    return stripped == l1
