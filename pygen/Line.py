import contextvars
import ast
from typing import Union, Optional
from pygen.Value import *
from pygen.__helpers import get_module


class Assign(ast.Assign):
    def __init__(self, targets: Union[list[Name], Name], value: int):
        if type(targets) is not list:
            super().__init__([targets], ast.Constant(value))
        else:
            super().__init__(targets, ast.Constant(value))

        get_module().append(self)


class alias(ast.alias):
    pass


class Import(ast.Import):
    def __init__(self, names: Union[list[alias], alias, ast.alias], module: Optional[str] = None):
        if module is not None:
            ImportFrom(names, module)
        else:
            if type(names) is not list:
                super().__init__(names=[names])
            else:
                super().__init__(names=names)

            get_module().append(self)


class ImportFrom(ast.ImportFrom):
    def __init__(self, names: Union[list[alias], alias, ast.alias], module: str):
        if type(names) is not list:
            super().__init__(names=[names], module=module)
        else:
            super().__init__(names=names, module=module)

        get_module().append(self)


class Pass(ast.Pass):
    def __init__(self):
        super().__init__()
        get_module().append(self)


class Delete(ast.Delete):
    def __init__(self, targets: Union[list[Value], Value]):
        if type(targets) is not list:
            super().__init__([targets])
        else:
            super().__init__(targets)

        get_module().append(self)


class Return(ast.Return):
    def __init__(self, value: Value):
        super().__init__(value)

        get_module().append(self)
