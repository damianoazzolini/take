import io
from contextlib import redirect_stdout
from hypothesis import given, settings, strategies
from tempfile import NamedTemporaryFile
import os


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
        with_filename : bool = False
    ) -> str:
    """
    Helper function to get the result of a command.
    """
    args = argparse.Namespace(
        filename=[filename],
        command=command,
        suppress_output=False,
        aggregate=aggregate,
        plot=False,
        max_count=max_count,
        with_filename=with_filename,
        uncolored=True,
        recursive=False,
        stats=False,
        debug=False
    )
    with io.StringIO() as buf, redirect_stdout(buf):
        loop_process(args)
        return buf.getvalue()

def test_integration_sw_len_gt_leq_cap():
    command = ["line(L), startswith(L,i), length(L,N), gt(N,5), leq(N,14), capitalize(L,LC), print(LC)"]
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename)
    os.unlink(filename)
    assert res == "Instance"

def test_integration_len_lt():
    command = ["line(L), length(L,N), lt(N,1), println(L)"]
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename)
    os.unlink(filename)
    assert res == "\n\n\n\n"

def test_integration_len_not_gt():
    command = ["line(L), length(L,N), not gt(N,1), println(L)"]
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename)
    os.unlink(filename)
    assert res == "\n\n\n\n"

def test_integration_sw_sps_t2s():
    command = ["line(L), startswith(L,'real'), split_select(L,tab,1,T), time_to_seconds(T,TS), println(TS)"]
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename)
    os.unlink(filename)
    assert res == "8.853\n31.248\n162.765\n"

def test_integration_sw_sps_st_agg_avg():
    command = ["line(L), startswith(L,'AUCPR'), split_select(L,':',1,L1), strip(L1,L2), println(L2)"]
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename, aggregate=["average"])
    os.unlink(filename)
    assert res == "0.720441984486102\n0.9423737373737374\n0.7111492673992674\n0.9536004273504273\n0.6554753579753579\n[average] 0.7966081549169783\n"

def test_integration_sw_sps_st_agg_sort():
    command = ["line(L), startswith(L,size), split_select(L,space,1,S), println(S)"]
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename, aggregate=["sort_descending"])
    os.unlink(filename)
    assert res.strip().replace("\n","").replace(" ","") == "7891011.5[sort_descending]11.510987"

def test_integration_sw_sps_st_max_count():
    command = ["line(L), startswith(L,size), split_select(L,space,1,S), println(S)"]
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename, max_count=4)
    os.unlink(filename)
    assert res.strip().replace("\n","").replace(" ","") == "78910"

def test_integration_sw_sps_st_max_count_double_print():
    command = ["line(L), startswith(L,size), split_select(L,space,1,S), print(S), println(S)"]
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename, max_count=4)
    os.unlink(filename)
    assert res.strip().replace("\n","").replace(" ","") == "7788991010"

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
        aggregate = random.sample(["count", "sum", "product", "average", "stddev", "variance", "min", "max", "concat", "unique", "first", "last", "sort_ascending", "sort_descending", "median", "word_count"], 1)
    else:
        aggregate = []
    try:
        _ = get_result([command], filename, aggregate=aggregate)
        # assert True
    except Exception as e:
        assert False, command + " " + str(aggregate) + "\n" + str(e)
    finally:
        os.unlink(filename)