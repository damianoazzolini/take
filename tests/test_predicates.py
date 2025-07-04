import pytest

from src.take.predicates import *

# Test cases for the `startswith` predicate
def test_startswith_0():
    instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": None}
    result = startswith("L1", "v", instantiations)
    assert result
def test_startswith_1():
    instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": None}
    result = startswith("L1", "b", instantiations)
    assert not result
def test_startswith_2():
    instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": "v0"}
    result = startswith("L1", "L2", instantiations)
    assert result
def test_startswith_3():
    instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": None}
    with pytest.raises(InstantiationError):
        startswith("L1", "L2", instantiations)
def test_startswith_4():
    instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": "v0"}
    assert not startswith("l1", "L2", instantiations)
# def test_startswith_5(): # all the variables are checked to exist, so this test is not needed
#     instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": "v0"}
#     with pytest.raises(VariableNotFoundError):
#         startswith("L3", "L2", instantiations)


# Test cases for lt_leq_gt_geq_eq_wrapper
# this is a nice candidate for property based
def test_lt_leq_gt_geq_eq_wrapper_0():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "10"}
    assert lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_1():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "10"}
    assert lt_leq_gt_geq_eq_wrapper("leq", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_2():
    instantiations : 'dict[str,str|None]' = {"N": "10", "V": "5"}
    assert lt_leq_gt_geq_eq_wrapper("gt", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_3():
    instantiations : 'dict[str,str|None]' = {"N": "10", "V": "5"}
    assert lt_leq_gt_geq_eq_wrapper("geq", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_4():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert lt_leq_gt_geq_eq_wrapper("leq", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_5():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert lt_leq_gt_geq_eq_wrapper("geq", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_6():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert not lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_7():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert not lt_leq_gt_geq_eq_wrapper("gt", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_8():
    instantiations : 'dict[str,str|None]' = {"N": None, "V": "5"}
    with pytest.raises(InstantiationError):
        lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_9():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": None}
    with pytest.raises(InstantiationError):
        lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_10():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "a"}
    with pytest.raises(NotANumberError):
        lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_eq_wrapper_11():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert not lt_leq_gt_geq_eq_wrapper("gt", "5", "5", instantiations)

# Test cases for the `length` predicate
def test_length_0():
    instantiations : 'dict[str,str|None]' = {"L": "v0,2,6", "N": None}
    result = length("L", "N", instantiations)
    assert result
    assert instantiations["N"] == "6"
def test_length_1():
    instantiations : 'dict[str,str|None]' = {"L": "v0,2,6", "N": "6"}
    assert length("L", "N", instantiations)
def test_length_2():
    instantiations : 'dict[str,str|None]' = {"L": "v0,2,6", "N": "4"}
    assert not length("L", "N", instantiations)
def test_length_3():
    instantiations : 'dict[str,str|None]' = {"L": None, "N": "6"}
    with pytest.raises(InstantiationError):
        length("L", "N", instantiations)
def test_length_4():
    instantiations : 'dict[str,str|None]' = {"L": "adf", "N": "a6"}
    with pytest.raises(NotANumberError):
        length("L", "N", instantiations)
def test_length_5():
    instantiations : 'dict[str,str|None]' = {"L": "adf", "N": None}
    assert length("L", "3", instantiations)
def test_length_6():
    instantiations : 'dict[str,str|None]' = {"L": None, "N": None}
    assert length("adf", "3", instantiations)
def test_length_7():
    instantiations : 'dict[str,str|None]' = {"L": None, "N": None}
    assert not length("adfh", "3", instantiations)

# Test cases for the 'capitalize' predicate
def test_capitalize_0():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "L1": None}
    result = capitalize("L", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "Hello"
def test_capitalize_1():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "L1": "Hello"}
    assert capitalize("L", "L1", instantiations)
def test_capitalize_2():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "L1": "hello"}
    assert not capitalize("L", "L1", instantiations)
def test_capitalize_3():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": "Hello"}
    with pytest.raises(InstantiationError):
        capitalize("L", "L1", instantiations)
def test_capitalize_4():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": "Hello"}
    assert not capitalize("ab", "L1", instantiations)
def test_capitalize_5():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": None}
    capitalize("ab", "L1", instantiations)
    assert instantiations["L1"] != "AB"
def test_capitalize_6():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": "Hello"}
    capitalize("cIAo", "L1", instantiations)
    assert instantiations["L1"] != "Ciao"

# Test cases for the `split_select` predicate
def test_split_select_0():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "c"
def test_split_select_1():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "0", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "a"
def test_split_select_2():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "4", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "e"
def test_split_select_3():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "5", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert not result
    assert instantiations["L1"] is None
def test_split_select_4():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "c"
def test_split_select_5():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": "c"}
    assert split_select("L", "V", "P", "L1", instantiations)
def test_split_select_6():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": "d"}
    assert not split_select("L", "V", "P", "L1", instantiations)
def test_split_select_7():
    instantiations : 'dict[str,str|None]' = {"L": "a b c d e", "V": "space", "P": "2", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "c"
def test_split_select_8():
    instantiations : 'dict[str,str|None]' = {"L": "a b c d e", "V": "space", "P": "2.6", "L1": None}
    with pytest.raises(NotAnIntegerError):
        split_select("L", "V", "P", "L1", instantiations)


# Test cases for the `replace` predicate
def test_replace_0():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": ":", "L1": None}
    result = replace("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "a:b:c:d:e"
def test_replace_1():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": ":", "L1": "a:b:c:d:e"}
    assert replace("L", "V", "P", "L1", instantiations)
def test_replace_2():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": ":", "L1": "a:b:c:d"}
    assert not replace("L", "V", "P", "L1", instantiations)
def test_replace_3():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": ":", "L1": None}
    result = replace("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "a:b:c:d:e"
def test_replace_4():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": None, "P": ":", "L1": None}
    with pytest.raises(InstantiationError):
        replace("L", "V", "P", "L1", instantiations)
def test_replace_5():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": None, "L1": None}
    with pytest.raises(InstantiationError):
        replace("L", "V", "P", "L1", instantiations)
def test_replace_6():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": "w", "P": ":", "L1": "a,b,c,d,e"}
    result = replace("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == instantiations["L"]
def test_replace_7():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": "w", "P": ":", "L1": "a,,c,d,e"}
    assert not replace("L", "V", "P", "L1", instantiations)


# Test cases for the `line_number` predicate
def test_line_number_0():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "N": None}
    result = line_number("L", "N", 0, instantiations)
    assert result
    assert instantiations["N"] == "1"
def test_line_number_1():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "N": "1"}
    assert line_number("L", "N", 0, instantiations)
def test_line_number_2():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "N": "1"}
    assert not line_number("L", "N", 2, instantiations)


# Test cases for the `contains` predicate
def test_contains_0():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "S": "b"}
    assert contains("L", "S", instantiations)
def test_contains_1():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "S": "f"}
    assert not contains("L", "S", instantiations)
def test_contains_2():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "S": None}
    with pytest.raises(InstantiationError):
        contains("L", "S", instantiations)


# Test cases for the 'strip' predicate
def test_strip_0():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": None}
    result = strip("L", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "a,b,c,d,e"
def test_strip_1():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": "a,b,c,d,e"}
    assert strip("L", "L1", instantiations)
def test_strip_2():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": "a,b,c,d"}
    assert not strip("L", "L1", instantiations)
def test_strip_3():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": None}
    result = strip("L", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "a,b,c,d,e"
def test_strip_4():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": "a,b,c,d,e"}
    with pytest.raises(InstantiationError):
        strip("L", "L1", instantiations)
