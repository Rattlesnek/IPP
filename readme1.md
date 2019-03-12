# Documentation of Project Implementation of 1. Task for IPP 2018/2019
* Name and surname: Adam Pankuch
* Login: xpanku00

## Task

The goal was to create a script in PHP 7.3 which performs lexical and syntactic analysis of a program written in IPPcode19 and then returns XML representation of the program.


## Solution

### Parse Arguments of the Script

Command line arguments are parsed using php function `getopt` and further handled using function `handle_stat_options` (only relevant for arguments used for STATP extension). 


### Lexical and Syntactic Analysis

Script `parse.php` reads given IPPcode19 program from standard input, line by line and checks whether the lines are lexically and syntactically correct. This is done using only regular expressions and PHP 7.3 functions for strings and arrays (no finite state automata or context-free grammar is used). Important part of analysis are constant arrays:

* Constant array `instructions` which contains all opcodes of instructions (keys) and their correct operand types (values).
* Constant array `operands` which contains operand types (keys) and arrays containing indexes of corresponding regular expressions (values).
* Constant indexed array `regexes` which contains regular expressions (values).


Main Processing Loop

1. If possible, read line from standard input.
2. If there is comment in the line, remove it.
3. Split line according to white spaces -> get an array containing "actual" opcode and "actual" operands.
4. If the line is empty continue with point 1.
5. Check if "actual" opcode exists according to array `instructions`.
6. Prepare array of "expected" operand types using array `instructions`.
7. Check if the number of "actual" operands matches the number of "expected" operand types.
8. For each "actual" operand check if it has correct type. That is executed using regular expressions from array `regexes` which are selected by "expected" operand type (and array `operands`).
9. If any of the checks fail then return lexical / syntax error.
10. Continue with point 1.



### Generation of XML

XML representation of the analysed IPPcode19 program is generated using PHP extension `DOMDocument`. To further simplify the generation of XML the class `XMLCreator` (see file `gen_xml.php`) is used. This class allows us to create new XML document, add instructions to the document, add arguments 
to the instructions and is able to return the XML document as a string. During lexical and syntactic analysis the XML document is gradually created and if the lexical and syntactic analysis succeed the XML document is returned.


### Error Handling

Errors are handled via function `error` which prints given error message to standard error output and exits from script with given return code. Return codes are stored as constants starting with `ERR_`. 


## Bonus Extensions

The class `Stats` (see file `stats.php`) implements bonus extension STATP. An object of this class collects and wraps all statistics and is able to return them in correct order as a string.