<?php
/**********************************************************************

  FileName    [stats.php]

  SystemName  [IPP - Interpreter]

  PackageName [Statistics and XML classes]

  Author      [Adam Pankuch]

  Login       [xpanku00]

  Date        [5/3/2019]

***********************************************************************/

////////////////////////////////////////////////////////////////////////
///                             CLASSES                              ///
////////////////////////////////////////////////////////////////////////

class Stats {
    private $select;
    private $loc;
    private $comments;
    private $labels;
    private $jumps;

    public function __construct($select, $loc=0, $comments=0, $labels=0, $jumps=0) {
        $this->select = $select;
        $this->loc = $loc;
        $this->comments = $comments;
        $this->labels = $labels;
        $this->jumps = $jumps;
    }

    /**
     * Method increments number of comments
     */
    public function incComments() {
        $this->comments++;
    }

    /**
     * Method increments instruction counters based on opcode
     * @param $instruct     opcode of instruction
     */
    public function incInstructs($instruct) {
        $this->loc++;

        if ($instruct == 'LABEL')      
            $this->labels++;
        elseif (strpos($instruct, 'JUMP') !== false)
            $this->jumps++;
    }

    /**
     * Method returns string of statistics based on selected statistics in select
     */
    public function str() {
        $string = '';
        foreach ($this->select as $sel) {
            if ('loc' == $sel)
                $string .= "$this->loc\n";
            elseif ('comments' == $sel)
                $string .= "$this->comments\n";
            elseif ('labels' == $sel)
                $string .= "$this->labels\n";
            elseif ('jumps' == $sel)
                $string .= "$this->jumps\n";
        }
        return $string;
    }

    public function __get($attr) {
        if (property_exists($this, $attr))
            return $this->$attr;
    }
}


/**
 * Function replaces all amperants in string to be usable in XML
 * @param $string   string 
 */
function replace_amp($string) {
    return str_replace('&', '&amp;', $string);
}


class XMLCreator {
    private $ins_cnt;
    public $DOM;
    public $root;

    public function __construct() {
        $this->ins_cnt = 0;

        $this->DOM = new DOMDocument('1.0', 'UTF-8');
        $this->DOM->formatOutput = true;

        $this->root = $this->DOM->createElement('program');
        $this->root->setAttribute('language', 'IPPcode19');
        $this->DOM->appendChild($this->root);
    }

    /**
     * Method adds instruction to XML and returns its handle
     * @param $opcode   opcode of instruction
     */
    public function addInstruction($opcode) {
        $this->ins_cnt++;

        $instructXML = $this->DOM->createElement('instruction');
        $instructXML->setAttribute('order', $this->ins_cnt);
        $instructXML->setAttribute('opcode', $opcode);
        $this->root->appendChild($instructXML);
        return $instructXML;
    }

    /**
     * Method adds argument to instruction in XML and returns its handle
     * @param $instructXML  handle of instruciton where argument will be added
     * @param $number       number of argument
     * @param $type         type of argument
     * @param $value        value of argument
     */
    public function addArgument($instructXML, $number, $type, $value) {
        $argXML = $this->DOM->createElement('arg'.$number, replace_amp($value));
        $argXML->setAttribute('type', $type);
        $instructXML->appendChild($argXML);
        return $argXML;
    }

    /**
     * Method returns XML as string
     */
    public function str() {
        return $this->DOM->saveXML();
    }
}

?>