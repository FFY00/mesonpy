# SPDX-FileCopyrightText: 2023 The meson-python developers
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import ast
import operator
import string
import sys
import typing


if typing.TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Callable, Iterator, Mapping, Optional, Type


_methods = {}


def _register(nodetype: Type[ast.AST]) -> Callable[..., Callable[..., Any]]:
    def closure(method: Callable[[Interpreter, ast.AST], Any]) -> Callable[[Interpreter, ast.AST], Any]:
        _methods[nodetype] = method
        return method
    return closure


class Interpreter(typing.Mapping[str, object]):

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
    }

    def __init__(self, variables: Mapping[str, Any]):
        self._variables = variables

    def eval(self, string: str) -> Any:
        try:
            expr = ast.parse(string, mode='eval')
            return self._eval(expr)
        except KeyError as exc:
            raise ValueError(f'unknown variable "{exc.args[0]}"') from exc
        except NotImplementedError as exc:
            raise ValueError(f'invalid expression {string!r}') from exc

    __getitem__ = eval

    def __len__(self) -> int:
        return len(self._variables)

    def __iter__(self) -> Iterator[str]:
        return iter(self._variables)

    def _eval(self, node: ast.AST) -> Any:
        # Cannot use functools.singlemethoddispatch as long as Python 3.7 is supported.
        method = _methods.get(type(node), None)
        if method is None:
            raise NotImplementedError
        return method(self, node)

    @_register(ast.Expression)
    def _expression(self, node: ast.Expression) -> Any:
        return self._eval(node.body)

    @_register(ast.BinOp)
    def _binop(self, node: ast.BinOp) -> Any:
        func = self._operators.get(type(node.op))
        if func is None:
            raise NotImplementedError
        return func(self._eval(node.left), self._eval(node.right))

    @_register(ast.Constant)
    def _constant(self, node: ast.Constant) -> Any:
        return node.value

    if sys.version_info < (3, 8):

        # Python 3.7, replaced by ast.Constant is later versions.
        @_register(ast.Num)
        def _num(self, node: ast.Num) -> Any:
            return node.n

        # Python 3.7, replaced by ast.Constant is later versions.
        @_register(ast.Str)
        def _str(self, node: ast.Str) -> Any:
            return node.s

    @_register(ast.Name)
    def _variable(self, node: ast.Name) -> Any:
        value = self._variables[node.id]
        if callable(value):
            value = value()
        return value


def _ncores() -> int:
    return 42


class Template(string.Template):
    braceidpattern = r'[^}]+'


def eval(template: str, variables: Optional[Mapping[str, Any]] = None) -> str:
    if variables is None:
        variables = {'ncores': _ncores}
    return Template(template).substitute(Interpreter(variables))
