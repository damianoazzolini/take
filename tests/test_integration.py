import io
from contextlib import redirect_stdout
from tempfile import NamedTemporaryFile
import os


from src.take.take import *

CONTENT = """
test
0.2
  3

try

content_longer_than_14_characters

LL: 0.56
instance
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
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename)
    os.unlink(filename)
    assert res == "Instance"

def test_integration_2():
    command = ["line(L), length(L,N), lt(N,1), println(L)"]
    filename = get_temporary_file(CONTENT)
    res = get_result(command, filename)
    os.unlink(filename)
    assert res == "\n\n\n\n"


