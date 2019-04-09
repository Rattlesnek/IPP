"""
    Interpreter of IPPcode19 - FIT VUT
    
    File:   intermachine.py
    
    Author: Adam Pankuch
    
    Login:  xpanku00
    
    Date:   7.4.2019
"""
import xml.etree.ElementTree as ElementTree
import structure as struc
import instruc as inst
import data
import error


class Program:
    """
    Class representing a single program consisting of Instruction objects

    Raises:
        error.LabelError_52
    """

    def __init__(self):
        self.instructions = []
        self.labels = {}

    def append_instruction(self, instruction):
        """ Append instruction to the program """
        self.instructions.append(instruction)
        try:
            if instruction.opcode == 'LABEL':
                self.add_label(instruction.operands[0], len(self.instructions) - 1)
        except IndexError: # TODO
            raise error.LabelError_52(instruction)

    def add_label(self, label, index):
        """ Add label to dict of labels with its location in program """
        if label in self.labels:
            raise error.LabelError_52(label)
        self.labels[label] = index

    def __len__(self):
        return len(self.instructions)


class Parser:
    """
    Class representing the IPPcode19 parser
    able to parse source XML and return Program object
    
    Raises:
        error.XMLFormatError_31
        error.XMLStructError_32 
    """

    def __init__(self, src):
        try:
            tree = ElementTree.parse(src)
            self.root = tree.getroot()
        except ElementTree.ParseError:
            raise error.XMLFormatError_31      

    def get_operands(self, inst_XML):
        """ Get operands of a single instruction """
        operands = []
        for j in range(1, 4):
            arg_XML = inst_XML.find('arg' + str(j))
            if arg_XML is None:
                break
            op = struc.Operand(arg_XML.attrib['type'], arg_XML.text)
            op_interpr = op.apply_type()
            operands.append(op_interpr)
        # in case there are other elements (or arguments with wrong number)
        # ... in inst_XML other then arguments
        if len(operands) != len([None for _ in inst_XML]):
            raise error.XMLStructError_32
        return operands

    def parse_XML(self, debug=False):
        """ Parse source XML """
        program = Program()
        i = 0
        while True:
            i += 1
            # find single element which hast tag: instruction and attribute order: number of inst
            inst_XML = self.root.find("./instruction[@order='{}']".format(i))
            if inst_XML is None:
                break
            
            try:
                operands = self.get_operands(inst_XML)
                instruction = inst.Instruction(inst_XML.attrib['opcode'].upper(), *operands)
            except KeyError: # in case attributes 'opcode' or 'type' are missing
                raise error.XMLStructError_32
            program.append_instruction(instruction)
            
            if debug:
                print(instruction)

        # in case there are other elements (or instructions with wrong order) 
        # ... in self.root other than instructions
        if i - 1 != len([None for _ in self.root]):
            raise error.XMLStructError_32
        
        return program


class Interpreter:
    """
    Class representing the IPPcode19 interpreter
    able to interpret a program given as parameter
    
    Raises:
        error.LabelError_52
    """

    def __init__(self, program):
        self.program = program
        self.inst_pointer = 0
        self.frame_sel = data.FrameSelect()
        self.call_stack = data.Stack()

    def interpret(self, inp):
        """ Interpret a program - MAIN INTERPRETATION LOOP """
        self.inst_pointer = 0
        while self.inst_pointer < len(self.program.instructions):
            instruction = self.program.instructions[self.inst_pointer]
            label_info = instruction.execute(self.frame_sel, inp)
            if label_info is not None:
                self.wormhole(*label_info)   
            # should work when jump and also return
            self.inst_pointer += 1 

    def wormhole(self, call, ret, label):
        """ Handles jumps and calls, returns + allows recursion """
        try:
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
        except KeyError:
            raise error.LabelError_52(label)

