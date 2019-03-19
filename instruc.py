import structure as struc
import data

# ERR_PARAM = 10
# ERR_INFILE = 11
# ERR_OUTFILE = 12
# ERR_XML_FORMAT = 31
# ERR_XML_STRUCT = 32

# ERR_SEMANTIC = 52
# ERR_TYPE = 53
# ERR_UNDEF_VAR = 54
# ERR_NO_FRAME = 55
# ERR_MISS_VAL = 56
# ERR_OPERAND_VAL = 57
# ERR_STRING = 58

# ERR_INTER = 99 


class InvalidTypeError(Exception): pass # ERR_TYPE
class InterpretZeroDiv(Exception): pass # ERR_OPERAND_VAL
class OperandValueError(Exception): pass # ERR_OPERAND_VAL


class InstructionError(Exception): pass # ? 
class WrongOperandsError(Exception): pass # ?
class StringOperationError(Exception): pass # ERR_STRING

class InterpretExit(Exception): pass

class Instruction:
    # allowed types for symb function arguments
    symb = {int, bool, str, struc.Variable, struc.Nil}

    def __init__(self, opcode, *operands):
        try:
            self.func = self.return_instruction(opcode)
        except KeyError:
            raise InstructionError(str(opcode))
        
        self.opcode = opcode
        self.operands = operands or []

    def return_instruction(self, opcode):
        instructions = {
            'MOVE'          : self.move_f,
            'CREATEFRAME'   : self.createframe_f,
            'PUSHFRAME'     : self.pushframe_f,
            'POPFRAME'      : self.popframe_f,
            'DEFVAR'        : self.defvar_f,
            'CALL'          : self.call_f,
            'RETURN'        : self.return_f,
            'PUSHS'         : self.pushs_f,
            'POPS'          : self.pops_f,
            'ADD'           : self.add_f,
            'SUB'           : self.sub_f,
            'MUL'           : self.mul_f,
            'IDIV'          : self.idiv_f,
            'LT'            : self.lt_f,
            'GT'            : self.gt_f,
            'EQ'            : self.eq_f,
            'AND'           : self.and_f,
            'OR'            : self.or_f,
            'NOT'           : self.not_f,
            'INT2CHAR'      : self.int2char_f,
            'STRI2INT'      : self.stri2int_f,
            'READ'          : self.read_f,
            'WRITE'         : self.write_f,
            'CONCAT'        : self.concat_f,
            'STRLEN'        : self.strlen_f,
            'GETCHAR'       : self.getchar_f,
            'SETCHAR'       : self.setchar_f,
            'TYPE'          : self.type_f,
            'LABEL'         : self.label_f,
            'JUMP'          : self.jump_f,
            'JUMPIFEQ'      : self.jumpifeq_f,
            'JUMPIFNEQ'     : self.jumpifneq_f,
            'EXIT'          : self.exit_f,
            'DPRINT'        : self.dprint_f,
            'BREAK'         : self.break_f
        }
        return instructions[opcode]

    def execute(self, frame_sel):
        """Executes instruction with operands in self.operands"""
        try:
            return self.func(frame_sel, *self.operands)
        except (TypeError, AssertionError):
            raise WrongOperandsError

    def __str__(self):
        operands = ' '.join(str(op) for op in self.operands)
        return str(self.opcode) + ' ' + operands 

    def __repr__(self):
        operands = ' '.join(str(op) for op in self.operands)
        return str(self.opcode) + ' ' + operands 

    ##########################################################################

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
            raise InvalidTypeError

        return val1, val2

    ##########################################################################

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

    #########################################

    def add_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, int, symb1, int, symb2)
        value = val1 + val2 # TODO
        frame_sel.set_value(var, value)


    def sub_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, int, symb1, int, symb2)
        value = val1 - val2 # TODO
        frame_sel.set_value(var, value)


    def mul_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, int, symb1, int, symb2)
        value = val1 * val2 # TODO
        frame_sel.set_value(var, value)

    ################################

    def idiv_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, int, symb1, int, symb2)
        if val2 == 0:
            raise InterpretZeroDiv
        
        value = val1 // val2
        frame_sel.set_value(var, value)
    
    ##################################

    def lt_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb

        val1, val2 = self.get_type_values(frame_sel, [int, bool, str], symb1, [int, bool, str], symb2)
        value = val1 < val2
        frame_sel.set_value(var, value)


    def gt_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, [int, bool, str], symb1, [int, bool, str], symb2)
        value = val1 > val2
        frame_sel.set_value(var, value)

    def eq_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, [int, bool, str], symb1, [int, bool, str], symb2)
        value = val1 == val2
        frame_sel.set_value(var, value)

    #################################

    def and_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, bool, symb1, bool, symb2)
        value = val1 and val2
        frame_sel.set_value(var, value)


    def or_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        val1, val2 = self.get_type_values(frame_sel, bool, symb1, bool, symb2)
        value = val1 or val2
        frame_sel.set_value(var, value)

    def not_f(self, frame_sel, var, symb1):
        assert type(var) is struc.Variable and type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        if type(value) is not bool:
            raise InvalidTypeError
        frame_sel.set_value(var, not value)

    ##################################

    def int2char_f(self, frame_sel, var, symb1):
        assert type(var) is struc.Variable and type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        try:
            frame_sel.set_value(var, chr(value))
        except TypeError:
            raise StringOperationError
        

    def stri2int_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        string, position = self.get_type_values(frame_sel, str, symb1, int, symb2)
        try:
            value = ord(string[position])
            frame_sel.set_value(var, value)
        except (IndexError, TypeError):
            raise StringOperationError


    ##################################

    def read_f(self, frame_sel, var, typ):
        assert type(var) is struc.Variable and type(typ) == struc.Type
        ...

    def write_f(self, frame_sel, symb1):
        assert type(symb1) in Instruction.symb
        ...

    ##################################

    def concat_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        string1, string2 = self.get_type_values(frame_sel, str, symb1, str, symb2)
        value = string1 + string2
        frame_sel.set_value(var, value)

    def strlen_f(self, frame_sel, var, symb1):
        assert type(var) is struc.Variable and type(symb1) in Instruction.symb
        
        string = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        frame_sel.set_value(var, len(string))

    def getchar_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        string, position = self.get_type_values(frame_sel, str, symb1, int, symb2)
        try:
            frame_sel.set_value(var, string[position])
        except IndexError:
            raise StringOperationError


    def setchar_f(self, frame_sel, var, symb1, symb2):
        assert type(var) is struc.Variable
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        string = frame_sel.get_value(var)
        position, char = self.get_type_values(frame_sel, int, symb1, str, symb2)
        try:
            if position >= len(string):
                raise IndexError
            value = string[:position] + char[0] + string[position+1:]
            frame_sel.set_value(var, value)
        except IndexError:
            raise StringOperationError

    #########################

    def type_f(self, frame_sel, var, symb1):
        assert type(var) is struc.Variable and type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        if type(value) is int:
            typ = 'int'
        elif type(value) is bool:
            typ = 'bool'
        elif type(value) is str:
            typ = 'str'
        elif type(value) is struc.Nil:
            typ = 'nil'
        elif value is None:
            typ = ''
        frame_sel.set_value(var, typ)

    #############################

    def label_f(self, frame_sel, label):
        assert type(label) is struc.Label
        ...

    def jump_f(self, frame_sel, label):
        assert type(label) is struc.Label
        return False, False, label

    def jumpifeq_f(self, frame_sel, label, symb1, symb2):
        assert type(label) is struc.Label
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        types = [int, bool, str, struc.Nil]
        val1, val2 = self.get_type_values(frame_sel, types, symb1, types, symb2)
        if val1 == val2:
            return False, False, label
        else:
            return None


    def jumpifneq_f(self, frame_sel, label, symb1, symb2):
        assert type(label) is struc.Label
        assert type(symb1) in Instruction.symb and type(symb2) in Instruction.symb
        
        types = [int, bool, str, struc.Nil]
        val1, val2 = self.get_type_values(frame_sel, types, symb1, types, symb2)
        if val1 != val2:
            return False, False, label
        else:
            return None

    def exit_f(self, frame_sel, symb1):
        assert type(symb1) in Instruction.symb
        
        value = frame_sel.get_value(symb1) if type(symb1) is struc.Variable else symb1
        if type(value) is not int:
            raise OperandValueError # TODO
        if not (0 <= value <= 49):
            raise OperandValueError

        raise InterpretExit(value)

    #############################

    def dprint_f(self, frame_sel, symb1):
        assert type(symb1) in Instruction.symb
        ...

    def break_f(self, frame_sel):
        ...
