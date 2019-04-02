import sys
import structure as struc
import data
import error

# EXIT Exception
class ExitInterpret(Exception): pass # EXIT

class Instruction:
    # allowed types for symb function arguments
    symb = {int, bool, str, struc.Variable, struc.Nil}

    def __init__(self, opcode, *operands):
        self.func, self.lamb = self.return_instruction(opcode)        
        self.opcode = opcode
        self.operands = operands or []

    def return_instruction(self, opcode):
        try:
            instructions = {
                'MOVE'          : (self.move_f, None),
                'CREATEFRAME'   : (self.createframe_f, None),
                'PUSHFRAME'     : (self.pushframe_f, None),
                'POPFRAME'      : (self.popframe_f, None),
                'DEFVAR'        : (self.defvar_f, None),
                'CALL'          : (self.call_f, None),
                'RETURN'        : (self.return_f, None),
                'PUSHS'         : (self.pushs_f, None),
                'POPS'          : (self.pops_f, None),
                'ADD'           : (self.add_sub_mul_f, lambda x, y : x + y),
                'SUB'           : (self.add_sub_mul_f, lambda x, y : x - y),
                'MUL'           : (self.add_sub_mul_f, lambda x, y : x * y),
                'IDIV'          : (self.idiv_f, None),
                'LT'            : (self.lt_gt_f, lambda x, y : x < y),
                'GT'            : (self.lt_gt_f, lambda x, y : x > y),
                'EQ'            : (self.eq_f, None),
                'AND'           : (self.and_or_f, lambda x, y : x and y),
                'OR'            : (self.and_or_f, lambda x, y : x or y),
                'NOT'           : (self.not_f, None),
                'INT2CHAR'      : (self.int2char_f, None),
                'STRI2INT'      : (self.stri2int_f, None),
                'READ'          : (self.read_f, None),
                'WRITE'         : (self.write_f, None),
                'CONCAT'        : (self.concat_f, None),
                'STRLEN'        : (self.strlen_f, None),
                'GETCHAR'       : (self.getchar_f, None),
                'SETCHAR'       : (self.setchar_f, None),
                'TYPE'          : (self.type_f, None),
                'LABEL'         : (self.label_f, None),
                'JUMP'          : (self.jump_f, None),
                'JUMPIFEQ'      : (self.jumpifeq_neq_f, lambda x, y : x == y),
                'JUMPIFNEQ'     : (self.jumpifeq_neq_f, lambda x, y : x != y),
                'EXIT'          : (self.exit_f, None),
                'DPRINT'        : (self.dprint_f, None),
                'BREAK'         : (self.break_f, None)
            }
            return instructions[opcode]
        except KeyError:
            raise error.InstructionError_32(opcode)

    ######################################################################
    ###                       RUNTIME FUNCTIONS                        ###
    ######################################################################
    
    def execute(self, frame_sel, inp):
        """Executes instruction with operands in self.operands"""
        try:
            if (self.opcode == 'READ'):
                return self.func(frame_sel, inp, *self.operands)
            else:
                return self.func(frame_sel, *self.operands)

            #
            # TODO ako je to s nespravnym poctom paramterov
            #

        except TypeError:   # invalid number of arguments
            raise error.XMLStructError_32(self.__str__())
        except AssertionError: # invalid type of arguments
            raise error.XMLStructError_32(self.__str__())

    def __str__(self):
        operands = ' '.join(str(op) for op in self.operands)
        operands = ' '+operands if operands != '' else operands
        return 'instruction(' + str(self.opcode) + operands + ')'

    def __repr__(self):
        operands = ' '.join(str(op) for op in self.operands)
        operands = ' '+operands if operands != '' else operands
        return 'instruction(' + str(self.opcode) + operands + ')'

    #######################################################################
    
    def get_type_values(self, frame_sel, type1, symb1, type2, symb2):
        type1 = [type1] if type(type1) is not list else type1
        type2 = [type2] if type(type2) is not list else type2

        val1 = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        val2 = frame_sel.get_value(symb2) if type(symb2) is struc.Variable else symb2
        
        invalid_type = True
        for t1, t2 in zip(type1, type2):
            if type(val1) is t1 and type(val2) is t2:
                invalid_type = False
                break

        if invalid_type:
            raise error.OperandTypeError_53(self.__str__())

        return val1, val2

    #######################################################################

    def move_f(self, frame_sel, var, symb1):
        assert type(var) is struc.Variable and type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        frame_sel.set_value(var, value)

    def createframe_f(self, frame_sel):
        frame_sel.create_frame()

    def pushframe_f(self, frame_sel):
        frame_sel.push_frame()

    def popframe_f(self, frame_sel):
        frame_sel.pop_frame()

    def defvar_f(self, frame_sel, var):
        assert type(var) is struc.Variable
        frame_sel.def_var(var)

    def call_f(self, frame_sel, label):
        assert type(label) is struc.Label
        # TODO
        return True, False, label
        
    def return_f(self, frame_sel):
        # TODO
        return False, True, None

    def pushs_f(self, frame_sel, symb1):
        assert type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        frame_sel.pushs(value)


    def pops_f(self, frame_sel, var):
        assert type(var) is struc.Variable
        value = frame_sel.pops()
        frame_sel.set_value(var, value)

    #######################################################################

    def add_sub_mul_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, int, symb1, int, symb2)
        value = self.lamb(val1, val2)
        frame_sel.set_value(var, value)

    #######################################################################

    def idiv_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, int, symb1, int, symb2)
        if val2 == 0:
            raise error.InterpretZeroDivError_57(self.__str__())
        
        value = val1 // val2
        frame_sel.set_value(var, value)
    
    #######################################################################

    def lt_gt_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        types = [int, bool, str]
        val1, val2 = self.get_type_values(frame_sel, types, symb1, types, symb2)
        value = self.lamb(val1, val2)
        frame_sel.set_value(var, value)

    def eq_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1 = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        val2 = frame_sel.get_value(symb2) if type(symb2) is struc.Variable else symb2
        if type(val1) is struc.Nil or type(val2) is struc.Nil:
            pass
        else:
            types = [int, bool, str]
            val1, val2 = self.get_type_values(frame_sel, types, symb1, types, symb2)

        value = val1 == val2
        frame_sel.set_value(var, value)

    #######################################################################

    def and_or_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, bool, symb1, bool, symb2)
        value = self.lamb(val1, val2)
        frame_sel.set_value(var, value)

    def not_f(self, frame_sel, var, symb1):
        assert type(var) is struc.Variable and type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        if type(value) is not bool:
            raise error.OperandTypeError_53(self.__str__())
        frame_sel.set_value(var, not value)

    #######################################################################

    def int2char_f(self, frame_sel, var, symb1):
        assert type(var) is struc.Variable and type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        try:
            frame_sel.set_value(var, chr(value))
        except TypeError:
            raise error.OperandTypeError_53(self.__str__())
        except ValueError:
            raise error.StringError_58(self.__str__())
        
    def stri2int_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        string, position = self.get_type_values(frame_sel, str, symb1, int, symb2)
        try:
            value = ord(string[position])
            frame_sel.set_value(var, value)
        except (IndexError, TypeError):
            raise error.StringError_58(self.__str__())

    #######################################################################

    def input(self, inp):
        user_input = inp.readline()
        return user_input if user_input == '' or user_input[-1] != '\n' else user_input[:-1]

    def read_f(self, frame_sel, inp, var, typ):
        assert type(var) is struc.Variable and type(typ) == struc.Type
        
        user_input = self.input(inp)

        if typ == struc.Type('int'):
            try:
                value = int(user_input)
            except ValueError:
                value = 0
        elif typ == struc.Type('string'):
            value = str(user_input)
        elif typ == struc.Type('bool'):
            value = (user_input.upper() == 'TRUE')
        frame_sel.set_value(var, value)

    def write_f(self, frame_sel, symb1):
        assert type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        if type(value) is bool:
            value = 'true' if value == True else 'false'
        print(value, end='')

    #######################################################################

    def concat_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        string1, string2 = self.get_type_values(frame_sel, str, symb1, str, symb2)
        value = string1 + string2
        frame_sel.set_value(var, value)

    def strlen_f(self, frame_sel, var, symb1):
        assert type(var) is struc.Variable and type(symb1) in Instruction.symb
        
        string = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        if type(string) is not str:
            raise error.OperandTypeError_53(self.__str__())
        frame_sel.set_value(var, len(string))

    def getchar_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        string, position = self.get_type_values(frame_sel, str, symb1, int, symb2)
        try:
            frame_sel.set_value(var, string[position])
        except IndexError:
            raise error.StringError_58(self.__str__())

    def setchar_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        string = frame_sel.get_value(var)
        if type(string) is not str:
            raise error.OperandTypeError_53(self.__str__())
        position, char = self.get_type_values(frame_sel, int, symb1, str, symb2)
        try:
            if position >= len(string):
                raise IndexError
            value = string[:position] + char[0] + string[position+1:]
            frame_sel.set_value(var, value)
        except IndexError:
            raise error.StringError_58(self.__str__())

    #######################################################################

    def type_f(self, frame_sel, var, symb1):
        assert type(var) is struc.Variable and type(symb1) in Instruction.symb
        try:
            value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
            if type(value) is int:
                typ = 'int'
            elif type(value) is bool:
                typ = 'bool'
            elif type(value) is str:
                typ = 'string'
            elif type(value) is struc.Nil:
                typ = 'nil'
        except error.VariableMissingValueError_56: 
            typ = '' # in case the variable is unitialized -- type is empty string
        frame_sel.set_value(var, typ)

    #######################################################################

    def label_f(self, frame_sel, label):
        assert type(label) is struc.Label
        ...

    def jump_f(self, frame_sel, label):
        assert type(label) is struc.Label
        return False, False, label

    def jumpifeq_neq_f(self, frame_sel, label, symb1, symb2):
        assert type(label) is struc.Label
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        types = [int, bool, str, struc.Nil]
        val1, val2 = self.get_type_values(frame_sel, types, symb1, types, symb2)
        if self.lamb(val1, val2):
            return False, False, label
        else:
            return None

    def exit_f(self, frame_sel, symb1):
        assert type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        if type(value) is not int:
            raise error.OperandTypeError_53(self.__str__())
        if not (0 <= value <= 49):
            raise error.OperandValueError_57(self.__str__())

        raise ExitInterpret(value)

    #######################################################################

    def dprint_f(self, frame_sel, symb1):
        assert type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        if type(value) is bool:
            value = 'true' if value == True else 'false'
        print(value, file=sys.stderr, end='')


    def break_f(self, frame_sel):
        print('Number of executed instructions: n/a\n', file=sys.stderr) # TODO number of instruct
        print(str(frame_sel), file=sys.stderr, end='')
