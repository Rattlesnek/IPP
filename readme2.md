# Documentation of Project Implementation of 2. Task for IPP 2018/2019
* Name and surname: Adam Pankuch
* Login: xpanku00

## Task - `interpret.py`

The goal was to create a script in Python 3.6 which reads the XML representation of a IPPcode19 program and interprets it using standard input and output.

## Solution - `interpret.py`

### Files

* `interpret.py` - main file, runs the whole interpret
* `intermachine.py` - contains classes `Program`, `Parser`, `Interpreter`
* `data.py` - contains classes `Frame`, `FrameStack`, `FrameSelect`, `CallStack`
* `instruct.py` - contains class `Instruction`
* `struct.py` - contains classes `Operand`, `Variable`, `Type`, `Label`, `Nil`
* `error.py` - contains all error exceptions and error return values


### Classes

* `Program`
    * represents a IPPcode19 program
    * contains list of Instruction objects and dictionary of Label objects refering to a certain location in program
* `Parser`
    * parser of XML representation of IPPcode19 program
    * able to parse XML representation of a program and creates a Program object
* `Interpreter`
    * interpreter of internal representation of IPPcode19 program
    * able to interpret a Program object

* `Frame`
    * dictionary of variables with their values
    * can be global, local or temporary
* `FrameStack`
    * stack of local frames
* `FrameSelect`

* `CallStack`
    * function call stack

* `Instruction`
    * represents an instruction
* `Operand`
    * represents an operand

* `Variable`
    * represents a variable
* `Type`
    * represents a type "type"
* `Label`
    * represents a type "label"
* `Nil`
    * represents a type "nil"



### Interpretation


### Error Handling



## Task - `test.php`

The goal was to create a script in PHP 7.3 which performs automatic tests of `parse.php` and `interpret.py`.


## Solution - `test.php`








