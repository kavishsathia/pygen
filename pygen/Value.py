import ast
from collections import deque
from typing import Union, Optional, Any
import contextvars


class Value(ast.expr):
    def __init__(self, **kwargs):
        super().__init__()

    def call(self):
        return Call(self)

    def subscript(self, slice: 'Value'):
        return Subscript(value=self, slice=slice)

    def slice(self, lower: 'Value', upper: 'Value', step: 'Value'):
        return Subscript(value=self, slice=ast.Slice(lower, upper, step))

    def attribute(self, attr: str):
        return Attribute(value=self, attr=attr)

    def ifexp(self, test, orelse):
        return IfExp(self, test, orelse)


class Expr(ast.Expr):
    def __init__(self, value: Value):
        super().__init__(value)

        ctx = contextvars.copy_context()
        for item in ctx.items():
            if item[0].name == "genesis":
                item[1].append(self)


class Name(ast.Name, Value):
    def __init__(self, id: str):
        ast.Name.__init__(self, id=id)
        Value.__init__(self)


class Constant(ast.Constant, Value):
    def __init__(self, value: Any):
        ast.Constant.__init__(self, value=value)
        Value.__init__(self)


class Call(ast.Call, Value):
    def __init__(self, func: Value):
        ast.Call.__init__(self, func=func, args=[], keywords=[])
        Value.__init__(self)

    def add_arg(self, arg: Value):
        self.args.append(arg)
        return self

    def add_kwarg(self, arg: str, value: Value):
        self.keywords.append(ast.keyword(arg, value))
        return self


class Subscript(ast.Subscript, Value):
    def __init__(self, value: Value, slice: Value):
        ast.Subscript.__init__(self, value=value, slice=slice)
        Value.__init__(self)


class Slice(ast.Slice, Value):
    def __init__(self, value: Value, lower: Value, upper: Value, step: Value):
        ast.Slice.__init__(self, lower, upper, step)
        Value.__init__(self)


class Attribute(ast.Attribute, Value):
    def __init__(self, value: Value, attr: str):
        ast.Attribute.__init__(self, value=value, attr=attr)
        Value.__init__(self)


class IfExp(ast.IfExp, Value):
    def __init__(self, body: Value, test: Value, orelse: Value):
        ast.IfExp.__init__(self, test, body, orelse)
        Value.__init__(self)
