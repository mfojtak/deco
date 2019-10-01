import deco
import asyncio
import sys
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import contextlib
import collections
import keras_bert
from deco.sources import Dataset
import math
import timeit
import time
from typing import Iterable, TypeVar, Generic
from numba import jit, jitclass
import inspect, ast
import mlir_bindings
from typed_ast import ast3
import struct
from typing_extensions import Literal

from pytype.tools.annotate_ast import annotate_ast
from pytype.tools import debug
from pytype import config

def printWithCurrentFunctionName(str):
  print(inspect.stack()[1][3])
  print(str)

module = mlir_bindings.MLIRModule()
boolType = module.make_scalar_type("i", 1)
i32Type = module.make_scalar_type("i", 32)
f32Type = module.make_scalar_type("f32")
indexType = module.make_index_type()

callee = module.declare_function("sqrtf", [f32Type],
                                          [f32Type])
with module.function_context("call", [f32Type], [f32Type]) as fun:
    funCst = mlir_bindings.constant_function(callee)
    f42 = funCst([fun.arg(0)]) + mlir_bindings.constant_float(42., f32Type)
    mlir_bindings.ret([f42])
module.compile()

a = mlir_bindings.Float(64)
b = mlir_bindings.Float()

ba = bytearray(struct.pack("f", 100)) 
baa = memoryview(a)

module.invoke("call", [baa,b])
print(a.value, b.value)
print(module.get_ir())


A = TypeVar('A')
B = TypeVar('B', bound=int)
C = TypeVar('C', bound=tuple)

class Gen(Generic[A,B,C]):
    def __init__(self):
        pass

g: Gen[int, Literal[2], Literal[(1,2)]] = Gen[int, Literal[2], Literal[(1,2)]]()

class Int:
    def __init__(self, val: int):
        self.val: int = val

def add(a: int, b: int, c: Gen[int, Literal[2], Literal[(1,2)]]):
    rr=a
    return a + b + 2


src = inspect.getsource(add)
sig = inspect.signature(add)
v = inspect.getclosurevars(add)
#print(v)
#print(src)
#print(sig.parameters)
source = """
class Gen(Generic[A,C]):
    def __init__(self):
        pass
L = Literal
g = Gen[int,L[1,2]]()
"""
root = ast3.parse(src)
options = config.Options.create(python_version=(3,7))
ast_factory = lambda unused_options: ast3
module2 = annotate_ast.annotate_source(source, ast_factory, options)
#print(ast3.dump(root))
print(debug.dump(module2, ast3))
print(module2.body[2].targets[0].__dict__)