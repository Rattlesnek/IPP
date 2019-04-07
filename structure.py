"""
    Interpreter of IPPcode19 - FIT VUT
    
    File:   structure.py
    
    Author: Adam Pankuch
    
    Login:  xpanku00
    
    Date:   7.4.2019
"""
import re
import error


class Operand:
    """
    Class representing factory of operand types
    
    Raises:
        error.ArgumentError_32
        error.StructureError_32
    """

    def __init__(self, typ, value):
        self.type = typ
        self.value = value

    def __str__(self):
        return self.type + ';' +  self.value

    def __repr__(self):
        return self.type + ';' +  self.value

    def return_operand_factory(self, typ):
        """ Return function able to create operand type """
        try:
            categories = {
                'var'       : self.variable,
                'bool'      : self.boolean,
                'int'       : self.integer,
                'string'    : self.string,
                'nil'       : self.nil,
                'type'      : self.type_of,
                'label'     : self.label
            }
            return categories[typ]
        except KeyError:
            raise error.ArgumentError_32(self.__str__())

    def apply_type(self):
        """ Applies type of operand and returns operand with correct type """
        factory = self.return_operand_factory(self.type)
        return factory()
    
    def variable(self):
        """ Creates Variable and returns it """
        return Variable(self.value) # error.StructureError_32 if fail

    def boolean(self):
        """ Creates bool and returns it """
        if self.value == 'true':
            return True
        elif self.value == 'false':
            return False
        else:
            raise error.StructureError_32(self.value)

    def integer(self):
        """ Creates int and returns it """
        try:
            return int(self.value)
        except ValueError:
            raise error.StructureError_32(self.value)

    def string(self):
        """ Creates str and returns it """
        if self.value is None:
            self.value = ''
        if re.match(r'^(\\[0-9]{3}|[^\\#\s])*$', self.value) is None: # TODO
            raise error.StructureError_32(self.value)

        escape = re.findall(r'\\[0-9]{3}', self.value)
        not_escape = re.split(r'\\[0-9]{3}', self.value)

        final_string = ''
        for not_esc, esc in zip(not_escape, escape):
            final_string += not_esc + chr(int(esc[1:]))
        final_string += not_escape[-1]

        return str(final_string)

    def nil(self):
        """ Creates Nil and returns it """
        return Nil(self.value) # error.StructureError_32 if fail

    def type_of(self):
        """ Creates Type and returns it """
        return Type(self.value) # error.StructureError_32 if fail

    def label(self):
        """ Creates Label and returns it """
        return Label(self.value) # error.StructureError_32 if fail



class Variable:
    """
    Class representing a variable
    
    Raises:
        error.StructureError_32
    """

    def __init__(self, variable):
        if re.match(r'^((GF|TF|LF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$', variable) is None:
            raise error.StructureError_32(variable)
        frame, name = variable.split('@', 2)
        self.frame = frame
        self.name = name

    def __str__(self):
        return '[Var {} {}]'.format(self.frame, self.name)

    def __repr__(self):
        return '[Var {} {}]'.format(self.frame, self.name)


class Type:
    """
    Class representing type "type"
    
    Raises:
        error.StructureError_32
    """

    def __init__(self, typ):
        if typ not in {'int', 'bool', 'string'}:
            raise error.StructureError_32(typ) 
        self._type = typ
  
    def __str__(self):
        return '[Type ' + self._type + ']'

    def __repr__(self):
        return '[Type ' + self._type + ']'

    def __eq__(self, other):
        return self._type == other._type


class Label:
    """
    Class representing type label
    
    Raises:
        error.StructureError_32
    """

    def __init__(self, name):
        if re.match(r'^([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$', name) is None:
            raise error.StructureError_32(name)
        self._name = name

    def __str__(self):
        return '[Label ' + self._name + ']'

    def __repr__(self):
        return '[Label ' + self._name + ']'

    def __eq__(self, other):
        return self._name == other._name

    def __hash__(self):
        return hash(self._name)


class Nil:
    """
    Class representing type nil
    
    Raises:
        error.StructureError_32
    """

    def __init__(self, text):
        if text != 'nil':
            raise error.StructureError_32(text)
        self._nil = None
    
    def __str__(self):
        return ''

    def __repr__(self):
        return '[Nil nil]'

    def __eq__(self, other):
        try:
            return self._nil == other._nil
        except AttributeError:
            return False
    