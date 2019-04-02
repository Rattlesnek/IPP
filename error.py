

ERR_PARAM = 10      # script parameter is missing or use of invalid combination
ERR_INFILE = 11     # error during input file opening
ERR_OUTFILE = 12    # error during output file opening


ERR_XML_FORMAT = 31 # invalid XML format of source file
ERR_XML_STRUCT = 32 # unexpected structure XML or lexical / syntactic error of elements
                    # and attributes in source file

ERR_SEMANTIC = 52   # semantic error of code (eg. not defined label)

# RUNTIME ERRORS
ERR_OPERAND_TYPE = 53   # invalid types of operands
ERR_DEF_VAR = 54        # access to variable not defined (frame exists)
ERR_FRAME = 55          # frame does not exist
ERR_MISS_VAL = 56       # missing value (variable, data stack, call stack)
ERR_OPERAND_VAL = 57    # invalid value of operand (zero division, EXIT instruction)
ERR_STRING = 58         # wrong string manipulation


ERR_INTER = 99      # internal error


# 31
class XMLFormatError_31(Exception): pass # 31 intermachine.py

# 32
class XMLStructError_32(Exception): pass # 32 intermachine.py
class OrderError_32(XMLStructError_32): pass # 32 intermachine.py
class InstructionError_32(XMLStructError_32): pass # 32 instruc.py
class ArgumentError_32(XMLStructError_32): pass # 32 structure.py
class StructureError_32(XMLStructError_32): pass # 32 structure.py

# 52
class SemanticError_52(Exception): pass # 52
class LabelError_52(SemanticError_52): pass # 52

# 53
class OperandTypeError_53(Exception): pass # 53

# 54
class VarDefineError_54(Exception): pass # 54

# 55
class FrameError_55(Exception): pass # 55

# 56
class MissingValueError_56(Exception): pass # 56
class CallStackError_56(MissingValueError_56): pass # 56
class DataStackError_56(MissingValueError_56): pass # 56
class VariableMissingValueError_56(MissingValueError_56): pass # 56

# 57
class OperandValueError_57(Exception): pass # 57
class InterpretZeroDivError_57(OperandValueError_57): pass # 57

# 58
class StringError_58(Exception): pass # 58






