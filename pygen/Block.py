import contextvars
import ast
from typing import Union, Optional
from pygen.Value import *
from pygen.__helpers import get_module


class Block:
    def add_to_module(self):
        get_module().append(self)

    def __enter__(self):
        get_module().append_context(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        get_module().pop_context()


class If(ast.If, Block):
    def __init__(self, test):
        super().__init__(test=test, body=[], orelse=[])
        self.add_to_module()


class ClassDef(ast.ClassDef, Block):
    def __init__(self, name: str, bases: list[Value] = [], keywords: list[ast.keyword] = []):
        super().__init__(name=name, bases=bases, keywords=keywords, body=[], decorator_list=[])
        self.add_to_module()

    def add_base(self, value: Value):
        self.bases.append(value)

    def add_keyword(self, arg: str, value: Value):
        self.keywords.append(ast.keyword(
            arg=arg,
            value=value
        ))


class FunctionDef(ast.FunctionDef, Block):
    def __init__(self, name: str,
                 arguments: ast.arguments = ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[],
                                                          kwarg=None, vararg=None, defaults=[])):
        super().__init__(name=name, args=arguments, body=[], decorator_list=[])
        self.add_to_module()

    def add_arg(self, arg: str, annotation: str, default: Optional[Value] = None):
        self.args.args.append(ast.arg(
            arg=arg,
            annotation=Constant(annotation)
        ))

        if default is not None:
            self.args.defaults.append(default)

    def add_var_arg(self, arg: str, annotation: str):
        self.args.vararg = ast.arg(
            arg=arg,
            annotation=Constant(annotation)
        )

    def add_kwarg(self, arg: str, annotation: str, default: Optional[Value] = None):
        self.args.kwonlyargs.append(ast.arg(
            arg=arg,
            annotation=Constant(annotation)
        ))

        if default is not None:
            self.args.kw_defaults.append(default)

    def add_var_kwarg(self, arg: str, annotation: str):
        self.args.kwarg = ast.arg(
            arg=arg,
            annotation=Constant(annotation)
        )


class Else(ast.If, Block):
    def __init__(self):
        super().__init__(test=Constant(True), body=[], orelse=[])
        self.add_to_module()


class While(ast.While, Block):
    def __init__(self, test):
        super().__init__(test=test, body=[], orelse=[])
        self.add_to_module()


class For(ast.For, Block):
    def __init__(self, target: Name, iter: Name):
        super().__init__(target=target, iter=iter, body=[], orelse=[])
        self.add_to_module()
