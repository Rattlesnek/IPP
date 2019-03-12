<?php
/**********************************************************************

  FileName    [gen_xml.php]

  SystemName  [IPP - Interpreter]

  PackageName [XML generator class]

  Author      [Adam Pankuch]

  Login       [xpanku00]

  Date        [5/3/2019]

***********************************************************************/

////////////////////////////////////////////////////////////////////////
///                             CLASSES                              ///
////////////////////////////////////////////////////////////////////////

/**
 * Function replaces all ampersands in string to be usable in XML
 * @param $string   string 
 */
function replace_amp($string) {
    return str_replace('&', '&amp;', $string);
}

/**
 * Class wraps XML generation
 */
class XMLCreator {
    private $ins_cnt;   // instruction counter
    public $DOM;        // DOMDocument object
    public $root;       // root entity in XML -- program

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
     * @return handle of instruction
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
     * @param $instructXML  handle of instruction where argument will be added
     * @param $number       number of argument
     * @param $type         type of argument
     * @param $value        value of argument
     * @return handle of argument
     */
    public function addArgument($instructXML, $number, $type, $value) {
        $argXML = $this->DOM->createElement('arg'.$number, replace_amp($value));
        $argXML->setAttribute('type', $type);
        $instructXML->appendChild($argXML);
        return $argXML;
    }

    /**
     * Method returns XML as string
     * @return XML formated string
     */
    public function str() {
        return $this->DOM->saveXML();
    }
}

?>