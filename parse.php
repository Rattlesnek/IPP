<?php
/**********************************************************************

  FileName    [parse.php]

  SystemName  [IPP - Interpreter]

  PackageName [Parser of IPPcode19 to XML]

  Author      [Adam Pankuch]

  Login       [xpanku00]

  Date        [5/3/2019]

***********************************************************************/

include 'stats.php';

////////////////////////////////////////////////////////////////////////
///                            CONSTANTS                             ///
////////////////////////////////////////////////////////////////////////

// error return codes
const ERR_PARAM = 10;
const ERR_INFILE = 11;
const ERR_OUTFILE = 12;
const ERR_HEAD = 21;
const ERR_OPCODE = 22;
const ERR_LEX_SYN = 23;
const ERR_INTER = 99;

// array contains all instructions (keys) and their operands (values)
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
    'NOT'           => 'var symb',
    'INT2CHAR'      => 'var symb',
    'STRI2INT'       => 'var symb symb',
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

// array contains type of operand (key) and corresponding regexes (value)
const operands = array(
    'var'   => [0],
    'symb'  => [0, 1, 2, 3, 4],
    'label' => [5],
    'type'  => [6]
);

// array contains regexes for operands
const regexes = array(
    0 => '/^((GF|TF|LF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$/',  # VAR
    1 => '/^nil@(nil)$/', # NIL
    2 => '/^int@(.+)$/',  # INT
    3 => '/^bool@(true|false)$/', # BOOL 
    4 => '/^string@((\\\\[0-9]{3}|((?!#|\\\\)(?!\p{Z})\P{C})+)+)$/u', # STRING
    5 => '/^([a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*)$/', # LABEL
    6 => '/^(int|string|bool)$/' # TYPE
);

// array for mapping operand types
const map_type = array('var', 'nil', 'int', 'bool', 'string', 'label', 'type');


////////////////////////////////////////////////////////////////////////
///                           FUNCTIONS                              ///
////////////////////////////////////////////////////////////////////////

/**
 * Function prints error message to STDERR and then exits with return code
 * @param $error_string     error message
 * @param $ret_code         return code
 */
function error($error_string, $ret_code) {
    fprintf(STDERR, $error_string);
    exit($ret_code);
}

/**
 * Function prints help and then exits with return code 0
 */
function help() {
    echo "HELP\n";   
    exit(0); 
}

/**
 * Function handles command line arguments of script
 * @param $opt  command line arguments
 */
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

/**
 * Function checks if program starts with header .IPPcode19
 * @param $line     first line of program
 * @param $stats    statistics about program Stats()
 */
function check_header($line, $stats) {
    $comment_parts = preg_split('/#/', $line); 
    if (count($comment_parts) > 1) {
        $stats->incComments();
    }
    if (strtoupper(rtrim($comment_parts[0])) != '.IPPCODE19') {
        error("ERROR: wrong file header!\n", ERR_HEAD);
    }
}

////////////////////////////////////////////////////////////////////////
///                             MAIN                                 ///
////////////////////////////////////////////////////////////////////////

// handle command line arguments
const SHORT_OPTS = 'hs:lcbj';
const LONG_OPTS = array('help', 'stats:', 'loc', 'comments', 'labels', 'jumps');
$opt = getopt(SHORT_OPTS, LONG_OPTS);
$enable_stats = handle_options($opt);

$keys = array_keys($opt);
if ($enable_stats) {
    // open file for statistics
    $stat_file = fopen($opt['stats'], 'w');
    if (! $stat_file) {
        error("ERROR: ".$e."\n", ERR_OUTFILE);
    }
    $keys = array_diff($keys, ['stats']);
}

// create XML and statistics
$XML = new XMLCreator();
$stats = new Stats($keys);

// check header .IPPcode19
$line = fgets(STDIN);
check_header($line, $stats);

// MAIN PROCESSING LOOP
while ($line = fgets(STDIN)) {
    // search for comment and remove it
    $comment_parts = preg_split('/#/', trim($line));
    if (count($comment_parts) > 1) {
        $stats->incComments();
    }
    // split acording to whitespaces -- opcode + operands
    $parts = preg_split('/\s+/', trim($comment_parts[0]));
    $opcode = strtoupper(array_shift($parts));

    // if its an empty line or only comment then continue
    if ($opcode == '' or $opcode[0] == '#') {
        continue;
    }

    // check if instruction exist
    if (array_key_exists($opcode, instructions)) {
        $stats->incInstructs($opcode);
        $instructXML = $XML->addInstruction($opcode);

        $inst_operands = explode(' ', instructions[$opcode]);
        if ($inst_operands[0] == '') {
            // speciality for instructions that dont have operands - see behaviour of explode()
            array_shift($inst_operands);
        }
        // check if number of operands matches
        if (count($inst_operands) != count($parts)) {
            error("ERROR: wrong number of operands!\n", ERR_LEX_SYN);
        }

        // for each operand check if it has right type
        for ($i = 0; $i < count($inst_operands); $i++) {
            $success = false;
            // loop through allowed operand types for current operand and check if there is match
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

if ($enable_stats) {
    // print statistics to file
    fwrite($stat_file, $stats->str());
    fclose($stat_file);
}

// print XML to standard output
echo $XML->str();

?>