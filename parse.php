<?php
include 'stats.php';

const ERR_INF = 11;
const ERR_OUTF = 12;
const ERR_HEAD = 21;
const ERR_OPCODE = 22;
const ERR_LEX_SYN = 23;
const ERR_INTER = 99;

const instructions = array(
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

const operands = array(
    'var'   => array(0),
    'symb'  => array(0, 1, 2, 3, 4),
    'label' => array(5),
    'type'  => array(6)
);

const map = array(
    0 => 'var',
    1 => 'nil',
    2 => 'int',
    3 => 'bool',
    4 => 'string',
    5 => 'label',
    6 => 'type'
);

const regexes = array(
    0 => '/^(GF|TF|LF)@([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$/',  # VAR
    1 => '/^(nil)@(nil)$/', # NIL
    2 => '/^(int)@(.+)$/',  # INT
    3 => '/^(bool)@(true|false)$/', # BOOL 
    4 => '/^(string)@((\\\\[0-9]{3}|((?!#|\\\\)(?!\p{Z})\P{C})*)*)$/u', # STRING
    5 => '/^([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$/', # LABEL
    6 => '/^(int|string|bool)$/' # TYPE
);

function map_text($matches, $reg_idx) {
    if (1 <= $reg_idx and $reg_idx <= 4)
        return $matches[2];
    else
        return $matches[0];
}

function error($error_string, $ret_code) {
    fprintf(STDERR, $error_string);
    exit($ret_code);
}

function help() {
    echo "HELP\n";    
}

function check_header($line) {
    if ($line == '' or rtrim($line) != '.IPPcode19')
        error("ERROR: wrong file header!\n", ERR_HEAD);
}

function addElement($dom, $to, $name) {
    $elem = $dom->createElement($name);
    $to->appendChild($elem);
    return $elem;
}

const SHORT_OPTS = 'hs:lcbj';
const LONG_OPTS = array('help', 'stats:', 'loc', 'comments', 'labels', 'jumps');
$opt = getopt(SHORT_OPTS, LONG_OPTS);
if (array_key_exists('help', $opt) or array_key_exists('h', $opt))
    help();

var_dump($opt);

$stats = new Stats();

$line = fgets(STDIN);
check_header($line);

# create XML
$DOM = new DOMDocument('1.0', 'UTF-8');
$DOM->formatOutput = true;
$progXML = addElement($DOM, $DOM, 'program');
$progXML->setAttribute('language', 'IPPcode19');

# MAIN LOOP
$ins_cnt = 0;
while ($line = fgets(STDIN)) {
    echo "line: $line";
    
    $parts = preg_split('/\s+/', trim($line));
    $instruct = strtoupper(array_shift($parts));
    # if empty line then continue in main loop
    if ($instruct == '') {
        continue;
    } elseif ($instruct[0] == '#') {
        $stats->incComments();
        continue;
    } else {
        $stats->incInstructs($instruct);
    }

    echo " ... instruct: $instruct\n";
    
    if (array_key_exists($instruct, instructions)) {
        $ins_cnt++;
        $insXML = addElement($DOM, $progXML, 'instruction');
        $insXML->setAttribute('order', $ins_cnt);
        $insXML->setAttribute('opcode', $instruct);
        
        $inst_operands = explode(' ', instructions[$instruct]);
        # for instructions that dont have operands - see behavior of explode()
        if ($inst_operands[0] == '')
            array_shift($inst_operands);

        if (count($inst_operands) != count($parts))
            error("ERROR: wrong number of operands!\n", ERR_LEX_SYN);

        for ($i = 0; $i < count($inst_operands); $i++) {
            echo " ... operand_$i: ", $inst_operands[$i], " vs \"", $parts[$i], "\"\n";
            
            $success = FALSE;
            foreach (operands[$inst_operands[$i]] as $reg_idx) {
                if (preg_match(regexes[$reg_idx], $parts[$i], $matches)) {
                    $success = TRUE;
                    break;
                }
            }
            if ($success == FALSE)
                error("ERROR: regex failed!\n", ERR_LEX_SYN); 
            
            $argXML = $DOM->createElement('arg'.($i+1), map_text($matches, $reg_idx));
            $argXML->setAttribute('type', map[$reg_idx]);
            $insXML->appendChild($argXML);
        }
    } else {
        error("ERROR: wrong or unknown opcode!\n", ERR_OPCODE);
    }
}

echo "====== SUCCESS ======\n\n";

echo $DOM->saveXML();
echo "\n";

echo $stats->str();


?>