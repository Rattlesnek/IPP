"""
    Interpreter of IPPcode19 - FIT VUT
    
    File:   interpret.py
    
    Author: Adam Pankuch
    
    Login:  xpanku00
    
    Date:   7.4.2019
"""
import sys
import os.path
import argparse
import intermachine
import instruc
import error


def main(src, inp):
    """ MAIN FUNCTION - parse XML program and then interpret the program """
    try:
        # run parsing of program
        parser = intermachine.Parser(src)
        program = parser.parse_XML(debug=False)

    except error.XMLFormatError_31 as err:
        error.err_exit('XML Format Error', err, error.ERR_XML_FORMAT)
    except error.XMLStructError_32 as err:
        error.err_exit('XML Struct Error', err, error.ERR_XML_STRUCT)
    except error.SemanticError_52 as err:
        error.err_exit('XML Semantic Error', err, error.ERR_SEMANTIC)
    
    try:
        # run interpretation of program
        interpreter = intermachine.Interpreter(program)
        interpreter.interpret(inp)

    except error.XMLStructError_32 as err:
        error.err_exit('XML Struct Error', err, error.ERR_XML_STRUCT)  
    except error.SemanticError_52 as err:
        error.err_exit('XML Semantic Error', err, error.ERR_SEMANTIC)
    except error.OperandTypeError_53 as err:
        error.err_exit('invalid type of operand', err, error.ERR_OPERAND_TYPE)
    except error.VarDefineError_54 as err:
        error.err_exit('variable does not exist', err, error.ERR_DEF_VAR)
    except error.FrameError_55 as err:
        error.err_exit('frame does not exist', err, error.ERR_FRAME)
    except error.MissingValueError_56 as err:
        error.err_exit('missing value', err, error.ERR_MISS_VAL)
    except error.OperandValueError_57 as err:
        error.err_exit('invalud value of operand', err, error.ERR_OPERAND_VAL)
    except error.StringError_58 as err:
        error.err_exit('invalid string operation', err, error.ERR_STRING)

    except instruc.ExitInterpret as return_value:
        sys.exit(int(str(return_value)))
            
    
if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='file with XML representation of source code')
    parser.add_argument('--input', help='file with inputs for interpretation')
    args = parser.parse_args()
    
    if not (args.source or args.input):
        print('ERROR: Need to specify at least one of the arguments: --source / --input', file=sys.stderr)
        sys.exit(error.ERR_PARAM)

    source, inputt = None, None 
    if args.source:
        source = os.path.realpath(args.source)
    if args.input:
        inputt = os.path.realpath(args.input)
    
    # call MAIN FUNCTION with correct parameters according to the arguments
    try:
        if source and inputt:
            with open(source) as src, open(inputt) as inp:
                main(src, inp)
        elif source:
            with open(source) as src:
                main(src, sys.stdin)
        elif inputt:
            with open(inputt) as inp:
                main(sys.stdin, inp)
    except FileNotFoundError as err:
        print('ERROR:', err, file=sys.stderr)
        sys.exit(error.ERR_INFILE)
    
    
