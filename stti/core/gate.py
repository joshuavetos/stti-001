import dis
from typing import Callable

class PurityGate:
    """
    STTI-001 Bytecode Purity Gate.
    Analyzes function structures for closure leaks and unauthorized opcodes.
    """
    FORBIDDEN_OPS = {
        'LOAD_GLOBAL', 
        'STORE_GLOBAL', 
        'LOAD_DEREF', 
        'STORE_DEREF', 
        'IMPORT_NAME', 
        'IMPORT_FROM'
    }
    
    FORBIDDEN_DUNDERS = {
        '__subclasses__', 
        '__globals__', 
        '__builtins__', 
        '__mro__', 
        '__class__', 
        '__reduce__', 
        '__reduce_ex__'
    }

    @classmethod
    def verify(cls, fn: Callable):
        code = fn.__code__

        # 1. Closure Check: Ensure no variables are captured from outer scopes
        if code.co_freevars:
            raise SecurityError(f"STTI Violation: Unauthorized closure variables: {code.co_freevars}")

        # 2. Name Scan: Check co_names for forbidden dunder attributes
        for name in code.co_names:
            if name in cls.FORBIDDEN_DUNDERS:
                raise SecurityError(f"STTI Violation: Forbidden attribute access: {name}")

        # 3. Opcode Scan: Check for forbidden global/deref/import instructions
        for instr in dis.get_instructions(fn):
            if instr.opname in cls.FORBIDDEN_OPS:
                raise SecurityError(f"STTI Violation: Forbidden Opcode {instr.opname}")

        return True

class SecurityError(Exception):
    pass
