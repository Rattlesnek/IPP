# Documentation of Project Implementation of 2. Task for IPP 2018/2019
* Name and surname: Adam Pankuch
* Login: xpanku00

## Task - `interpret.py`

The goal was to create a script in Python 3.6 which reads the XML representation of an IPPcode19 program and interprets it using the standard input and output.

## Solution - `interpret.py`

### Files

* `interpret.py` - main file, runs the whole interpret, catches exceptions
* `intermachine.py` - contains classes `Program`, `Parser`, `Interpreter`
* `data.py` - contains classes `Frame`, `FrameStack`, `FrameSelect`, `Stack`
* `instruct.py` - contains class `Instruction`
* `struct.py` - contains classes `Operand`, `Variable`, `Type`, `Label`, `Nil`
* `error.py` - contains all error exceptions and error return values

### Classes

* `Program`
    * internal representation of an IPPcode19 program
    * contains list of `Instruction` objects and dictionary of `Label` objects referring to a certain location in the list of instructions
* `Parser`
    * parser of the XML representation of an IPPcode19 program
    * able to parse the XML representation of a program and create a `Program` object
* `Interpreter`
    * interpreter of the internal representation of an IPPcode19 program (`Program` instance)
    * contains `FrameSelect` object, instruction pointer and function call `Stack` object

* `Frame`
    * dictionary of variable names with their values
    * can be global, local or temporary
* `FrameStack`
    * stack of local `Frame` instances
    * allows operations only with `Frame` object on the top of the stack
* `FrameSelect`
    * class grouping memory management methods
    * consists of global `Frame`, local `FrameStack`, temporary `Frame`, and data `Stack` objects
    * provides easy interface for manipulation with variables and memory
* `Stack`
    * used either for function call stack or data stack

* `Instruction`
    * represents an instruction consisting of opcode and operands
    * `execute()` method allows to execute the instance of `Instruction`
    * the correct method for execution is chosen according to the opcode
* `Operand`
    * represents an operand
    * used during parsing of the XML representation of an IPPcode19 program
    * `apply_type()` method is able to create an operand from some XML entity
    * `apply_type()` returns instance of one of the types: `int`, `bool`, `str`, `Variable`, `Type`, `Label`, `Nil`

* `Variable`
    * represents a variable
    * consist of frame specification and name of the variable
* `Type`
    * represents a type "type"
* `Label`
    * represents a type "label"
* `Nil`
    * represents a type "nil"


### Parsing of XML representation of IPPcode19

1. Create instance of `Program` and initialize variable: `i = 1`.
2. Find an instruction XML entity with attribute order equal to `i`.
4. If such an instruction entity does not exist, terminate parsing.
5. Get opcode and operands from the instruction entity and create an instance of `Instruction`.
6. Append the `Instruction` instance to the `Program` instance.
7. If the `Instruction` instance has opcode "LABEL" save name of the label to the dictionary of labels in `Program` instance.
8. Increment variable `i` and continue with point 2.
* In case of an error a corresponding exception is raised.

### Interpretation

Precondition: correctly loaded instance of `Program`.
1. Initialize instruction pointer: `ip = 0`.
2. If `ip` >= length of the `Program` instance then terminate interpretation as successful.
3. Get an instruction from the `ip` index of the `Program` instance.
4. Execute the `Instruction` instance using the method `execute()`.
5. Handle jumps, calls or returns by changing the value of `ip` and using function call stack and dictionary of labels in the `Program` instance.
6. Increment `ip` and continue with point 2.
* In case of an error a corresponding exception is raised.



### Error Handling

Errors are handled via use of exceptions. List of all exceptions and error return values can be found in file `error.py`. These exceptions are raised in different parts of the program and are caught in the `main()` function in `interpret.py`. According to caught exception the program is terminated with a specific return value.


## Task - `test.php`

The goal was to create a script in PHP 7.3 which performs automatic tests of `parse.php` and `interpret.py`.


## Solution - `test.php`

Arguments are parsed using function `getopt()` and checked afterwards whether they are correct. After that follows a check whether specified files and directories exist. Argument `--recursive` is executed using `RecursiveDirectoryIterator` and if it is not specified `DirectoryIterator` is used.

At first the beginning of the HTML is printed to standard output and as script iterates over files in specified (or default) directory the logs for each test are printed to the standard output. Logs are aligned in the table.

For each test the reference return code is compared with the actual return code returned by either `parse.php` or `interpret.py` according to the arguments of the script. In case the argument `--parse-only` is specified, only the output of the `parse.php` is compared to the reference output using the `jexamxml`. If the argument `--int-only` is specified, only the output of the `interpret.py` is compared to a reference output using bash `diff`. The script creates temporary files which are named as the test files but have suffix `.parseout` and `.intout`. These files are removed when they are not necessary anymore.

After all tests were executed, the ending of HTML is printed to the standard output.

Errors are handled using the function `error()` which prints an error message to the standard error output and terminates the script with given return code. 




