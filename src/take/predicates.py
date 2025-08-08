from .utils import bcolors

PREDICATES = {
    # arity 1
    "line": 1,
    "print": 1,
    "println": 1,
    # arity 2
    "startswith": 2,
    "startswith_i": 2,
    "endswith": 2,
    "endswith_i": 2,
    "length": 2,
    "lt": 2,
    "leq": 2,
    "gt": 2,
    "geq": 2,
    "eq": 2,
    "neq": 2,
    "capitalize": 2,
    "line_number": 2,
    "contains": 2,
    "contains_i": 2,
    "strip": 2,
    "time_to_seconds": 2,
    "abs": 2,
    # arity 3
    "add": 3,
    "sub": 3,
    "mul": 3,
    "div": 3,
    "pow": 3,
    "mod": 3,
    # arity 4
    "split_select": 4,
    "replace": 4,
    "substring": 4
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
class UnsafeError(Exception):
    pass

def is_instantiated(s : str, instantiations : 'dict[str,str|None]') -> bool:
    """
    Check if a variable is instantiated in the instantiations dictionary.
    Returns True if the variable is instantiated, False otherwise.
    """
    if s in instantiations:
        return instantiations[s] is not None
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


def check_safe_negation(args : 'list[str]', instantiations : 'dict[str,str|None]', pred_name : str) -> None:
    """
    Check if all arguments are ground (i.e., not variables) for safe negation.
    If any argument is a variable, raise UnsafeError.
    """
    for arg in args:
        if is_variable(arg) and not is_instantiated(arg, instantiations):
            raise UnsafeError(f"Negation is not safe for variable {arg} in {pred_name}.")

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

        instantiations[l] = current_line
        return True

    return current_line == l

def print_line(l : str, instantiations : 'dict[str,str|None]', with_newline : bool = False, filename : str|None = None, uncolored_output : bool = False, max_columns : int = 0) -> bool:
    """
    Print the value of the variable l from the instantiations dictionary.
    If l is not a variable, print it directly.
    Returns True if the variable exists and is printed, False otherwise.
    """
    stop = False
    if is_variable(l):
        max_len = max_columns
        if instantiations[l] is not None:
            if filename is not None:
                if max_columns > 0 and len(filename) > max_columns-1:
                    stop = True
                    filename = filename[:max_columns-1]
                if not uncolored_output:
                    print(f"{bcolors.PURPLE}{filename}:{bcolors.ENDC}", end='')
                else:
                    print(f"{filename}:", end='')
                if stop:
                    print("")
                    return True
                max_len -= len(filename) + 1
            if max_columns > 0:
                to_print = instantiations[l][:max_len]
            else:
                to_print = instantiations[l]
            print(f"{to_print}", end="\n" if with_newline else "")
    else:
        l = get_constant(l)
        if max_columns > 0:
            print(l[:max_columns], end="\n" if with_newline else "")
        else:
            print(l, end="\n" if with_newline else "")
    return True


def startswith(l : str, s : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Input:
    - l: a variable representing a string
    - s: a string to check if it is a prefix of the string in l
    - instantiations: a dictionary that maps variable names to their string values
    Returns:
    - True if the string in l1 starts with s, False otherwise
    """
    return _starts_end_with(True, l, s, instantiations, is_negated)

def startswith_i(l : str, s : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Input:
    - l: a variable representing a string
    - s: a string to check if it is a prefix of the string in l
    - instantiations: a dictionary that maps variable names to their string values
    Returns:
    - True if the string in l1 starts with s, case insensitive, False otherwise
    """
    return _starts_end_with(True, l, s, instantiations, is_negated, False)

def endswith(l : str, s : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Input:
    - l: a variable representing a string
    - s: a string to check if it is a suffix of the string in l
    - instantiations: a dictionary that maps variable names to their string values
    Returns:
    - True if the string in l1 ends with s, False otherwise
    """
    return _starts_end_with(False, l, s, instantiations, is_negated)

def endswith_i(l : str, s : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Input:
    - l: a variable representing a string
    - s: a string to check if it is a suffix of the string in l
    - instantiations: a dictionary that maps variable names to their string values
    Returns:
    - True if the string in l1 ends with s, case insensitive, False otherwise
    """
    return _starts_end_with(False, l, s, instantiations, is_negated, False)

def _starts_end_with(t : bool, l : str, s : str, instantiations : 'dict[str,str|None]', is_negated : bool, case_sensitive : bool = True) -> bool:
    """
    Wrapper. t = True for startswith, False for endswith.
    """
    if is_negated:
        check_safe_negation([l, s], instantiations, f"{'startswith' if t else 'endswith'}")

    if is_variable(s):
        s = get_instantiation(s, instantiations)
    else:
        s = get_constant(s)

    # to allow nonsense things like checking if a constant starts with another constant
    if is_variable(l):
        # check_exists(l, instantiations)
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)

    # print(f"Checking if {l} {'starts' if t else 'ends'} with {s}")
    if case_sensitive:
        return ((t and l.startswith(s)) or (not t and l.endswith(s))) ^ is_negated

    return ((t and l.lower().startswith(s.lower())) or (not t and l.lower().endswith(s.lower()))) ^ is_negated

def lt(n : str, v : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Check if n < v.
    """
    return lt_leq_gt_geq_eq_wrapper("lt", n, v, instantiations, is_negated)
def leq(n : str, v : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Check if n =< v.
    """
    return lt_leq_gt_geq_eq_wrapper("leq", n, v, instantiations, is_negated)
def gt(n : str, v : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Check if n > v.
    """
    return lt_leq_gt_geq_eq_wrapper("gt", n, v, instantiations, is_negated)
def geq(n : str, v : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Check if n >= v.
    """
    return lt_leq_gt_geq_eq_wrapper("geq", n, v, instantiations, is_negated)
def eq(n : str, v : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Check if n == v.
    """
    return lt_leq_gt_geq_eq_wrapper("eq", n, v, instantiations, is_negated)
def neq(n : str, v : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Check if n == v.
    """
    return lt_leq_gt_geq_eq_wrapper("neq", n, v, instantiations, is_negated)

def lt_leq_gt_geq_eq_wrapper(t : str, n : str, v : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Check if 
    - t = lt: n < v
    - t = leq: n =< v
    - t = gt: n > v
    - t = geq: n > v
    - t = eq: n == v
    - t = neq: n != v
    """
    if is_negated:
        check_safe_negation([n, v], instantiations, t)

    if is_variable(n):
        n = get_instantiation(n, instantiations)
    else:
        n = get_constant(n)
    if is_variable(v):
        v = get_instantiation(v, instantiations)
    else:
        v = get_constant(v)
    
    n_number = get_number(n)
    v_number = get_number(v)

    if t == "lt":
        return (n_number < v_number) ^ is_negated
    elif t == "leq":
        return (n_number <= v_number) ^ is_negated
    elif t == "gt":
        return (n_number > v_number) ^ is_negated
    elif t == "geq":
        return (n_number >= v_number) ^ is_negated
    elif t == "eq":
        return (n_number == v_number) ^ is_negated
    elif t == "neq":
        return (n_number != v_number) ^ is_negated

    raise ValueError(f"Unknown comparison type: {t}. Expected one of 'lt', 'leq', 'gt', 'geq', 'eq', 'neq'.")

def length(l : str, n : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Compute the length of a string and store it in the instantiations dictionary.
    """
    if is_negated:
        check_safe_negation([l, n], instantiations, "length")
    
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)

    if is_variable(n):
        if is_instantiated(n, instantiations):
            num = get_number(instantiations[n])
            return (len(l) == num) ^ is_negated

        instantiations[n] = str(len(l))
        return True

    n = get_constant(n)
    return (len(l) == get_number(n)) ^ is_negated


def capitalize(l: str, s: str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Capitalize the string in l and store it in s.
    If s is a variable, store the capitalized string in it.
    If s is not a variable, check if it matches the capitalized string.
    """
    if is_negated:
        check_safe_negation([l, s], instantiations, "capitalize")
    
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)

    capitalized = l.capitalize()

    if is_variable(s):
        if instantiations[s] is None:
            instantiations[s] = capitalized
            return True
        return (instantiations[s] == capitalized) ^ is_negated

    s = get_constant(s)
    return (capitalized == s) ^ is_negated


def split_select(l: str, v: str, p: str, l1: str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Split the string l at each occurrence of v, then select the part at position p and store it in l1.
    If l1 is a variable, store the selected part in it.
    If l1 is not a variable, check if it matches the selected part.
    """
    if is_negated:
        check_safe_negation([l, v, p, l1], instantiations, "split_select")
    
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)
    
    if is_variable(v):
        v = get_instantiation(v, instantiations)
    else:
        v = get_constant(v)
    if v == "space":
        v = " "
    elif v == "tab":
        v = "\t"
    

    if is_variable(p):
        p = get_instantiation(p, instantiations)
    
    parts = l.split(v)
    
    p_number = get_integer(p)

    if is_variable(l1):
        if not is_instantiated(l1, instantiations):
            if p_number < len(parts):
                instantiations[l1] = parts[p_number]
                return True
            return False
        return (p_number < len(parts) and instantiations[l1] == parts[p_number]) ^ is_negated

    l1 = get_constant(l1)    
    if p_number < len(parts):
        return (parts[p_number] == l1) ^ is_negated
    return False ^ is_negated


def replace(l: str, old: str, new: str, l1 : str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Replace all occurrences of old in l with new.
    If l is a variable, replace the value in the instantiations dictionary.
    If l is not a variable, check if it matches the replaced string.
    """
    if is_negated:
        check_safe_negation([l, old, new, l1], instantiations, "replace")
    
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)
    if is_variable(old):
        old = get_instantiation(old, instantiations)
    else:
        old = get_constant(old)
    if is_variable(new):
        new = get_instantiation(new, instantiations)
    else:
        new = get_constant(new)
    
    replaced = l.replace(old, new)

    if is_variable(l1):
        if not is_instantiated(l1, instantiations):
            instantiations[l1] = replaced
            return True
        return (instantiations[l1] == replaced) ^ is_negated

    l1 = get_constant(l1)    
    return (replaced == l1) ^ is_negated


def line_number(l: str, n: str, current_idx : int, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Get the line number of the string l.
    The line number is 1-based and it is passed in current_idx from the main loop.
    """

    if is_negated:
        check_safe_negation([l, n], instantiations, "line_number")

    if is_variable(l):
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)
    
    if is_variable(n):
        if not is_instantiated(n, instantiations):
            instantiations[n] = str(current_idx + 1)
            return True
        return (instantiations[n] == str(current_idx + 1)) ^ is_negated

    n = get_constant(n)    
    return (get_integer(n) == current_idx + 1) ^ is_negated


def contains(l: str, s: str, instantiations: 'dict[str,str|None]', is_negated : bool, case_sensitive: bool = True) -> bool:
    """
    Check if the string l contains the substring s.
    If l is a variable, get its value from the instantiations dictionary.
    If s is a variable, get its value from the instantiations dictionary.
    """
    if is_negated:
        check_safe_negation([l, s], instantiations, "contains")
    
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)
    
    if is_variable(s):
        s = get_instantiation(s, instantiations)
    else:
        s = get_constant(s)
    
    if case_sensitive:
        return (s in l) ^ is_negated
    return (s.lower() in l.lower()) ^ is_negated


def contains_i(l: str, s: str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Check if the string l contains the substring s, case insensitive.
    If l is a variable, get its value from the instantiations dictionary.
    If s is a variable, get its value from the instantiations dictionary.
    """
    return contains(l, s, instantiations, is_negated, case_sensitive=False)


def strip(l : str, l1 : str, instantiations : 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Strip leading and trailing whitespace from the string l.
    If l is a variable, get its value from the instantiations dictionary.
    If l1 is a variable, store the stripped string in it.
    If l1 is not a variable, check if it matches the stripped string.
    """
    if is_negated:
        check_safe_negation([l, l1], instantiations, "strip")

    if is_variable(l):
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)
    
    stripped = l.strip()

    if is_variable(l1):
        if not is_instantiated(l1, instantiations):
            instantiations[l1] = stripped
            return True
        return (instantiations[l1] == stripped) ^ is_negated

    l1 = get_constant(l1)    
    return (stripped == l1) ^ is_negated


def time_to_seconds(l : str, l1 : str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Convert a bash time string of the form 0m1.131s to seconds.
    If l is a variable, get its value from the instantiations dictionary.
    If l1 is a variable, store the seconds in it.
    If l1 is not a variable, check if it matches the seconds.
    """
    if is_negated:
        check_safe_negation([l, l1], instantiations, "time_to_seconds")

    if is_variable(l):
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)

    # Example: 0m1.131s -> 1.131
    parts = l.split("m")
    if len(parts) != 2 or not parts[1].endswith("s"):
        raise ValueError(f"Invalid time format: {l}")

    minutes = int(parts[0])
    seconds = float(parts[1][:-1])  # Remove the 's' at the end

    total_seconds = minutes * 60 + seconds

    if is_variable(l1):
        if not is_instantiated(l1, instantiations):
            instantiations[l1] = str(total_seconds)
            return True
        return (instantiations[l1] == str(total_seconds)) ^ is_negated

    l1 = get_constant(l1)
    return (total_seconds == get_number(l1)) ^ is_negated


def abs(l: str, l1: str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    """
    Checks if the absolute value of l is equal to the absolute value of l1.
    """
    if is_negated:
        check_safe_negation([l, l1], instantiations, "abs")

    if is_variable(l):
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)

    # abs by hand
    n = get_number(l)
    result = n if n < 0 else n

    if is_variable(l1):
        if not is_instantiated(l1, instantiations):
            instantiations[l1] = str(result)
            return True
        return (instantiations[l1] == str(result)) ^ is_negated

    l1 = get_constant(l1)
    return (result == get_number(l1)) ^ is_negated

def add(l : str, v: str, l1: str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    return _wrap_arithmetic("add", l, v, l1, instantiations, is_negated)
def sub(l : str, v: str, l1: str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    return _wrap_arithmetic("sub", l, v, l1, instantiations, is_negated)
def mul(l : str, v: str, l1: str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    return _wrap_arithmetic("mul", l, v, l1, instantiations, is_negated)
def div(l : str, v: str, l1: str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    return _wrap_arithmetic("div", l, v, l1, instantiations, is_negated)
def pow(l : str, v: str, l1: str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    return _wrap_arithmetic("pow", l, v, l1, instantiations, is_negated)
def mod(l : str, v: str, l1: str, instantiations: 'dict[str,str|None]', is_negated : bool) -> bool:
    return _wrap_arithmetic("mod", l, v, l1, instantiations, is_negated)

def _wrap_arithmetic(op: str, l: str, v: str, l1: str, instantiations: 'dict[str,str|None]', is_negated: bool) -> bool:
    """
    Applies the specified arithmetic operation (add, sub, mul, div) on the values of l and v,
    and stores the result in l1.
    """
    if is_negated:
        check_safe_negation([l, v, l1], instantiations, op)
    
    if is_variable(l):
        l = get_instantiation(l, instantiations)
    else:
        l = get_constant(l)

    if is_variable(v):
        v = get_instantiation(v, instantiations)
    else:
        v = get_constant(v)

    if op == "add":
        result = get_number(l) + get_number(v)
    elif op == "sub":
        result = get_number(l) - get_number(v)
    elif op == "mul":
        result = get_number(l) * get_number(v)
    elif op == "div":
        result = get_number(l) / get_number(v)
    elif op == "pow":
        result = get_number(l) ** get_number(v)
    elif op == "mod":
        result = get_number(l) % get_number(v)
    else:
        raise ValueError(f"Unknown operation: {op}")

    if is_variable(l1):
        if not is_instantiated(l1, instantiations):
            instantiations[l1] = str(result)
            return True
        return (instantiations[l1] == str(result)) ^ is_negated

    l1 = get_constant(l1)
    return (result == get_number(l1)) ^ is_negated

def substring(text: str, start: str, end: str, result: str, instantiations: 'dict[str,str|None]', is_negated: bool) -> bool:
    """
    Extract substring from text[start:end].
    If result is a variable, store the substring in it.
    If result is not a variable, check if it matches the substring.
    """
    if is_negated:
        check_safe_negation([text, start, end, result], instantiations, "substring")

    if is_variable(text):
        text = get_instantiation(text, instantiations)
    else:
        text = get_constant(text)

    if is_variable(start):
        start_index = int(get_instantiation(start, instantiations))
    else:
        start_index = get_integer(start)

    if is_variable(end):
        end_index = int(get_instantiation(end, instantiations))
    else:
        end_index = get_integer(end)

    substring = text[start_index:end_index]

    if is_variable(result):
        if not is_instantiated(result, instantiations):
            instantiations[result] = substring
            return True
        return (instantiations[result] == substring) ^ is_negated

    result = get_constant(result)
    return (substring == result) ^ is_negated