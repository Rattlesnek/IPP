import structure as struc
import error


class Frame(dict):
    types = {'GF', 'LF', 'TF'}

    def __init__(self, typ):
        assert typ in Frame.types
        self.type = typ
        super().__init__()

    def __str__(self):
        string = ''
        for var, value in super().items():
            string += '{}@{}={}\n'.format(self.type, var, str(value))        
        return string
    
    def def_var(self, var_name):
        """Defines a variable in the frame (raise Error if it already exists)"""
        if type(var_name) != str:
            raise TypeError('its fcked up!')
        if super().__contains__(var_name):
            raise error.VarDefineError_54(var_name)
        super().__setitem__(var_name, None)
            
    def __setitem__(self, var_name, value):
        """Moves value to the variable (raise Error if it is not defined)"""
        if type(var_name) != str:
            raise TypeError('its fcked up!')
        if not super().__contains__(var_name):
            raise error.VarDefineError_54(var_name)
        super().__setitem__(var_name, value)

    def __getitem__(self, var_name):
        if type(var_name) != str:
            raise TypeError('its fcked up!')
        if not super().__contains__(var_name):
            raise error.VarDefineError_54(var_name)
        value = super().__getitem__(var_name) 
        if value is None:
            raise error.VariableMissingValueError_56(var_name)
        return value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, typ):
        assert typ in Frame.types
        self.__type = typ



class FrameStack:

    def __init__(self):
        self.stack = []

    def __str__(self):
        return '' if len(self.stack) == 0 else str(self.stack[-1])
    
    def push_frame(self, frame):
        """Puses frame to stack"""
        if type(frame) != Frame:
            raise TypeError('its fcked up!')
        self.stack.append(frame)

    def pop_frame(self):
        """Pops frame from stack (raise Error if no frame in stack)"""
        if len(self.stack) == 0:
            raise error.FrameError_55
        return self.stack.pop()

    def __getitem__(self, var_name):
        """Returns variable from top frame (raise Error if no frame in stack)"""
        if len(self.stack) == 0:
            raise error.FrameError_55
        return self.stack[-1][var_name]
    
    def def_var(self, var_name):
        """Defines variable in top frame
        (raise Error if no frame in stack or variable already exists)"""
        if len(self.stack) == 0:
            raise error.FrameError_55
        self.stack[-1].def_var(var_name)

    def __setitem__(self, var_name, value):
        """Moves value to the variable
        (raise Error if no frame in stack or variable not defined)"""
        if len(self.stack) == 0:
            raise error.FrameError_55
        self.stack[-1][var_name] = value

    def show_top(self):
        """Returns top frame as string"""
        return '' if len(self.stack) == 0 else str(self.stack[-1])


class FrameSelect:

    def __init__(self):
        self.global_frame = Frame('GF')
        self.temporary_frame = None
        self.local_stack = FrameStack()
        self.data_stack = []

    def str_data_stack(self):
        string = ''
        for val in self.data_stack:
            string += 'Stack@=' + str(val) + '\n'
        return string

    def __str__(self):
        string = 'Global Frame:\n' + str(self.global_frame) + '\n'
        string += 'Local Frame:\n' + str(self.local_stack) + '\n'
        string += 'Temporary Frame:\n'
        string += (str(self.temporary_frame) + '\n') if self.tf_exists() else '\n'
        string += 'Stack:\n' + self.str_data_stack()
        return string

    def tf_exists(self):
        """Returns true if TF exists"""
        return self.temporary_frame is not None

    def create_frame(self):
        """Creates TF, and throws away its content"""
        self.temporary_frame = Frame('TF')
    
    def push_frame(self):
        """Pushes TF (if does not exist raise Error) to LF stack and TF remains undefined"""
        if not self.tf_exists():
            raise error.FrameError_55
        self.temporary_frame.type = 'LF'
        self.local_stack.push_frame(self.temporary_frame)
        self.temporary_frame = None

    def pop_frame(self):
        """Pops LF from LF stack and save it to TF (raise Error in case LF does no exist)"""
        self.temporary_frame = self.local_stack.pop_frame()
        self.temporary_frame.type = 'TF'

    def def_var(self, var):
        """Defines a unitialized variable in a certain frame"""
        if var.frame == 'GF':
            self.global_frame.def_var(var.name)
        elif var.frame == 'TF':
            if not self.tf_exists():
                raise error.FrameError_55
            self.temporary_frame.def_var(var.name)
        elif var.frame == 'LF':
            self.local_stack.def_var(var.name)

    def set_value(self, var, value):
        """Moves value to the variable in a certain frame"""
        if var.frame == 'GF':
            self.global_frame[var.name] = value
        elif var.frame == 'TF':
            if not self.tf_exists():
                raise error.FrameError_55
            self.temporary_frame[var.name] = value
        elif var.frame == 'LF':
            self.local_stack[var.name] = value

    def get_value(self, var):
        """Get value of variable in a certain frame"""
        if var.frame == 'GF':
            return self.global_frame[var.name]
        elif var.frame == 'TF':
            if not self.tf_exists():
                raise error.FrameError_55
            return self.temporary_frame[var.name]
        elif var.frame == 'LF':
            return self.local_stack[var.name]


    def pushs(self, value):
        """Pushs value to the data stack"""
        self.data_stack.append(value)

    def pops(self):
        """Pops value from the data stack"""
        if len(self.data_stack) == 0:
            raise error.DataStackError_56
        return self.data_stack.pop()
    

class CallStack:

    def __init__(self):
        self.stack = []

    def push(self, inst_pointer):
        self.stack.append(inst_pointer)
    
    def pop(self):
        if len(self.stack) == 0:
            raise error.CallStackError_56
        return self.stack.pop()