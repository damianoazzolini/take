import pytest

from src.take.predicates import *

# Test cases for the `startswith` predicate
def test_startswith_0():
    instantiations = {"L1": "v0,2,6", "L2": None}
    result = startswith("L1", "v", instantiations)
    assert result
def test_startswith_1():
    instantiations = {"L1": "v0,2,6", "L2": None}
    result = startswith("L1", "b", instantiations)
    assert not result
def test_startswith_2():
    instantiations = {"L1": "v0,2,6", "L2": "v0"}
    result = startswith("L1", "L2", instantiations)
    assert result
def test_startswith_3():
    instantiations = {"L1": "v0,2,6", "L2": None}
    with pytest.raises(InstantiationError):
        startswith("L1", "L2", instantiations)
def test_startswith_4():
    instantiations = {"L1": "v0,2,6", "L2": "v0"}
    assert not startswith("l1", "L2", instantiations)
# def test_startswith_5(): # all the variables are checked to exist, so this test is not needed
#     instantiations = {"L1": "v0,2,6", "L2": "v0"}
#     with pytest.raises(VariableNotFoundError):
#         startswith("L3", "L2", instantiations)


# Test cases for lt_leq_gt_geq_wrapper
# this is a nice candidate for property based
def test_lt_leq_gt_geq_wrapper_0():
    instantiations = {"N": "5", "V": "10"}
    assert lt_leq_gt_geq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_1():
    instantiations = {"N": "5", "V": "10"}
    assert lt_leq_gt_geq_wrapper("leq", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_2():
    instantiations = {"N": "10", "V": "5"}
    assert lt_leq_gt_geq_wrapper("gt", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_3():
    instantiations = {"N": "10", "V": "5"}
    assert lt_leq_gt_geq_wrapper("geq", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_4():
    instantiations = {"N": "5", "V": "5"}
    assert lt_leq_gt_geq_wrapper("leq", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_5():
    instantiations = {"N": "5", "V": "5"}
    assert lt_leq_gt_geq_wrapper("geq", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_6():
    instantiations = {"N": "5", "V": "5"}
    assert not lt_leq_gt_geq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_7():
    instantiations = {"N": "5", "V": "5"}
    assert not lt_leq_gt_geq_wrapper("gt", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_8():
    instantiations = {"N": None, "V": "5"}
    with pytest.raises(InstantiationError):
        lt_leq_gt_geq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_9():
    instantiations = {"N": "5", "V": None}
    with pytest.raises(InstantiationError):
        lt_leq_gt_geq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_10():
    instantiations = {"N": "5", "V": "a"}
    with pytest.raises(NotANumberError):
        lt_leq_gt_geq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_11():
    instantiations = {"N": "5", "V": "5"}
    assert not lt_leq_gt_geq_wrapper("gt", "5", "5", instantiations)

# Test cases for the `length` predicate
def test_length_0():
    instantiations = {"L": "v0,2,6", "N": None}
    result = length("L", "N", instantiations)
    assert result
    assert instantiations["N"] == "6"
def test_length_1():
    instantiations = {"L": "v0,2,6", "N": "6"}
    assert length("L", "N", instantiations)
def test_length_2():
    instantiations = {"L": "v0,2,6", "N": "4"}
    assert not length("L", "N", instantiations)
def test_length_3():
    instantiations = {"L": None, "N": "6"}
    with pytest.raises(InstantiationError):
        length("L", "N", instantiations)
def test_length_4():
    instantiations = {"L": "adf", "N": "a6"}
    with pytest.raises(NotANumberError):
        length("L", "N", instantiations)
def test_length_5():
    instantiations = {"L": "adf", "N": None}
    assert length("L", "3", instantiations)
def test_length_6():
    instantiations = {"L": None, "N": None}
    assert length("adf", "3", instantiations)
def test_length_7():
    instantiations = {"L": None, "N": None}
    assert not length("adfh", "3", instantiations)

# Test cases for the 'capitalize' predicate
def test_capitalize_0():
    instantiations = {"L": "hello", "L1": None}
    result = capitalize("L", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "Hello"
def test_capitalize_1():
    instantiations = {"L": "hello", "L1": "Hello"}
    assert capitalize("L", "L1", instantiations)
def test_capitalize_2():
    instantiations = {"L": "hello", "L1": "hello"}
    assert not capitalize("L", "L1", instantiations)
def test_capitalize_3():
    instantiations = {"L": None, "L1": "Hello"}
    with pytest.raises(InstantiationError):
        capitalize("L", "L1", instantiations)
def test_capitalize_4():
    instantiations = {"L": None, "L1": "Hello"}
    assert not capitalize("ab", "L1", instantiations)
def test_capitalize_5():
    instantiations = {"L": None, "L1": None}
    capitalize("ab", "L1", instantiations)
    assert instantiations["L1"] != "AB"
def test_capitalize_6():
    instantiations = {"L": None, "L1": "Hello"}
    capitalize("cIAo", "L1", instantiations)
    assert instantiations["L1"] != "Ciao"

# Test cases for the `split_select` predicate
def test_split_select_0():
    instantiations = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "c"
def test_split_select_1():
    instantiations = {"L": "a,b,c,d,e", "V": ",", "P": "0", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "a"
def test_split_select_2():
    instantiations = {"L": "a,b,c,d,e", "V": ",", "P": "4", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "e"
def test_split_select_3():
    instantiations = {"L": "a,b,c,d,e", "V": ",", "P": "5", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert not result
    assert instantiations["L1"] is None
def test_split_select_4():
    instantiations = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "c"
def test_split_select_5():
    instantiations = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": "c"}
    assert split_select("L", "V", "P", "L1", instantiations)
def test_split_select_6():
    instantiations = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": "d"}
    assert not split_select("L", "V", "P", "L1", instantiations)
def test_split_select_7():
    instantiations = {"L": "a b c d e", "V": "space", "P": "2", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations)
    assert result
    assert instantiations["L1"] == "c"
def test_split_select_8():
    instantiations = {"L": "a b c d e", "V": "space", "P": "2.6", "L1": None}
    with pytest.raises(NotAnIntegerError):
        split_select("L", "V", "P", "L1", instantiations)
