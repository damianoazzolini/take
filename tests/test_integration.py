import io
from contextlib import redirect_stdout


from src.take.take import *

def get_result(command : 'list[str]', filename: str) -> str:
    """
    Helper function to get the result of a command.
    """
    args = argparse.Namespace(filename=filename, command=command, suppress_output=False, aggregate=None)
    with io.StringIO() as buf, redirect_stdout(buf):
        loop_process(args)
        return buf.getvalue()

def test_integration_1():
    command = ["line(L), startswith(L,i), length(L,N), gt(N,5), leq(N,14), capitalize(L,LC), print(LC)"]
    filename = "f.txt"
    assert get_result(command, filename) == "Import random"
def test_integration_2():
    command = ["line(L), length(L,N), lt(N,1), println(L)"]
    filename = "f.txt"
    assert get_result(command, filename) == "\n\n\n\n"


