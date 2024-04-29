from pygen.Module import Module, macro
from pygen.Block import *
from pygen.Value import *
from pygen.Line import *


@macro
def trial():
    with Module() as m:
        Expr(Name("print").call().add_arg(Constant("Hello world")))
        
        with If(Constant(True)) as _:
            Expr(Name("print").call().add_arg(Constant("Hello world")))
    return m


trial()
