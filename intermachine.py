
import xml.etree.ElementTree as ElementTree
import structure as struc
import instruc as inst
import data

class OrderError(Exception): pass
class LabelError(Exception): pass

class Program:

    def __init__(self):
        self.instructions = []
        self.labels = {}

    def append_instruction(self, instruction):
        self.instructions.append(instruction)
        try:
            if instruction.opcode == 'LABEL':
                self.add_label(instruction.operands[0], len(self.instructions) - 1)
        except IndexError: # TODO
            raise inst.WrongOperandsError

    def add_label(self, label, index):
        if label in self.labels:
            raise LabelError
        self.labels[label] = index

    def __len__(self):
        return len(self.instructions)

class Parser:

    def __init__(self, src):
        tree = ElementTree.parse(src)
        self.root = tree.getroot()

    def parse_XML(self, debug=False):
        program = Program()
        for i, inst_XML in enumerate(self.root, 1):
            if i != int(inst_XML.attrib['order']):
                raise OrderError

            operands = []
            for arg_XML in inst_XML:
                op = struc.Operand(arg_XML.attrib['type'], arg_XML.text)
                op_interpr = op.apply_type()
                operands.append(op_interpr)

            instruction = inst.Instruction(inst_XML.attrib['opcode'], *operands)
            program.append_instruction(instruction)
            
            if debug:
                print(instruction)

        return program


class Interpreter:

    def __init__(self, program):
        self.program = program
        self.inst_pointer = 0
        self.frame_sel = data.FrameSelect()
        self.call_stack = data.CallStack()

    def interpret(self, inp):
        while self.inst_pointer < len(self.program.instructions):
            instruction = self.program.instructions[self.inst_pointer]
            label_info = instruction.execute(self.frame_sel)

            if label_info is not None:
                call, ret, label = label_info

                if call == False and ret == False:
                    # classic jump
                    self.inst_pointer = self.program.labels[label]
                elif call == True and ret == False:
                    # open subroutine call
                    self.call_stack.push(self.inst_pointer)
                    self.inst_pointer = self.program.labels[label]
                elif call == False and ret == True:
                    # return from open subroutine
                    self.inst_pointer = self.call_stack.pop()

            # should work when jump and also return
            self.inst_pointer += 1 