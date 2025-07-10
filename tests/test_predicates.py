import pytest
from io import StringIO
import sys

from src.take.predicates import *

# Test cases for the `startswith` predicate
def test_startswith_0():
    instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": None}
    result = startswith("L1", "v", instantiations, is_negated=False)
    assert result
def test_startswith_1():
    instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": None}
    result = startswith("L1", "b", instantiations, is_negated=False)
    assert not result
def test_startswith_2():
    instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": "v0"}
    result = startswith("L1", "L2", instantiations, is_negated=False)
    assert result
def test_startswith_3():
    instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": None}
    with pytest.raises(InstantiationError):
        startswith("L1", "L2", instantiations, is_negated=False)
def test_startswith_4():
    instantiations : 'dict[str,str|None]' = {"L1": "v0,2,6", "L2": "v0"}
    assert not startswith("l1", "L2", instantiations, is_negated=False)
# Tests for endswith function
def test_endswith_variable_true():
    instantiations : 'dict[str,str|None]' = {"L": "hello world", "S": "world"}
    assert endswith("L", "S", instantiations, is_negated=False)
def test_endswith_variable_false():
    instantiations : 'dict[str,str|None]' = {"L": "hello world", "S": "hello"}
    assert not endswith("L", "S", instantiations, is_negated=False)
def test_endswith_constant_true():
    instantiations : 'dict[str,str|None]' = {"L": "hello world"}
    assert endswith("L", "world", instantiations, is_negated=False)
def test_endswith_constant_false():
    instantiations : 'dict[str,str|None]' = {"L": "hello world"}
    assert not endswith("L", "hello", instantiations, is_negated=False)
def test_endswith_quoted_constant():
    instantiations : 'dict[str,str|None]' = {"L": "hello world"}
    assert endswith("L", "'world'", instantiations, is_negated=False)
def test_endswith_uninstantiated_suffix():
    instantiations : 'dict[str,str|None]' = {"L": "hello world", "S": None}
    with pytest.raises(InstantiationError):
        endswith("L", "S", instantiations, is_negated=False)
def test_endswith_constant_line_and_suffix():
    instantiations : 'dict[str,str|None]' = {}
    assert endswith("hello world", "world", instantiations, is_negated=False)


# Test cases for lt_leq_gt_geq_eq_wrapper
# this is a nice candidate for property based
def test_lt_leq_gt_geq_eq_wrapper_0():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "10"}
    assert lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_1():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "10"}
    assert lt_leq_gt_geq_eq_wrapper("leq", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_2():
    instantiations : 'dict[str,str|None]' = {"N": "10", "V": "5"}
    assert lt_leq_gt_geq_eq_wrapper("gt", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_3():
    instantiations : 'dict[str,str|None]' = {"N": "10", "V": "5"}
    assert lt_leq_gt_geq_eq_wrapper("geq", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_4():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert lt_leq_gt_geq_eq_wrapper("leq", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_5():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert lt_leq_gt_geq_eq_wrapper("geq", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_6():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert not lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_7():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert not lt_leq_gt_geq_eq_wrapper("gt", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_8():
    instantiations : 'dict[str,str|None]' = {"N": None, "V": "5"}
    with pytest.raises(InstantiationError):
        lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_9():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": None}
    with pytest.raises(InstantiationError):
        lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_10():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "a"}
    with pytest.raises(NotANumberError):
        lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations, is_negated=False)
def test_lt_leq_gt_geq_eq_wrapper_11():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert not lt_leq_gt_geq_eq_wrapper("gt", "5", "5", instantiations, is_negated=False)
def test_lt_function():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "10"}
    assert lt("N", "V", instantiations, is_negated=False)
    assert not lt("V", "N", instantiations, is_negated=False)
def test_leq_function():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "10"}
    assert leq("N", "V", instantiations, is_negated=False)
    instantiations["N"] = "10"
    assert leq("N", "V", instantiations, is_negated=False)
def test_gt_function():
    instantiations : 'dict[str,str|None]' = {"N": "10", "V": "5"}
    assert gt("N", "V", instantiations, is_negated=False)
    assert not gt("V", "N", instantiations, is_negated=False)
def test_geq_function():
    instantiations : 'dict[str,str|None]' = {"N": "10", "V": "5"}
    assert geq("N", "V", instantiations, is_negated=False)
    instantiations["N"] = "5"
    assert geq("N", "V", instantiations, is_negated=False)
def test_eq_function():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "5"}
    assert eq("N", "V", instantiations, is_negated=False)
    instantiations["V"] = "10"
    assert not eq("N", "V", instantiations, is_negated=False)
def test_comparison_wrapper_floats():
    instantiations : 'dict[str,str|None]' = {"N": "5.5", "V": "10.2"}
    assert lt_leq_gt_geq_eq_wrapper("lt", "N", "V", instantiations, is_negated=False)
    assert lt_leq_gt_geq_eq_wrapper("leq", "N", "V", instantiations, is_negated=False)
    assert not lt_leq_gt_geq_eq_wrapper("gt", "N", "V", instantiations, is_negated=False)
    assert not lt_leq_gt_geq_eq_wrapper("geq", "N", "V", instantiations, is_negated=False)
    assert not lt_leq_gt_geq_eq_wrapper("eq", "N", "V", instantiations, is_negated=False)
def test_comparison_wrapper_constants():
    assert lt_leq_gt_geq_eq_wrapper("lt", "5", "10", {}, is_negated=False)
    assert lt_leq_gt_geq_eq_wrapper("eq", "5", "5", {}, is_negated=False)
def test_comparison_wrapper_invalid_type():
    instantiations : 'dict[str,str|None]' = {"N": "5", "V": "10"}
    with pytest.raises(ValueError):
        lt_leq_gt_geq_eq_wrapper("invalid", "N", "V", instantiations, is_negated=False)


# Test cases for the `length` predicate
def test_length_0():
    instantiations : 'dict[str,str|None]' = {"L": "v0,2,6", "N": None}
    result = length("L", "N", instantiations, is_negated=False)
    assert result
    assert instantiations["N"] == "6"
def test_length_1():
    instantiations : 'dict[str,str|None]' = {"L": "v0,2,6", "N": "6"}
    assert length("L", "N", instantiations, is_negated=False)
def test_length_2():
    instantiations : 'dict[str,str|None]' = {"L": "v0,2,6", "N": "4"}
    assert not length("L", "N", instantiations, is_negated=False)
def test_length_3():
    instantiations : 'dict[str,str|None]' = {"L": None, "N": "6"}
    with pytest.raises(InstantiationError):
        length("L", "N", instantiations, is_negated=False)
def test_length_4():
    instantiations : 'dict[str,str|None]' = {"L": "adf", "N": "a6"}
    with pytest.raises(NotANumberError):
        length("L", "N", instantiations, is_negated=False)
def test_length_5():
    instantiations : 'dict[str,str|None]' = {"L": "adf", "N": None}
    assert length("L", "3", instantiations, is_negated=False)
def test_length_6():
    instantiations : 'dict[str,str|None]' = {"L": None, "N": None}
    assert length("adf", "3", instantiations, is_negated=False)
def test_length_7():
    instantiations : 'dict[str,str|None]' = {"L": None, "N": None}
    assert not length("adfh", "3", instantiations, is_negated=False)
def test_length_empty_string():
    instantiations : 'dict[str,str|None]' = {"L": "", "N": None}
    result = length("L", "N", instantiations, is_negated=False)
    assert result
    assert instantiations["N"] == "0"
def test_length_unicode_string():
    instantiations : 'dict[str,str|None]' = {"L": "héllo", "N": None}
    result = length("L", "N", instantiations, is_negated=False)
    assert result
    assert instantiations["N"] == "5"
def test_length_constants():
    instantiations : 'dict[str,str|None]' = {}
    assert length("hello", "5", instantiations, is_negated=False)
    assert not length("hello", "3", instantiations, is_negated=False)


# Test cases for the 'capitalize' predicate
def test_capitalize_0():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "L1": None}
    result = capitalize("L", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "Hello"
def test_capitalize_1():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "L1": "Hello"}
    assert capitalize("L", "L1", instantiations, is_negated=False)
def test_capitalize_2():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "L1": "hello"}
    assert not capitalize("L", "L1", instantiations, is_negated=False)
def test_capitalize_3():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": "Hello"}
    with pytest.raises(InstantiationError):
        capitalize("L", "L1", instantiations, is_negated=False)
def test_capitalize_4():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": "Hello"}
    assert not capitalize("ab", "L1", instantiations, is_negated=False)
def test_capitalize_5():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": None}
    capitalize("ab", "L1", instantiations, is_negated=False)
    assert instantiations["L1"] != "AB"
def test_capitalize_6():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": "Hello"}
    capitalize("cIAo", "L1", instantiations, is_negated=False)
    assert instantiations["L1"] != "Ciao"
def test_capitalize_empty_string():
    instantiations : 'dict[str,str|None]' = {"L": "", "L1": None}
    result = capitalize("L", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == ""
def test_capitalize_single_char():
    instantiations : 'dict[str,str|None]' = {"L": "a", "L1": None}
    result = capitalize("L", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "A"
def test_capitalize_already_capitalized():
    instantiations : 'dict[str,str|None]' = {"L": "Hello", "L1": None}
    result = capitalize("L", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "Hello"
def test_capitalize_constants():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "L1": "hello"}
    assert not capitalize("L", "L1", instantiations, is_negated=False)
    instantiations : 'dict[str,str|None]' = {"L": "Hello", "L1": "hello"}
    assert not capitalize("L", "L1", instantiations, is_negated=False)
    assert capitalize("c", "'C'", {}, is_negated=False)
    assert not capitalize("'C'", "c", {}, is_negated=False)

# Test cases for the `split_select` predicate
def test_split_select_0():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "c"
def test_split_select_1():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "0", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "a"
def test_split_select_2():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "4", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "e"
def test_split_select_3():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "5", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations, is_negated=False)
    assert not result
    assert instantiations["L1"] is None
def test_split_select_4():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "c"
def test_split_select_5():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": "c"}
    assert split_select("L", "V", "P", "L1", instantiations, is_negated=False)
def test_split_select_6():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": "2", "L1": "d"}
    assert not split_select("L", "V", "P", "L1", instantiations, is_negated=False)
def test_split_select_7():
    instantiations : 'dict[str,str|None]' = {"L": "a b c d e", "V": "space", "P": "2", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "c"
def test_split_select_8():
    instantiations : 'dict[str,str|None]' = {"L": "a b c d e", "V": "space", "P": "2.6", "L1": None}
    with pytest.raises(NotAnIntegerError):
        split_select("L", "V", "P", "L1", instantiations, is_negated=False)
def test_split_select_empty_string():
    instantiations : 'dict[str,str|None]' = {"L": "", "V": ",", "P": "0", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == ""
def test_split_select_no_delimiter():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "V": ",", "P": "0", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "hello"
def test_split_select_variable_delimiter():
    instantiations : 'dict[str,str|None]' = {"L": "a|b|c", "V": "|", "P": "1", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "b"
def test_split_select_negative_index():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c", "V": ",", "P": "-1", "L1": None}
    result = split_select("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "c"


# Test cases for the `replace` predicate
def test_replace_0():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": ":", "L1": None}
    result = replace("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "a:b:c:d:e"
def test_replace_1():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": ":", "L1": "a:b:c:d:e"}
    assert replace("L", "V", "P", "L1", instantiations, is_negated=False)
def test_replace_2():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": ":", "L1": "a:b:c:d"}
    assert not replace("L", "V", "P", "L1", instantiations, is_negated=False)
def test_replace_3():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": ":", "L1": None}
    result = replace("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "a:b:c:d:e"
def test_replace_4():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": None, "P": ":", "L1": None}
    with pytest.raises(InstantiationError):
        replace("L", "V", "P", "L1", instantiations, is_negated=False)
def test_replace_5():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": ",", "P": None, "L1": None}
    with pytest.raises(InstantiationError):
        replace("L", "V", "P", "L1", instantiations, is_negated=False)
def test_replace_6():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": "w", "P": ":", "L1": "a,b,c,d,e"}
    result = replace("L", "V", "P", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == instantiations["L"]
def test_replace_7():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "V": "w", "P": ":", "L1": "a,,c,d,e"}
    assert not replace("L", "V", "P", "L1", instantiations, is_negated=False)
def test_replace_no_occurrence():
    instantiations : 'dict[str,str|None]' = {"L": "hello world", "OLD": "xyz", "NEW": "abc", "L1": None}
    result = replace("L", "OLD", "NEW", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "hello world"
def test_replace_multiple_occurrences():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,a,c,a", "OLD": "a", "NEW": "x", "L1": None}
    result = replace("L", "OLD", "NEW", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "x,b,x,c,x"
def test_replace_empty_replacement():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c", "OLD": ",", "NEW": "", "L1": None}
    result = replace("L", "OLD", "NEW", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "abc"


# Test cases for the `line_number` predicate
def test_line_number_0():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "N": None}
    result = line_number("L", "N", 0, instantiations, is_negated=False)
    assert result
    assert instantiations["N"] == "1"
def test_line_number_1():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "N": "1"}
    assert line_number("L", "N", 0, instantiations, is_negated=False)
def test_line_number_2():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "N": "1"}
    assert not line_number("L", "N", 2, instantiations, is_negated=False)
def test_line_number_constant():
    instantiations : 'dict[str,str|None]' = {}
    assert line_number("test", "5", 4, instantiations, is_negated=False)
    assert not line_number("test", "5", 3, instantiations, is_negated=False)
def test_line_number_large_index():
    instantiations : 'dict[str,str|None]' = {"L": "test", "N": None}
    result = line_number("L", "N", 999, instantiations, is_negated=False)
    assert result
    assert instantiations["N"] == "1000"
def test_line_number_negated_0():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "N": None}
    with pytest.raises(UnsafeError):
        line_number("L", "N", 0, instantiations, is_negated=True)
def test_line_number_negated_1():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "N": "1"}
    assert not line_number("L", "N", 0, instantiations, is_negated=True)
def test_line_number_negated_2():
    instantiations : 'dict[str,str|None]' = {"L": None, "N": "1"}
    with pytest.raises(UnsafeError):
        line_number("L", "N", 0, instantiations, is_negated=True)
def test_line_number_negated_3():
    instantiations : 'dict[str,str|None]' = {"L": None, "N": None}
    with pytest.raises(UnsafeError):
        line_number("L", "N", 0, instantiations, is_negated=True)


# Test cases for the `contains` predicate
def test_contains_0():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "S": "b"}
    assert contains("L", "S", instantiations, is_negated=False)
def test_contains_1():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "S": "f"}
    assert not contains("L", "S", instantiations, is_negated=False)
def test_contains_2():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "S": None}
    with pytest.raises(InstantiationError):
        contains("L", "S", instantiations, is_negated=False)
def test_contains_empty_substring():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "S": ""}
    assert contains("L", "S", instantiations, is_negated=False)
def test_contains_same_string():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "S": "hello"}
    assert contains("L", "S", instantiations, is_negated=False)
def test_contains_constants():
    instantiations : 'dict[str,str|None]' = {}
    assert contains("hello world", "world", instantiations, is_negated=False)
    assert not contains("hello world", "xyz", instantiations, is_negated=False)
def test_contains_negated_0():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "S": "b"}
    assert not contains("L", "S", instantiations, is_negated=True)
def test_contains_negated_1():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "S": "f"}
    assert contains("L", "S", instantiations, is_negated=True)
def test_contains_negated_2():
    instantiations : 'dict[str,str|None]' = {"L": "a,b,c,d,e", "S": None}
    with pytest.raises(UnsafeError):
        contains("L", "S", instantiations, is_negated=True)
def test_contains_negated_3():
    instantiations : 'dict[str,str|None]' = {"L": None, "S": "a"}
    with pytest.raises(UnsafeError):
        contains("L", "S", instantiations, is_negated=True)
def test_contains_negated_4():
    instantiations : 'dict[str,str|None]' = {"L": None, "S": None}
    with pytest.raises(UnsafeError):
        contains("L", "S", instantiations, is_negated=True)

# Test cases for the 'strip' predicate
def test_strip_0():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": None}
    result = strip("L", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "a,b,c,d,e"
def test_strip_1():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": "a,b,c,d,e"}
    assert strip("L", "L1", instantiations, is_negated=False)
def test_strip_2():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": "a,b,c,d"}
    assert not strip("L", "L1", instantiations, is_negated=False)
def test_strip_3():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": None}
    result = strip("L", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "a,b,c,d,e"
def test_strip_4():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": "a,b,c,d,e"}
    with pytest.raises(InstantiationError):
        strip("L", "L1", instantiations, is_negated=False)
def test_strip_no_whitespace():
    instantiations : 'dict[str,str|None]' = {"L": "hello", "L1": None}
    result = strip("L", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "hello"
def test_strip_only_whitespace():
    instantiations : 'dict[str,str|None]' = {"L": "   ", "L1": None}
    result = strip("L", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == ""
def test_strip_tabs_and_newlines():
    instantiations : 'dict[str,str|None]' = {"L": "\t\nhello world\n\t", "L1": None}
    result = strip("L", "L1", instantiations, is_negated=False)
    assert result
    assert instantiations["L1"] == "hello world"
def test_strip_constants():
    instantiations : 'dict[str,str|None]' = {}
    assert strip("  hello  ", "hello", instantiations, is_negated=False)
    assert not strip("  hello  ", "  hello  ", instantiations, is_negated=False)
def test_strip_negated_0():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": "b,c,d,e"}
    assert strip("L", "L1", instantiations, is_negated=True)
def test_strip_negated_1():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": "a,b,c,d,e"}
    assert not strip("L", "L1", instantiations, is_negated=True)
def test_strip_negated_2():
    instantiations : 'dict[str,str|None]' = {"L": "  a,b,c,d,e  ", "L1": None}
    with pytest.raises(UnsafeError):
        strip("L", "L1", instantiations, is_negated=True)
def test_strip_negated_3():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": "a,b,c,d,e"}
    with pytest.raises(UnsafeError):
        strip("L", "L1", instantiations, is_negated=True)
def test_strip_negated_4():
    instantiations : 'dict[str,str|None]' = {"L": None, "L1": None}
    with pytest.raises(UnsafeError):
        strip("L", "L1", instantiations, is_negated=True)


# Test cases for the `time_to_seconds` predicate
def test_time_to_seconds_0():
    instantiations : 'dict[str,str|None]' = {"T": "0m1.131s", "S": None}
    result = time_to_seconds("T", "S", instantiations, is_negated=False)
    assert result
    assert instantiations["S"] == "1.131"
def test_time_to_seconds_1():
    instantiations : 'dict[str,str|None]' = {"T": "0m1.131s", "S": "1.131"}
    assert time_to_seconds("T", "S", instantiations, is_negated=False)
def test_time_to_seconds_2():
    instantiations : 'dict[str,str|None]' = {"T": "0m1.131s", "S": "2.0"}
    assert not time_to_seconds("T", "S", instantiations, is_negated=False)

# Test cases for helper functions

# Tests for is_instantiated
def test_is_instantiated_true():
    instantiations : 'dict[str,str|None]' = {"X": "value", "Y": None}
    assert is_instantiated("X", instantiations)

def test_is_instantiated_false():
    instantiations : 'dict[str,str|None]' = {"X": "value", "Y": None}
    assert not is_instantiated("Y", instantiations)

def test_is_instantiated_not_found():
    instantiations : 'dict[str,str|None]' = {"X": "value"}
    with pytest.raises(VariableNotFoundError):
        is_instantiated("Z", instantiations)

# Tests for get_instantiation
def test_get_instantiation_success():
    instantiations : 'dict[str,str|None]' = {"X": "test_value", "Y": None}
    assert get_instantiation("X", instantiations) == "test_value"

def test_get_instantiation_not_instantiated():
    instantiations : 'dict[str,str|None]' = {"X": "test_value", "Y": None}
    with pytest.raises(InstantiationError):
        get_instantiation("Y", instantiations)

def test_get_instantiation_not_found():
    instantiations : 'dict[str,str|None]' = {"X": "test_value"}
    with pytest.raises(VariableNotFoundError):
        get_instantiation("Z", instantiations)

# Tests for is_variable
def test_is_variable_true():
    assert is_variable("Variable")
    assert is_variable("X")
    assert is_variable("TEST")

def test_is_variable_false():
    assert not is_variable("variable")
    assert not is_variable("x")
    assert not is_variable("test")
    assert not is_variable("123")
    assert not is_variable("'string'")

# Tests for get_constant
def test_get_constant_with_quotes():
    assert get_constant("'hello world'") == "hello world"
    assert get_constant("'test'") == "test"

def test_get_constant_without_quotes():
    assert get_constant("hello") == "hello"
    assert get_constant("123") == "123"

# Tests for get_integer
def test_get_integer_valid():
    assert get_integer("123") == 123
    assert get_integer("-456") == -456
    assert get_integer("0") == 0

def test_get_integer_invalid():
    with pytest.raises(NotAnIntegerError):
        get_integer("12.5")
    with pytest.raises(NotAnIntegerError):
        get_integer("abc")
    with pytest.raises(NotAnIntegerError):
        get_integer("12.0")

# Tests for get_number
def test_get_number_integer():
    assert get_number("123") == 123
    assert get_number("-456") == -456

def test_get_number_float():
    assert get_number("123.45") == 123.45
    assert get_number("-456.78") == -456.78
    assert get_number("12.0") == 12.0

def test_get_number_invalid():
    with pytest.raises(NotANumberError):
        get_number("abc")
    with pytest.raises(NotANumberError):
        get_number("12.34.56")

# Tests for line function
def test_line_variable_uninstantiated():
    instantiations : 'dict[str,str|None]' = {"L": None}
    result = line("test line", "L", instantiations)
    assert result
    assert instantiations["L"] == "test line"

def test_line_variable_instantiated_match():
    instantiations : 'dict[str,str|None]' = {"L": "test line"}
    result = line("test line", "L", instantiations)
    assert result

def test_line_variable_instantiated_no_match():
    instantiations : 'dict[str,str|None]' = {"L": "different line"}
    result = line("test line", "L", instantiations)
    assert not result

def test_line_constant_match():
    instantiations : 'dict[str,str|None]' = {}
    result = line("test line", "test line", instantiations)
    assert result

def test_line_constant_no_match():
    instantiations : 'dict[str,str|None]' = {}
    result = line("test line", "different line", instantiations)
    assert not result

# Tests for print_line function
def test_print_line_variable():
    instantiations : 'dict[str,str|None]' = {"L": "test output"}
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    result = print_line("L", instantiations)
    
    sys.stdout = old_stdout
    output = mystdout.getvalue()
    
    assert result
    assert output == "test output"

def test_print_line_variable_with_newline():
    instantiations : 'dict[str,str|None]' = {"L": "test output"}
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    result = print_line("L", instantiations, with_newline=True)
    
    sys.stdout = old_stdout
    output = mystdout.getvalue()
    
    assert result
    assert output == "test output\n"

def test_print_line_constant():
    instantiations : 'dict[str,str|None]' = {}
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    result = print_line("direct output", instantiations)
    
    sys.stdout = old_stdout
    output = mystdout.getvalue()
    
    assert result
    assert output == "direct output"
