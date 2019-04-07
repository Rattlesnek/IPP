"""
    Interpreter of IPPcode19 - FIT VUT
    
    File:   error.py
    
    Author: Adam Pankuch
    
    Login:  xpanku00
    
    Date:   7.4.2019
"""
import sys


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

ERR_INTER = 99  # internal error


# 31
class XMLFormatError_31(Exception): pass 

# 32
class XMLStructError_32(Exception): pass 
class OrderError_32(XMLStructError_32): pass 
class InstructionError_32(XMLStructError_32): pass
class ArgumentError_32(XMLStructError_32): pass
class StructureError_32(XMLStructError_32): pass

# 52
class SemanticError_52(Exception): pass
class LabelError_52(SemanticError_52): pass

# 53
class OperandTypeError_53(Exception): pass

# 54
class VarDefineError_54(Exception): pass

# 55
class FrameError_55(Exception): pass

# 56
class MissingValueError_56(Exception): pass
class CallStackError_56(MissingValueError_56): pass
class DataStackError_56(MissingValueError_56): pass
class VariableMissingValueError_56(MissingValueError_56): pass

# 57
class OperandValueError_57(Exception): pass
class InterpretZeroDivError_57(OperandValueError_57): pass

# 58
class StringError_58(Exception): pass



def err_exit(text, err, return_value):
    """ Prints text to sys.stderr and exits from program with return_value """
    print('ERROR:', text, err, file=sys.stderr)
    sys.exit(return_value)

