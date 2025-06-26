import pytest

from src.take.take import *

def test_parser_1():
    with pytest.raises(MalformedLiteralError):
        Command("line(L),length(1L,N), gt(N,4), startswith(L,v), lt(N,7)")
def test_parser_2():
    c = Command("line(L),length(L,N), gt(N,4), startswith(L,v), lt(N,7)")
    assert len(c.literals) == 5
def test_parser_3():
    c = Command("line(L),length(L,N), gt(N,4), startswith(L,v), lt(N,7)")
    assert len(c.variables_dict) == 2
def test_parser_4():
    with pytest.raises(LiteralNotFoundError):
        Command("line(L),length(L,N,C), gt(N,4), startswith(L,v), lt(N,7)")
def test_parser_5():
    with pytest.raises(MissingLineError):
        Command("length(L,N), gt(N,4), startswith(L,v), lt(N,7)")
def test_parser_6():
    with pytest.raises(MissingLineError):
        Command("length(L,N), line(L), gt(N,4), startswith(L,v), lt(N,7)")
