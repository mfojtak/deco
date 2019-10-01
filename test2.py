import numpy as np
from typing import Generic, TypeVar, Tuple
from typing_extensions import Literal, Protocol

T = TypeVar("T", bound=tuple, covariant=True)

class Tensor(Protocol[T]):
    shape: tuple
    def __add__(self, other) -> "Tensor":
        ...

L = Literal
def t(par: Tensor[L[1,2]]):
    return par

ret = t(np.array([1,2,3]))
print(ret)

A = TypeVar('A')
B = TypeVar('B', bound=int)
C = TypeVar('C', bound=tuple)

class Gen(Generic[A,C]):
    def __init__(self):
        pass

#L = Literal
#T = TypeVar('T', covariant=True)
#S = TypeVar('S', bound=int, covariant=True)
#class StaticTensor(Tensor, Protocol[T,S]):
#    ...

g: Gen[int,L[1,2]] = Gen[int,L[1,2]]()

ten1: Tensor[L[1,2]] = np.array([1, 2, 3, 4])
#ten2 = ten1 + 1

s="ssf"
a=1
b=2
c = (a + 1) + 5
if True:
    d: int = 56
    c: int = c + 5
else:
    e = c + 4

def f(a: int):
    return a

print(g)