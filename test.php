<?php
/**********************************************************************

  FileName    [test.php]

  SystemName  [Tester for parse.php and interpret.py]

  PackageName []

  Author      [Adam Pankuch]

  Login       [xpanku00]

  Date        [9/3/2019]

***********************************************************************/

// error return codes
const ERR_PARAM = 10;
const ERR_INFILE = 11;
const ERR_OUTFILE = 12;
const ERR_INTER = 99;
// color standard output
const GREEN = "\e[0;32m";
const YELLOW = "\e[1;33m";
const RED = "\e[0;31m";
const TRAIL = "\e[0m";

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
    echo "usage: test.php [--help] [--directory DIR] [recursive]\n"
        ."                [--parse-script SCRIPT] [--int-script SCRIPT]\n"
        ."                [--parse-only] [--int-only]\n\n"
        ."optional arguments:\n"
        ."  -h, --help              show this help message and exit\n"
        ."  --directory DIR         specify directory with tests (default: current dir)\n"
        ."  --recursive             search for tests recursively in subdirectories\n"
        ."  --parse-script SCRIPT   specify path to parser (default: current dir)\n"
        ."  --int-script SCRIPT     specify path to interpreter (default: current dir)\n"
        ."  --parse-only            test only parser\n"
        ."  --int-only              test only interpreter\n";   
    exit(0); 
}

/**
 * Function creates an empty file
 * @param $filename name of the file
 * @param $write_zero if true write zero to file else dont
 */
function create_file($filename, $error=ERR_INFILE, $write_zero=false) {
    $fw = fopen($filename, 'w');
    if (! $fw) {
        error("ERROR: could not create $filename\n", $error);
    }
    if ($write_zero) {
        fwrite($fw, "0\n");
    }
    fclose($fw);
}

/**
 * Function prints html colored text
 * @param $color    color string
 * @param $text     text to be colored
 */
function color_text($color, $text) {
    echo "<td> <font color=\"$color\">$text</font> <br> </td>\n</tr>\n";
}


const SHORT_OPTS = 'h';
const LONG_OPTS = array('help', 'directory:', 'recursive', 'parse-script:', 'int-script:', 'parse-only', 'int-only');

// default values of control variables
$dir = '.';
$recursive = false;
$parse_script = './parse.php';
$int_script = './interpret.py';
$parse_only = false;
$int_only = false;

$jexamxml = '/pub/courses/ipp/jexamxml/jexamxml.jar';
// TODO
//$jexamxml = '../jexamxml/jexamxml.jar';

$jexamxml_opt = '/pub/courses/ipp/jexamxml/options';
// TODO
//$jexamxml_opt = '../jexamxml/options';

$opt = getopt(SHORT_OPTS, LONG_OPTS);
if (array_key_exists('help', $opt) or array_key_exists('h', $opt))
    help(); 
if (array_key_exists('directory', $opt))
    $dir = $opt['directory'];
if (array_key_exists('recursive', $opt))
    $recursive = true;
if (array_key_exists('parse-script', $opt))
    $parse_script = $opt['parse-script'];
if (array_key_exists('int-script', $opt))
    $int_script = $opt['int-script'];
if (array_key_exists('parse-only', $opt)) {
    $parse_only = true;
    if (array_key_exists('int-script', $opt) or array_key_exists('int-only', $opt))
        error("ERROR: forbiden parameter combination!\n", ERR_PARAM);
}
if (array_key_exists('int-only', $opt)) {
    $int_only = true;
    if (array_key_exists('parse-script', $opt) or array_key_exists('parse-only', $opt))
        error("ERROR: forbiden parameter combination!\n", ERR_PARAM);
}

if (! is_dir($dir))
    error("ERROR: wrong path to directory $dir\n", ERR_PARAM);
if (! file_exists($parse_script) and $int_only == false) 
    error("ERROR: $parse_script does not exist\n", ERR_INFILE);
if (! file_exists($int_script) and $parse_only == false) 
    error("ERROR: $int_script does not exist\n", ERR_INFILE);


$dir = realpath($dir);
$parse_script = realpath($parse_script);
$int_script = realpath($int_script);

const HEADER = "<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <title>Test.php log</title>
</head>
<body>

<h1>Test.php log</h1>
";

const TABLE = "
<table style=\"width:60%\">
<tr>
<th> <p align=\"left\">Test file</p> </th>
<th> <p align=\"left\">Outcome</p> </th>
</tr>\n
";

const ENDING = "
</table>

</body>
</html>
";

if ($recursive) {  
    $files = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir));
} else {
    $files = new DirectoryIterator($dir);
}

$src_files = array();
// collect all .src files to array
foreach ($files as $file) {
    if (preg_match('/^.+\.src$/', $file->getPathname()))
        array_push($src_files, $file->getPathname());
}

// create diff file
$diff_file = './diffs.xml';
create_file($diff_file, $error=ERR_OUTFILE);
$diff_file = realpath($diff_file);

// print HTML header and some info
echo HEADER;
if ($int_only) {
    echo "<h2>Interpreter only</h2>\n";
} elseif ($parse_only) {
    echo "<h2>Parser only</h2>\n";
} else {
    echo "<h2>Parser togheter with interpreter</h2>\n";
}
echo "<h2>Directory: $dir</h2>\n";
echo TABLE;

// for each .src file run test
sort($src_files);
foreach ($src_files as $src_file) {
    $nosuffix_file = substr($src_file, 0, -4);
    // create files which are missing {.in, .out, .rc}
    $in_file = $nosuffix_file . '.in';
    $out_file = $nosuffix_file . '.out';
    $rc_file = $nosuffix_file . '.rc';
    $parse_out_file = $nosuffix_file . '.parseout';
    $int_out_file = $nosuffix_file . '.intout';
    if (! file_exists($in_file)) {
        create_file($in_file);
    }
    if (! file_exists($out_file)) {
        create_file($out_file);
    }
    if (! file_exists($rc_file)) {
        create_file($rc_file, $write_zero=true);
    }

    // get expected return code value from .rc file
    $fr = fopen($rc_file, 'r');
    if (! $fr) {
        error("ERROR: could not open $rc_file\n", ERR_INFILE);
    }
    $expected_ret_code = (int) trim(fgets($fr));
    fclose($fr);

    //fprintf(STDERR, "call: $src_file\n");
    $call = str_replace($dir, "", $nosuffix_file);
    echo "<tr>\n<td>$call</td>\n";

    if (! $int_only) {
        // PARSE execute
        exec("php7.3 $parse_script <$src_file >$parse_out_file 2>/dev/null", $exec, $parse_ret_code);
        $int_src_file = $parse_out_file;
        $actual_ret_code = $parse_ret_code;
    } else {
        $int_src_file = $src_file;
    }

    if (! $parse_only) {
        // INTERPRET execute
        exec("python $int_script --input=$in_file <$int_src_file >$int_out_file 2>/dev/null", $exec, $int_ret_code);
        $actual_ret_code = $int_ret_code;
    }

    // compare return codes
    if ($actual_ret_code == $expected_ret_code) {
        // find out if error ocurred during parsing/interpretation
        if ($actual_ret_code == 0) {
            // check either output XML or output from interpreter
            if ($parse_only) {
                exec("java -jar $jexamxml $parse_out_file $out_file $diff_file /D $jexamxml_opt", $exec, $diff_code);
                //fprintf(STDERR, "jexamxml\n");
            } else {
                exec("diff $int_out_file $out_file >$diff_file", $exec, $diff_code);
                //fprintf(STDERR, "diff\n");
            }
            
            // according to return value print success or fail
            if ($diff_code == 0) {
                //fprintf(STDERR, GREEN . " ... SUCCESS -- expected: $expected_ret_code got: $actual_ret_code\n" . TRAIL);
                color_text("green", "SUCCESS");
            } else {
                //fprintf(STDERR, RED . " ... FAIL\n" . TRAIL);
                color_text("red", "FAIL -- return codes match but output is different");
            }
        } else {
            //fprintf(STDERR, GREEN . " ... SUCCESS -- expected: $expected_ret_code got: $actual_ret_code\n" . TRAIL);
            color_text("green", "SUCCESS");
        }
    } else {
        //fprintf(STDERR, RED . " ... RC comparison FAIL -- expected: $expected_ret_code got: $actual_ret_code\n" . TRAIL);
        color_text("red", "FAIL -- expected return code: $expected_ret_code got: $actual_ret_code");
    }

    if ($parse_only) {
        unlink($parse_out_file);
    } elseif ($int_only) {
        unlink($int_out_file);
    } else {
        unlink($parse_out_file);
        unlink($int_out_file);
    }
}

echo ENDING;

unlink($diff_file);

fprintf(STDERR, "Testing finished!\n");

?>
