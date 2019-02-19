<?php

const ERR_INF = 11;
const ERR_OUTF = 12;
const ERR_HEAD = 21;
const ERR_OPCODE = 22;
const ERR_LEX_SYN = 23;
const ERR_INTER = 99;

const INSTRUCTS = array(
    'MOVE'          => 'var symb',
    'CREATEFRAME'   => '',
    'PUSHFRANE'     => '',
    'POPFRAME'      => '',
    'DEFVAR'        => 'var',
    'CALL'          => 'label',
    'RETURN'        => '',
    
    'PUSHS'         => 'symb',
    'POPS'          => 'var',

    'ADD'           => 'var symb symb',
    'SUB'           => 'var symb symb',
    'MUL'           => 'var symb symb',
    'IDIV'          => 'var symb symb',
    'LT'            => 'var symb symb',
    'GT'            => 'var symb symb',
    'EQ'            => 'var symb symb',
    'AND'           => 'var symb symb',
    'OR'            => 'var symb symb',
    'NOT'           => 'var symb symb',
    'INT2CHAR'      => 'var symb',
    'STR2INT'       => 'var symb symb',
    
    'READ'          => 'var type',
    'WRITE'         => 'symb',

    'CONCAT'        => 'var symb symb',
    'STRLEN'        => 'var symb',
    'GETCHAR'       => 'var symb symb',
    'SETCHAR'       => 'var symb symb',

    'TYPE'          => 'var symb',

    'LABEL'         => 'label',
    'JUMP'          => 'label',
    'JUMPIFEQ'      => 'label symb symb',
    'JUMPIFNEQ'     => 'label symb symb',
    'EXIT'          => 'symb',

    'DPRINT'        => 'symb',
    'BREAK'         => ''
);

const REGEX = array(
    0 => '/^(GF@|TF@|LF@)([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$/',  # VAR
    1 => '/^(nil@)(nil)$/', # NIL
    2 => '/^(int@)(.+$)/',  # INT
    3 => '/^(bool@)(true|false)$/', # BOOL 
    4 => '/^(string@)((\\\\[0-9]{3}|((?!#|\\\\)(?!\p{Z})\P{C})*)*)$/', # STRING
    5 => '/^([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$/', # LABEL
    6 => '/^(int|string|bool)$/' # TYPE
);

function error($error_string, $ret_code)
{
    fprintf(STDERR, $error_string);
    exit($ret_code);
}

function help()
{
    echo "HELP\n";    
}

function check_header($line)
{
    if ($line == '' or rtrim($line) != '.IPPcode19')
        error("ERROR: wrong file header!\n", ERR_HEAD);
}


const SHORT_OPTS = 'h';
const LONG_OPTS = array('help');

$opt = getopt(SHORT_OPTS, LONG_OPTS);
if (array_key_exists('help', $opt) or array_key_exists('h', $opt))
    help();

$line = fgets(STDIN);
check_header($line);

# MAIN LOOP
while ($line = fgets(STDIN))
{
    $parts = preg_split('/\s+/', trim($line));
    if (count($parts) > 4)
        error("ERROR: lexical or syntactic!\n", ERR_LEX_SYN);
    
    if ($parts[0] == '')
        continue;
   
    if (array_key_exists($parts[0]))
    {

    }
    else
        error("ERROR: wrong or unknown opcode!\n", ERR_OPCODE);

    for ($i = 1; $i < count($parts); $i++)
    {
        if ($i == 0)
        {

        }
        elseif ($i == 1)
        {

        }
    }
}


?>