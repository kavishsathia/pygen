import ast
from collections import deque
from typing import Union, Optional, Any
import contextvars

from pygen.Block import Else


def macro(func):
    def macro_wrapper(*args, **kwargs):
        exec(str(func(*args, **kwargs)))
    return macro_wrapper


class Module(ast.Module):
    def __init__(self):
        super().__init__([], [])
        self._stack = deque()
        self._stack.append(self)
        self.ctx = contextvars.ContextVar("genesis")
        self.token = None

    def append(self, tree):
        if type(tree) is not Else:
            self._stack[-1].body.append(tree)
        else:
            self._stack[-1].body[-1].orelse.append(tree)

    def __enter__(self):
        self.token = self.ctx.set(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ctx.reset(self.token)

    def append_context(self, tree):
        self._stack.append(tree)

    def pop_context(self):
        self._stack.pop()

    def __str__(self):
        ast.fix_missing_locations(self._stack[0])
        return ast.unparse(self._stack[0])
