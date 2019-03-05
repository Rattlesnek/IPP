<?php

const ERR_PARAM = 10;
const ERR_INFILE = 11;
const ERR_OUTFILE = 12;
const ERR_INTER = 99;

function error($error_string, $ret_code) {
    fprintf(STDERR, $error_string);
    exit($ret_code);
}

function help() {
    echo "HELP\n";   
    exit(0); 
}

function create_file($filename, $write_zero=false) {
    $fw = fopen($filename, 'w');
    if (! $fw) {
        error("ERROR: could not create $filename\n", ERR_OUTFILE);
    }
    if ($write_zero) {
        fwrite($fw, "0\n");
    }
    fclose($fw);
}

const SHORT_OPTS = '';
const LONG_OPTS = array('help', 'directory:', 'recursive', 'parse-script:', 'int-script:', 'parse-only', 'int-only');

# default values of control variables
$dir = '.';
$recursive = false;
$parse_script = './parse.php';
$int_script = './interpret.py';
$parse_only = false;
$int_only = false;

$opt = getopt(SHORT_OPTS, LONG_OPTS);
if (array_key_exists('help', $opt))
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
    error("ERROR: wrong path to directory\n", ERR_PARAM);
if (! file_exists($parse_script) and $int_only == false) 
    error("ERROR: $parse_script does not exist\n", ERR_INFILE);
if (! file_exists($int_script) and $parse_only == false) 
    error("ERROR: $int_script does not exist\n", ERR_INFILE);


$dir = realpath($dir);
$parse_script = realpath($parse_script);
$int_script = realpath($int_script);


if ($recursive)   
    $files = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir));
else
    $files = new DirectoryIterator($dir);


$src_files = array();
foreach ($files as $file) {
    if (preg_match('/^.+\.src$/', $file->getPathname()))
        array_push($src_files, $file->getPathname());
}

$diff_file = './diffs.xml';
$fr = fopen($diff_file, 'w');
fclose($fr);

foreach ($src_files as $src_file) {
    $nosuffix_file = substr($src_file, 0, -4);
    $in_file = $nosuffix_file . '.in';
    $out_file = $nosuffix_file . '.out';
    $rc_file = $nosuffix_file . '.rc';
    if (! file_exists($in_file))
        create_file($in_file);
    if (! file_exists($out_file))
        create_file($out_file);
    if (! file_exists($rc_file))
        create_file($rc_file, $write_zero=true);
    
    $actual_out_file = $nosuffix_file . '.actout';
    $call = "php7.3 $parse_script <$src_file >$actual_out_file";
    echo "call: $src_file\n";
    exec($call, $output, $ret_code);
    
    $fr = fopen($rc_file, 'r');
    // TODO
    $expected_ret_code = (int) trim(fgets($fr));
    fclose($fr);

    if ($ret_code == $expected_ret_code) {
        exec("java -jar /pub/courses/ipp/jexamxml/jexamxml.jar $actual_out_file $out_file $diff_file /D /pub/courses/ipp/jexamxml/options", $output, $diff_code);
        echo "jexamxml ret code: $diff_code\n";
	exec("cat $diff_file");
    } else {
        echo "return codes are not same\n";
    }
}
    

?>
