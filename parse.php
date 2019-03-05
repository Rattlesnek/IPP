<?php
include 'stats.php';

const ERR_PARAM = 10;
const ERR_INFILE = 11;
const ERR_OUTFILE = 12;
const ERR_HEAD = 21;
const ERR_OPCODE = 22;
const ERR_LEX_SYN = 23;
const ERR_INTER = 99;

const instructions = array(
    'MOVE'          => 'var symb',
    'CREATEFRAME'   => '',
    'PUSHFRAME'     => '',
    'POPFRAME'      => '',
    'DEFVAR'        => 'var',
    'CALL'          => 'label',
    'RETURN'        => '',
/**/'PUSHS'         => 'symb',
    'POPS'          => 'var',
/**/'ADD'           => 'var symb symb',
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
/**/'READ'          => 'var type',
    'WRITE'         => 'symb',
/**/'CONCAT'        => 'var symb symb',
    'STRLEN'        => 'var symb',
    'GETCHAR'       => 'var symb symb',
    'SETCHAR'       => 'var symb symb',
/**/'TYPE'          => 'var symb',
/**/'LABEL'         => 'label',
    'JUMP'          => 'label',
    'JUMPIFEQ'      => 'label symb symb',
    'JUMPIFNEQ'     => 'label symb symb',
    'EXIT'          => 'symb',
/**/'DPRINT'        => 'symb',
    'BREAK'         => ''
);

const operands = array(
    'var'   => [0],
    'symb'  => [0, 1, 2, 3, 4],
    'label' => [5],
    'type'  => [6]
);

const regexes = array(
    0 => '/^((GF|TF|LF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$/',  # VAR
    1 => '/^nil@(nil)$/', # NIL
    2 => '/^int@(.+)$/',  # INT
    3 => '/^bool@(true|false)$/', # BOOL 
    4 => '/^string@((\\\\[0-9]{3}|((?!#|\\\\)(?!\p{Z})\P{C})+)+)$/u', # STRING
    5 => '/^([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$/', # LABEL
    6 => '/^(int|string|bool)$/' # TYPE
);

const map_type = array('var', 'nil', 'int', 'bool', 'string', 'label', 'type');

function error($error_string, $ret_code) {
    fprintf(STDERR, $error_string);
    exit($ret_code);
}

function help() {
    echo "HELP\n";   
    exit(0); 
}

function handle_options($opt) {
    if (array_key_exists('help', $opt) or array_key_exists('h', $opt)) {
        help();
    } elseif (array_key_exists('stats', $opt)) {
        return true;
    } elseif (array_key_exists('loc', $opt) or array_key_exists('comments', $opt) or
              array_key_exists('labels', $opt) or array_key_exists('jumps', $opt)) {
        error("ERROR: param --stats=file is missing!\n", ERR_PARAM);
    } else {
        return false;
    }
}

function check_header($line, $stats) {
    $comment_parts = preg_split('/#/', $line);
    if (count($comment_parts) > 1) {
        $stats->incComments();
    }
    if (rtrim($comment_parts[0]) != '.IPPcode19') {
        error("ERROR: wrong file header!\n", ERR_HEAD);
    }
}

const SHORT_OPTS = 'hs:lcbj';
const LONG_OPTS = array('help', 'stats:', 'loc', 'comments', 'labels', 'jumps');
$opt = getopt(SHORT_OPTS, LONG_OPTS);
$enable_stats = handle_options($opt);

$keys = array_keys($opt);
if ($enable_stats) {
    $stat_file = fopen($opt['stats'], 'w');
    if (! $stat_file) {
        error("ERROR: ".$e."\n", ERR_OUTFILE);
    }
    $keys = array_diff($keys, ['stats']);
}

// create XML and Statistics
$XML = new XMLCreator();
$stats = new Stats($keys);

$line = fgets(STDIN);
check_header($line, $stats);

// MAIN LOOP
while ($line = fgets(STDIN)) {
    //echo "line: $line";    
    $comment_parts = preg_split('/#/', trim($line));
    if (count($comment_parts) > 1) {
        $stats->incComments();
    }
    $parts = preg_split('/\s+/', trim($comment_parts[0]));
    $opcode = strtoupper(array_shift($parts));

    // if empty line then continue in main loop
    if ($opcode == '' or $opcode[0] == '#') {
        continue;
    }
    //echo " ... instruct: $opcode\n";
    if (array_key_exists($opcode, instructions)) {
        $stats->incInstructs($opcode);
        $instructXML = $XML->addInstruction($opcode);

        $inst_operands = explode(' ', instructions[$opcode]);
        // for instructions that dont have operands - see behaviour of explode()
        if ($inst_operands[0] == '') {
            array_shift($inst_operands);
        }
        if (count($inst_operands) != count($parts)) {
            error("ERROR: wrong number of operands!\n", ERR_LEX_SYN);
        }
        for ($i = 0; $i < count($inst_operands); $i++) {
            //echo " ... operand_$i: ", $inst_operands[$i], " vs \"", $parts[$i], "\"\n";
            $success = false;
            foreach (operands[$inst_operands[$i]] as $reg_idx) {
                if (preg_match(regexes[$reg_idx], $parts[$i], $matches)) {
                    $success = true;
                    break;
                }
            }
            if ($success == false) {
                error("ERROR: regex failed!\n", ERR_LEX_SYN); 
            }
            $XML->addArgument($instructXML, $i+1, map_type[$reg_idx], $matches[1]);
        }
    } else {
        error("ERROR: wrong or unknown opcode!\n", ERR_OPCODE);
    }
}
//echo "====== SUCCESS ======\n\n";

if ($enable_stats) {
    fwrite($stat_file, $stats->str());
    fclose($stat_file);
}

echo $XML->str();
?>