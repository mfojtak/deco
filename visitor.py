import mlir_bindings as M
from typed_ast import ast3
from copy import copy, deepcopy
import sys
from pytype.tools.annotate_ast import annotate_ast
from pytype.tools import debug
from pytype import config
import inspect
import numpy as np

class VisitorComplete(ast3.NodeVisitor):

    def visit_Num(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Str(self, node):
        print(node)
        self.generic_visit(node)

    def visit_FormattedValue(self, node):
        print(node)
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Bytes(self, node):
        print(node)
        self.generic_visit(node)

    def visit_List(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Tuple(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Set(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Dict(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Ellipsis(self, node):
        print(node)
        self.generic_visit(node)

    def visit_NameConstant(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Name(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Load(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Store(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Del(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Starred(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Expr(self, node):
        print(node)
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_UAdd(self, node):
        print(node)
        self.generic_visit(node)

    def visit_USub(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Not(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Invert(self, node):
        print(node)
        self.generic_visit(node)

    def visit_BinOp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Add(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Sub(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Mult(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Div(self, node):
        print(node)
        self.generic_visit(node)

    def visit_FloorDiv(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Mod(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Pow(self, node):
        print(node)
        self.generic_visit(node)

    def visit_LShift(self, node):
        print(node)
        self.generic_visit(node)

    def visit_RShift(self, node):
        print(node)
        self.generic_visit(node)

    def visit_BitOr(self, node):
        print(node)
        self.generic_visit(node)

    def visit_BitXor(self, node):
        print(node)
        self.generic_visit(node)

    def visit_BitAnd(self, node):
        print(node)
        self.generic_visit(node)

    def visit_MatMult(self, node):
        print(node)
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_And(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Or(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Compare(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Eq(self, node):
        print(node)
        self.generic_visit(node)

    def visit_NotEq(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Lt(self, node):
        print(node)
        self.generic_visit(node)

    def visit_LtE(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Gt(self, node):
        print(node)
        self.generic_visit(node)

    def visit_GtE(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Is(self, node):
        print(node)
        self.generic_visit(node)

    def visit_IsNot(self, node):
        print(node)
        self.generic_visit(node)

    def visit_In(self, node):
        print(node)
        self.generic_visit(node)

    def visit_NotIn(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Call(self, node):
        print(node)
        self.generic_visit(node)

    def visit_keyword(self, node):
        print(node)
        self.generic_visit(node)

    def visit_IfExp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Subscript(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Index(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Slice(self, node):
        print(node)
        self.generic_visit(node)

    def visit_ExtSlice(self, node):
        print(node)
        self.generic_visit(node)

    def visit_ListComp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_SetComp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_DictComp(self, node):
        print(node)
        self.generic_visit(node)

    def visit_comprehension(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Assign(self, node):
        print(node)
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        print(node)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Print(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Raise(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Assert(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Delete(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Pass(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Import(self, node):
        print(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        print(node)
        self.generic_visit(node)

    def visit_alias(self, node):
        print(node)
        self.generic_visit(node)

    def visit_If(self, node):
        print(node)
        self.generic_visit(node)

    def visit_For(self, node):
        print(node)
        self.generic_visit(node)

    def visit_While(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Break(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Continue(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Try(self, node):
        print(node)
        self.generic_visit(node)

    def visit_TryFinally(self, node):
        print(node)
        self.generic_visit(node)

    def visit_TryExcept(self, node):
        print(node)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        print(node)
        self.generic_visit(node)

    def visit_With(self, node):
        print(node)
        self.generic_visit(node)

    def visit_withitem(self, node):
        print(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Lambda(self, node):
        print(node)
        self.generic_visit(node)

    def visit_arguments(self, node):
        print(node)
        self.generic_visit(node)

    def visit_arg(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Return(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Yield(self, node):
        print(node)
        self.generic_visit(node)

    def visit_YieldFrom(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Global(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Nonlocal(self, node):
        print(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        print(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        print(node)
        self.generic_visit(node)

    def visit_Await(self, node):
        print(node)
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        print(node)
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        print(node)
        self.generic_visit(node)


class Var:
    def __init__(self):
        self.name = ""
        self.arg_index = -1
        self.is_arg = False
        self.type = None
        self.m = None
    def __deepcopy__(self, memo):
        new_var = Var()
        new_var.name = self.name
        new_var.arg_index = self.arg_index
        new_var.is_arg = self.is_arg
        new_var.m = self.m
        return new_var

class Context:
        def __init__(self):
            self.args = {}
            self.vars = {}
        def get_var_types(self):
            return [item.type for item in self.vars.values()]
        def get_arg_types(self):
            return [item.type for item in self.args.values()]
        def get_var_values(self):
            return [item.m for item in self.vars.values()]
        def get_arg_values(self):
            return [item.m for item in self.args.values()]
        def get_var(self, name):
            if name in self.args:
                return self.args[name]
            if name in self.vars:
                return self.vars[name]
            return None
        def __deepcopy__(self, memo):
            new_ctx = Context()
            new_ctx.args = self.args
            new_ctx.vars = deepcopy(self.vars)
            return new_ctx


class Type:
    def __init__(self, name):
        self.name = name
        self.elements = []

class TypeVisitor(ast3.NodeTransformer):
    def visit_Name(self, node):
        t = Type(name = node.id)
        return t
    def visit_Subscript(self, node):
        t = self.visit(node.value)
        t.elements = self.visit(node.slice)
        return t
    def visit_Index(self, node):
        return self.visit(node.value)
    def visit_Tuple(self, node):
        return [self.visit(e) for e in node.elts]
    def visit_Num(self, node):
        return node.n

    
class Function:
    def __init__(self, name=None, m=None, return_type=None):
        self.name = name
        self.m = m
        self.return_type = return_type

class Expr(ast3.NodeTransformer):
    def __init__(self):
        self.module = M.MLIRModule()
        self.float_type =  self.module.make_scalar_type("f32")
        self.int_type = self.module.make_scalar_type("i", 32)
        self.bool_type = self.module.make_scalar_type("i", 1)
        self.index_type = self.module.make_index_type()
        self.typemap = {
            "float": self.float_type,
            "int": self.int_type,
            "bool": self.bool_type,
            "index": self.index_type
        }
        self.funcmap = {}
    
    def get_function(self, name):
        if name not in self.funcmap:
            if name == "math.sqrt":
                m = self.module.declare_function("sqrtf", [self.typemap["float"]],
                                          [self.typemap["float"]])
                self.funcmap[name] = Function(name, m, Type("float"))

        f = self.funcmap[name]
        return f

    def get_mlir_type(self, t: Type):
        if t.name in self.typemap:
            return self.typemap[t.name]
        elif t.name == "Tensor":
            base_type = self.get_mlir_type(t.elements[0])
            shape = t.elements[1].elements
            return self.module.make_memref_type(base_type, shape)

    def visit_FunctionDef(self, node):
        ctx = Context()
        node.args.context = ctx
        self.visit_arguments(node.args)
        ret_type = Type(node.returns.id)
        outputtypes = [self.get_mlir_type(ret_type)]

        argtypes = [self.get_mlir_type(t) for t in ctx.get_arg_types()]

        with self.module.function_context(node.name, argtypes, outputtypes) as fun_m:
            for arg in ctx.args.values():
                arg.m = fun_m.arg(arg.arg_index)
          
            current_block = []
            cond = None
            for item in node.body:
                if cond:
                    cond.next_block.append(item)
                else:
                    current_block.append(item)
                if isinstance(item, ast3.If):
                    item.next_block = []
                    cond = item
            
            for item in current_block:
                item.context = ctx
                self.visit(item)

        self.funcmap[node.name] = Function(node.name, fun_m, ret_type)
    
    def visit_arguments(self, node):
        ctx = node.context
        for i, arg in enumerate(node.args):
            arg.context = ctx
            var = self.visit(arg)
            var.arg_index = i
            ctx.args[var.name] = var
    
    def visit_arg(self, node):
        var = Var()
        var.name = node.arg
        tv = TypeVisitor()
        t = tv.visit(node.annotation)
        var.type = t
        var.is_arg = True
        return var
    
    def visit_Name(self, node):
        ctx = node.context
        var = ctx.get_var(node.id)
        if var:
            return var
        func = self.get_function(node.id)
        return func
    
    def visit_Attribute(self, node):
        name = "{}.{}".format(node.value.id, node.attr)
        ctx = node.context
        var = ctx.get_var(name)
        if var:
            return var.m
        func = self.get_function(name)
        return func

    def visit_Num(self, node):
        var = Var()
        if isinstance(node.n, int):
            var.m = M.constant_int(node.n, 32)
            var.type = Type(name = "int")
        else:
            if isinstance(node.n, float):
                var.m = M.constant_float(node.n, self.float_type)
                var.type = Type(name="float")
        return var
    
    def visit_BinOp(self, node):
        ctx = node.context
        node.left.context = ctx
        node.right.context = ctx
        var = Var()
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(node.op, ast3.Add):
            l = left.m
            r = right.m
            if left.type.name == "float" and right.type.name != "float":
                r = M.op("std.sitofp", [right.m], [self.float_type])
            if left.type.name != "float" and right.type.name == "float":
                l = M.op("std.sitofp", [left.m], [self.float_type])
            if left.type.name == "int" and right.type.name == "index":
                r = M.op("std.index_cast", [right.m], [self.int_type])
            if left.type.name == "index" and right.type.name == "int":
                l = M.op("std.index_cast", [left.m], [self.int_type])
            var.m = l + r
            var.type = left.type
        if isinstance(node.op, ast3.Sub):
            return left.m - right.m
        if isinstance(node.op, ast3.Mult):
            return left.m * right.m
        if isinstance(node.op, ast3.Div):
            return left.m / right.m
        if isinstance(node.op, ast3.FloorDiv):
            return left.m // right.m
        if isinstance(node.op, ast3.Mod):
            return left.m & right.m
        return var
    
    
    def visit_AnnAssign(self, node):
        ctx = node.context
        node.value.context = ctx
        var = self.visit(node.value)
        var.name = node.target.id
        t = Type()
        t.name = node.annotation.id
        var.type = t
        ctx.vars[var.name] = var
    
    def visit_Assign(self, node):
        ctx = node.context
        node.value.context = ctx
        var = self.visit(node.value)
        var.name = node.targets[0].id
        var.type = Type(name=node.targets[0].resolved_annotation)
        ctx.vars[var.name] = var
     
    def visit_If(self, node):
        ctx = node.context
        node.test.vars = ctx
        test = self.visit(node.test)
        types = ctx.get_var_types()
        with M.BlockContext(types) as next_block:
            local_ctx = deepcopy(ctx)
            for i, item in enumerate(local_ctx.vars.values()):
                item.m = next_block.arg(i)
            for item in node.next_block:
                item.context = local_ctx
                self.visit(item)
        with M.BlockContext() as true_block:
            local_ctx = deepcopy(ctx)
            for item in node.body:
                item.context = local_ctx
                self.visit(item)
            vals = local_ctx.get_var_values()
            M.br(next_block, vals[0:len(types)])
        with M.BlockContext() as false_block:
            local_ctx = deepcopy(ctx)
            for item in node.orelse:
                item.context = local_ctx
                self.visit(item)
            vals = local_ctx.get_var_values()
            M.br(next_block, vals[0:len(types)])
        M.cond_br(test, true_block, [], false_block, [])

    def visit_NameConstant(self, node):
        var = Var()
        if node.value == True:
            var.m = M.constant_int(1, 1)
        if node.value == False:
            var.m = M.constant_int(0, 1)
        t = Type()
        t.name = "bool"
        var.type = t
        return var
    
    def visit_Return(self, node):
        ctx = node.context
        node.value.context = ctx
        val = self.visit(node.value)
        m_returns = []
        m_returns.append(val.m)
        M.ret(m_returns)
    
    def visit_For(self, node):
        ctx = node.context
        node.iter.args[0].context = ctx
        if len(node.iter.args) == 1:
            end = self.visit(node.iter.args[0])
            start = M.constant_int(0, 32)
        if len(node.iter.args) == 2:
            node.iter.args[1].context = ctx
            start = self.visit(node.iter.args[0])
            end = self.visit(node.iter.args[1])
        s = start.m
        e = end.m
        if start.type.name != "index":
                s = M.op("std.index_cast", [start.m], [self.index_type])
        if end.type.name != "index":
                e = M.op("std.index_cast", [end.m], [self.index_type])
        var = Var()
        var.name = node.target.id
        var.type = Type(name="index")
        with M.LoopContext(s, e, 1) as i:
            local_ctx = deepcopy(ctx)
            var.m = i
            local_ctx.vars[var.name] = var
            for item in node.body:
                item.context = local_ctx
                self.visit(item)
    
    def visit_Call(self, node):
        ctx = node.context
        node.func.context = ctx
        func = self.visit(node.func)
        args = []
        for arg in node.args:
            arg.context = ctx
            arg_var = self.visit(arg)
            args.append(arg_var.m)
        var = Var()
        var.type = func.return_type
        funCst = M.constant_function(func.m)
        var.m = funCst(args)
        return var
    
    def visit_Subscript(self, node):
        ctx = node.context
        node.value.context = ctx
        var = self.visit(node.value)
        ind = []
        for el in node.slice.value.elts:
            el.context = ctx
            ind_var = self.visit(el)
            m = ind_var.m
            if ind_var.type.name != "index":
                m = M.op("std.index_cast", [ind_var.m], [self.index_type])
            ind.append(m)
        A = M.IndexedValue(var.m)
        var = Var()
        var.m = A.load(ind)
        return var

SOURCE = """
#import math
def f(a: float) -> float:
    b = 1
    return a
def add(a: int, b: int, tt: Tensor[int, L[20,20]]) -> int:
    uu = tt[0,0]
    e = f(6.1) + 1
    g = math.sqrt(5.1)
    for i in range(0,10):
        v = 1 + i
    #c = a + 1 + 5
    #if True:
    #    c = c + 5
    #r = 5
    #c = 1 + 1.1
    return a
"""


if __name__ == "__main__":
    root = ast3.parse(SOURCE)
    options = config.Options.create(python_version=(3,7))
    ast_factory = lambda unused_options: ast3
    module = annotate_ast.annotate_source(SOURCE, ast_factory, options)
    print(ast3.dump(root))
    visitor = Expr()
    visitor.visit(module)
    print(str(visitor.module))
    visitor.module.compile()
    print(visitor.module.get_ir())
