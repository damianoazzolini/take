from contextlib import redirect_stdout
from hypothesis import given, settings, strategies
import io
import os
import pytest
from tempfile import NamedTemporaryFile


from src.take.take import *
from src.take.predicates import PREDICATES
import random

CONTENT = """
test
0.2
  3

try

content_longer_than_14_characters

instance
Started at: 
size 7
[RESULT]                   [4. 4.]
real	0m8.853s
user	0m8.231s
sys	0m0.110s
size 8
[RESULT]                    [4. 4.]
real	0m31.248s
user	0m30.784s
sys	0m0.177s
size 9
[RESULT]                    [4. 4.]
real	2m42.765s
user	2m41.007s
sys	0m1.205s
----- CV 1 ----- 
Train on: f2,f3,f4,f5, Test on: f1
AUCPR1:  0.720441984486102
AUCROC1: 0.735
LL1: -12.753700137597306
----- CV 2 ----- 
Train on: f1,f3,f4,f5, Test on: f2
AUCPR2:  0.9423737373737374
AUCROC2: 0.94
LL2: -7.4546895016487245
----- CV 3 ----- 
Train on: f1,f2,f4,f5, Test on: f3
AUCPR3:  0.7111492673992674
AUCROC3: 0.71
LL3: -11.836606612796992
----- CV 4 ----- 
Train on: f1,f2,f3,f5, Test on: f4
AUCPR4:  0.9536004273504273
AUCROC4: 0.95
LL4: -6.458126608595575
----- CV 5 ----- 
Train on: f1,f2,f3,f4, Test on: f5
AUCPR:  0.6554753579753579
AUCROC: 0.765
LL5: -12.149458117122595
size 10
size 11.5
"""

def get_temporary_file(content: str) -> str:
    """
    Create a temporary file with the given content and return its name.
    """
    f = NamedTemporaryFile(mode='w+', delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name

def get_result(
        command : 'list[str]',
        filename: str,
        aggregate : 'list[str]' = [],
        max_count: int = 0,
        suppress_output: bool = False,
        keep_separated: bool = False,
        with_filename : bool = False
    ) -> str:
    """
    Helper function to get the result of a command.
    """
    args = argparse.Namespace(
        filename=[filename],
        command=command,
        suppress_output=suppress_output,
        aggregate=aggregate,
        plot=False,
        max_count=max_count,
        with_filename=with_filename,
        uncolored=True,
        recursive=False,
        stats=False,
        debug=False,
        max_columns=0,
        keep_separated=keep_separated
    )
    with io.StringIO() as buf, redirect_stdout(buf):
        loop_process(args)
        return buf.getvalue()

@pytest.mark.parametrize("command, expected, aggregate, strip_results, max_count, keep_separated, suppress_output", [
    (
        ["line(L), startswith(L,i), length(L,N), gt(N,5), leq(N,14), capitalize(L,LC), print(LC)"], 
        "Instance",
        [],
        False,
        0,
        False,
        False
    ),
    (
        ["line(L), length(L,N), lt(N,1), println(L)"],
        "\n\n\n\n",
        [],
        False,
        0,
        False,
        False
    ),
    ([
        "line(L), length(L,N), not gt(N,1), println(L)"],
        "\n\n\n\n",
        [],
        False,
        0,
        False,
        False
    ),
    (
        ["line(L), startswith(L,'real'), split_select(L,tab,1,T), time_to_seconds(T,TS), println(TS)"], "8.853\n31.248\n162.765\n",
        [],
        False,
        0,
        False,
        False
    ),
    (
        ["line(L), startswith(L,'AUCPR'), split_select(L,':',1,L1), strip(L1,L2), println(L2)"],
        "[average] 0.7966081549169783\n",
        ["average"],
        False,
        0,
        False,
        True
    ),
    (
        ["line(L), startswith(L,'AUCPR'), split_select(L,':',1,L1), strip(L1,L2), println(L2)"],
        "[average __FILENAME__] 0.7966081549169783\n",
        ["average"],
        False,
        0,
        True,
        True
    ),
    (
        ["line(L), startswith(L,'AUCPR'), split_select(L,':',1,L1), strip(L1,L2), println(L2)"],
        "[count] 5\n",
        ["count"],
        False,
        0,
        False,
        True
    ),
    (
        ["line(L), startswith(L,'AUCPR'), split_select(L,':',1,L1), strip(L1,L2), println(L2)"],
        "[count __FILENAME__] 5\n",
        ["count"],
        False,
        0,
        True,
        True
    ),
    (
        ["line(L), startswith(L,size), split_select(L,space,1,S), println(S)"],
        "7\n8\n9\n10\n11.5\n[sort_descending] 11.510987",
        ["sort_descending"],
        True,
        0,
        False,
        False
    ),
    (
        ["line(L), startswith(L,size), split_select(L,space,1,S), println(S)"],
        "[first] 7",
        ["first"],
        True,
        0,
        False,
        True
    ),
    (
        ["line(L), startswith(L,size), split_select(L,space,1,S), println(S)"],
        "[last] 11.5",
        ["last"],
        True,
        0,
        False,
        True
    ),
    (
        ["line(L), startswith(L,size), split_select(L,space,1,S), println(S)"],
        "78910",
        [],
        True,
        4,
        False,
        False
    ),
    (
        ["line(L), startswith(L,size), split_select(L,space,1,S), print(S), println(S)"],
        "7788991010",
        [],
        True,
        4,
        False,
        False
    )
])
def test_integration(command : 'list[str]', expected: str, aggregate : 'list[str]', strip_results: bool, max_count: int, keep_separated : bool, suppress_output : bool):
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename, aggregate=aggregate, max_count=max_count, keep_separated=keep_separated, suppress_output=suppress_output)
    os.unlink(filename)
    if strip_results:
        res = res.strip().replace("\n", "").replace(" ", "")
        expected = expected.strip().replace("\n", "").replace(" ", "")
    assert res == expected.replace("__FILENAME__", filename)


def test_equality_keep_separated():
    command = ["line(L), startswith(L,'AUCPR'), split_select(L,':',1,L1), strip(L1,L2), println(L2)"]
    aggregates : 'list[str]' = ["count", "sum", "product", "average", "mean", "stddev", "variance", "median", "min", "max", "range", "summary", "concat", "unique", "first", "last", "sort_ascending", "sort_descending", "word_count"]
    filename = get_temporary_file(CONTENT)
    res_separated = get_result(command, filename, aggregates, keep_separated=True, suppress_output=True)
    res_not_separated = get_result(command, filename, aggregates, keep_separated=False, suppress_output=True)
    os.unlink(filename)
    assert res_separated.count(filename) == len(aggregates)
    assert res_separated.replace(f" {filename}", "") == res_not_separated


def test_integration_sw_sps_st_max_count_filename():
    command = ["line(L), startswith(L,size), split_select(L,space,1,S), println(S)"]
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename, max_count=4, with_filename=True)
    os.unlink(filename)
    assert res.strip().replace("\n","").replace(" ","") == f"{filename}:7{filename}:8{filename}:9{filename}:10"


def generate_random_command() -> str:
    available_predicates = [(k,v) for k,v in PREDICATES.items()]
    command_len = random.randint(1, 10)
    len_args = random.randint(4, 5)
    args : 'list[str]' = []
    for i in range(len_args):
        # lowercase, uppercase, string, or digit
        arg_type = random.choice(["lowercase", "uppercase", "string", "digit"])
        if arg_type == "lowercase":
            args.append(f"l{i}")
        elif arg_type == "uppercase":
            args.append(f"L{i}")
        elif arg_type == "string":
            args.append(f"'L{i}'")
        elif arg_type == "digit":
            args.append(f"{random.randint(0, 9)}")
    # args = [f"L{i}" for i in range(len_args)]

    predicates_list : 'list[str]' = []

    for i in range(command_len):
        idx = random.randint(0, len(available_predicates) - 1)
        predicate_name = available_predicates[idx][0]
        predicate_arity = available_predicates[idx][1]
        current_arguments = random.sample(args, predicate_arity)
        predicates_list.append(f"{predicate_name}({', '.join(current_arguments)})")
    predicates_list.insert(0, f"line({random.choice(args)})")

    return f"{', '.join(predicates_list)}"


@given(strategies.integers(), strategies.booleans())
@settings(max_examples=10_000)
def test_random_command(seed : int, aggregator: bool):
    random.seed(seed)
    command = generate_random_command()
    filename = get_temporary_file(CONTENT)
    if aggregator:
        aggregate = random.sample(["count", "sum", "product", "average", "mean", "stddev", "variance", "min", "max", "range", "summary", "concat", "unique", "first", "last", "sort_ascending", "sort_descending", "median", "word_count"], 1)
    else:
        aggregate = []
    try:
        _ = get_result([command], filename, aggregate=aggregate)
        # assert True
    except Exception as e:
        assert False, command + " " + str(aggregate) + "\n" + str(e)
    finally:
        os.unlink(filename)