import sys
import os.path
import argparse
import intermachine


ERR_PARAM = 10
ERR_INFILE = 11
ERR_OUTFILE = 12
ERR_XML_FORMAT = 31
ERR_XML_STRUCT = 32

ERR_SEMANTIC = 52
ERR_TYPE = 53
ERR_UNDEF_VAR = 54
ERR_NO_FRAME = 55
ERR_MISS_VAL = 56
ERR_OPERAND_VAL = 57
ERR_STRING = 58

ERR_INTER = 99 




def main(src, inp):

    parser = intermachine.Parser(src)
    program = parser.parse_XML(debug=True)

    print(program.labels)

    interpreter = intermachine.Interpreter(program)
    interpreter.interpret(inp)
            
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='file with XML representation of source code')
    parser.add_argument('--input', help='file with inputs for interpretation')
    args = parser.parse_args()
    
    if not (args.source or args.input):
        print('ERROR: Need to specify at least one of the arguments: --source / --input')
        sys.exit(ERR_PARAM)

    source, inputt = None, None 
    if args.source:
        source = os.path.realpath(args.source)
    if args.input:
        inputt = os.path.realpath(args.input)
    
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
        sys.exit(ERR_INFILE)
    
    
