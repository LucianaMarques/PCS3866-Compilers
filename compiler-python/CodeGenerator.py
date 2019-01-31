'''
Part of the code in this file was highly based on llvmlite's docs!
Reference for PRINT function: https://gist.github.com/alendit/defe3d518cd8f3f3e28cb46708d4c9d6
'''

import llvmlite.ir as ir
import llvmlite.binding as llvm
import llvmlite.llvmpy
from ctypes import CFUNCTYPE

# necessary to code generation
llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter() 

def create_execution_engine():
    """
    Create an ExecutionEngine suitable for JIT code generation on
    the host CPU.  The engine is reusable for an arbitrary number of
    modules.
    """
    # Create a target machine representing the host
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine

def compile_ir(engine, llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """
    # Create a LLVM module object from the IR
    mod = llvm.parse_assembly(llvm_ir)
    mod.verify()
    # Now add the module and make sure it is ready for execution
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()
    return mod

'''
TO COMPILE

from __future__ import print_function

from ctypes import CFUNCTYPE, c_double

llvm_ir = """
   ; ModuleID = "examples/ir_fpadd.py"
   target triple = "unknown-unknown-unknown"
   target datalayout = ""

   define double @"fpadd"(double %".1", double %".2")
   {
   entry:
     %"res" = fadd double %".1", %".2"
     ret double %"res"
   }
   """
engine = create_execution_engine()
mod = compile_ir(engine, llvm_ir)

# Look up the function pointer (a Python int)
func_ptr = engine.get_function_address("fpadd")

# Run the function via ctypes
cfunc = CFUNCTYPE(c_double, c_double, c_double)(func_ptr)
res = cfunc(1.0, 3.5)
print("fpadd(...) =", res)
'''

# variable type definitions
int = ir.IntType(32);
double = ir.DoubleType()

# function type definitions
fnty = ir.FunctionType(double, [double])

#function types definitions
#fn_int_to_int_type = ir.FunctionType(int_type, [int_type])
# void types, used in: PRINT
# fn_voidty = ir.FunctionType(ir.VoidType(), [])
# fn_voidptr = ir.IntType(8).as_pointer()

# known function definition
# PRINT
# printf_ty = ir.FunctionType(int, [voidptr_ty], var_arg=True)
# printf_ty = ir.FunctionType(int, fn_void, var_arg=True)
# printf = ir.Function(m, printf_ty, name="printf")
# print_block = printf.append_basic_block(name="print_identifier")

class CodeGenerator:
    def __init__ (self):
        self.module = ir.Module()
        # tabela de símbolos de variáveis
        self.global_variables = {}
        # tabela de símbolos de funções definidas
        # por usuários
        self.user_functions = {}

        # Debugging purposes:
        self.print_module()

    # for debug purposes
    def print_module(self):
        print(self.module)

    # adds a variable to the symbol table
    def generate_global_variable(self, name, value):
        glob = ir.GlobalVariable(self.module, int, name)
        glob.initializer = ir.Constant(int,value)
        self.global_variables[name] = glob

    # adds a programmer-defined function
    def generate_user_function(self, func_name):
        # append generic block with func_name
        fnty = ir.FunctionType(double, [double])
        func = ir.Function(self.module, fnty, name = func_name)
        block_name = func_name + "_block"
        block_func = func.append_basic_block(name=block_name)
        builder = ir.IRBuilder(func.append_basic_block(block_func))
        x = func.arg
        
    
    def printf_id(self, name):
        func_ty = ir.FunctionType(ir.VoidType(), [])
        i32_ty = ir.IntType(32)
        func = ir.Function(self.module, func_ty, name="printer")

        voidptr_ty = ir.IntType(8).as_pointer()

        fmt = "%s%i\n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        arg = "\0"
        c_str_val = ir.Constant(ir.ArrayType(ir.IntType(8), len(arg)),bytearray(arg.encode("utf8")))

        printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name="printf")

        builder = ir.IRBuilder(func.append_basic_block('entry'))
        
        c_str = builder.alloca(c_str_val.type)
        builder.store(c_str_val, c_str)

        # this val can come from anywhere
        int_val = self.global_variables[name].initializer

        fmt_arg = builder.bitcast(global_fmt, voidptr_ty)
        builder.call(printf, [fmt_arg, c_str, int_val])
        builder.ret_void()

        llvm_ir = str(self.module)
        engine = create_execution_engine()
        print(self.module)
        mod = compile_ir(engine, llvm_ir)
        # Look up the function pointer (a Python int)
        func_ptr = engine.get_function_address("printer")
        # Run the function via ctypes
        cfunc = CFUNCTYPE(None)(func_ptr)
        cfunc()

    # Generate Predef functions - all functions are suposed double type
    def sin(self,a):
        # SIN
        sin = ir.Function(self.module, fnty, "llvm.sin.f64")
        builder = ir.IRBuilder(sin.append_basic_block('sin_block'))
        a = sin.args
        result = builder.call(sin, a, name = "")
        builder.ret(result)

    def cos(self,a):
        # COS
        cos = ir.Function(self.module, fnty, "llvm.cos.f64")
        builder = ir.IRBuilder(cos.append_basic_block('block_cos'))
        a = cos.args
        result = builder.call(sin, a, name = "")
        builder.ret(result)

    def tan(self,a):
        # TAN   
        tan = ir.Function(self.module, fnty, name = "tan_func")
        builder = ir.IRBuilder(tan.append_basic_block('block_tan'))
        a = tan.args
        result1 = builder.call(sin, a, name = "")
        result2 = builder.call(cos, a, name = "")
        #result3 = builder.udiv(result1, result2, name ="")
        builder.ret(result2)

    def exp(self,a):
        # EXP
        exp = ir.Function(self.module, fnty, name="llvm.exp.f64")
        builder = ir.IRBuilder(exp.append_basic_block('block_exp'))
        a = exp.args
        result = builder.call(exp, a, name = "")
        builder.ret(result)

    def abs(self,a):
        # ABS
        abs = ir.Function(self.module, fnty, name="llvm.fabs.f64")
        builder = ir.IRBuilder(abs.append_basic_block('block_abs'))
        a = abs.args
        result = builder.call(abs, a, name = "")
        builder.ret(result)

    def log(self,a):
        # LOG
        log = ir.Function(self.module, fnty, name="llvm.log.f64")
        builder = ir.IRBuilder(log.append_basic_block('block_log'))
        a = log.args
        result = builder.call(log, a, name = "")
        builder.ret(result)

    def sqr(self,a):
        # SQR
        sqr = ir.Function(self.module, fnty, name="llvm.sqrt.f64")
        builder = ir.IRBuilder(sqr.append_basic_block('block_sqr'))
        a = sqr.args
        result = builder.call(sqr, a, name = "")
        builder.ret(result)

        # # INT
        # int_func = ir.Function(module, fnty, name="int_func")
        # block_int_func = sin.append_basic_block(name="int_fun
        #block_sqr = sqr.append_basic_block(name="sqr_block")c_block"
        # a = int_func.args
        # # aproxima seno por serie de taylor
        # a2 = builder.fadd() 
        # result = a
        # builder.ret(result)

        # # RND
        # rnd = ir.Function(module, fnty, name="rnd")
        # block_rnd = sin.append_basic_block(name="rnd_block")
        # a = rnd.args
        # # aproxima seno por serie de taylor
        # a2 = builder.fadd() 
        # result = a
        # builder.ret(result)

    def generate_code(self):
        self.print_module()
        print("END")