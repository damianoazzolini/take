import pytest

from src.take.predicates import *

# Test cases for the `startswith` predicate
def test_startswith_0():
    instantiations = {"L1": "v0,2,6", "L2": ""}
    result = startswith("L1", "v", instantiations)
    assert result
def test_startswith_1():
    instantiations = {"L1": "v0,2,6", "L2": ""}
    result = startswith("L1", "b", instantiations)
    assert not result
def test_startswith_2():
    instantiations = {"L1": "v0,2,6", "L2": "v0"}
    result = startswith("L1", "L2", instantiations)
    assert result
def test_startswith_3():
    instantiations = {"L1": "v0,2,6", "L2": ""}
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
    instantiations = {"N": "", "V": "5"}
    with pytest.raises(InstantiationError):
        lt_leq_gt_geq_wrapper("lt", "N", "V", instantiations)
def test_lt_leq_gt_geq_wrapper_9():
    instantiations = {"N": "5", "V": ""}
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
    instantiations = {"L": "v0,2,6", "N": ""}
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
    instantiations = {"L": "", "N": "6"}
    with pytest.raises(InstantiationError):
        length("L", "N", instantiations)
def test_length_4():
    instantiations = {"L": "adf", "N": "a6"}
    with pytest.raises(NotANumberError):
        length("L", "N", instantiations)
def test_length_5():
    instantiations = {"L": "adf", "N": ""}
    assert length("L", "3", instantiations)
def test_length_6():
    instantiations = {"L": "", "N": ""}
    assert length("adf", "3", instantiations)
def test_length_7():
    instantiations = {"L": "", "N": ""}
    assert not length("adfh", "3", instantiations)
