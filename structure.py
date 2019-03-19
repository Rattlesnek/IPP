

class StructureError(Exception): pass

class Operand:

    def __init__(self, category, value):
        self.category = category
        self.value = value

    def __str__(self):
        return self.category + ';' +  self.value

    def __repr__(self):
        return self.category + ';' +  self.value

    def apply_type(self):
        """Applies type of operand and returns operand with correct type"""
        return Operand.categories[self.category](self)
    
    def variable(self):
        """Creates Variable and returns it"""
        try:
            parts = self.value.split('@', 2)
            return Variable(*parts)
        except TypeError:
            raise StructureError

    def boolean(self):
        """Creates bool and returns it"""
        if self.value == 'true':
            return True
        elif self.value == 'false':
            return False
        else:
            raise StructureError

    def integer(self):
        """Creates int and returns it"""
        try:
            return int(self.value)
        except ValueError:
            raise StructureError

    def string(self):
        """Creates str and returns it"""
        return str(self.value)
        # TODO

    def nil(self):
        """Creates Nil and returns it"""
        return Nil()

    def type_of(self):
        """Creates Type and returns it"""
        return Type(self.value)

    def label(self):
        """Creates Label and returns it"""
        return Label(self.value)

    categories = {
        'var'       : variable,
        'bool'      : boolean,
        'int'       : integer,
        'string'    : string,
        'nil'       : nil,
        'type'      : type_of,
        'label'     : label
    }


class Variable:
    frames = {'LF', 'TF', 'GF'}

    def __init__(self, frame, name):
        if frame not in Variable.frames:
            raise StructureError
        self.frame = frame
        self.name = name

    def __str__(self):
        return '[Var {} {}]'.format(self.frame, self.name)

    def __repr__(self):
        return '[Var {} {}]'.format(self.frame, self.name)



class Type:
    types = {'int', 'bool', 'string'}

    def __init__(self, typ):
        if typ not in Type.types:
            raise StructureError 
        self.type = typ
  
    def __str__(self):
        return '[Type ' + self.type + ']'

    def __repr__(self):
        return '[Type ' + self.type + ']'


class Label:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '[Label ' + self.name + ']'

    def __repr__(self):
        return '[Label ' + self.name + ']'

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class Nil:

    def __init__(self):
        self.nil = 'nil'
        # TODO
    
    def __str__(self):
        return '[Nil ' + self.nil + ']'

    def __repr__(self):
        return '[Nil ' + self.nil + ']'

    def __eq__(self, other):
        return self.nil == other.nil

    