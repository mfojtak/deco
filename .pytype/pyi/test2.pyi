# (generated with --quick)

import typing
from typing import Any, Generic, Type, TypeVar

L: Type[typing.Literal]
Literal: Type[typing.Literal]
Protocol: Type[typing.Protocol]
a: int
b: int
c: int
d: int
g: Any
np: module
s: str

A = TypeVar('A')
B = TypeVar('B', bound=int)
C = TypeVar('C', bound=tuple)
T = TypeVar('T', bound=tuple)

class Gen(Generic[A, C]):
    def __init__(self: Gen[nothing, nothing]) -> None: ...

def f(a: int) -> int: ...
