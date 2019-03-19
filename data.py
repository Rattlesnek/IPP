import structure as struc

class FrameError(Exception): pass
class CallStackError(Exception): pass
class DataStackError(Exception): pass
class VarDefineError(Exception): pass

class Frame(dict):

    def __init__(self):
        super().__init__()
    
    def def_var(self, var_name):
        """Defines a variable in the frame (raise Error if it already exists)"""
        if type(var_name) != str:
            raise struc.StructureError
        if super().__contains__(var_name):
            raise VarDefineError
        super().__setitem__(var_name, None)
            
    def __setitem__(self, var_name, value):
        """Moves value to the variable (raise Error if it is not defined)"""
        if type(var_name) != str:
            raise struc.StructureError
        if not super().__contains__(var_name):
            raise VarDefineError
        super().__setitem__(var_name, value)


class FrameStack:

    def __init__(self):
        self.stack = []
    
    def push_frame(self, frame):
        """Puses frame to stack"""
        if type(frame) != Frame:
            raise FrameError
        self.stack.append(frame)

    def pop_frame(self):
        """Pops frame from stack (raise Error if no frame in stack)"""
        if len(self.stack) == 0:
            raise FrameError
        return self.stack.pop()

    def __getitem__(self, var_name):
        """Returns variable from top frame (raise Error if no frame in stack)"""
        if len(self.stack) == 0:
            raise FrameError
        return self.stack[-1][var_name]
    
    def def_var(self, var_name):
        """Defines variable in top frame
        (raise Error if no frame in stack or variable already exists)"""
        if len(self.stack) == 0:
            raise FrameError
        self.stack[-1].def_var(var_name)

    def __setitem__(self, var_name, value):
        """Moves value to the variable
        (raise Error if no frame in stack or variable not defined)"""
        if len(self.stack) == 0:
            raise FrameError
        self.stack[-1][var_name] = value

    def show_top(self):
        """Returns top frame as string"""
        return '' if len(self.stack) == 0 else str(self.stack[-1])


class FrameSelect:

    def __init__(self):
        self.global_frame = Frame()
        self.temporary_frame = None
        self.local_stack = FrameStack()
        self.data_stack = []

    def tf_exists(self):
        """Returns true if TF exists"""
        return self.temporary_frame is not None

    def create_frame(self):
        """Creates TF, and throws away its content"""
        self.temporary_frame = Frame()
    
    def push_frame(self):
        """Pushes TF (if does not exist raise Error) to LF stack and TF remains undefined"""
        if not self.tf_exists():
            raise FrameError
        self.local_stack.push_frame(self.temporary_frame)
        self.temporary_frame = None

    def pop_frame(self):
        """Pops LF from LF stack and save it to TF (raise Error in case LF does no exist)"""
        self.temporary_frame = self.local_stack.pop_frame()

    def def_var(self, var):
        """Defines a unitialized variable in a certain frame"""
        if var.frame == 'GF':
            self.global_frame.def_var(var.name)
        elif var.frame == 'TF':
            if not self.tf_exists():
                raise FrameError
            self.temporary_frame.def_var(var.name)
        elif var.frame == 'LF':
            self.local_stack.def_var(var.name)
        else:
            raise FrameError

    def set_value(self, var, value):
        """Moves value to the variable in a certain frame"""
        if var.frame == 'GF':
            self.global_frame[var.name] = value
        elif var.frame == 'TF':
            if not self.tf_exists():
                raise FrameError
            self.temporary_frame[var.name] = value
        elif var.frame == 'LF':
            self.local_stack[var.name] = value
        else:
            raise FrameError

    def get_value(self, var):
        """Get value of variable in a certain frame"""
        if var.frame == 'GF':
            return self.global_frame[var.name]
        elif var.frame == 'TF':
            if not self.tf_exists():
                raise FrameError
            return self.temporary_frame[var.name]
        elif var.frame == 'LF':
            return self.local_stack[var.name]
        else:
            raise FrameError 

    def pushs(self, value):
        """Pushs value to the data stack"""
        self.data_stack.append(value)

    def pops(self):
        """Pops value from the data stack"""
        if len(self.data_stack) == 0:
            raise DataStackError
        return self.data_stack.pop()
    
class CallStack:

    def __init__(self):
        self.stack = []

    def push(self, inst_pointer):
        self.stack.append(inst_pointer)
    
    def pop(self):
        if len(self.stack) == 0:
            raise CallStackError
        return self.stack.pop()